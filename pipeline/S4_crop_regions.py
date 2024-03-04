import os
import shutil
from copy import deepcopy
import cv2
import json

import cv2
import numpy as np

# https://github.com/amusi/Non-Maximum-Suppression/blob/master/nms.py
"""
    Non-max Suppression Algorithm

    @param list  Object candidate bounding boxes
    @param list  Confidence score of bounding boxes
    @param float IoU threshold

    @return Rest boxes after nms operation
"""
def nms(bounding_boxes, confidence_score, threshold):
    # If no bounding boxes, return empty list
    if len(bounding_boxes) == 0:
        return [], []

    # Bounding boxes
    boxes = np.array(bounding_boxes)

    # coordinates of bounding boxes
    start_x = boxes[:, 0]
    start_y = boxes[:, 1]
    end_x = boxes[:, 2]
    end_y = boxes[:, 3]

    # Confidence scores of bounding boxes
    score = np.array(confidence_score)

    # Picked bounding boxes
    picked_boxes = []
    picked_score = []

    # Compute areas of bounding boxes
    areas = (end_x - start_x + 1) * (end_y - start_y + 1)

    # Sort by confidence score of bounding boxes
    order = np.argsort(score)

    # Iterate bounding boxes
    while order.size > 0:
        # The index of largest confidence score
        index = order[-1]

        # Pick the bounding box with largest confidence score
        picked_boxes.append(bounding_boxes[index])
        picked_score.append(confidence_score[index])

        # Compute ordinates of intersection-over-union(IOU)
        x1 = np.maximum(start_x[index], start_x[order[:-1]])
        x2 = np.minimum(end_x[index], end_x[order[:-1]])
        y1 = np.maximum(start_y[index], start_y[order[:-1]])
        y2 = np.minimum(end_y[index], end_y[order[:-1]])

        # Compute areas of intersection-over-union
        w = np.maximum(0.0, x2 - x1 + 1)
        h = np.maximum(0.0, y2 - y1 + 1)
        intersection = w * h

        # Compute the ratio between intersection and union
        ratio = intersection / (areas[index] + areas[order[:-1]] - intersection)

        left = np.where(ratio < threshold)
        order = order[left]

    return picked_boxes, picked_score
    

def prune_regions(indir, outdir):
    # Opening JSON file
    f = open(os.path.join(outdir, "DINO_boxes.json"))
    data = json.load(f)

    bboxes = []
    certainties = []
    for d in data:
        bboxes.append(d["box"])
        certainties.append(d["certainty"])

    img = cv2.imread(os.path.join(indir, "slide.jpg"))
    imgsize = img.shape[0] * img.shape[1]

    print("before prune: ", len(bboxes))

    new_bboxes = []
    new_certainties = []
    for i in range(len(bboxes)):
        b = bboxes[i]
        c = certainties[i]
        area_b = (b[2]-b[0]) * (b[3]-b[1])
        if area_b * 4 < imgsize:
            new_bboxes.append(b)
            new_certainties.append(c)
    
    bboxes, _ = nms(new_bboxes, new_certainties, 0.5)

    # Draw bounding boxes and confidence score after non-maximum supression
    for (start_x, start_y, end_x, end_y) in bboxes:
        cv2.rectangle(img, (start_x, start_y), (end_x, end_y), (0, 0, 255), 2)
    
    cv2.imwrite(os.path.join(outdir, 'pruned.jpg'), img)

    with open(os.path.join(outdir, "pruned_boxes.json"), 'w') as f:
        json.dump(bboxes, f, ensure_ascii=False)

    print("after prune: ", len(bboxes))

def crop_regions(indir, outdir):

    # Opening JSON file
    f = open(os.path.join(outdir, "pruned_boxes.json"))
    
    # returns JSON object as 
    # a dictionary
    bboxes = json.load(f)

    dir_name = os.path.join(outdir, "proposed_regions")
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)

    img = cv2.imread(os.path.join(indir, "slide.jpg"))
    for i in range(len(bboxes)):
        x0, y0, x1, y1 = bboxes[i]
        img1 = deepcopy(img)
        img1 = img[y0:y1, x0:x1]
        cv2.imwrite(os.path.join(dir_name, str(i)+'.jpg'), img1)

    



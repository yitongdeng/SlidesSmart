import os
import base64
import requests
import cv2
import json
import re
from .S0_presegment import *
import copy
import shutil
from ext.process_video import *

def bb_iou(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    if interArea == 0:
        return 0
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = abs((boxA[2] - boxA[0]) * (boxA[3] - boxA[1]))
    boxBArea = abs((boxB[2] - boxB[0]) * (boxB[3] - boxB[1]))

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area

    #iou = interArea / float(boxAArea + boxBArea - interArea)
    iou = interArea / boxBArea

    # return the intersection over union value
    return iou

def bb_union(boxA, boxB):
    return [min(boxA[0], boxB[0]), min(boxA[1], boxB[1]), max(boxA[2], boxB[2]), max(boxA[3], boxB[3])]

def bb_list_union(boxList):
    if len(boxList) < 1:
        return []
    union = boxList[0]
    for i in range(1, len(boxList)):
        union = bb_union(union, boxList[i])
    return union

def grow_bbox(bbox, other_bboxes):
    if len(bbox) < 4:
        return [], [[]]

    intersecteds = []
    for other in other_bboxes:
        iou = bb_iou(bbox, other)
        if iou > 0.15:
            intersecteds.append(other)
    if len(intersecteds) < 1:
        intersecteds.append([])

    return bb_list_union(intersecteds), intersecteds


def help_parse(answer, slide_shape):
    height, width, _ = slide_shape

    all_bboxes = []
    for s in answer:
        s_bboxes = []
        YN = s.split(",")[0]
        if YN == "Yes":
            segment_cells = re.findall(r'([A-Z]\d-[A-Z]\d)', s)
            if len(segment_cells) == 0:
                segment_cells = re.findall(r'([A-Z]\d)', s)
            c = segment_cells[0]
            if c[0].isupper() and c[-1].isdigit():
                cs = c.split("-")
                # print(cs)
                j0 = int(ord(cs[0][0])) - 65 # x0, y0 depend on the first entry
                i0 = int(cs[0][1])
                j1 = int(ord(cs[-1][0])) - 65 # x1, y1 depend on the last entry
                i1 = int(cs[-1][1])

                i0, i1 = min(i0, i1), max(i0, i1)
                j0, j1 = min(j0, j1), max(j0, j1)

                x0 = int(i0 * width / n_horizotnal)
                y0 = int(j0 * height / n_vertical)
                x1 = int((i1+1) * width / n_horizotnal)
                y1 = int((j1+1) * height / n_vertical)
                s_bboxes.append([x0, y0, x1, y1])
        else:
            s_bboxes.append([])
        
        all_bboxes.append(s_bboxes)
    
    return all_bboxes


def grow_preds(indir, outdir):
    # Opening JSON file
    f = open(os.path.join(outdir, "pruned_boxes.json"))
    CV_bboxes = json.load(f)

    slide = cv2.imread(os.path.join(outdir, 'pruned.jpg'))

    f = open(os.path.join(indir, "processed_annotation.json"))
    segments_loaded = json.load(f)

    f = open(os.path.join(outdir, "GPT_1.json"))
    GPT_1 = json.load(f)

    bboxes = help_parse(GPT_1, slide.shape)
    
    grown_bboxes = []
    intersect_bboxes = []
    
    for b in bboxes:
        grown, intersect = grow_bbox(b[0], CV_bboxes)
        grown_bboxes.append([grown])
        intersect_bboxes.append(intersect)

    #print("grown_bboxes: ", grown_bboxes)

    dir_name = os.path.join(outdir, "pred_growth")
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)

    for i in range(len(segments_loaded)):
        print("processing segment: ", i)
        print(bboxes[i])
        slide_copy2 = copy.deepcopy(slide)
        if len(bboxes[i][0])>=4:
            start_x, start_y, end_x, end_y = bboxes[i][0]
        else:
            start_x, start_y, end_x, end_y = 0, 0, 0, 0
        cv2.rectangle(slide_copy2, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
        if len(grown_bboxes[i][0])>=4:
            start_x, start_y, end_x, end_y = grown_bboxes[i][0]
        else:
            start_x, start_y, end_x, end_y = 0, 0, 0, 0
        cv2.rectangle(slide_copy2, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)
        cv2.imwrite(os.path.join(dir_name, str(i)+'.jpg'), slide_copy2)
    
    highlighteds = []
    slide2 = cv2.imread(os.path.join(outdir, 'presegmented.jpg'))
    for i in range(len(segments_loaded)):
        slide_copy = copy.deepcopy(slide)
        slide_copy = paint_bboxes(slide_copy, grown_bboxes[i])
        #print("intersect_bboxes: ", intersect_bboxes[i])
        #slide_copy = paint_bboxes(slide_copy, intersect_bboxes[i])

        if len(bboxes[i][0])>=4:
            start_x, start_y, end_x, end_y = bboxes[i][0]
        else:
            start_x, start_y, end_x, end_y = 0, 0, 0, 0
        cv2.rectangle(slide_copy, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
        highlighteds.append(slide_copy)
    
    create_image_video(indir, dir_name, slide, highlighteds, [s["start"] for s in segments_loaded], [s["end"] for s in segments_loaded])

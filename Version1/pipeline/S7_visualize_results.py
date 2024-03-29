import json
import os
import re
from ext.process_video import *
import copy
import shutil

def visualize_results(indir, outdir):
 
    slide = cv2.imread(os.path.join(outdir, "pruned.jpg"))

    f = open(os.path.join(outdir, "matched_result.json"))
    data = json.load(f)

    bbox_idxs = []
    for d in data:
        idx = int(re.findall(r'The most relevant sentence on the slide is: (.*)\.', d)[0])
        bbox_idxs.append(idx)

    # Opening JSON file
    f = open(os.path.join(outdir, "pruned_boxes.json"))
    
    # returns JSON object as 
    # a dictionary
    bboxes = json.load(f)

    matched_bboxes = []
    for idx in bbox_idxs:
        if idx < 0:
            matched_bboxes.append([0, 0, slide.shape[1]-1, slide.shape[0]-1])
        else:
            matched_bboxes.append(bboxes[idx])

    dir_name = os.path.join(outdir, "highlighted_slides")
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)

    highlighteds = []
    for i in range(len(matched_bboxes)):
        print("processing: ", i)
        slide_copy = copy.deepcopy(slide)
        slide_copy = paint_bboxes(slide_copy, [matched_bboxes[i]])
        highlighteds.append(slide_copy)
        cv2.imwrite(os.path.join(dir_name, str(i)+'.jpg'), slide_copy)

    f = open(os.path.join(outdir, "segments_processed.json"))
    
    data = json.load(f)

    starts = []
    ends = []
    for d in data:
        starts.append(d["start"])
        ends.append(d["end"])

    # print("starts: ", len(starts))
    # print("ends: ", len(ends))

    create_image_video(indir, outdir, slide, highlighteds, starts, ends)
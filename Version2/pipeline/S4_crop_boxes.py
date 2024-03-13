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

def crop_GPT_boxes(indir, outdir):
    slide = cv2.imread(os.path.join(outdir, 'presegmented.jpg'))

    height, width, _ = slide.shape

    f = open(os.path.join(outdir, "answer.json"))
    gpt_answer = json.load(f)

    f = open(os.path.join(outdir, "words.json"))
    data = json.load(f)

    starts = []
    ends = []
    words = []

    for d in data:
        word = d["word"]
        if word == "": 
            word = "percent"
        words.append(word.lower())
        starts.append(d["start"])
        ends.append(d["end"])


    segment_cells = re.findall(r'refers to region[s]* (.*?)[, ]', gpt_answer)
    segment_contents = re.findall(r'Segment \d+: "(.*?)"', gpt_answer)

    # fixes mismatch between GPT segments and whisper words
    lens = []
    seg_splits = []
    for segment in segment_contents:
        seg_stripped = segment.replace(",", "").replace(".", "")
        seg_split = seg_stripped.split()
        seg_splits.append(seg_split)
        lens.append(len(seg_split))
    
    tot_len = 0
    for l in lens:
        tot_len += l
    print("tot len before fix: ", tot_len)
    
    idx = 0
    for i in range(len(seg_splits)):
    #for i in range(3):
        seg_split = seg_splits[i]
        for w in seg_split:
            if w.lower() == words[idx].lower():
                idx += 1
            else:
                while idx < len(words) and (w.lower() != words[idx].lower()):
                    lens[i-1] += 1
                    idx += 1

                idx += 1

    tot_len = 0
    for l in lens:
        tot_len += l
    print("tot len after fix: ", tot_len)

    # shove the remaining into the last segment
    lens[-1] += len(words) - tot_len
    # 

    
    print("segment cells: ", segment_cells)
    segment_bboxes = []
    for c in segment_cells:
        # first check if is valid
        if c[0].isupper() and c[-1].isdigit():
            cs = c.split("-")
            print(cs)
            j0 = int(ord(cs[0][0])) - 65 # x0, y0 depend on the first entry
            i0 = int(cs[0][1])
            j1 = int(ord(cs[-1][0])) - 65 # x1, y1 depend on the last entry
            i1 = int(cs[-1][1])

            x0 = int(i0 * width / n_horizotnal)
            y0 = int(j0 * height / n_vertical)
            x1 = int((i1+1) * width / n_horizotnal)
            y1 = int((j1+1) * height / n_vertical)
            segment_bboxes.append([x0, y0, x1, y1])
        else:
            segment_bboxes.append([0, 0, width, height])
    
    print("segment bboxes: ", segment_bboxes)

    total_words = 0
    segment_starts = []
    segment_ends = []
    for i in range(len(segment_contents)):
        segment_starts.append(starts[total_words])
        num_words = lens[i]
        total_words += num_words
        segment_ends.append(ends[total_words-1])

    print("total words: ", total_words)
    print("correct total words: ", len(starts))
    if total_words != len(starts):
        print("Two numbers doesn't match! Exitting")
        exit()

    print("len segment_bboxes: ", len(segment_bboxes))
    print("len segment_starts: ", len(segment_starts))

    dir_name = os.path.join(outdir, "cropped_boxes")
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)

    highlighteds = []
    for i in range(len(segment_bboxes)):
        print("processing: ", i)
        x0, y0, x1, y1 = segment_bboxes[i]
        img1 = slide[y0:y1, x0:x1]
        cv2.imwrite(os.path.join(dir_name, str(i)+'.jpg'), img1)
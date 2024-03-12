import os
import base64
import requests
import cv2
import json
import re
from .presegment import *
import copy
import shutil
from ext.process_video import *



# Returns number of words in string
def countWords(string):
    OUT = 0
    IN = 1
    state = OUT
    wc = 0

    # Scan all characters one by one
    for i in range(len(string)):

        # If next character is a separator, 
        # set the state as OUT
        if (string[i] == ' ' or string[i] == '\n' or
            string[i] == '\t'):
            state = OUT

        # If next character is not a word 
        # separator and state is OUT, then 
        # set the state as IN and increment 
        # word count
        elif state == OUT:
            state = IN
            wc += 1

    # Return the number of words
    return wc

def parse_GPT_answer(indir, outdir):
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
        words.append(d["word"].lower())
        starts.append(d["start"])
        ends.append(d["end"])


    segment_cells = re.findall(r'refers to region (.*?)\,', gpt_answer)
    segment_contents = re.findall(r'Segment \d+: "(.*?)"', gpt_answer)

    print("segment cells: ", segment_cells)
    segment_bboxes = []
    for c in segment_cells:
        j = int(ord(c[0])) - 65
        i = int(c[1])
        print("j: ", j)
        print("i: ", i)
        x0 = int(i * width / n_horizotnal)
        y0 = int(j * height / n_vertical)
        x1 = int((i+1) * width / n_horizotnal)
        y1 = int((j+1) * height / n_vertical)
        segment_bboxes.append([x0, y0, x1, y1])
    
    print("segment bboxes: ", segment_bboxes)

    total_words = 0
    segment_starts = []
    segment_ends = []
    for m in segment_contents:
        segment_starts.append(starts[total_words])
        num_words = countWords(m)
        total_words += num_words
        segment_ends.append(ends[total_words-1])

    print("total words: ", total_words)
    print("correct total words: ", len(starts))

    dir_name = os.path.join(outdir, "highlighted_slides")
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)

    highlighteds = []
    for i in range(len(segment_bboxes)):
        print("processing: ", i)
        slide_copy = copy.deepcopy(slide)
        slide_copy = paint_bboxes(slide_copy, [segment_bboxes[i]])
        highlighteds.append(slide_copy)
        cv2.imwrite(os.path.join(dir_name, str(i)+'.jpg'), slide_copy)
    
    create_image_video(indir, outdir, slide, highlighteds, segment_starts, segment_ends)
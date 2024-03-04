import pytesseract
from pytesseract import Output
import cv2
import os
import shutil
from copy import deepcopy
import nltk
import re
import random
from nltk.corpus import wordnet as wn
import string

# paint bboxes
def paint_bboxes(img, bboxes, path):
    img1 = deepcopy(img)
    for bbox in bboxes:
        x0, y0, x1, y1 = bbox
        cv2.rectangle(img1, (x0, y0), (x1, y1), (255, 0, 0), 4)
    cv2.imwrite(path, img1)

# filter out bboxes with text that doesn't have '[A-Za-z0-9]'
def filter(bboxes, centers, words):
    regexp = re.compile(r'[A-Za-z0-9]')
    new_bboxes = []
    new_centers = []
    new_words = []
    for bbox, center, word in zip(bboxes, centers, words):
        w = "".join(word) # list to string
        if regexp.search(w):
            new_bboxes.append(bbox)
            new_centers.append(center)
            new_words.append(word)

    return new_bboxes, new_centers, new_words

def interval_dist_1D(r1, r2):
     # sort the two ranges such that the range with smaller first element
     # is assigned to x and the bigger one is assigned to y
     x, y = sorted((r1, r2))

     #now if x[1] lies between x[0] and y[0](x[1] != y[0] but can be equal to x[0])
     #then the ranges are not overlapping and return the differnce of y[0] and x[1]
     #otherwise return 0 
     if x[0] <= x[1] < y[0] and all( y[0] <= y[1] for y in (r1,r2)):
        return y[0] - x[1]
     return 0

def merge_horizontal_step(bboxes, centers, words):
    horizontal_margin = 50
    vertical_margin = 20
    new_bboxes = []
    new_centers = []
    new_words = []
    num_merges = 0
    for bbox, center, word in zip(bboxes, centers, words):
        w = "".join(word)
        has_merged = False
        # new bboxes that are already in the list
        for new_bbox, new_center, new_word in zip(new_bboxes, new_centers, new_words):
            new_w = "".join(new_word)
            if abs(center[1] - new_center[1]) < vertical_margin: # if roughly one the same horizontal line (same vertical coordinate)
                if interval_dist_1D([bbox[0], bbox[2]], [new_bbox[0], new_bbox[2]]) < horizontal_margin:
                    x0_A, y0_A, x1_A, y1_A = bbox
                    x0_B, y0_B, x1_B, y1_B = new_bbox
                    x0_C, y0_C = min(x0_A, x0_B), min(y0_A, y0_B) # compute new bbox 
                    x1_C, y1_C = max(x1_A, x1_B), max(y1_A, y1_B)
                    merged_bbox = [x0_C, y0_C, x1_C, y1_C]
                    xc_C = 0.5 * (x0_C + x1_C)
                    yc_C = 0.5 * (y0_C + y1_C)
                    merged_center = [xc_C, yc_C]
                    if center[0] < new_center[0]: # if merge to the left
                        merged_word = word  + [" "] + new_word
                    else: # if merge to the right
                        merged_word = new_word + [" "] + word
                    new_bbox[:] = merged_bbox[:]
                    new_center[:] = merged_center[:]
                    new_word[:] = merged_word[:]
                    has_merged = True
                    num_merges += 1
                    break
                
        if not has_merged:
            new_bboxes.append(bbox)
            new_centers.append(center)
            new_words.append(word)
    
    return new_bboxes, new_centers, new_words, num_merges

def merge_horizontal(bboxes, centers, words):
    while True:
        bboxes, centers, words, num_merges = merge_horizontal_step(bboxes, centers, words)
        if num_merges <= 0:
            break
    return bboxes, centers, words

# input: image
# output: 1. list of bounding boxes  2. list of texts
def get_bboxes(img):
    vis_dir = "bbox_vis"
    os.makedirs(vis_dir, exist_ok=True)

    bboxes = []
    centers = []
    words = []
    # use pytesseract to run initial OCR
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        if d['level'][i] == 5: # only process the word level
            x0, y0 = d['left'][i], d['top'][i]
            x1, y1 = x0 + d['width'][i], y0 + d['height'][i]
            xc = 0.5 * (x0 + x1)
            yc = 0.5 * (y0 + y1)
            bbox = [x0, y0, x1, y1]
            center = [xc, yc]
            word = list(d['text'][i])
            bboxes.append(bbox)
            words.append(word)
            centers.append(center)
    
    paint_bboxes(img, bboxes, os.path.join(vis_dir, "1_initial.jpg"))
    # filter
    bboxes, centers, words = filter(bboxes, centers, words)
    paint_bboxes(img, bboxes, os.path.join(vis_dir, "2_filtered.jpg"))
    # merge horizontal
    bboxes, centers, words = merge_horizontal(bboxes, centers, words)
    paint_bboxes(img, bboxes, os.path.join(vis_dir, "3_merged_horizontal.jpg"))

    return bboxes, ["".join(w) for w in words]
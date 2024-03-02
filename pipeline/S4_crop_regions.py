import os
import shutil
from copy import deepcopy
import cv2
import json

def crop_regions(indir, outdir):

    # Opening JSON file
    f = open(os.path.join(outdir, "DINO_boxes.json"))
    
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

    



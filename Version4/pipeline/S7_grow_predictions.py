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
from .S6_detect_regions import *
from .S2_ask_GPT import *

from openai import OpenAI

def paint_bboxes(img, bboxes):
    base = 0.5
    img1 = deepcopy(img).astype(np.float32)
    mask = np.zeros([img1.shape[0], img1.shape[1]])
    dist = np.zeros([img1.shape[0], img1.shape[1]])
    x, y = np.meshgrid(np.arange(img1.shape[1]), np.arange(img1.shape[0]))
    for bbox in bboxes:
        if len(bbox) < 4:
            x0, y0, x1, y1 = 0, 0, img1.shape[1], img1.shape[0]
        else:
            x0, y0, x1, y1 = bbox
        # xc = int(0.5 * (x0 + x1))
        # yc = int(0.5 * (y0 + y1))
        # Rw = x1 - x0 # rectangle width
        # Rh = y1 - y0 # rectangle height
        # A = int(Rw/np.sqrt(2))
        # B = int(Rh/np.sqrt(2))
        # #cv2.rectangle(img1, (x0, y0), (x1, y1), (255, 0, 0), 4)
        # dist = (x-xc) ** 2 / A ** 2 + (y-yc) ** 2 / B ** 2
        # mask[dist < 1] = 1
        mask[y0:y1, x0:x1] = 1
                            
    mask = cv2.GaussianBlur(mask, (55, 55), 0) 
    img1 *= base + (1-base) * mask[..., np.newaxis]
    return img1.astype(np.uint8)

def ask_GPT_yes_no(image_path, text):
    client = OpenAI()
    # Getting the base64 string
    base64_image = encode_image(image_path)
    print("text at hand: ", text)

    try:
        response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": 
            '''
You are a helpful teaching assistant in a Computer Science class. You are given with a region of a slide (image) and a segment from the lecture (text). Your task is to tell whether the image represents the central object discussed in the text.
            '''},
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f'''                
The text: "{text.rstrip()}"

Please answer strictly in one of the following formats:

Yes, because [why you think the image is the central object].

No, because [why you think the image is not the central object].

Think step by step.
                ''',
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "high"
                },
                },
            ],
            }
        ],
        max_tokens=4000,
        temperature=0.2,
        top_p = 0.1,
        )

        answer = response.choices[0].message.content
        print("GPT answer: \n", answer)

    except Exception as error:
        print("Encountered Exception: \n", error)
        answer = "GPT generation failed"

    return answer

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

    dir_name = os.path.join(outdir, "pred_growth")
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)

    slide_orig = cv2.imread(os.path.join(indir, 'slide.jpg'))
    for i in range(len(segments_loaded)):
        slide_copy2 = copy.deepcopy(slide_orig)
        inter = intersect_bboxes[i]
        print("num intersections:", len(inter))
        if len(inter) > 1:
            inter, _ = nms(inter, [0.5 for _ in range(len(inter))], 0.1)
        print("num intersections afterwards:", len(inter))
        dir_name_i = os.path.join(dir_name, str(i))
        if os.path.exists(dir_name_i):
            shutil.rmtree(dir_name_i)
        os.makedirs(dir_name_i)
        idx = -1
        for bbox in inter:
            idx+=1
            if len(bbox)>=4:
                start_x, start_y, end_x, end_y = bbox
            else:
                start_x, start_y, end_x, end_y = 0, 0, 0, 0
            cv2.rectangle(slide_copy2, (start_x, start_y), (end_x, end_y), (0, 0, 255), 2)
            cv2.imwrite(os.path.join(dir_name_i, 'raw.jpg'), slide_copy2)
            if len(bbox)>=4:
                slide_copy = copy.deepcopy(slide_orig)
                x0, y0, x1, y1 = bbox
                img1 = slide_copy[y0:y1, x0:x1]
                cv2.imwrite(os.path.join(dir_name_i, str(idx)+'.jpg'), img1)

        f = open(os.path.join(indir, "processed_annotation.json"))
        segments_loaded = json.load(f)

        if len(inter[0])>=4:
            answers = []
            for idx in range(len(inter)):
                answer = ask_GPT_yes_no(os.path.join(dir_name_i, str(idx)+'.jpg'), segments_loaded[i]['text'])
                answers.append(answer)
            with open(os.path.join(dir_name_i, "GPT_yes_no.json"), 'w') as f:
                json.dump(answers, f, ensure_ascii=False)

    with open(os.path.join(dir_name, "intersect_bboxes.json"), 'w') as f:
        json.dump(intersect_bboxes, f, ensure_ascii=False)

def process_intersections(indir, outdir):
    dir_name = os.path.join(outdir, "pred_growth")

    slide = cv2.imread(os.path.join(outdir, 'pruned.jpg'))

    f = open(os.path.join(outdir, "GPT_1.json"))
    GPT_1 = json.load(f)

    bboxes = help_parse(GPT_1, slide.shape)

    f = open(os.path.join(indir, "processed_annotation.json"))
    segments_loaded = json.load(f)

    f = open(os.path.join(outdir, "pred_growth", "intersect_bboxes.json"))
    intersect_bboxes = json.load(f)

    #prune intersect_bboxes from gpt
    new_intersect_bboxes = []
    for i in range(len(intersect_bboxes)):
        inter = intersect_bboxes[i]
        if len(intersect_bboxes[i][0]) < 1:
            new_intersect_bboxes.append(intersect_bboxes[i])
        else:
            curr_bboxes = []
            inter, _ = nms(inter, [0.5 for _ in range(len(inter))], 0.1)
            f = open(os.path.join(dir_name, str(i), "GPT_yes_no.json"))
            GPT_answer = json.load(f)
            for idx in range(len(GPT_answer)):
                yes_no = re.findall(r'\s|,|[^,\s]+', GPT_answer[idx])[0]
                print("yes no: ",  yes_no)
                if yes_no == "Yes":
                    curr_bboxes.append(inter[idx])
            new_intersect_bboxes.append(curr_bboxes)
    print("NEW: ", new_intersect_bboxes)
    intersect_bboxes = new_intersect_bboxes

    grown_bboxes = []
    for i in range(len(intersect_bboxes)):
        grown_bboxes.append([bb_list_union(intersect_bboxes[i])])

    print(intersect_bboxes)
    print(grown_bboxes)
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

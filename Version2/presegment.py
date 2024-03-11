import cv2
import os
import numpy as np
from copy import deepcopy
import math

slide = cv2.imread('../slides_collection/248_10_76_graphics/slide.jpg')

breach = 0.25
slide = slide * (1-breach) + 255 * breach

height, width, _ = slide.shape

line_thick = 3
n_horizotnal = 8
n_vertical = 5
for i in range(n_horizotnal+1):
    x = int(i * width / n_horizotnal)
    slide = cv2.line(slide, (x,0), (x, height-1), (0, 255, 0), thickness=line_thick)

for i in range(n_vertical+1):
    y = int(i * height / n_vertical)
    slide = cv2.line(slide, (0,y), (width-1, y), (0, 255, 0), thickness=line_thick)

for i in range(n_horizotnal):
    for j in range(n_vertical):
        x = int((i+0.5) * width / n_horizotnal)
        y = int((j+0.5) * height / n_vertical)
        text = f'{chr(65+j)}{i}'
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 1
        font_thickness = 2
        (text_width, text_height), baseline = cv2.getTextSize(text, font, fontScale=font_scale, thickness=font_thickness)
        cv2.putText(slide, text, (x-int(0.5*text_width), y+int(0.5*text_height)), font, font_scale, (0, 255, 0), font_thickness, lineType=cv2.LINE_AA)

cv2.imwrite("test.jpg", slide)
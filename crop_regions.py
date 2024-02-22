import os
import shutil
from copy import deepcopy
import cv2

bboxes = [(361, 361, 533, 533), (595, 555, 671, 619)] # this is to be changed

video_dir = "slides_collection/149_1_65_graphics"

dir_name = os.path.join(video_dir, "proposed_regions")
if os.path.exists(dir_name):
    shutil.rmtree(dir_name)
os.makedirs(dir_name)

img = cv2.imread(os.path.join(video_dir, "slide.jpg"))
for i in range(len(bboxes)):
    x0, y0, x1, y1 = bboxes[i]
    img1 = deepcopy(img)
    img1 = img[y0:y1, x0:x1]
    cv2.imwrite(os.path.join(dir_name, str(i)+'.jpg'), img1)



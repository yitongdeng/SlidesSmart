import os
from ext.bounding_box import *
import json

def detect_regions(indir, outdir):
  os.system(f'python ext/GroundingDINO/demo/inference_on_a_image.py \
            -c ext/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py \
            -p ext/GroundingDINO/weights/groundingdino_swint_ogc.pth \
            -i {indir}/slide.jpg \
            -o {outdir} \
            -t "object . equation ." \
            --cpu-only')

  bboxes_json = []
  slide_img = cv2.imread(os.path.join(indir, "slide.jpg"))
  bboxes, slide_texts = get_bboxes(slide_img, outdir)
  for b in bboxes:
    bboxes_json.append({"box": b, "certainty": 1.0})
  img1 = paint_bboxes(slide_img, bboxes, os.path.join(outdir, "OCR_preds.jpg"))
  
  with open(os.path.join(outdir, "OCR_boxes.json"), 'w') as f:
    json.dump(bboxes_json, f, ensure_ascii=False)
  
  
  
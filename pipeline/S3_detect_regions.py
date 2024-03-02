import os
 
def detect_regions(indir, outdir):
  os.system(f'python ext/GroundingDINO/demo/inference_on_a_image.py \
            -c ext/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py \
            -p ext/GroundingDINO/weights/groundingdino_swint_ogc.pth \
            -i {indir}/slide.jpg \
            -o {outdir} \
            -t "diagrams . modules . text ." \
            --cpu-only')
from pipeline.S0_presegment import *
from pipeline.S1_audio_to_words import *
from pipeline.S2_ask_GPT import *
from pipeline.S3_parse_GPT import *
from pipeline.S4_crop_boxes import *

import argparse
import os

if __name__ == "__main__":
    record = []
    for name in os.listdir("../slides_collection"):
        if name[0] == ".": # .DS_Store
            continue
        indir = os.path.join("../slides_collection", name)
        outdir = os.path.join("results", name)
        os.makedirs(outdir, exist_ok=True)
        print("===== Processing ", name, " =====")
        
        # print("+++ Presegment +++")
        # presegment_slide(indir, outdir)
        # print("+++ Audio to words +++")
        # audio_to_words(indir, outdir)
        # print("+++ Ask GPT +++")
        # ask_GPT_for_answer(indir, outdir)
        # print("+++ Parse GPT +++")
        # parse_GPT_answer(indir, outdir)

        print("+++ Crop Bbox +++")
        crop_GPT_boxes(indir, outdir)
        
    
    print(record)
    
    






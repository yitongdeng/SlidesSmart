from pipeline.S0_presegment import *
from pipeline.S2_ask_GPT import *
from pipeline.S3_parse_GPT import *
from pipeline.S4_crop_boxes import *
from pipeline.S5_get_texts import *
from pipeline.S6_detect_regions import *
from pipeline.S7_grow_predictions import *

import argparse
import os

if __name__ == "__main__":
    basedir = "../../Kayvon_Lecture_Dataset/slides"
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, required=True)
    args = parser.parse_args()
    indir = os.path.join(basedir, args.name)
    outdir = os.path.join("results", args.name)

    os.makedirs(outdir, exist_ok=True)

    # print("+++ Presegment +++")
    # presegment_slide(indir, outdir)
    # print("+++ Ask GPT +++")
    # ask_GPT_for_answer(indir, outdir)
    # print("+++ Parse GPT +++")
    # parse_GPT_answer(indir, outdir)
    
    print("+++ Detecting Regions +++")
    #detect_regions(indir, outdir)
    prune_regions(indir, outdir)
    print("__Growing Predictions___")
    grow_preds(indir, outdir)


    # print("+++ Print +++")
    # print_texts(indir, outdir)
    # print("+++ Print +++")
    # print_texts(indir, outdir)









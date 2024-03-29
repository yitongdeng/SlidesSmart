from pipeline.S0_presegment import *
from pipeline.S1_audio_to_words import *
from pipeline.S2_ask_GPT import *
from pipeline.S3_parse_GPT import *
from pipeline.S4_crop_boxes import *

import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, required=True)
    args = parser.parse_args()
    indir = os.path.join("../slides_collection", args.name)
    outdir = os.path.join("results", args.name)

    os.makedirs(outdir, exist_ok=True)

    # print("+++ Presegment +++")
    # presegment_slide(indir, outdir)
    # print("+++ Audio to words +++")
    # audio_to_words(indir, outdir)
    # print("+++ Ask GPT +++")
    # ask_GPT_for_answer(indir, outdir)
    print("+++ Parse GPT +++")
    parse_GPT_answer(indir, outdir)
    print("+++ Crop Bbox +++")
    crop_GPT_boxes(indir, outdir)








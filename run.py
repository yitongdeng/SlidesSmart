from pipeline.S0_audio_to_words import *
from pipeline.S1_words_to_segments import *
from pipeline.S2_process_segments import *
from pipeline.S3_detect_regions import *
from pipeline.S4_crop_regions import *
from pipeline.S5_caption_regions import *
from pipeline.S6_match_lecture_slide import *
from pipeline.S7_visualize_results import *

import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, required=True)
    args = parser.parse_args()
    indir = os.path.join("slides_collection", args.name)
    outdir = os.path.join("results", args.name)

    os.makedirs(outdir, exist_ok=True)

    # audio_to_words(indir, outdir)
    # words_to_segments(indir, outdir)
    # process_segments(indir, outdir)
    # detect_regions(indir, outdir)
    crop_regions(indir, outdir)
    caption_regions(indir, outdir)
    match_lecture_slide(indir, outdir)
    visualize_results(indir, outdir)





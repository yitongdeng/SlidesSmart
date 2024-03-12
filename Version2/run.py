from pipeline.S0_presegment import *
from pipeline.S1_audio_to_words import *
from pipeline.S2_ask_GPT import *
from pipeline.S3_parse_GPT import *

import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, required=True)
    args = parser.parse_args()
    indir = os.path.join("../slides_collection", args.name)
    outdir = os.path.join("results", args.name)

    os.makedirs(outdir, exist_ok=True)

    #presegment_slide(indir, outdir)
    #audio_to_words(indir, outdir)
    #ask_GPT_for_answer(indir, outdir)
    parse_GPT_answer(indir, outdir)

    # # print("+++ Audio to Words +++")
    # # audio_to_segments(indir, outdir)
    # # print("+++ Words to Segment +++")
    # # words_to_segments(indir, outdir)
    # # print("+++ Process Segments +++")
    # # process_segments(indir, outdir)
    # # print("+++ Detect Regions +++")
    # # detect_regions(indir, outdir)
    # # print("+++ Prune Regions +++")
    # # prune_regions(indir, outdir)
    # # print("+++ Crop Regions +++")
    # # crop_regions(indir, outdir)
    # print("+++ Caption Regions +++")
    # caption_regions(indir, outdir)
    # print("+++ Match Regions with Lecture +++")
    # match_lecture_slide(indir, outdir)
    # print("+++ Generate Output Video +++")
    # visualize_results(indir, outdir)






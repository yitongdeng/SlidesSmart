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
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-n', '--name', type=str, required=True)
    # args = parser.parse_args()
    # indir = os.path.join("slides_collection", args.name)
    # outdir = os.path.join("results", args.name)

    # os.makedirs(outdir, exist_ok=True)

    #print(os.listdir("slides_collection"))
    for name in os.listdir("slides_collection"):
        if name[0] == ".": # .DS_Store
            continue
        indir = os.path.join("slides_collection", name)
        outdir = os.path.join("results", name)
        os.makedirs(outdir, exist_ok=True)
        print("===== Processing ", name, " =====")
        # print("+++ Audio to Words +++")
        # audio_to_words(indir, outdir)
        # print("+++ Words to Segment +++")
        # words_to_segments(indir, outdir)
        # print("+++ Process Segments +++")
        # process_segments(indir, outdir)
        print("+++ Detect Regions +++")
        detect_regions(indir, outdir)
        print("+++ Prune Regions +++")
        prune_regions(indir, outdir)
        print("+++ Crop Regions +++")
        crop_regions(indir, outdir)
        # print("+++ Caption Regions +++")
        # caption_regions(indir, outdir)
        # print("+++ Match Regions with Lecture +++")
        # match_lecture_slide(indir, outdir)
        #print("+++ Generate Output Video +++")
        #visualize_results(indir, outdir)
        exit()





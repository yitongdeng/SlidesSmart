from pipeline.S5_get_texts import *

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
        
        print_texts(indir, outdir)
    






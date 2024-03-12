import json
import os
import re
from ext.process_video import *

def group_words(indir, outdir):
    
    # Opening "words" JSON file
    f = open(os.path.join(outdir, "words.json"))
    data = json.load(f)

    aggregate_words = "" 
    starts = []
    ends = []
    words = []

    for d in data:
        words.append(d["word"].lower())
        starts.append(d["start"])
        ends.append(d["end"])
    
    print("words: ", words)

    capital_next = True
    for i in range(len(words)):
        if capital_next:
            word = words[i].title()
            capital_next = False
        else:
            word = words[i]

        if i+1 < len(words):
            if starts[i+1] - ends[i] > 0.2:
                aggregate_words += word + ". "
                capital_next = True
            elif starts[i+1] - ends[i] > 0.06:
                aggregate_words += word + ", "
            else:
                aggregate_words += word + " "
        else:
            aggregate_words += word + "."
    
    return aggregate_words







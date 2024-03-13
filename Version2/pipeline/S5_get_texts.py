import os
import base64
import requests
import cv2
import json
from openai import OpenAI

def group_words(indir, outdir):
    
    # Opening "words" JSON file
    f = open(os.path.join(outdir, "words.json"))
    data = json.load(f)

    aggregate_words = "" 
    starts = []
    ends = []
    words = []

    for d in data:
        word = d["word"]
        if word == "": 
            word = "percent"
        words.append(word.lower())
        starts.append(d["start"])
        ends.append(d["end"])

    capital_next = True
    for i in range(len(words)):
        if capital_next:
            word = words[i].title()
            capital_next = False
        else:
            word = words[i]

        if i+1 < len(words):
            if starts[i+1] - ends[i] > 0.3:
                aggregate_words += word + ". "
                capital_next = True
            elif starts[i+1] - ends[i] > 0.05:
                aggregate_words += word + ", "
            else:
                aggregate_words += word + " "
        else:
            aggregate_words += word + "."

    return aggregate_words

def print_texts(indir, outdir):
    print("Lecture text: \n")
    print(group_words(indir, outdir))
import os
import base64
import requests
import cv2
import json
from openai import OpenAI

def print_texts(indir, outdir):
    f = open(os.path.join(indir, "processed_annotation.json"))
    GT = json.load(f)
    
    full_string = ""
    full_paragraph = ""
    for segment in GT:
        full_string += segment['text'] + "\n\n"
        full_paragraph += segment['text'].capitalize() + ". "

    full_string += "\n\n\n" + full_paragraph
    
    with open(os.path.join(outdir, 'out_text.txt'),'w') as f:
        f.write(full_string)
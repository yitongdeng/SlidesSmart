import json
import os
import re
from ext.process_video import *

def process_segments(indir, outdir):
    
    # Opening "words" JSON file
    f = open(os.path.join(outdir, "words.json"))
    data = json.load(f)

    aggregate_words = "" 
    starts = []
    ends = []

    for d in data:
        word = d["word"]
        starts.append(d["start"])
        ends.append(d["end"])
        if word == "": 
            word = "percent"
        aggregate_words += word + " "
        
    aggregate_words = aggregate_words[:-1].lower()

    # Opening "segments" JSON file
    f = open(os.path.join(outdir, "segments.json"))
    data = json.load(f)

    # extract the things inside double quote
    matches = re.findall(r'"(.*?)"', data)
    matches = [m.lower() for m in matches]

    # Returns number of words in string
    def countWords(string):
        OUT = 0
        IN = 1
        state = OUT
        wc = 0
    
        # Scan all characters one by one
        for i in range(len(string)):
    
            # If next character is a separator, 
            # set the state as OUT
            if (string[i] == ' ' or string[i] == '\n' or
                string[i] == '\t'):
                state = OUT
    
            # If next character is not a word 
            # separator and state is OUT, then 
            # set the state as IN and increment 
            # word count
            elif state == OUT:
                state = IN
                wc += 1
    
        # Return the number of words
        return wc

    # aggregate_words2 are the words assembled from GPT's answer
    # this should be the same as the original words
    aggregate_words2 = ""
    total_words = 0
    segment_starts = []
    segment_ends = []
    for m in matches:
        segment_starts.append(starts[total_words])
        aggregate_words2 += m + " "
        num_words = countWords(m)
        total_words += num_words
        segment_ends.append(ends[total_words-1])

    aggregate_words2 = aggregate_words2[:-1].lower()

    success = True

    # this is to make sure the strings match
    if aggregate_words == aggregate_words2:
        print("The original and processed paragraph DOES match")
    else:
        print("The original and processed paragraph DOESN'T match")
        print("words after: ", aggregate_words2)
        print("words before: ", aggregate_words)
        success = False

    # this is to make sure that the division into words match
    if total_words == len(starts):
        print("Number of words DOES match")
    else:
        print("Number of words DOESN'T match")
        print("num words after: ", total_words)
        print("num words before: ", len(starts))
        success = False

    gen_video = True
    if gen_video:
        create_text_video(indir, outdir, matches, segment_starts, segment_ends)

    segment_contents = re.findall(r'Segment\s+\d+:\s*(.*)', data)

    segments = []
    for i in range(len(segment_contents)):
        segments.append({"words": segment_contents[i], "start": segment_starts[i], "end": segment_ends[i]})

    with open(os.path.join(outdir, "segments_processed.json"), 'w') as f:
        json.dump(segments, f, ensure_ascii=False)
    

    return success







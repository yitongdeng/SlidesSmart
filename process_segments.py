import json
import os

video_dir = "slides_collection/149_1_65_graphics"
 
# Opening ORIGINAL JSON file
f = open(os.path.join(video_dir, "words.json"))
 
# returns JSON object as 
# a dictionary
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

# Opening PROCESSED JSON file
f = open(os.path.join(video_dir, "segments.json"))
 
# returns JSON object as 
# a dictionary
data = json.load(f)

# print(data)

import re

# Regular expression to find content within double quotes
matches = re.findall(r'"(.*?)"', data)
matches = [m.lower() for m in matches]
print("matches: ", matches)

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

aggregate_words2 = ""
total_words = 0
segment_starts = []
segment_ends = []
for m in matches:
    segment_starts.append(starts[total_words])
    aggregate_words2 += m + " "
    num_words = countWords(m)
    print("m: ", m)
    print("num words in m: ", num_words)
    total_words += num_words
    segment_ends.append(ends[total_words-1])


aggregate_words2 = aggregate_words2[:-1].lower()

print("aggregate_words: ", aggregate_words)
print("aggregate_words2: ", aggregate_words2)

if aggregate_words == aggregate_words2:
    print("The original and processed paragraph DOES match")
else:
    print("The original and processed paragraph DOESN'T match")

print("starts: ", starts)
print("ends: ", ends)

if total_words == len(starts):
    print("Number of words DOES match")
else:
    print("Number of words DOESN'T match")


print("segment starts: ", segment_starts)
print("segment ends: ", segment_ends)

gen_video = False
if gen_video:
    from process_video import *
    create_text_video(video_dir, matches, segment_starts, segment_ends)

segment_contents = re.findall(r'Segment\s+\d+:\s*(.*)', data)

segments = []
for i in range(len(segment_contents)):
    segments.append({"words": segment_contents[i], "start": segment_starts[i], "end": segment_ends[i]})

with open(os.path.join(video_dir, "segments_processed.json"), 'w') as f:
  json.dump(segments, f, ensure_ascii=False)







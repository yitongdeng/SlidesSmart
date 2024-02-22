import json
import os

video_dir = "slides_collection/149_1_65_graphics"
 
# Opening JSON file
f = open(os.path.join(video_dir, "segments_processed.json"))
 
# returns JSON object as 
# a dictionary
data = json.load(f)

segments = []
for d in data:
    word = d["words"]
    segments.append(word)

# Opening JSON file
f = open(os.path.join(video_dir, "captions.json"))
 
# returns JSON object as 
# a dictionary
captions = json.load(f)

system_str = '''
You are a helpful teaching assistant whose job is to match a sentence that the professor says to a section on the lecture slide.
'''

str0 = '''
All the available sections are described below: 
'''

for i in range(len(captions)):
    str0 += f'''
{i}: {captions[i]}
'''

str0 += '''
Professor's sentence: '''

str1 = '''

Please provide your answer in the following format: The most relevant sentence on the slide is: "[choose one of the sections from above]" 

Think step by step. Also make sure to provide a short (less than 100 words) analysis for why you think the match is appropriate. Emphasize what you think the professor is saying, and the slide is saying, and why they are relevant.
'''

# for i in range(len(segments)):
for i in range(1):
    segment = segments[i]
    print("i: ", i)
    print("segment: ", segment)
    print("text: ", str0 + segment + str1)




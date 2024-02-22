import json
import os
from openai import OpenAI
client = OpenAI()

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

Please provide your answer in the following format: The most relevant sentence on the slide is: [index of the most relevant section]. 

Please always find a match, even if all slide sections are reletively unrelated to the lecture.

Think step by step. Also make sure to provide a short (less than 100 words) analysis for why you think the match is appropriate. Emphasize what you think the professor is saying, and the slide is saying, and why they are relevant.
'''

answers = []
for i in range(len(segments)):
#for i in range(1):
    segment = segments[i]
    print("i: ", i)
    user_str = str0 + segment + str1
    
    response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    messages=[{"role": "system", "content": system_str},
    {"role": "user", "content": user_str}]
    )
    answer = response.choices[0].message.content
    answers.append(answer)
    print("answer: ", answer)

with open(os.path.join(video_dir, "matched_result.json"), 'w') as f:
  json.dump(answers, f, ensure_ascii=False)



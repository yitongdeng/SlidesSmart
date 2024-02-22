import json
import os

video_dir = "slides_collection/149_1_65_graphics"
 
# Opening JSON file
f = open(os.path.join(video_dir, "words.json"))
 
# returns JSON object as 
# a dictionary
data = json.load(f)

aggregate_words = "" 

for d in data:
    word = d["word"]
    if word == "": 
        word = "percent"
    aggregate_words += word + " "
    
    
aggregate_words = aggregate_words[:-1].lower()

print(aggregate_words)
print("num words: ", len(data))

from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    messages=[{"role": "system", "content": 
    '''You are a helpful teaching assistant in a computer science class. You are presented with a paragraph that is transcribed from the professor's lecture, and your job is to break it down into a sequence of disjoint segments (sentences, partial phrases, or groups of sentences) where each segment refers to a single concept or object. 
    
    Make sure to create multiple segments to reflect different numerical references. For instance, "core 1" and "core 2" refer to different objects and should be divided into two segments. 
    
    Feel free to create segments that are partial / incomplete phrases, grammar is not important.
    '''},
    {"role": "user", "content": 
    f'''The paragraph: "{aggregate_words}"

    Please provide your answer in the following format:

    Segment 1: "[a phrase, sentence, or multiple sentences from the paragraph]", which [a description of what the concept or object that this segment refers to]."
    Segment 2: "[a phrase, sentence, or multiple sentences from the paragraph]", which [a description of what the concept or object that this segment refers to]."
    ...

    Think step by step. Please don't miss or add any words in the original paragraph, and please contain the description strictly within 30 words.
    '''}]
)
answer = response.choices[0].message.content
print("answer: ", answer)

with open(os.path.join(video_dir, "segments.json"), 'w') as f:
  json.dump(answer, f, ensure_ascii=False)
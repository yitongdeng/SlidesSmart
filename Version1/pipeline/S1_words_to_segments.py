import json
import os
from openai import OpenAI

def words_to_segments(indir, outdir):
    
    # opening "words" JSON file
    f = open(os.path.join(outdir, "words.json"))
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    # join words together 
    aggregate_words = "" 
    for d in data:
        word = d["word"]
        if word == "": 
            word = "percent"
        aggregate_words += word + " "
        
    aggregate_words = aggregate_words[:-1].lower()

    client = OpenAI()

    # ask GPT to break it apart into chunks
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[{"role": "system", "content": 
        '''You are a helpful teaching assistant in a computer science class. You are presented with a paragraph that is transcribed from the professor's lecture, and your job is to break it down into a sequence of disjoint segments (sentences, partial phrases, or groups of sentences) where each segment refers to a single concept or object. 
                
        Feel free to create segments that are partial / incomplete phrases, grammar is not important.
        '''},
        {"role": "user", "content": 
        f'''The paragraph: "{aggregate_words}"

        Please provide your answer in the following format:

        Segment 1: "[a phrase, sentence, or multiple sentences from the paragraph]", which [a description of what the concept or object that this segment refers to]."
        Segment 2: "[a phrase, sentence, or multiple sentences from the paragraph]", which [a description of what the concept or object that this segment refers to]."
        ...

        Think step by step. Please MAKE SURE TO INCLUDE EXACTLY THE SAME WORDS in the original paragraph. Please contain the description strictly within 30 words.
        '''}]
    )
    answer = response.choices[0].message.content
    print("answer: ", answer)

    with open(os.path.join(outdir, "segments.json"), 'w') as f:
        json.dump(answer, f, ensure_ascii=False)
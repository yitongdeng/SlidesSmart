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
    
    print("words: ", words)

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
        
    print(aggregate_words)
    
    return aggregate_words

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def ask_GPT_for_answer(indir, outdir):

    client = OpenAI()

    # Path to your image
    image_path = os.path.join(outdir, "presegmented.jpg")

    # Getting the base64 string
    base64_image = encode_image(image_path)

    try:
        response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": 
            '''
            You are a helpful teaching assistant in a Computer Science class. You are presented with a slide along with a transcription of the professor's lecture about this slide. Based on your understanding of text and image, your job is to break up the transcription into segments (roughly 5 to 50 words) and match each segment to a slide region as separated by green lines and labeled by green text.

            '''},
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f'''                
                The professor's lecture: "{group_words(indir, outdir)}"

                Please provide your answer strictly in the following format:

                Segment 1: "[lecture segment]" refers to region [your region proposal e.g. "A1-B2"], because the lecture segment [what you think the lecture segment talks about] and the slide region [your region proposal] [what you think the region conveys visually]. The two matches because [reason for believing it is a match].

                Think step by step. Avoid identifying a matching region based on the literal text it contains; instead match with a region based on its visual meaning.
                ''',
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "high"
                },
                },
            ],
            }
        ],
        max_tokens=4000,
        )

        answer = response.choices[0].message.content

    except Exception as error:
        answers = "Null as region may contain safety issues."
        print("ChatGPT refuse to process image: ", i)
        print("Exception: \n", error)

    with open(os.path.join(outdir, "answer.json"), 'w') as f:
        json.dump(answer, f, ensure_ascii=False)
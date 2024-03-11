import os
import base64
import requests
import cv2
import json
from openai import OpenAI

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
            '''You are a helpful teaching assistant whose job is to caption a region of a lecture slide for a visually impaired student. The first image is the full slide, and the second image is the region you will be focusing on.
            '''},
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": '''The professor's lecture: "So here again this is that iphone and now i'm highlighting some of the stuff down here on this processor there are six cpus two of which are big cpu cores that are supposedly good at running single threads there are four small cpu cores that are lower power and good for background stuff Then there's a whole bunch of stuff on there for camera neural networks sensing your heart monitor all this other stuff that's never even run on the cpu it's run on specialized processing."

                Please provide your answer strictly in the following format:

                Segment 1: "[lecture segment]" refers to region [your region proposal, e.g. “A1-C3”], because the lecture segment [what you think the lecture segment talks about] and the slide region [your region proposal] [what you think the region conveys visually].

                Think step by step. Please be doubly careful to avoid omitting or adding new words to the original transcription -- in other words, your lecture segments must add up to exactly the original lecture transcription.
                ''',
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                },
                },
            ],
            }
        ],
        max_tokens=1024,
        )

        answer = response.choices[0].message.content

    except Exception as error:
        answers = "Null as region may contain safety issues."
        print("ChatGPT refuse to process image: ", i)
        print("Exception: \n", error)

    with open(os.path.join(outdir, "answer.json"), 'w') as f:
        json.dump(answer, f, ensure_ascii=False)
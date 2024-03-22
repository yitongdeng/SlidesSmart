import os
import base64
import requests
import cv2
import json
from openai import OpenAI

def get_texts(indir, outdir):
    f = open(os.path.join(indir, "processed_annotation.json"))
    GT = json.load(f)
    
    segments = []
    full_paragraph = ""
    for segment in GT:
        segments.append(segment['text'])
        full_paragraph += segment['text'].capitalize() + ". "

    return segments, full_paragraph

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def ask_GPT_for_answer(indir, outdir):
    segments, full_paragraph = get_texts(indir, outdir)

    client = OpenAI()

    # Path to your image
    image_path = os.path.join(outdir, "presegmented.jpg")
    # Getting the base64 string
    base64_image = encode_image(image_path)

    answers = []
    for i in range(len(segments)):
    #for i in range(5,7):
        print("Processing segment: ", i)
        segment = segments[i]
        try:
            response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": 
                '''
You are a helpful teaching assistant in a Computer Science class. You are given a slide and a transcription of the professor's lecture. Based on your understanding of text and image, your task is to decide if a segment of the lecture is directly referring to a region of the slide. The region has been segmented for you with green lines.
                '''},
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": f'''                
The full transcription: "{full_paragraph.rstrip()}"

The segment: "{segment.rstrip()}"

Please answer strictly in one of the following formats:

Yes, the relevant region is [A1-B2 where A1 and B2 are replaced with the two corners of your bounding box], because [why you think the text and region match].

No, because [why you think a match cannot be found]

Think step by step. Match with regions that are part of illustrations or diagrams, instead of pure text of code.
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
            temperature=0.2,
            top_p = 0.1,
            )

            answer = response.choices[0].message.content

            print("GPT answer: \n", answer)
            answers.append(answer)

        except Exception as error:
            print("Encountered Exception: \n", error)
            answers.append("GPT generation failed")

    with open(os.path.join(outdir, "GPT_1.json"), 'w') as f:
        json.dump(answers, f, ensure_ascii=False)
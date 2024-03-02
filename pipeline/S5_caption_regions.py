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

def caption_regions(indir, outdir):

    client = OpenAI()

    # Path to your image
    image_path = os.path.join(indir, "slide.jpg")

    # Getting the base64 string
    base64_image = encode_image(image_path)

    # List to hold the loaded images
    images = []

    # Loop through each file in the subfolder
    subfolder_path = os.path.join(outdir, "proposed_regions")
    filenames = os.listdir(subfolder_path)
    sorted_filenames = sorted(filenames, key=lambda x: int(os.path.splitext(x)[0]))
    for filename in sorted_filenames:
        if filename.endswith(".jpg"):  # Check if the file is a .jpg image
            img_path = os.path.join(subfolder_path, filename)  # Full path to the image
            print("img_path: ", img_path)
            image = encode_image(img_path)  # Read the image
            if image is not None:
                images.append(image)  # Append the image to the list
            else:
                print(f"Failed to load image: {img_path}")

    answers = []

    for i in range(len(images)):
        image = images[i]
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
                "text": "Provide an informative caption strictly within 30 words. Please be as concise as possible and refrain from offering irrelevant information.",
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                },
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image}",
                },
                },
            ],
            }
        ],
        max_tokens=300,
        )

        answer = response.choices[0].message.content
        answers.append(answer)
        print("answer: ", answer)

    with open(os.path.join(outdir, "captions.json"), 'w') as f:
        json.dump(answers, f, ensure_ascii=False)
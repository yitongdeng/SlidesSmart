from openai import OpenAI
import json
import os

client = OpenAI()

video_dir = "slides_collection/149_1_65_graphics"

audio_file = open(os.path.join(video_dir, "video.mp4"), "rb")
transcript = client.audio.transcriptions.create(
  file=audio_file,
  model="whisper-1",
  response_format="verbose_json",
  timestamp_granularities=["word"]
)

with open(os.path.join(video_dir, "words.json"), 'w') as f:
  json.dump(transcript.words, f, ensure_ascii=False)
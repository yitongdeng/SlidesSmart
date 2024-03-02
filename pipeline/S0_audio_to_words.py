from openai import OpenAI
import json
import os


def audio_to_words(indir, outdir):
  client = OpenAI()

  # open audio file
  audio_file = open(os.path.join(indir, "video.mp4"), "rb")

  # use whisper to generate transcription
  transcript = client.audio.transcriptions.create(
    file=audio_file,
    model="whisper-1",
    response_format="verbose_json",
    timestamp_granularities=["word"]
  )

  # dump transcription
  with open(os.path.join(outdir, "words.json"), 'w') as f:
    json.dump(transcript.words, f, ensure_ascii=False)
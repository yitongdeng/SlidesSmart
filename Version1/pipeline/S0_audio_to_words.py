from openai import OpenAI
import json
import os
from ext.process_video import *



def audio_to_words(indir, outdir):
  client = OpenAI()

  # open audio file
  audio_file = open(os.path.join(indir, "audio.mp3"), "rb")

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

def audio_to_segments(indir, outdir):

  client = OpenAI()

  # open audio file
  audio_file = open(os.path.join(indir, "audio.mp3"), "rb")

  # use whisper to generate transcription
  transcript = client.audio.transcriptions.create(
    file=audio_file,
    model="whisper-1",
    response_format="verbose_json",
    timestamp_granularities=["segment"]
  )

  segments_processed = []
  segment_contents = []
  segment_starts = []
  segment_ends = []
  for s in transcript.segments:
    segment_contents.append(s["text"])
    segment_starts.append(s["start"])
    segment_ends.append(s["end"])
    segments_processed.append({"words": s["text"], "start": s["start"], "end": s["end"]})
  # dump transcription
  with open(os.path.join(outdir, "segments_processed.json"), 'w') as f:
    json.dump(segments_processed, f, ensure_ascii=False)

  gen_video = True
  if gen_video:
      create_text_video(indir, outdir, segment_contents, segment_starts, segment_ends)
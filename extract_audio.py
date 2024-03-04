import argparse
import os

if __name__ == "__main__":
    for name in os.listdir("slides_collection"):
        if name[0] == ".": # .DS_Store
            continue
        indir = os.path.join("slides_collection", name)
        os.system(f'ffmpeg -i {indir}/video.mp4 -ab 160k -ac 2 -ar 44100 -vn {indir}/audio.wav')





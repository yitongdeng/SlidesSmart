import argparse
import os

if __name__ == "__main__":
    for name in os.listdir("results"):
        if name[0] == ".": # .DS_Store
            continue
        outdir1 = os.path.join("../Version1/results", name)
        outdir2 = os.path.join("results", name)
        os.system(f'ffmpeg -i {outdir1}/image_video.mp4 -i {outdir2}/image_video.mp4 -filter_complex "[0:v][1:v]hstack=inputs=2" {outdir2}/merged.mp4')
        





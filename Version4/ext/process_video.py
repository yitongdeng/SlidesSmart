import cv2
import os
import numpy as np
from copy import deepcopy
import ffmpeg
import math
from mutagen.mp3 import MP3


def paint_bboxes(img, bboxes):
    base = 0.5
    img1 = deepcopy(img).astype(np.float32)
    mask = np.zeros([img1.shape[0], img1.shape[1]])
    dist = np.zeros([img1.shape[0], img1.shape[1]])
    x, y = np.meshgrid(np.arange(img1.shape[1]), np.arange(img1.shape[0]))
    for bbox in bboxes:
        if len(bbox) < 4:
            x0, y0, x1, y1 = 0, 0, img1.shape[1], img1.shape[0]
        else:
            x0, y0, x1, y1 = bbox
        xc = int(0.5 * (x0 + x1))
        yc = int(0.5 * (y0 + y1))
        Rw = x1 - x0 # rectangle width
        Rh = y1 - y0 # rectangle height
        A = int(Rw/np.sqrt(2))
        B = int(Rh/np.sqrt(2))
        #cv2.rectangle(img1, (x0, y0), (x1, y1), (255, 0, 0), 4)
        dist = (x-xc) ** 2 / A ** 2 + (y-yc) ** 2 / B ** 2
        mask[dist < 1] = 1
                            
    mask = cv2.GaussianBlur(mask, (55, 55), 0) 
    img1 *= base + (1-base) * mask[..., np.newaxis]
    return img1.astype(np.uint8)


def find_infimum(sorted_list, target):
    left, right = 0, len(sorted_list) - 1
    result = -1  # Initial result value
    result_index = -1  # Index of the result

    while left <= right:
        mid = (left + right) // 2
        # Check if the middle element is less than target
        if sorted_list[mid] < target:
            result = sorted_list[mid]  # Update result
            result_index = mid  # Update result index
            left = mid + 1  # Move to the right half to find a closer number
        else:
            right = mid - 1  # Move to the left half
    
    return result, result_index


def create_image_video(indir, outdir, base_slide, slides, starts, ends):
    video_name = os.path.join(outdir, 'tmp_video.mp4')
    final_video_name = os.path.join(outdir, 'image_video.mp4')
    
    audio = MP3(os.path.join(indir, 'audio.mp3'))
    audio_info = audio.info
    duration = audio_info.length

    fps = 30
    num_frames = math.ceil(duration * fps)

    print("num_frames: ", num_frames)
    print("fps: ", fps)
    print("duration: ", duration)
    width = base_slide.shape[1]
    height = base_slide.shape[0]
    canvas = np.zeros([height, width, 3]).astype(np.uint8)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, fps, (width,height))
    for i in range(num_frames):
        t = i / fps
        if i%100 == 0:
            print("Processing: ", i, " with t: ", t)
            
        canvas_copy = deepcopy(canvas)
        # find what text to display
        start, idx = find_infimum(starts, t)
        end = ends[idx]
        # print(start)
        # print(end)
        # print(idx)
        if idx>=0 and t <= end:
            canvas_copy[:, :] = slides[idx][:, :]
        else:
            canvas_copy[:, :] = base_slide[:, :]

        video.write(canvas_copy)

    cv2.destroyAllWindows()
    video.release()
    audio = ffmpeg.input(os.path.join(indir, 'audio.mp3'))
    video = ffmpeg.input(video_name)
    ffmpeg.output(audio, video, final_video_name).run()
    os.remove(video_name)


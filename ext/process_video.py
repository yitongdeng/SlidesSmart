import cv2
import os
import numpy as np
from copy import deepcopy
import ffmpeg
import math

def extract_frames():
    frame_dir = "../assets/sample_1/frames"
    os.makedirs(frame_dir, exist_ok=True)

    cap = cv2.VideoCapture('../assets/sample_1/video.mp4')
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imwrite(os.path.join(frame_dir, str(i)+'.jpg'), frame)
        i += 1

    cap.release()
    cv2.destroyAllWindows()

def combine_frames():
    image_folder = 'frames'
    video_name = 'video.mp4'

    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # video = cv2.VideoWriter(video_name, 0, 1, (width,height))
    video = cv2.VideoWriter('output.mp4', fourcc, 30.0, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

def intp(frac):
    return 1.-(1.-frac)**2

def interp_func(S, E, tS, tE, t, dist):
    duration = tE - tS
    if duration == 0:
        return E
    #print(dist)
    travel_time = dist # estimate the time needed to travel due to distance 

    travel_time_ratio = min(1.0, travel_time / duration)
    travel_time_ratio = max(0.01, travel_time_ratio) # need a little travel time otherwise divide by 0
    wait_time_ratio = 1 - travel_time_ratio

    frac = (t-tS)/duration
    if frac < wait_time_ratio: # if waiting then do nothing
        return S

    travel_frac = (frac-wait_time_ratio) / travel_time_ratio
    tmp = intp(travel_frac)
    return tmp * E + (1-tmp) * S

def interp_bbox(bbox_start, bbox_end, t, tS, tE, diagonal):
    x0S, y0S, x1S, y1S = bbox_start
    x0E, y0E, x1E, y1E = bbox_end
    wS = x1S - x0S
    wE = x1E - x0E
    hS = y1S - y0S
    hE = y1E - y0E
    centerS = np.array([0.5 * (x0S + x1S), 0.5 * (y0S + y1S)])
    centerE = np.array([0.5 * (x0E + x1E), 0.5 * (y0E + y1E)])
    distance = np.linalg.norm(centerE-centerS)
    dist_ratio = distance / diagonal
    w = interp_func(wS, wE, tS, tE, t, dist_ratio)
    h = interp_func(hS, hE, tS, tE, t, dist_ratio)
    center = interp_func(centerS, centerE, tS, tE, t, dist_ratio)
    return (int(center[0]-0.5*w), int(center[1]-0.5*h), int(center[0]+0.5*w), int(center[1]+0.5*h))


def comp_slide(slide, frame_num, num_frames, ts, bs):
    slide_w = slide.shape[0]
    slide_h = slide.shape[1]
    t = frame_num / 30.0
    final_t = (num_frames) / 30.0
    
    timestamps = [0] + ts + [final_t]
    # Glove avg.
    bboxes = [(0, 0, slide_h, slide_w)] + bs + [(0, 0, slide_h, slide_w)]

    idx = 0
    while idx < len(timestamps)-1 and timestamps[idx+1] < t:
        idx += 1
    
    idx_next = min(idx+1, len(bboxes)-1)
    bbox_start = bboxes[idx]
    bbox_end = bboxes[idx_next]
    diagonal = np.linalg.norm(np.array([slide_w, slide_h]))
    bbox_intped = interp_bbox(bbox_start, bbox_end, t, timestamps[idx], timestamps[idx_next], diagonal)

    return paint_bboxes(slide, [bbox_intped])

def paint_bboxes(img, bboxes):
    base = 0.5
    img1 = deepcopy(img).astype(np.float32)
    mask = np.zeros([img1.shape[0], img1.shape[1]])
    dist = np.zeros([img1.shape[0], img1.shape[1]])
    x, y = np.meshgrid(np.arange(img1.shape[1]), np.arange(img1.shape[0]))
    for bbox in bboxes:
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

def create_video(ts, bs):
    image_folder = '../assets/sample_1/frames'
    video_name = 'created_video.mp4'
    final_video_name = "video_with_audio.mp4"
    

    width = 1920
    height = 1080
    canvas = np.zeros([height, width, 3]).astype(np.uint8)


    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    frame = canvas #cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, 30.0, (width,height))

    num_frames = len(images)
    for i in range(num_frames + 10):
    #for i in range(200):
    #for i in range(1300, 1398):
        if i%1 == 0:
            print("Processing: ", i)
        canvas_copy = deepcopy(canvas)

        # overlay lecture video
        img_name = images[min(i, len(images)-1)]
        image = cv2.imread(os.path.join(image_folder, img_name))
        lecture_h, lecture_w = image.shape[0], image.shape[1]
        h_begin = int((height-lecture_h)/2)
        canvas_copy[h_begin:h_begin+lecture_h, -lecture_w:] = image

        # overlay slide
        slide = cv2.imread('../assets/sample_1/slide.jpg')
        slide_masked = comp_slide(slide, i, num_frames, ts, bs)
        #print(slide.shape)
        slide_w = width - lecture_w
        slide_h = int(slide_w * (slide.shape[0] / slide.shape[1]))
        slide_resized = cv2.resize(slide_masked, (slide_w, slide_h))
        h_begin = int((height-slide_h)/2)
        canvas_copy[h_begin:h_begin+slide_h, :slide_w] = slide_resized

        video.write(canvas_copy)

    cv2.destroyAllWindows()
    video.release()
    audio = ffmpeg.input('../assets/sample_1/audio.wav')
    video = ffmpeg.input(video_name)
    ffmpeg.output(audio, video, final_video_name).run()


def get_video_length(filename):
    cap = cv2.VideoCapture(filename)
    if not cap.isOpened():
        return None
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frame rate
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    cap.release()
    return frame_count, fps, duration

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

import textwrap

def draw_text(img, text, pos, font, max_width, font_scale, font_thickness, text_color, bg_color):    
    (text_width, text_height), baseline = cv2.getTextSize(text, font, fontScale=font_scale, thickness=font_thickness)
    line_height = text_height + baseline + 10  # Calculate line height

    wrapper = textwrap.TextWrapper(width=max_width, break_long_words = False) 
    lines = wrapper.wrap(text = text) # Split the text into lines based on the max width

    for i, line in enumerate(lines):
        (text_width, text_height), baseline = cv2.getTextSize(line, font, fontScale=font_scale, thickness=font_thickness)
        line_y = pos[1] + i * line_height  # Calculate the y position for each line
        cv2.putText(img, line, (pos[0]-int(0.5*text_width), line_y), font, font_scale, text_color, font_thickness, lineType=cv2.LINE_AA)

def create_text_video(root_dir, texts, starts, ends):
    video_name = os.path.join(root_dir, 'tmp_video.mp4')
    final_video_name = os.path.join(root_dir, 'text_video.mp4')
    
    video_source = os.path.join(root_dir, 'video.mp4')
    num_frames, fps, duration = get_video_length(video_source)
    print("num_frames: ", num_frames)
    print("fps: ", fps)
    print("duration: ", duration)
    width = 1920
    height = 1080
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
            max_width = 50
            draw_text(canvas_copy, texts[idx], (int(width/2-0.5*max_width), int(height/2)), \
                    cv2.FONT_HERSHEY_SIMPLEX, max_width, 1, 2, (230, 230, 230), (0,0,0))

        video.write(canvas_copy)

    cv2.destroyAllWindows()
    video.release()
    audio = ffmpeg.input(os.path.join(root_dir, 'audio.wav'))
    video = ffmpeg.input(video_name)
    ffmpeg.output(audio, video, final_video_name).run()
    os.remove(video_name)

def create_image_video(indir, outdir, base_slide, slides, starts, ends):
    video_name = os.path.join(outdir, 'tmp_video.mp4')
    final_video_name = os.path.join(outdir, 'image_video.mp4')
    
    video_source = os.path.join(indir, 'video.mp4')
    num_frames, fps, duration = get_video_length(video_source)
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
    audio = ffmpeg.input(os.path.join(indir, 'audio.wav'))
    video = ffmpeg.input(video_name)
    ffmpeg.output(audio, video, final_video_name).run()
    os.remove(video_name)


import json
import os

video_dir = "slides_collection/149_1_65_graphics"
 
f = open(os.path.join(video_dir, "matched_result.json"))
 
data = json.load(f)

print(data)
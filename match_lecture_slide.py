import json
import os

video_dir = "slides_collection/149_1_65_graphics"
 
# Opening JSON file
f = open(os.path.join(video_dir, "segments_processed.json"))
 
# returns JSON object as 
# a dictionary
data = json.load(f)

segments = []
for d in data:
    word = d["words"]
    segments.append(word)

# Opening JSON file
f = open(os.path.join(video_dir, "captions.json"))
 
# returns JSON object as 
# a dictionary
data = json.load(f)

print(data)
exit()

system_str = '''
You are a helpful teaching assistant whose job is to match a sentence that the professor says to a section on the lecture slide.
'''

str0 = '''
All the available sections are described below: 

Illustration of CPU architecture with three stacked blocks labeled Fetch/Decode, ALU, Execution Context; color-coded orange, yellow, and blue, representing the processor's functional units.

Bottom slide region; blue box labeled "Execution Context," contains four registers R0 to R3, signifies CPU's temporary storage for instruction processing.

Top slide region; black bold text on white background reads "A processor executes instructions," serving as the title of the slide.

Top block of the CPU diagram; orange rectangle labeled "Fetch/Decode," representing the stage where instructions are retrieved and interpreted.

Middle block of the CPU diagram; yellow rectangle labeled "ALU (Execution Unit)," representing the part that performs arithmetic and logical operations.

Part of the Execution Context; detail of Register 0 (R0), the first register in a series, indicating its role as a storage unit within the processor.

Detail of Execution Context; Register 1 (R1) labeled, second in a sequence, indicating its function as temporary storage in the processor.

Detail of Execution Context; Register 2 (R2) labeled, third in a sequence, represents a storage unit for data within the CPU.

Part of Execution Context; Register 3 (R3) labeled, fourth in sequence, depicts a storage location for computational data in the CPU.

Text above the Fetch/Decode block; black, bold, describes the processor's next action determination in the instruction execution cycle.

Text adjacent to ALU block; black, bold, explains the ALU's role in performing operations as described by instructions, potentially modifying processor and memory values.

Text at the bottom of the CPU diagram; black, bold, describes the function of registers in maintaining the state of the program by storing variable values.

Footer of slide; black text on white background indicates "Stanford CS149, Fall 2023," denoting the course and semester.

Professor's sentence: '''

str1 = '''

Please provide your answer in the following format: The most relevant sentence on the slide is: "[choose one of the sections from above]" 

Think step by step. Also make sure to provide a short (less than 100 words) analysis for why you think the match is appropriate. Emphasize what you think the professor is saying, and the slide is saying, and why they are relevant.
'''

# for i in range(len(segments)):
for i in range(1):
    segment = segments[i]
    print("i: ", i)
    print("segment: ", segment)
    print("text: ", str0 + segment + str1)




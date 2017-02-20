from moviepy.editor import VideoFileClip
import matplotlib.pyplot as plt
from scipy import misc

INPUT_VIDEO = "astoria.mp4"
OUTPUT_VIDEO = "video/clip2.mp4"


clip = VideoFileClip(INPUT_VIDEO)

"""
for i in range(10):
	t = 80 + i*3
	f = clip.get_frame(t)
	misc.imsave("images/frame_1_{}.png".format(str(t).zfill(4)), f)
"""


out_clip = clip.subclip(110, 130)
out_clip.write_videofile(OUTPUT_VIDEO)
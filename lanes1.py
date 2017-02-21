import matplotlib.pyplot as plt
from pipeline2 import *
from scipy import misc
from moviepy.editor import VideoFileClip


INPUT_VIDEO = "videos/clip1.mp4"
OUTPUT_VIDEO = "out1.mp4"

def img_test():
	img = misc.imread("images/frame_1_0086.png")
	plt.imshow(pipeline(img))
	plt.show()

def video_test():
	clip = VideoFileClip(INPUT_VIDEO).subclip(0,5)
	transformed = clip.fl_image(pipeline)
	transformed.write_videofile(OUTPUT_VIDEO, audio=False)


#img_test()
video_test()
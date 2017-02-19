from moviepy.editor import VideoFileClip
import matplotlib.pyplot as plt
from scipy import misc

INPUT_VIDEO = "astoria.mp4"
OUTPUT_VIDEO = "out.mp4"


clip = VideoFileClip(INPUT_VIDEO)

for i in range(10):
	t = 80 + i*3
	f = clip.get_frame(t)
	misc.imsave("images/frame_1_{}.png".format(str(t).zfill(4)), f)
#plt.imshow(f)
#plt.show()

#out_clip = clip.subclip(90, 110)
#out_clip.write_videofile(OUTPUT_VIDEO)
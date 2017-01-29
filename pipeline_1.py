# TODO: Build your pipeline that will draw lane lines on the test_images
# then save them to the test_images directory.
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
from math import *
#%matplotlib inline

def get_line(x1, y1, x2, y2):
	m = (y2 - y1)  / (x2 - x1)
	b1 = y1 - m * x1
	return m, b1

def get_y(m, b, x):
	return int(m * x  + b)

def get_x(m, b, y):
	return int((y-b) / m)

def pipeline(img):

	gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	kernel_size = 7
	blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

	low_threshold = 50
	high_threshold = 150
	edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

	mask = np.zeros_like(edges)   
	ignore_mask_color = 255  

	H = img.shape[0]
	W = img.shape[1]	

	Y1_CUT = int(H * 0.5)
	Y2_CUT = int(H)

	vertices = np.array([[
		(int(W * 0.49), int(H * 0.5)),
		(int(W * 0.51), int(H * 0.5)),
		(int(W * 0.9) , int(H)),
		(int(W * 0.1), int(H))]])


	cv2.fillPoly(mask, vertices, ignore_mask_color)
	masked_edges = cv2.bitwise_and(edges, mask)

	# Define the Hough transform parameters
	# Make a blank the same size as our image to draw on
	rho = 1 # distance resolution in pixels of the Hough grid
	theta = np.pi/90 # angular resolution in radians of the Hough grid
	threshold = 15     # minimum number of votes (intersections in Hough grid cell)
	min_line_length = 70 #minimum number of pixels making up a line
	max_line_gap = 30    # maximum gap in pixels between connectable line segments
	line_image = np.copy(img)*0 # creating a blank to draw lines on


	# Run Hough on edge detected image
	# Output "lines" is an array containing endpoints of detected line segments
	lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
	                            min_line_length, max_line_gap)

	for line in lines:
		for x1, y1, x2, y2 in line:

			adj = abs(x1 - x2)
			opp = abs(y1 - y2)

			if (opp == 0) : continue

			at = adj / opp

			# if the slope is higher than the threshold, it is probably not a lane
			if  degrees(atan(at)) > 60 : continue


			m, b = get_line(x1, y1, x2, y2)
			print ('{} {}'.format(m, b))



			cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)

			cv2.line(line_image, (get_x(m, b, Y1_CUT), Y1_CUT), (get_x(m, b, Y2_CUT), Y2_CUT), (0, 0, 255), 8   )



	edges3col = np.dstack((edges, edges, edges))

	fine = cv2.addWeighted(img, 0.8, line_image, 1, 0)
	#fine = cv2.addWeighted(edges3col, 0.8, line_image, 1, 0)

	return fine



img_list = os.listdir("test_images/")
img_list = img_list[1:2]

i = 1
for img_file in img_list:
    img = mpimg.imread("test_images/" + img_file)
    print(img_file)
    img_processed = pipeline(img)
    plt.subplot(1, len(img_list), i)
    plt.imshow(img_processed)
    i += 1


plt.show()
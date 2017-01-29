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

	Y1_CUT = int(H * 0.6)
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

	## a line with less slope probably is not a lane
	MIN_SLOPE = 0.6
	
	## a map with the line candidates
	## key : slope m's sign (pos / neg)
	line_map = { True : [], False : []}

	for line in lines:
		for x1, y1, x2, y2 in line:

			m, b = get_line(x1, y1, x2, y2)
			if (abs(m) < MIN_SLOPE) : continue
			line_map[m > 0].append((m, b))


			cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 4)

			#cv2.line(line_image, (get_x(m, b, Y1_CUT), Y1_CUT), (get_x(m, b, Y2_CUT), Y2_CUT), (0, 0, 255), 8   )


	## calculating the avarage lines from the candidates (positive and negative slope candidates)
	line_avg = { True : [], False : []}
	for key in line_map:
		m_sum = 0
		b_sum = 0
		for m, b in line_map[key]:
			m_sum += m
			b_sum += b

		m_avg = m_sum / len(line_map[key])
		b_avg = b_sum / len(line_map[key])
		line_avg[key] = m_avg, b_avg

	## drawing the final candidate lane
	# positive slope
	pos_m, pos_b = line_avg[True]
	px1, py1, px2, py2 = get_x(pos_m, pos_b, Y1_CUT), Y1_CUT, get_x(pos_m, pos_b, Y2_CUT), Y2_CUT 
	# negative slope
	neg_m, neg_b = line_avg[False]
	nx1, ny1, nx2, ny2 = get_x(neg_m, neg_b, Y1_CUT), Y1_CUT, get_x(neg_m, neg_b, Y2_CUT), Y2_CUT 

	cv2.line(line_image, (px1, py1), (px2, py2), (0, 0, 255), 10   )
	cv2.line(line_image, (nx1, ny1), (nx2, ny2), (0, 0, 255), 10   )


	edges3col = np.dstack((edges, edges, edges))

	fine = cv2.addWeighted(img, 0.8, line_image, 1, 0)
	#fine = cv2.addWeighted(edges3col, 0.8, line_image, 1, 0)

	return fine



img_list = os.listdir("test_images/")
img_list = img_list[0:1]

i = 1
for img_file in img_list:
    img = mpimg.imread("test_images/" + img_file)
    print(img_file)
    img_processed = pipeline(img)
    plt.subplot(1, len(img_list), i)
    plt.imshow(img_processed)
    i += 1


plt.show()
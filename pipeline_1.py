# TODO: Build your pipeline that will draw lane lines on the test_images
# then save them to the test_images directory.
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
from math import *
#%matplotlib inline

POS_LINE_STACK = []
NEG_LINE_STACK = []

POS_LINE_HISTORY = []
NEG_LINE_HISTORY = []

def get_m_b_smoothed(mb, hist):
	HIST_FRAMES = 5
	hist.append(mb)
	
	m_sum = 0
	b_sum = 0
	l = len(hist[-HIST_FRAMES:])
	for (m, b) in hist[-HIST_FRAMES:]:
		m_sum += m
		b_sum += b

	return (m_sum / l, b_sum / l)

def get_line(x1, y1, x2, y2):
	m = (y2 - y1)  / (x2 - x1)
	b1 = y1 - m * x1
	return m, b1

def get_x(m, b, y):
	return int((y-b) / m)

def get_lane_coords(line_avg, Y1_CUT, Y2_CUT, W, H):
	if True in line_avg:
		pos_m, pos_b = get_m_b_smoothed(line_avg[True], POS_LINE_HISTORY)
		px1, py1, px2, py2 = get_x(pos_m, pos_b, Y1_CUT), Y1_CUT, get_x(pos_m, pos_b, Y2_CUT), Y2_CUT 
		POS_LINE_STACK.append((px1, py1, px2, py2))
	else :
		# no line? use the previous
		px1, py1, px2, py2 = POS_LINE_STACK[-1]
		#px1, py1, px2, py2  = W, 0, W, H 
	# negative slope
	if False in line_avg:
		neg_m, neg_b = get_m_b_smoothed(line_avg[False], NEG_LINE_HISTORY)
		nx1, ny1, nx2, ny2 = get_x(neg_m, neg_b, Y1_CUT), Y1_CUT, get_x(neg_m, neg_b, Y2_CUT), Y2_CUT 
		NEG_LINE_STACK.append((nx1, ny1, nx2, ny2))
	else :
		nx1, ny1, nx2, ny2 = NEG_LINE_STACK[-1]
		#nx1, ny1, nx2, ny2  = 0, 0, 0, H

	return px1, py1, px2, py2, nx1, ny1, nx2, ny2

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

	# Run Hough on edge detected image
	# Output "lines" is an array containing endpoints of detected line segments
	lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
	                            min_line_length, max_line_gap)

	## a line with less slope probably is not a lane
	MIN_SLOPE = 0.5
	
	## a map with the line candidates
	## key : slope m's sign (pos / neg)
	line_map = { True : [], False : []}

	for line in lines:
		for x1, y1, x2, y2 in line:
			m, b = get_line(x1, y1, x2, y2)
			if (abs(m) < MIN_SLOPE) : continue
			line_map[m > 0].append((m, b))

	## calculating the avarage lines from the candidates (positive and negative slope candidates)
	line_avg = {}
	for key in line_map:
		if len(line_map[key]) == 0 : continue
		m_sum = 0
		b_sum = 0
		for m, b in line_map[key]:
			m_sum += m
			b_sum += b

		m_avg = m_sum / len(line_map[key])
		b_avg = b_sum / len(line_map[key])
		line_avg[key] = m_avg, b_avg

	## drawing the final candidate lanes
	# positive slope
	
	px1, py1, px2, py2, nx1, ny1, nx2, ny2 = get_lane_coords(line_avg, Y1_CUT, Y2_CUT, W, H)

	lane_cover = cv2.fillPoly(np.copy(img) * 0, np.array([[(px1, py1), (px2, py2), (nx2, ny2), (nx1, ny1)]]), (200, 200, 0))
	final = cv2.addWeighted(img, 1, lane_cover, 0.5, 0)

	return final



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
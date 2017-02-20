import numpy as np
import cv2
from math import *

BLUR_KERNEL_SIZE = 5
CANNY_LOW_THRESHOLD = 50
CANNY_HIGH_THRESHOLD = 150


# the hough transaform parameters
H_RHO = 1 # distance resolution in pixels of the Hough grid
H_THETA = np.pi/90 # angular resolution in radians of the Hough grid
H_THRESHOLD = 15     # minimum number of votes (intersections in Hough grid cell)
H_MIN_LINE_LENGTH = 30 #minimum number of pixels making up a line
H_MAX_LINE_GAP = 100    # maximum gap in pixels between connectable line segments

MIN_ABS_LINE_SLOPE = 0.2

LANE_CUT = 0.6

def get_line_func(x1, y1, x2, y2):
	m = (y2 - y1)  / (x2 - x1)
	b1 = y1 - m * x1
	return m, b1

# calculates the x for a linear function
def get_x(m, b, y):
	if m == inf or b == inf:  return 0
	return int((y-b) / m)

def pipeline(img):
	H = img.shape[0]
	W = img.shape[1]	

	## blur and canny edges
	blur_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	blur_gray = cv2.GaussianBlur(blur_gray, (BLUR_KERNEL_SIZE, BLUR_KERNEL_SIZE), 0)
	edges = cv2.Canny(blur_gray, CANNY_LOW_THRESHOLD, CANNY_HIGH_THRESHOLD)

	## masking
	vertices = np.array([[
		(int(W * 0.39), int(H * 0.5)),
		(int(W * 0.61), int(H * 0.5)),
		(int(W * 0.9) , int(H)),
		(int(W * 0.1), int(H))]])
	mask = np.zeros_like(edges)

	mask = cv2.fillPoly(mask, vertices, 255)
	masked_edges = cv2.bitwise_and(edges, mask)

	## getting the lines with a hough-transform
	lines = cv2.HoughLinesP(masked_edges, H_RHO, H_THETA, H_THRESHOLD, np.array([]),
	                            H_MIN_LINE_LENGTH, H_MAX_LINE_GAP)

	## processing the line coords

	# 2 lists for the lines.
	# grouping them by slope direction (positive / negative)
	line_map = {True  : [], False : []}

	img_with_lines = np.array(img)
	for line in lines:
		for (x1, y1, x2, y2) in line:
			m, b = get_line_func(x1, y1, x2, y2)

			# filtering by slope
			if (abs(m) < MIN_ABS_LINE_SLOPE) : continue

			# grouping the lines by slope
			line_map[m > 0].append((m, b))
			cv2.line(img_with_lines, (x1, y1), (x2, y2), (255, 0, 0), 3)


	## calculating the average slope, for both directions
	final_slopes = {}
	for direction in line_map:
		if len(line_map[direction]) == 0:
			final_slopes[direction] = (1,0)
			continue

		m_sum = 0
		b_sum = 0
		for m, b in line_map[direction]:
			m_sum += m
			b_sum += b
		final_slopes[direction] = (m_sum / len(line_map[direction]), b_sum / len(line_map[direction]))


	final_image = np.array(img)
	for dir in final_slopes:
		m, b = final_slopes[dir]
		cv2.line(final_image, (get_x(m, b, int(H * LANE_CUT)), int(H * LANE_CUT)), (get_x(m, b, H), H), (0, 255, 0), 3)


	# putting together the frame

	rgb_masked_edges = np.dstack((masked_edges, masked_edges, masked_edges))

	left = np.concatenate((img_with_lines, rgb_masked_edges), axis = 0 )
	right = np.concatenate((final_image, final_image), axis = 0)

	out = np.concatenate((left, right), axis = 1)
	
	return out

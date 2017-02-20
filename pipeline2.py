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
H_MIN_LINE_LENGTH = 70 #minimum number of pixels making up a line
H_MAX_LINE_LENGTH = 30    # maximum gap in pixels between connectable line segments

def pipeline(img):
	H = img.shape[0]
	W = img.shape[1]	

	# blur and canny edges
	blur_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	blur_gray = cv2.GaussianBlur(blur_gray, (BLUR_KERNEL_SIZE, BLUR_KERNEL_SIZE), 0)
	edges = cv2.Canny(blur_gray, CANNY_LOW_THRESHOLD, CANNY_HIGH_THRESHOLD)

	# masking
	vertices = np.array([[
		(int(W * 0.39), int(H * 0.5)),
		(int(W * 0.61), int(H * 0.5)),
		(int(W * 0.9) , int(H)),
		(int(W * 0.1), int(H))]])
	mask = np.zeros_like(edges)

	mask = cv2.fillPoly(mask, vertices, 255)
	masked_edges = cv2.bitwise_and(edges, mask)

	# getting the lines with a hough-transform
	lines = cv2.HoughLinesP(masked_edges, H_RHO, H_THETA, H_THRESHOLD, np.array([]),
	                            H_MIN_LINE_LENGTH, H_MAX_LINE_LENGTH)

	for line in lines:
		for (x1, y1, x2, y2) in line:
			cv2.line(masked_edges, (x1, y1), (x2, y2), 255, 3)


	out = np.dstack((masked_edges, masked_edges, masked_edges))

	out = np.concatenate((img, out), axis = 0 )

	
	return out

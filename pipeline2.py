import numpy as np
import cv2
from math import *

BLUR_KERNEL_SIZE = 5
CANNY_LOW_THRESHOLD = 50
CANNY_HIGH_THRESHOLD = 150

def pipeline(img):
	blur_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	blur_gray = cv2.GaussianBlur(blur_gray, (BLUR_KERNEL_SIZE, BLUR_KERNEL_SIZE), 0)
	edges = cv2.Canny(blur_gray, CANNY_LOW_THRESHOLD, CANNY_HIGH_THRESHOLD)

	out = np.dstack((edges, edges, edges))
	
	return out

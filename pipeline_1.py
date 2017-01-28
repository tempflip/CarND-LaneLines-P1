# TODO: Build your pipeline that will draw lane lines on the test_images
# then save them to the test_images directory.
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
#%matplotlib inline

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
	vertices = np.array([[
		(int(W * 0.49), int(H * 0.5)),
		(int(W * 0.51), int(H * 0.5)),
		(int(W * 0.9) , int(H)),
		(int(W * 0.1), int(H))]])

	print(vertices)

	cv2.fillPoly(mask, vertices, ignore_mask_color)
	masked_edges = cv2.bitwise_and(edges, mask)


	return masked_edges



img_list = os.listdir("test_images/")
img_list = img_list[0:1]

i = 1
for img_file in img_list:
    img = mpimg.imread("test_images/" + img_file)
    print(img_file)
    img_processed = pipeline(img)
    plt.subplot(len(img_list), 1, i)
    plt.imshow(img_processed)
    i += 1


plt.show()
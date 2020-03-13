import cv2
import os
import random

from cv2.ximgproc import thinning

from enum import Enum

from skimage import morphology

import numpy as np

ROOT_DIR = os.path.abspath(".")
IMAGE_PATH = os.path.join(ROOT_DIR, "images/itmo_logo_horiz_blue_en.jpg")
#IMAGE_PATH = os.path.join(ROOT_DIR, "images/itmo_logo_horiz_white_en.png")


WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# by default
STEP_PARAM = 1
RAD_PARAM = 1

LIGHT_BACKGROUND = True

def process_image(IMAGE_PATH, STEP_PARAM, RAD_PARAM):

	img = cv2.imread(IMAGE_PATH)
	skel = np.ones(img.shape, np.uint8)*255
	image = np.ones(img.shape, np.uint8)*255



	# change color
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# skeletonization
	if LIGHT_BACKGROUND:
		ret,img = cv2.threshold(img,100,255,cv2.THRESH_BINARY_INV)
	else:
		ret,img = cv2.threshold(img,100,255,cv2.THRESH_BINARY)
	img = cv2.ximgproc.thinning(img, img, cv2.ximgproc.THINNING_ZHANGSUEN)

	contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

	if (STEP_PARAM == 0 & RAD_PARAM == 0):
		# loop through the contours/hierarchy
		for j in range(len(contours)):
			cv2.drawContours(skel, contours, j, BLACK_COLOR);
	else:
		for j in range(len(contours)):
			contours1 = contours[j].reshape(-1,2)
			contours1 = contours1[::STEP_PARAM]
			print(contours1[0])
			for (x, y) in contours1:
				cv2.circle(skel, (x, y), RAD_PARAM, BLACK_COLOR, 1)

	image_gray = cv2.cvtColor(skel, cv2.COLOR_BGR2GRAY)
	ret,image_1 = cv2.threshold(image_gray,100,255,cv2.THRESH_BINARY_INV)
	contours, hierarchy = cv2.findContours(image_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	for j in range(len(contours)):
		contours2 = contours[j].reshape(-1,2)
		for (x, y) in contours2:
			cv2.circle(image, (x, y), 1, BLACK_COLOR, 1)

	cv2.imwrite("image.bmp", skel)
	cv2.imwrite("final.bmp", image)
	return skel

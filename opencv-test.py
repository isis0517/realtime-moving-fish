import cv2
import numpy as np
import sys
import tkinter as tk
from multiprocessing import Process,Queue		#multi process to aviod imshow be effected
import time
import matplotlib.pyplot as plt

if __name__ == '__main__':
	fish = cv2.imread("testdata\\zebrafish.png")
	blank = 255.0 * np.ones((1080,1920,3), dtype = np.int8)	#full with one and mutiply 255.0 to get blank background
	print(blank[2,2,1])

	cv2.imshow("test", blank)
	cv2.waitKey(2000)

	cv2.imshow("test", fish)
	cv2.waitKey(2000)

	fish = np.fliplr(fish)
	cv2.imshow("test", fish)
	cv2.waitKey(2000)

	flip = cv2.getRotationMatrix2D((fish.shape[0]/2, fish.shape[1]/2), -45, 1)
	new_fish = cv2.warpAffine()
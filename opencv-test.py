import cv2
import numpy as np
import time

if __name__ == '__main__':


	dtype = cv2.imread("testdata\\zebrafish.png").dtype	#get the type of the numpyarray
	raw_fish = cv2.imread("testdata\\zebrafish.png")	#get the raw fish data

	Len_fish = raw_fish.shape[1]						#get the longest side
	Drif = (raw_fish.shape[1]-raw_fish.shape[0])//2		#caculate the dift form sort side to long side
	square_fish = np.zeros((Len_fish,Len_fish,3),dtype=dtype)	#generate the square image
	square_fish[Drif+1:-Drif,:] = raw_fish				#put original fish image into square with dift

	blank = 255*np.ones((1080,1920,3), dtype=dtype)	#full with one and mutiply 255.0 to get blank background

	"""cv2.imshow("test", blank)
	cv2.waitKey(2000)

	cv2.imshow("test", fish)
	cv2.waitKey(2000)

	fish = np.fliplr(fish)
	cv2.imshow("test", fish)
	cv2.waitKey(2000)"""


	rota = cv2.getRotationMatrix2D((Len_fish/2, Len_fish/2), -45, 1)	#get the rotation matric
	rot_fish = cv2.warpAffine(square_fish, rota ,(Len_fish,Len_fish))	#apply the rotation matric on sequare_fish
	rot_fish_gray = cv2.cvtColor(rot_fish, cv2.COLOR_BGR2GRAY)			#generate the gray image
	ret, mask = cv2.threshold(rot_fish_gray, 10, 255, cv2.THRESH_BINARY)#generate the mask which used to determind where the pixel pass
	mask_inv = cv2.bitwise_not(mask)									#invers mask


	rows, cols, channel = square_fish.shape								#get the size of squared fish 

	roi = blank[0:rows, 0:cols]											#this
	show_bk = cv2.bitwise_and(blank,(0),mask = mask_inv)					#
	show_fg = cv2.bitwise_and(rot_fish,rot_fish,mask = mask)
	showup = cv2.add(show_bk,show_fg)

	#cv2.resizeWindow("test", 1000,1000)
	cv2.imshow("test", showup)
	cv2.waitKey(2000)
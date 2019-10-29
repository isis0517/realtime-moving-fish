import cv2
import numpy as np
import sys
import queue

cap = cv2.VideoCapture(0)
cv2.startWindowThread()
cv2.namedWindow("frame")

if cap.isOpened():
	print("Y")

while(True):
	# 從攝影機擷取一張影像
	ret, frame = cap.read()
	#翻轉影像
	frame = np.flip(frame,1)
	# 顯示圖片
	cv2.imshow('frame', frame)

	# 若按下 q 鍵則離開迴圈
	if cv2.waitKey(25) & 0xFF == ord('q'):
		break

# 釋放攝影機
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()
 
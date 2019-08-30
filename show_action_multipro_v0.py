import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
import tkinter as tk
from multiprocessing import Process, Queue		#multi process to aviod imshow be effected
from functools import partial

def show_window(action):

	Left = cv2.VideoCapture("testdata\\Left.mp4") 
	Right = cv2.VideoCapture("testdata\\Left.mp4")
	stop_img = cv2.imread("testdata\\Stop.jpg")


	if (not Left.isOpened() or not Right.isOpened()):
		print("You die")
		sys.die()

	while(Left.read()):
		action.put(frame)


	while(True):
		# 從攝影機擷取一張影像
		#ret, frame = cap.read()
		#翻轉影像
		#frame = np.flip(frame,1)
		frame = stop_img if action.empty() else action.get()
		# 顯示圖片
		cv2.imshow('frame', frame)

		# 若按下 q 鍵則離開迴圈
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# 釋放攝影機
	#cap.release()

	# 關閉所有 OpenCV 視窗
	cv2.destroyAllWindows()


def show_console(q):
	Left = cv2.VideoCapture("testdata\\Left.mp4") 
	q.put(Left)
	# 第1步，例項化object，建立視窗window
	window = tk.Tk()

	# 第2步，給視窗的視覺化起名字
	window.title('My Window')

	# 第3步，設定視窗的大小(長 * 寬)
	window.geometry('500x300')  # 這裡的乘是小x

	# 第4步，在圖形介面上設定標籤
	var = tk.StringVar()    # 將label標籤的內容設定為字元型別，用var來接收hit_me函式的傳出內容用以顯示在標籤上
	l = tk.Label(window, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)
	# 說明： bg為背景，fg為字型顏色，font為字型，width為長，height為高，這裡的長和高是字元的長和高，比如height=2,就是標籤有2個字元這麼高
	l.pack()

	# 定義一個函式功能（內容自己自由編寫），供點選Button按鍵時呼叫，呼叫命令引數command=函式名
	on_hit = False

	# 第5步，在視窗介面設定放置Button按鍵
	b = tk.Button(window, text='hit me', font=('Arial', 12), width=10, height=1, command=partial(hit_me,on_hit,var,q))
	b.pack() 	#Label內容content區域放置位置，自動調節尺寸
				# 放置lable的方法有：1）l.pack(); 2)l.place();

	# 第6步，主視窗迴圈顯示
	window.mainloop()	# 注意，loop因為是迴圈的意思，window.mainloop就會讓window不斷的重新整理，如果沒有mainloop,就是一個靜態的window,傳入進去的值就不會有迴圈，mainloop就相當於一個很大的while迴圈，有個while，每點選一次就會更新一次，所以我們必須要有迴圈
						# 所有的視窗檔案都必須有類似的mainloop函式，mainloop是視窗檔案的關鍵的關鍵。

def hit_me(on_hit,var,q):
	Left = cv2.VideoCapture("testdata\\Left.mp4") 
	Right = cv2.VideoCapture("testdata\\Left.mp4")
	stop_img = cv2.imread("testdata\\Stop.jpg")

	if on_hit == False:
		on_hit = True
		var.set('Go Left')
		while Left.isOpened():
			q.put(Left.read())

	else:
		on_hit = False
		var.set('')

if __name__ == '__main__':
		q = Queue()
		#q.put(cv2.VideoCapture("testdata\\Left.mp4"))
		#show_console(q)
		window = Process(target=show_window,args=(q,))
		console = Process(target=show_console, args=(q,))
		window.start()
		console.start()
		console.join()
		window.terminate()

 
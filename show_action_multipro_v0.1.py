import cv2
import numpy as np
import sys
import tkinter as tk
from multiprocessing import Process,Queue		#multi process to aviod imshow be effected
import time
import matplotlib.pyplot as plt
'''
also it work now, there are many plase can improve.
1. let moving continue, it can achieve by better action incode and moving logic improve
2. let movie be full screen, it should be found out way on opencv document
3. it may not work on linux, it should be tryed

'''

''' it is trush
class FrameQueue(object):		

	def __init__(self,num = 100):	#initial long = 100 and let fornt and back be zero
		super(FrameQueue, self).__init__()
		self.data =	[tuple() for x in range(num)]	#use array to store data
		self.fornt_index = 0
		self.back_index = 0
		self.num = num
	
	def put(self,input):
		self.data[self.back_index] = input
		self.back_index +=1
		if(self.back_index >= self.num):
			self.back_index = 0

	def get(self):

		if(self.back_index == self.fornt_index):
			raise Exception("no more data out")

		p = self.data[self.fornt_index]
		self.fornt_index+=1

		if(self.fornt_index >= self.num):
			self.fornt_index = 0

		return p

	def empty(self):
		if(self.back_index == self.fornt_index):
			return True
		else:
			return False
'''


def show_window(action,v):	#the fuction show movie


	stop_img = cv2.imread("testdata\\Stop.jpg")

	start = time.time()
	Max_time = 0

	cv2.namedWindow("frame1")
	cv2.startWindowThread()
	count = 0

	while(True):
		count=count+1
		if(count>100):
			Max_time = 0
			count=0

		#從Queue中取得下一張圖片，若Queue中沒有其他的Frame，則使用上次的圖片
		if action.empty():
			temp = stop_img.copy() 

		else:
			temp = action.get()

		frame = temp
		#把停下來的畫面存起
		stop_img = frame

		time_dash = round((time.time()-start)*1000)
		Max_time = time_dash if time_dash> Max_time else Max_time

		outputframe = frame.copy()

		cv2.putText(outputframe, str(time_dash), (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
  			1, (0, 125, 255), 1, cv2.LINE_AA)
		cv2.putText(outputframe, str(Max_time), (10, 100), cv2.FONT_HERSHEY_SIMPLEX,
  			1, (0, 0, 255), 1, cv2.LINE_AA)

		# 更新圖片
		#cv2.startWindowThread()
		cv2.imshow('frame1', outputframe)

		#紀錄時間
		start = time.time();

		# 若按下 q 鍵則離開迴圈
		if cv2.waitKey(25) & 0xFF == ord('q'):
			break


	# 關閉所有 OpenCV 視窗
	cv2.destroyAllWindows()


def show_console(q,v):

	#讀入影片,由於參數傳遞的關係，數據必須先預處理成list才能避免傳遞時使用傳址的方式

	# 第1步，例項化object，建立視窗window
	window = tk.Tk()

	# 第2步，給視窗的視覺化起名字
	window.title('console panel')

	# 第3步，設定視窗的大小(長 * 寬)
	window.geometry('500x300')  # 這裡的乘是小x

	# 第4步，在圖形介面上設定標籤
	var = tk.StringVar()    # 將label標籤的內容設定為字元型別，用var來接收hit_me函式的傳出內容用以顯示在標籤上
	Lable1 = tk.Label(window, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)
	# 說明： bg為背景，fg為字型顏色，font為字型，width為長，height為高，這裡的長和高是字元的長和高，比如height=2,就是標籤有2個字元這麼高
	Lable1.pack()

	# 定義一個函式功能（內容自己自由編寫），供點選Button按鍵時呼叫，呼叫命令引數command=函式名

	# 第5步，在視窗介面設定放置Button按鍵
	# lambda可以生成一個次級的funcion(?)以便於傳遞參數
	Bu_Left = tk.Button(window, text='Left', font=('Arial', 12), width=5, height=1, command=lambda: Go_Left(var,q,v))
	Bu_Left.pack() 	#Label內容content區域放置位置，自動調節尺寸
				# 放置lable的方法有：1）l.pack(); 2)l.place();
	Bu_Right = tk.Button(window, text="Right", font=('Arial',12), width=5 ,height=1, command=lambda: Go_Right(var,q,v))
	Bu_Right.pack()

	# 第6步，主視窗迴圈顯示
	window.mainloop()
	# 注意，loop因為是迴圈的意思，window.mainloop就會讓window不斷的重新整理，如果沒有mainloop,就是一個靜態的window,傳入進去的值就不會有迴圈，mainloop就相當於一個很大的while迴圈，有個while，每點選一次就會更新一次，所以我們必須要有迴圈
	# 所有的視窗檔案都必須有類似的mainloop函式，mainloop是視窗檔案的關鍵的關鍵。

def Go_Left (var,q,v):	#bu_Left的動作
	v=-1.
	var.set(str(v))
	return

def Go_Right(var,q,v):	#bu_Right的動作
	v=1.0
	var.set(str(v))
	return


if __name__ == '__main__':
	
	q = Queue()	
	v = 0.1
	Left = cv2.VideoCapture("testdata\\Left.mp4") 
	fish_img = cv2.imread("testdata\\zebrafish.png")
	print(fish_img.shape)

	window = Process(target=show_window,args=(q,v,))
	console = Process(target=show_console, args=(q,v,))
	console.start()
	window.start()
	console.join()	#等待console結束，主程序才會繼續
	window.terminate()	#一旦console join, 摧毀window程序


 	#plt.scatter(X,Y)

 	
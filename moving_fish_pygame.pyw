from ctypes import c_bool

import pygame
import numpy as np
import tkinter as tk
from multiprocessing import Process, Value  # multi process to aviod imshow be effected


class Fish(pygame.sprite.Sprite):

    def __init__(self, pos=(0, 0), filepath='.\\testdata\\zebrafish.png', scale=1.):
        super(Fish, self).__init__()
        self.CW_image = pygame.image.load(filepath)
        self.CCW_image = pygame.transform.flip(self.CW_image, True, False)
        self.image = self.CW_image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.scale = scale

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.angle += 1 % 360
        x, y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (x, y)  # Put the new rect's center at old center.

    def up_Pos(self, pos, angle, CW=1):  # use x-dir as axis and counterclockwise as positive
        if CW > 0:
            image = self.CW_image
        else:
            image = self.CCW_image
        self.image = pygame.transform.rotozoom(image, angle, self.scale)
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = pos  # Put the new rect's center at old center.

    def change_scale(self, scale):
        self.scale = scale



def moving_fish(S, O, clockwise, Radius):
    pygame.init()
    pygame.display.set_caption("OpenCV stream on Pygame")
    clock = pygame.time.Clock()
    #set resolution here.
    screen = pygame.display.set_mode([1000, 800])  # , pygame.DOUBLEBUF | pygame.HWSURFACE)  # pygame.FULLSCREEN

    fish = Fish(pos=(200, 200), scale=0.5)
    #scale can change the size of picture
    screen.fill([0, 0, 0])
    light = 200
    angle = 0
    center = (500, 400)

    # 關閉程式的程式碼
    running = True
    while running:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                """
				if event.key == pygame.K_c:
					CW *= -1
			if keys[pygame.K_EQUALS]:
				omega += 10
			if keys[pygame.K_MINUS]:
				omega -= 10
				if omega < 0:
					omega = 0
				"""
        # update the value
        omega = O.value
        R = Radius.value
        CW = clockwise.value


        # get time dash of last frame in millisecond
        time = clock.tick_busy_loop()
        # calculate the displacement
        angle += CW * omega * time / 1000
        theta = angle / 360 * 2 * np.pi
        # turn into X-Y coordinate
        width = center[0] + int(R * np.sin(theta))
        height = center[1] - int(R * np.cos(theta))
        # update fish position
        fish.up_Pos((width, height), -angle, CW)
        screen.fill([light, light, light])
        screen.blit(fish.image, fish.rect)
        pygame.display.update()
    pygame.quit()


def show_console(scale, omega, CW, Radius):
    # 第1步，例項化object，建立視窗window
    window = tk.Tk()

    # 第2步，給視窗的視覺化起名字
    window.title('console panel')

    # 第3步，設定視窗的大小(長 * 寬)
    window.geometry('500x300')  # 這裡的乘是小x

    # 第4步，在圖形介面上設定標籤
    var = tk.StringVar()  # 將label標籤的內容設定為字元型別，用var來接收hit_me函式的傳出內容用以顯示在標籤上
    Label1 = tk.Label(window, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)
    # 說明： bg為背景，fg為字型顏色，font為字型，width為長，height為高，這裡的長和高是字元的長和高，比如height=2,就是標籤有2個字元這麼高

    dir = tk.StringVar()
    dir.set("Turn")
    # 定義一個函式功能（內容自己自由編寫），供點選Button按鍵時呼叫，呼叫命令引數command=函式名
    Rot = tk.Button(window, textvariable=dir, text="Right", font=('Arial', 11), width=8, height=1,
                    command=lambda: Clockwise(CW, dir))
    Rot.pack()

    Speed_bar = tk.Scale(window, label="Speed", from_=0, to=360, orient=tk.HORIZONTAL,
                         length=400, showvalue=True, tickinterval=60,
                         command=lambda v: Speed(omega, int(v)))
    Speed_bar.pack()

    Radius_bar = tk.Scale(window, label='try me', from_=100, to=600, orient=tk.HORIZONTAL,
                          length=400, showvalue=True, tickinterval=50, resolution=1,
                          command=lambda v: getR(Radius, int(v)))
    Radius_bar.pack()

    # 第6步，主視窗迴圈顯示
    window.mainloop()


# 注意，loop因為是迴圈的意思，window.mainloop就會讓window不斷的重新整理，如果沒有mainloop,就是一個靜態的window,傳入進去的值就不會有迴圈，mainloop就相當於一個很大的while迴圈，有個while，每點選一次就會更新一次，所以我們必須要有迴圈
# 所有的視窗檔案都必須有類似的mainloop函式，mainloop是視窗檔案的關鍵的關鍵。

def Speed(omega, v):
    omega.value = v


def getR(Radius, v):
    Radius.value = v


def Clockwise(CW, dir):
    CW.value *= -1
    temp = CW.value
    dir.set("Turn")


if __name__ == '__main__':
    scale = Value("d", 0.5)
    omega = Value("I", 10)
    CW = Value("i", 1)
    Radius = Value("I", 200)
    window = Process(target=moving_fish, args=(scale, omega, CW, Radius,))
    console = Process(target=show_console, args=(scale, omega, CW, Radius,))
    window.start()
    console.start()
    console.join()  # 等待console結束，主程序才會繼續
    window.terminate()  # 一旦console join, 摧毀window程序

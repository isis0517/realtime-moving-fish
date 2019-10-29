import cv2
import numpy as np
import time


def limit_num(num, limit, dir=True):
    if (num > limit) ^ dir:  # ^ = xor
        return num, 0
    else:
        return limit, limit - num


def insert_image(background, insertd_image, position=(0, 0)):
    pos_h, pos_w = position
    img_h, img_w = insertd_image.shape[0:2]
    bak_h, bak_w = background.shape[0:2]

    height_up, rem_h_up = limit_num(pos_h + img_h // 2 + 1, bak_h)
    height_bot, rem_h_bot = limit_num(pos_h - img_h // 2, 0, False)
    width_up, rem_w_up = limit_num(pos_w + img_w // 2 + 1, bak_w)
    width_bot, rem_w_bot = limit_num(pos_w - img_w // 2, 0, False)

    background[height_bot: height_up, width_bot: width_up] = insertd_image[rem_h_bot: img_h + rem_h_up,
                                                             rem_w_bot: img_w + rem_w_up]
    return background


if __name__ == '__main__':
    dtype = np.dtype('uint8')
    fishes = np.load("./data/test.npy")
    blank = np.full((1080, 1920, 3), 255, dtype=dtype)
    img_center = (blank.shape[0] // 2, blank.shape[1] // 2)  # get the center of the image
    R = 400  # radius in pixel
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)  # creat the windows to show img
    cv2.resizeWindow("frame", 1080, 1920)  # change the size of the windows
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # let windows to full screen

    start = time.time()  # check the time
    for angle in range(0, 360):
        theta = angle / 360 * 2 * np.pi
        height = img_center[0] - int(R * np.cos(theta))
        width = img_center[1] + int(R * np.sin(theta))
        frame = insert_image(blank.copy(), fishes[359 - angle], (height, width))
        cv2.circle(frame, (width, height), 2, (255, 0, 0), -1)  # draw the center on the frame
        cv2.imshow("frame", frame)
        # press q on the keyboard can stop the windows
        if cv2.waitKey(25) % 0xFF == ord('q'):
            break

    print((time.time() - start) * 1000)  # show the time pass
    print(25 * 360)  # show the time we expect.
    cv2.destroyAllWindows()

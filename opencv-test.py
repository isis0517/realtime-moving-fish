import cv2
import numpy as np


def rotate_angle(image, angle):  # rotate the square image

    height, width = image.shape[0:2]  # get the height and width of image
    if height != width:
        raise NameError("it is not square image!")

    rota_matrix = cv2.getRotationMatrix2D((height / 2, width / 2), angle, 1)  # get the rotation matrix
    rot_image = cv2.warpAffine(image, rota_matrix, (height, width))  # apply the rotation matrix on image
    rot_image_gray = cv2.cvtColor(rot_image, cv2.COLOR_BGR2GRAY)  # generate the gray image
    ret, rot_mask = cv2.threshold(rot_image_gray, 10, 255, cv2.THRESH_BINARY)  # generate the mask
    rot_mask_inv = cv2.bitwise_not(rot_mask)  # generate the inverse mask
    rot_back = np.broadcast_to(rot_mask_inv.reshape(533, 533, 1), rot_image.shape)  # generate the blank inverse image
    rot_image = cv2.add(rot_image, rot_back)  # add togathor to get image with blank back

    return rot_image


def ROI(image, background, position):
    height, width = image.shape[0:2]
    x, y = position
    roi = background[x:x + height, y:y + width]

    return roi


if __name__ == '__main__':
    dtype = cv2.imread("testdata\\zebrafish.png").dtype  # get the type of the numpyarray
    raw_fish = cv2.imread("testdata\\zebrafish.png")  # get the raw fish data

    Len_fish = raw_fish.shape[1]  # get the longest side
    Drif = (raw_fish.shape[1] - raw_fish.shape[0]) // 2  # caculate the drift form sort side to long side
    square_fish = np.zeros((Len_fish, Len_fish, 3), dtype=dtype)  # generate the square image
    square_fish[Drif + 1:-Drif, :] = raw_fish  # put original fish image into square with drift

    blank = 255 * np.ones((1080, 1920, 3), dtype=dtype)  # full with one and mutiply 255.0 to get blank background

    """cv2.imshow("test", blank)
	cv2.waitKey(2000)

	cv2.imshow("test", fish)
	cv2.waitKey(2000)

	fish = np.fliplr(fish)
	cv2.imshow("test", fish)
	cv2.waitKey(2000)

    rota = cv2.getRotationMatrix2D((Len_fish / 2, Len_fish / 2), -45, 1)  # get the rotation matrix
    rot_fish = cv2.warpAffine(square_fish, rota, (Len_fish, Len_fish))  # apply the rotation matrix on square_fish
    rot_fish_gray = cv2.cvtColor(rot_fish, cv2.COLOR_BGR2GRAY)  # generate the gray image
    ret, mask = cv2.threshold(rot_fish_gray, 10, 255,cv2.THRESH_BINARY)  # generate the mask which used to determind where the pixel pass
    mask_inv = cv2.bitwise_not(mask)  # inverse mask
    rows, cols, channel = square_fish.shape  # get the size of squared fish
    roi = blank[0:rows, 0:cols]  # this is used to merge the fish and blank image.
    show_bk = cv2.bitwise_and(roi, roi, mask=mask_inv)  #
    show_fg = cv2.bitwise_and(rot_fish, rot_fish, mask=mask)
    show_up = cv2.add(show_bk, show_fg)"""

    rot_fish = rotate_angle(square_fish, 45)

    fishes = []

    for angle in range(0, 360):
        fishes.append(rotate_angle(square_fish, angle))

    num = 0
    while num < 360:
        cv2.imshow("fish", fishes[num])
        cv2.waitKey(25)
        num += 1
    cv2.imshow("test", rot_fish)
    cv2.waitKey(2000)
    cv2.destroyWindow("test")
import cv2
import numpy as np


def rotate_angle(image, angle):  # rotate the square image

    height, width = image.shape[0:2]  # get the height and width of image
    if height != width:
        raise NameError("it is not square image!")

    rota_matrix = cv2.getRotationMatrix2D((height / 2, width / 2), angle, 1)  # get the rotation matrix
    rot_image = cv2.warpAffine(image, rota_matrix, (height, width))  # apply the rotation matrix on image
    rot_image_gray = cv2.cvtColor(rot_image, cv2.COLOR_BGR2GRAY)  # generate the gray image
    ret, rot_mask = cv2.threshold(rot_image_gray, 10, 255, cv2.THRESH_BINARY)  # generate the mask (black background)
    rot_mask_inv = cv2.bitwise_not(rot_mask)  # generate the inverse mask(white background)
    rot_back = np.broadcast_to((rot_mask_inv).reshape(533, 533, 1), rot_image.shape)  # generate the blank inverse image
    rot_image = cv2.add(rot_image, rot_back)  # add together to get image with blank back

    return rot_image

def ROI(image, background, position):
    height, width = image.shape[0:2]
    x, y = position
    roi = background[x:x + height, y:y + width]

    return roi

def generate_fishes_datafile():
    fishes = list()
    for angle in range(0, 360):
        fishes.append(rotate_angle(square_fish, angle))
    np.save("./data/Right360.npy", np.array(fishes))

if __name__ == '__main__':
    dtype = cv2.imread("testdata\\zebrafish.png").dtype  # get the type of the numpyarray
    raw_fish = cv2.imread("testdata\\zebrafish.png")  # get the raw fish data

    Len_fish = raw_fish.shape[1]  # get the longest side
    Drif = (raw_fish.shape[1] - raw_fish.shape[0]) // 2  # calculate the drift form sort side to long side
    square_fish = np.zeros((Len_fish, Len_fish, 3), dtype=dtype)  # generate the square image
    square_fish[Drif + 1:-Drif, :] = raw_fish  # put original fish image into square with drift

    blank = np.full((1080, 1920, 3), 0, dtype=dtype)  # full with one and multiply 255.0 to get blank background
    print(type(np.dtype('uint8')))

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

    fishes = np.load("./data/test.npy")
    print(fishes.dtype)

    """fishes = list()
    for angle in range(0, 360):
        fishes.append(rotate_angle(square_fish, angle))

    fishes2 = np.array(fishes)
    np.save("./data/test.npy" , fishes2)"""

    num = 0
    img_center = (blank.shape[0]//2, blank.shape[1]//2)
    R = 250
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    #cv2.namedWindow("test", cv2.WINDOW_NORMAL)
    #cv2.namedWindow("test2", cv2.WINDOW_NORMAL)
    #blank2 = np.full((500, 500, 3), 0, dtype=dtype)

    #cv2.imshow("test", fishes[0])
    #cv2.imshow("test2", np.flip(fishes[0],1))

    
    angle = 0
    while angle < 360:
        theta = angle/360*2*np.pi
        height = img_center[0] - int(R*np.cos(theta))
        width = img_center[1] + int(R*np.sin(theta))
        frame = blank.copy()
        height_up = height+Len_fish//2+1
        height_bot = height-Len_fish//2

        frame[height-Len_fish//2 : height+Len_fish//2+1, width-Len_fish//2 : width+Len_fish//2+1] = fishes[int(359-angle)]
        cv2.circle(frame,(width,height),2,(255,0,0),-1)
        cv2.imshow("frame",frame)
        cv2.waitKey(100)
        angle += 1

    #cv2.namedWindow("test", cv2.WINDOW_NORMAL)
    #cv2.resizeWindow("test",1920,1080)
    #cv2.imshow("test", cv2.circle(blank,(1800,255),3,(0,0,0),-1))
    #cv2.waitKeheight(5000)
    cv2.destroyAllWindows()
import cv2
import numpy as np
from PIL import Image



def main():
    img = cv2.imread("pic.png")
    cnt = np.array([
            [[42, 21]],
            [[15, 67]],
            [[167,92]],
            [[140, 140]]
        ],)
    print("shape of cnt: {}".format(cnt.shape))
    rect = cv2.minAreaRect(cnt)
    print("rect: {}".format(rect))

    box = cv2.boxPoints(rect)
    box = np.int0(box)

    print("bounding box: {}".format(box))
    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

    img_crop, img_rot = crop_rect(img, rect)

    print("size of original img: {}".format(img.shape))
    print("size of rotated img: {}".format(img_rot.shape))
    print("size of cropped img: {}".format(img_crop.shape))

    new_size = (int(img_rot.shape[1]/2), int(img_rot.shape[0]/2))
    img_rot_resized = cv2.resize(img_rot, new_size)
    new_size = (int(img.shape[1]/2)), int(img.shape[0]/2)
    img_resized = cv2.resize(img, new_size)

    cv2.imshow("original contour", img_resized)
    cv2.imshow("rotated image", img_rot_resized)
    cv2.imshow("cropped_box", img_crop)

    # cv2.imwrite("crop_img1.jpg", img_crop)
    cv2.waitKey(0)


def crop_rect(img, rect):
    # get the parameter of the small rectangle
    center = rect[0]
    size = rect[1]
    angle = rect[2]
    center, size = tuple(map(int, center)), tuple(map(int, size))

    # get row and col num in img
    height, width = img.shape[0], img.shape[1]
    print("width: {}, height: {}".format(width, height))

    M = cv2.getRotationMatrix2D(center, angle, 1)
    img_rot = cv2.warpAffine(img, M, (width, height))

    img_crop = cv2.getRectSubPix(img_rot, size, center)

    return img_crop, img_rot



    
if __name__ == "__main__":
    main()
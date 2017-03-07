import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def get_image(path):
    img = cv2.imread(path)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def gray_blur(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.GaussianBlur(img, (21, 21), 0)
    return img


def img_diff(img1, img2, threshold = 60):
    dif = cv2.absdiff(gray1, gray2)
    dif = cv2.threshold(dif, threshold, 255, cv2.THRESH_BINARY)[1]
    return dif



# TODO: handle first and last images
#       determine if/how/where to save images for use in tensorflow
def event_dilate(color_list, threshold=15):
    img_list = []          #  Create list of grayed, blurred images
    dilate_kernel = np.ones((100,100),np.uint8)
    processed = []

    for im in color_list:
        img_list.append(gray_blur(im))

    # find common changes between an image and the image to the left and right
    # TODO: for now ignore first and last image
    for i, im in enumerate(img_list[1:-1]):
        # start w/ img_list[1] thus 'i' == index of the previous image
        prev = img_dif(im, img_list[i], threshold=threshold)
        post = img_dif(im, img_list[i+2], threshold=threshold)
        both = cv2.bitwise_and(prev,post)
        both = cv2.dilate(both, dilate_kernel, iterations=2)

        tmp = cv2.cvtColor(both, cv2.COLOR_GRAY2BGR)
        overlap = cv2.bitwise_and(tmp,color_list[i+1])

        processed.append(overlap)

    return processed

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


# TODO: determine if/how/where to save images for use in tensorflow
def find_overlapping_change(color_list, threshold=15):
    img_list = []          #  Create list of grayed, blurred images
    dilate_kernel = np.ones((100,100),np.uint8)
    processed = []

    for im in color_list:
        img_list.append(gray_blur(im))

    # find common changes between an image and the image to the left and right
    for i, im in enumerate(img_list):
        # wrapped to the other end to get the ends
        #  - not the best soln for long events
        before = (i-1)%len(img_list)
        after =  (i+1)%len(img_list)
        prev = getdif(im, img_list[before])
        post = getdif(im, img_list[after])
        both = cv2.bitwise_and(prev,post)
        both = cv2.dilate(both, dilate_kernel, iterations=2)
        both = cv2.cvtColor(both, cv2.COLOR_GRAY2RGB)
        overlap = cv2.bitwise_and(both,color_list[i])

        processed.append(overlap)

    return processed

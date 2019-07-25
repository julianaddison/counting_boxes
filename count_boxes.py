# Script Name:  count_boxes.py
#
# Description:  This script counts the number of boxes in an image
#
# Created:      14/02/2018
#
# Inputs:       boxes1.jpg, boxes2.jpg, table1.jpg
#
# Outputs:      Final image containing contours
#               No of boxes
######################################################################################


# Import required packages
import cv2
import os
import numpy as np
import platform
# from matplotlib import pyplot as plt

class CountBoxes():
    def __init__(self, img_path, output_path):
        self.IMG_PATH = img_path
        self.OUTPUT_PATH = output_path
        self.img = None
        self.img_w = None
        self.img_h = None
        self.buffer = 30

    def img_canvas(self):
        '''
        paste image on a white canvas i.e. add a buffer around the image
        :param img: original image
        :return: original image with a buffer region
        '''

        adj_w, adj_h = self.img_w+self.buffer, self.img_h+self.buffer
        buffered_img = np.ones([adj_w, adj_h], dtype=np.uint8)*255
        buffered_img[self.buffer//2:self.img_w+self.buffer//2, self.buffer//2:self.img_h+self.buffer//2] = self.img

        return buffered_img

    def visualize_cnts(self, cnts):
        '''

        :param cnts: list of contours
        :param counter: no. of boxes
        :return: white canvas with contours drawn on it
        '''
        adj_w, adj_h = self.img_w+self.buffer, self.img_h+self.buffer
        canvas = np.ones([adj_w, adj_h], dtype=np.uint8)*255

        cv2.drawContours(canvas, cnts, -1, 0, 1)

        return canvas

    def draw_mask(self, cnts):
        '''
        create a mask of non rectangle contours
        :param cnts: list of contours
        :return: mask and a list of the index of rejected contours
        '''
        def is_contour_bad(c):
            '''
            determines if a contour is a rectangle
            :param c: a single contour
            :return: true/false
            '''
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # the contour is 'bad' if it is not a rectangle
            return not len(approx) == 4

        adj_w, adj_h = self.img_w+self.buffer, self.img_h+self.buffer
        mask = np.ones([adj_w, adj_h], dtype=np.uint8)*255

        rejected_cnts = []

        # loop over the contours
        for i, c in enumerate(cnts):
            # if the contour is bad, draw it on the mask
            if is_contour_bad(c):
                cv2.drawContours(mask, [c], -1, 0, -1)
                rejected_cnts.append(i)
        return mask, rejected_cnts

    def run(self):
        # Load image in grayscale and get dimensions
        self.img = cv2.imread(self.IMG_PATH, 0)
        self.img_w, self.img_h = self.img.shape
        # plt.imshow(img)

        # Paste original img on a larger canvas
        res_img = self.img_canvas()
        # plt.imshow(res_img)

        # Blurring to thicken lines and remove noise
        blur = cv2.GaussianBlur(res_img, (5, 5), 0)
        # plt.imshow(blur)

        # Binarization - Local Otsu Threshold
        ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # plt.imshow(thresh)

        # Find contours
        cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        # print("Total Contours Length: ", len(cnts))

        # For visualization - draw contours on a blank image
        # res_img_cnts = self.visualize_cnts(cnts)
        # plt.imshow(res_img_cnts)

        # Remove text and any other artifact that is not a rectangle by creating a mask
        mask, rejected_cnts = self.draw_mask(cnts)
        mask = cv2.bitwise_not(mask)
        cleaned_thresh = thresh + mask
        # plt.imshow(cleaned_thresh)

        # Find contours on cleaned threshold image
        cnts, hierarchy = cv2.findContours(cleaned_thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        # print("Total Contours Length: ", len(cnts))

        # Remove max contour in the list
        cnt_largest_area = max(cnts, key=cv2.contourArea)

        updated_hierarchy = np.array([hierarchy[0][i] for i, c in enumerate(cnts) if np.all(c != cnt_largest_area)])
        # print("Updated hierarchy Length: ", len(updated_hierarchy))

        updated_cnts = [c for c in cnts if np.all(c != cnt_largest_area)]
        # print("Updated Contours Length: ", len(updated_cnts))

        # Find contours total number of boxes based on parent-child relationship
        counter = 0
        for h in updated_hierarchy:
            # find all at cnts without parent at the same hierarchy
            # [nxt cnt in same hierarchy, previous cnt in same hierarchy, first child in hierarchy 2, parent(if any)]
            if h[3] == -1:
                counter += 1

        print("The total number of boxes is: ", counter)

        # For visualization - draw contours on a blank image
        res_img_cnts = self.visualize_cnts(updated_cnts)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (40, 40)
        fontScale = 1
        fontColor = 0
        lineType = 2

        cv2.putText(res_img_cnts, "Total No. of Boxes: "+str(counter), bottomLeftCornerOfText, font, fontScale, fontColor, lineType)

        cv2.imwrite(self.OUTPUT_PATH, res_img_cnts)



if __name__ == '__main__':

    # system specific path seperator
    sep = "\\" if platform.system() == "Windows" else "/"

    # define parameters
    CURR_DIR = os.getcwd()
    INPUT_DIR = "data"
    OUTPUT_DIR = "output"
    IMG_FILENAMES = os.listdir(sep.join([CURR_DIR, INPUT_DIR]))

    for file in IMG_FILENAMES:

        # define parameters
        IMG_PATH = sep.join([CURR_DIR, INPUT_DIR, file])
        OUTPUT_PATH = sep.join([CURR_DIR, OUTPUT_DIR, file])

        # run
        CB = CountBoxes(IMG_PATH, OUTPUT_PATH)
        CB.run()


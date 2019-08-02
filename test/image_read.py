# coding:UTF-8
import cv2
import numpy as np
from norm import test_glay
from collections import Counter

class Image_Read:
    '''
    calculation of target environment
    '''
    def __init__(self, data, x, j, train=False):
        self.image = data
        self.x = x
        channel_one_hot = []
        zeros = np.zeros((7, 100, 100), dtype=np.float32)

        # Padding to prevent moving out of the scene
        zero_pading = 1000
        center = zero_pading/2

        # (width, height)
        w, h = self.image.shape[:2]

        # black background
        black_img = cv2.resize(np.ones((1, 1), np.uint8)*7, (h + zero_pading, w + zero_pading))
        black_img /= 7

        # paste on the created black background
        black_img[center:center+w, center:center+h] = self.image
        if train == True:
            # return normalized coordinates
            pass
        else:
            x, y = test_glay(self.x[0], self.x[1], j)

        # around the target (100 x 100)
        target_img = black_img[int(np.trunc(y)-50)+center:int(np.trunc(y)+50)+center, int(np.trunc(x)-50)+center:int(np.trunc(x)+50)+center]
        height, weight = target_img.shape
        for i in target_img:
            for item in i:
                channel_one_hot.append(item)

        result = [key for key, val in Counter(channel_one_hot).items() if val > 1]

        # channel split
        for num in range(len(result)):
            # sidewalk
            if result[num] == 0:
                for h_ in xrange(height):
                    for w_ in xrange(weight):
                        image_color = target_img[h_][w_]
                        if image_color == 0:
                            zeros[0][h_][w_] = 1
            # road
            elif result[num] == 1:
                for h_ in xrange(height):
                    for w_ in xrange(weight):
                        image_color = target_img[h_][w_]
                        if image_color == 1:
                            zeros[1][h_][w_] = 1
            # glass
            elif result[num] == 2:
                for h_ in xrange(height):
                    for w_ in xrange(weight):
                        image_color = target_img[h_][w_]
                        if image_color == 2:
                            zeros[2][h_][w_] = 1
            # bicycle parking space
            elif result[num] == 3:
                for h_ in xrange(height):
                    for w_ in xrange(weight):
                        image_color = target_img[h_][w_]
                        if image_color == 3:
                            zeros[3][h_][w_] = 1
            # round about
            elif result[num] == 4:
                for h_ in xrange(height):
                    for w_ in xrange(weight):
                        image_color = target_img[h_][w_]
                        if image_color == 4:
                            zeros[4][h_][w_] = 1
            # tree
            elif result[num] == 5:
                for h_ in xrange(height):
                    for w_ in xrange(weight):
                        image_color = target_img[h_][w_]
                        if image_color == 5:
                            zeros[5][h_][w_] = 1
            # building
            elif result[num] == 6:
                for h_ in xrange(height):
                    for w_ in xrange(weight):
                        image_color = target_img[h_][w_]
                        if image_color == 6:
                            zeros[6][h_][w_] = 1
            # padding (for moved outsides the scene)
            elif result[num] == 7:
                for h_ in xrange(height):
                    for w_ in xrange(weight):
                        image_color = target_img[h_][w_]
                        if image_color == 7:
                            zeros[7][h_][w_] = 1

        # (BATCH, CHANNEL, width, height)
        zeros = np.asarray(zeros, dtype=np.float32).reshape(1, 7, 100, 100)

        self.img = zeros
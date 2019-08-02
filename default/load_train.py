# coding:UTF-8
import numpy as np
import os
from glob import glob
from norm import train

'''---------------------------'''
PATH = '../dataset/train/*/*/'
'''---------------------------'''
class Train_DataLoader():
    '''
    :return
    all_data        :Target data for all scenes
    list_coordinate :Target in all scenes divides by list
    list            :Number of target per scene
    '''
    def __init__(self, sequence=10):
        self.path = glob(PATH)
        self.path.sort()

        self.sequence = sequence
        self.list = []
        self.list_coordinate = []
        self.all_data = []

        for i, j in zip(self.path, range(len(self.path))):
            print i, "----------------------------"
            print j
            self.out = []
            trajectory_split = []

            sub_path = os.path.join(i, "annotations_.txt")
            data = np.genfromtxt(sub_path, delimiter=' ')

            # Center coordinates from Bounding Box
            x_lim1, y_lim1 = data[:, 1], data[:, 2]
            x_lim2, y_lim2 = data[:, 3], data[:, 4]
            x = (x_lim1 + x_lim2) / 2
            y = (y_lim1 + y_lim2) / 2

            # Normalization
            x, y = train(x, y, j)

            data[:, 1], data[:, 2] = x, y
            # all target in the scene
            ID = np.unique(data[:, 0][-1])
            for j in range(0, int(ID[0])):
                trajectory = data[data[:, 0] == j, :]
                # ID,x,y,frame
                trajectory = trajectory[:, [0, 1, 2, 5]]
                if len(trajectory) > 0:
                    trajectory_split.append(trajectory)

            for split in xrange(len(trajectory_split)):
                data_split = trajectory_split[split]
                if data_split.shape[0] > self.sequence + 1:
                    self.out.append(data_split[:, [1, 2]])
                    self.all_data.append(data_split[:, [1, 2]])

            self.list_coordinate.append(self.out)
            self.list.append(len(self.out))
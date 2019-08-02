# coding:UTF-8
import numpy as np
'''
one-hot vector
biker       :1
pedestrian  :2
cart        :3
car         :4
bus         :5
skateboader :6
'''
def Attribute(trajectory):
    one_hot = np.zeros((len(trajectory), 6))

    if len(trajectory) == 0:
        return trajectory
    else:
        # biker
        if trajectory[0, 4] == 1:
            trajectory = np.delete(trajectory, 4, 1)
            trajectory_atr = np.hstack((trajectory, one_hot))
            trajectory_atr[:, 4] = 1
            return trajectory_atr

        # pedestrian
        elif trajectory[0, 4] == 2:
            trajectory = np.delete(trajectory, 4, 1)
            trajectory_atr = np.hstack((trajectory, one_hot))
            trajectory_atr[:, 5] = 1
            return trajectory_atr

        # cart
        elif trajectory[0, 4] == 3:
            trajectory = np.delete(trajectory, 4, 1)
            trajectory_atr = np.hstack((trajectory, one_hot))
            trajectory_atr[:, 6] = 1
            return trajectory_atr

        # car
        elif trajectory[0, 4] == 4:
            trajectory = np.delete(trajectory, 4, 1)
            trajectory_atr = np.hstack((trajectory, one_hot))
            trajectory_atr[:, 7] = 1
            return trajectory_atr

        # bus
        elif trajectory[0, 4] == 5:
            trajectory = np.delete(trajectory, 4, 1)
            trajectory_atr = np.hstack((trajectory, one_hot))
            trajectory_atr[:, 8] = 1
            return trajectory_atr

        # skateboarder
        elif trajectory[0, 4] == 6:
            trajectory = np.delete(trajectory, 4, 1)
            trajectory_atr = np.hstack((trajectory, one_hot))
            trajectory_atr[:, 9] = 1
            return trajectory_atr

def Test(trajectory):
    # biker
    if trajectory[0, 2] == 1:
        attribute = 1
        return attribute

    # pedestrian
    if trajectory[0, 3] == 1:
        attribute = 2
        return attribute

    # cart
    if trajectory[0, 4] == 1:
        attribute = 3
        return attribute

    # car
    if trajectory[0, 5] == 1:
        attribute = 4
        return attribute

    # bus
    if trajectory[0, 6] == 1:
        attribute = 5
        return attribute

    # skateboarder
    if trajectory[0, 7] == 1:
        attribute = 6
        return attribute
# coding:UTF-8
import numpy as np

# test data norm
def test(x, y, j):
    # bookstore
    if j == 0:
        # video0
        x = x / 1424
        y = y / 1088
        return x, y

    # coupa
    if j == 1:
        # video0
        x = x / 1980
        y = y / 1093
        return x, y

    # deathCircle
    if j == 2:
        # video0
        x = x / 1630
        y = y / 1948
        return x, y

    # gates
    if j == 3:
        # video0
        x = x / 1325
        y = y / 1973
        return x, y

    # hyang
    if j == 4:
        # video0
        x = x / 1455
        y = y / 1925
        return x, y

    # little
    if j == 5:
        # video0
        x = x / 1417
        y = y / 2019
        return x, y

    # nexus
    if j == 6:
        # video0
        x = x / 1330
        y = y / 1947
        return x, y

    # quad
    if j == 7:
        # video0
        x = x / 1983
        y = y / 1088
        return x, y

# return normalized coordinates
def test_glay(x, y, j):
    # bookstore
    if j == 0:
        # video0
        x = x * 1424
        y = y * 1088
        return x, y

    # coupa
    if j == 1:
        # video0
        x = x * 1980
        y = y * 1093
        return x, y

    # deathCircle
    if j == 2:
        # video0
        x = x * 1630
        y = y * 1948
        return x, y

    # gates
    if j == 3:
        # video0
        x = x * 1325
        y = y * 1973
        return x, y

    # hyang
    if j == 4:
        # video0
        x = x * 1455
        y = y * 1925
        return x, y

    # little
    if j == 5:
        # video0
        x = x * 1417
        y = y * 2019
        return x, y

    # nexus
    if j == 6:
        # video0
        x = x * 1330
        y = y * 1947
        return x, y

    # quad
    if j == 7:
        # video0
        x = x * 1983
        y = y * 1088
        return x, y

# return normalized coordinates (for euclid distance error)
def test_pixel(trajectory, j):
    height, weight = trajectory.shape
    new_trajectory_pixel = np.zeros((height, weight))
    # bookstore
    if j == 0:
        # video0
        new_trajectory_pixel[:, 0] = np.trunc(trajectory[:, 0] * 1424)
        new_trajectory_pixel[:, 1] = np.trunc(trajectory[:, 1] * 1088)

    # coupa
    if j == 1:
        # video0
        new_trajectory_pixel[:, 0] = np.trunc(trajectory[:, 0] * 1980)
        new_trajectory_pixel[:, 1] = np.trunc(trajectory[:, 1] * 1093)

    # deathCircle
    if j == 2:
        # video0
        new_trajectory_pixel[:, 0] = np.trunc(trajectory[:, 0] * 1630)
        new_trajectory_pixel[:, 1] = np.trunc(trajectory[:, 1] * 1948)

    # gates
    if j == 3:
        # video0
        new_trajectory_pixel[:, 0] = np.trunc(trajectory[:, 0] * 1325)
        new_trajectory_pixel[:, 1] = np.trunc(trajectory[:, 1] * 1973)

    # hyang
    if j == 4:
        # video0
        new_trajectory_pixel[:, 0] = np.trunc(trajectory[:, 0] * 1455)
        new_trajectory_pixel[:, 1] = np.trunc(trajectory[:, 1] * 1925)

    # little
    if j == 5:
        # video0
        new_trajectory_pixel[:, 0] = np.trunc(trajectory[:, 0] * 1417)
        new_trajectory_pixel[:, 1] = np.trunc(trajectory[:, 1] * 2019)

    # nexus
    if j == 6:
        # video0
        new_trajectory_pixel[:, 0] = np.trunc(trajectory[:, 0] * 1330)
        new_trajectory_pixel[:, 1] = np.trunc(trajectory[:, 1] * 1947)

    # quad
    if j == 7:
        # video0
        new_trajectory_pixel[:, 0] = np.trunc(trajectory[:, 0] * 1983)
        new_trajectory_pixel[:, 1] = np.trunc(trajectory[:, 1] * 1088)

    return new_trajectory_pixel

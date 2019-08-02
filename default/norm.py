# coding:UTF-8

# train data norm
def train(x, y, j):
    # bookstore
    if j == 0:
        # video1
        x = x / 1422.0
        y = y / 1079.0
        return x, y

    if j == 1:
        # video2
        x = x / 1422
        y = y / 1079
        return x, y

    if j == 2:
        # video3
        x = x / 1322
        y = y / 1079
        return x, y

    if j == 3:
        # video4
        x = x / 1322
        y = y / 1079
        return x, y

    if j == 4:
        # video5
        x = x / 1322
        y = y / 1079
        return x, y

    if j == 5:
        # video6
        x = x / 1322
        y = y / 1079
        return x, y

    # coupa
    if j == 6:
        # video1
        x = x / 1980
        y = y / 1093
        return x, y

    if j == 7:
        # video2
        x = x / 1980
        y = y / 1093
        return x, y

    if j == 8:
        # video3
        x = x / 1980
        y = y / 1093
        return x, y

    # deathCircle
    if j == 9:
        # video1
        x = x / 1409
        y = y / 1916
        return x, y

    if j == 10:
        # video2
        x = x / 1436
        y = y / 1959
        return x, y

    if j == 11:
        # video3
        x = x / 1400
        y = y / 1904
        return x, y

    if j == 12:
        # video4
        x = x / 1452
        y = y / 1994
        return x, y

    # gates
    if j == 13:
        # video1
        x = x / 1425
        y = y / 1973
        return x, y

    if j == 14:
        # video2
        x = x / 1325
        y = y / 1973
        return x, y

    if j == 15:
        # video3
        x = x / 1432
        y = y / 2002
        return x, y

    if j == 16:
        # video4
        x = x / 1434
        y = y / 1982
        return x, y

    if j == 17:
        # video5
        x = x / 1426
        y = y / 2011
        return x, y

    if j == 18:
        # video6
        x = x / 1326
        y = y / 2011
        return x, y

    if j == 19:
        # video7
        x = x / 1334
        y = y / 1982
        return x, y

    if j == 20:
        # video8
        x = x / 1334
        y = y / 1982
        return x, y

    # hyang
    if j == 21:
        # video1
        x = x / 1445
        y = y / 2002
        return x, y

    if j == 22:
        # video2
        x = x / 1433
        y = y / 841
        return x, y

    if j == 23:
        # video3
        x = x / 1433
        y = y / 741
        return x, y

    if j == 24:
        # video4
        x = x / 1340
        y = y / 1730
        return x, y

    if j == 25:
        # video5
        x = x / 1454
        y = y / 1991
        return x, y

    if j == 26:
        # video6
        x = x / 1416
        y = y / 848
        return x, y

    if j == 27:
        # video7
        x = x / 1450
        y = y / 1940
        return x, y

    if j == 28:
        # video8
        x = x / 1350
        y = y / 1940
        return x, y

    if j == 29:
        # video9
        x = x / 1350
        y = y / 1940
        return x, y

    if j == 30:
        # video10
        x = x / 1416
        y = y / 748
        return x, y

    if j == 31:
        # video11
        x = x / 1416
        y = y / 748
        return x, y

    if j == 32:
        # video12
        x = x / 1316
        y = y / 848
        return x, y

    if j == 33:
        # video13
        x = x / 1316
        y = y / 748
        return x, y

    if j == 34:
        # video14
        x = x / 1316
        y = y / 748
        return x, y

    # little
    if j == 35:
        # video1
        x = x / 1322
        y = y / 1945
        return x, y

    if j == 36:
        # video2
        x = x / 1322
        y = y / 1945
        return x, y

    if j == 37:
        # video3
        x = x / 1422
        y = y / 1945
        return x, y

    # nexus
    if j == 38:
        # video1
        x = x / 1430
        y = y / 1947
        return x, y

    if j == 39:
        # video2
        x = x / 1330
        y = y / 1947
        return x, y

    if j == 40:
        # video3
        x = x / 1184
        y = y / 1759
        return x, y

    if j == 41:
        # video4
        x = x / 1284
        y = y / 1759
        return x, y

    if j == 42:
        # video5
        x = x / 1184
        y = y / 1759
        return x, y

    if j == 43:
        # video6
        x = x / 1331
        y = y / 1962
        return x, y

    if j == 44:
        # video7
        x = x / 1431
        y = y / 1962
        return x, y

    if j == 45:
        # video8
        x = x / 1331
        y = y / 1962
        return x, y

    if j == 46:
        # video9
        x = x / 1411
        y = y / 1980
        return x, y

    if j == 47:
        # video10
        x = x / 1311
        y = y / 1980
        return x, y

    if j == 48:
        # video11
        x = x / 1311
        y = y / 1980
        return x, y

    # quad
    if j == 49:
        # video1
        x = x / 1983
        y = y / 1088
        return x, y

    if j == 50:
        # video2
        x = x / 1983
        y = y / 1088
        return x, y

    if j == 51:
        # video3
        x = x / 1983
        y = y / 1088
        return x, y


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
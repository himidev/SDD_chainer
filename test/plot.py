# coding:UTF-8
import matplotlib.pyplot as plt
import pickle
from glob import glob


def plot_trajectory(def_true, def_pred, atr_true, atr_pred, atr_attr, env_true, env_pred, atr_env_true, atr_env_pred, name, num, path, i):
    plt.figure()
    im = plt.imread(path)
    plt.imshow(im)

    # bookstore
    if i == 0:
        plt.xlim(0, 1424)
        plt.ylim(1088, 0)
        print "============", atr_attr
        pred_def = plt.plot(def_pred[:, 0] * 1424, def_pred[:, 1] * 1088, color='c', linestyle='solid', marker='o', linewidth='2')
        pred_atr = plt.plot(atr_pred[:, 0] * 1424, atr_pred[:, 1] * 1088, color='m', linestyle='solid', marker='o', linewidth='2')
        pred_env = plt.plot(env_pred[:, 0] * 1424, env_pred[:, 1] * 1088, color='b', linestyle='solid', marker='o', linewidth='2')
        true_10 = plt.plot(def_true[4:13, 0] * 1424, def_true[4:13, 1] * 1088, color='g', linestyle='solid', marker='o', linewidth='2')
        pred_atr_env = plt.plot(atr_env_pred[:, 0] * 1424, atr_env_pred[:, 1] * 1088, color='r', linestyle='solid', marker='o', linewidth='2')
        true_5 = plt.plot(def_true[0:5, 0] * 1424, def_true[0:5, 1] * 1088, color='k', linestyle='solid', marker='o', linewidth='2')
        plt.savefig('./film/bookstore/%d.jpg' % num)
        plt.close()

    # coupa
    if i == 1:
        plt.xlim(0, 1980)
        plt.ylim(1093, 0)
        print "============", atr_attr
        pred_def = plt.plot(def_pred[:, 0] * 1980, def_pred[:, 1] * 1093, color='c', linestyle='solid', marker='o', linewidth='2')
        pred_atr = plt.plot(atr_pred[:, 0] * 1980, atr_pred[:, 1] * 1093, color='m', linestyle='solid', marker='o', linewidth='2')
        pred_env = plt.plot(env_pred[:, 0] * 1980, env_pred[:, 1] * 1093, color='b', linestyle='solid', marker='o', linewidth='2')
        true_10 = plt.plot(def_true[4:13, 0] * 1980, def_true[4:13, 1] * 1093, color='g', linestyle='solid', marker='o', linewidth='2')
        pred_atr_env = plt.plot(atr_env_pred[:, 0] * 1980, atr_env_pred[:, 1] * 1093, color='r', linestyle='solid', marker='o', linewidth='2')
        true_5 = plt.plot(def_true[0:5, 0] * 1980, def_true[0:5, 1] * 1093, color='k', linestyle='solid', marker='o', linewidth='2')
        plt.savefig('./film/coupa/%d.jpg' % num)
        plt.close()

    # deathCircle
    if i == 2:
        plt.xlim(0, 1630)
        plt.ylim(1948, 0)
        print "============", atr_attr
        pred_def = plt.plot(def_pred[:, 0] * 1630, def_pred[:, 1] * 1948, color='c', linestyle='solid', marker='o', linewidth='2')
        pred_atr = plt.plot(atr_pred[:, 0] * 1630, atr_pred[:, 1] * 1948, color='m', linestyle='solid', marker='o',  linewidth='2')
        pred_env = plt.plot(env_pred[:, 0] * 1630, env_pred[:, 1] * 1948, color='b', linestyle='solid', marker='o',  linewidth='2')
        true_10 = plt.plot(def_true[4:13, 0] * 1630, def_true[4:13, 1] * 1948, color='g', linestyle='solid', marker='o', linewidth='2')
        pred_atr_env = plt.plot(atr_env_pred[:, 0] * 1630, atr_env_pred[:, 1] * 1948, color='r', linestyle='solid', marker='o', linewidth='2')
        true_5 = plt.plot(def_true[0:5, 0] * 1630, def_true[0:5, 1] * 1948, color='k', linestyle='solid', marker='o', linewidth='2')
        plt.savefig('./film/deathCircle/%d.jpg' % num)
        plt.close()

    # gate
    if i == 3:
        plt.xlim(0, 1325)
        plt.ylim(1973, 0)
        print "============", atr_attr
        pred_def = plt.plot(def_pred[:, 0] * 1325, def_pred[:, 1] * 1973, color='c', linestyle='solid', marker='o', linewidth='2')
        pred_atr = plt.plot(atr_pred[:, 0] * 1325, atr_pred[:, 1] * 1973, color='m', linestyle='solid', marker='o', linewidth='2')
        pred_env = plt.plot(env_pred[:, 0] * 1325, env_pred[:, 1] * 1973, color='b', linestyle='solid', marker='o', linewidth='2')
        true_10 = plt.plot(def_true[4:13, 0] * 1325, def_true[4:13, 1] * 1973, color='g', linestyle='solid', marker='o', linewidth='2')
        pred_atr_env = plt.plot(atr_env_pred[:, 0] * 1325, atr_env_pred[:, 1] * 1973, color='r', linestyle='solid', marker='o', linewidth='2')
        true_5 = plt.plot(def_true[0:5, 0] * 1325, def_true[0:5, 1] * 1973, color='k', linestyle='solid', marker='o', linewidth='2')
        plt.savefig('./film/gate/%d.jpg' % num)
        plt.close()

    # hyang
    if i == 4:
        plt.xlim(0, 1455)
        plt.ylim(1925, 0)
        print "============", atr_attr
        pred_def = plt.plot(def_pred[:, 0] * 1455, def_pred[:, 1] * 1925, color='c', linestyle='solid', marker='o', linewidth='2')
        pred_atr = plt.plot(atr_pred[:, 0] * 1455, atr_pred[:, 1] * 1925, color='m', linestyle='solid', marker='o', linewidth='2')
        pred_env = plt.plot(env_pred[:, 0] * 1455, env_pred[:, 1] * 1925, color='b', linestyle='solid', marker='o', linewidth='2')
        true_10 = plt.plot(def_true[4:13, 0] * 1455, def_true[4:13, 1] * 1925, color='g', linestyle='solid', marker='o', linewidth='2')
        pred_atr_env = plt.plot(atr_env_pred[:, 0] * 1455, atr_env_pred[:, 1] * 1925, color='r', linestyle='solid', marker='o', linewidth='2')
        true_5 = plt.plot(def_true[0:5, 0] * 1455, def_true[0:5, 1] * 1925, color='k', linestyle='solid', marker='o', linewidth='2')
        plt.savefig('./film/hyang/%d.jpg' % num)
        plt.close()

    # little
    if i == 5:
        plt.xlim(0, 1417)
        plt.ylim(2019, 0)
        print "============", atr_attr
        pred_def = plt.plot(def_pred[:, 0] * 1417, def_pred[:, 1] * 2019, color='c', linestyle='solid', marker='o', linewidth='2')
        pred_atr = plt.plot(atr_pred[:, 0] * 1417, atr_pred[:, 1] * 2019, color='m', linestyle='solid', marker='o', linewidth='2')
        pred_env = plt.plot(env_pred[:, 0] * 1417, env_pred[:, 1] * 2019, color='b', linestyle='solid', marker='o', linewidth='2')
        true_10 = plt.plot(def_true[4:13, 0] * 1417, def_true[4:13, 1] * 2019, color='g', linestyle='solid', marker='o', linewidth='2')
        true_5 = plt.plot(def_true[0:5, 0] * 1417, def_true[0:5, 1] * 2019, color='k', linestyle='solid', marker='o', linewidth='2')
        pred_atr_env = plt.plot(atr_env_pred[:, 0] * 1417, atr_env_pred[:, 1] * 2019, color='r', linestyle='solid', marker='o', linewidth='2')
        plt.savefig('./film/little/%d.jpg' % num)
        plt.close()

    # nexus
    if i == 6:
        plt.xlim(0, 1330)
        plt.ylim(1947, 0)
        print "============", atr_attr
        pred_def = plt.plot(def_pred[:, 0] * 1330, def_pred[:, 1] * 1947, color='c', linestyle='solid', marker='o', linewidth='2')
        pred_atr = plt.plot(atr_pred[:, 0] * 1330, atr_pred[:, 1] * 1947, color='m', linestyle='solid', marker='o', linewidth='2')
        pred_env = plt.plot(env_pred[:, 0] * 1330, env_pred[:, 1] * 1947, color='b', linestyle='solid', marker='o', linewidth='2')
        true_10 = plt.plot(def_true[4:13, 0] * 1330, def_true[4:13, 1] * 1947, color='g', linestyle='solid', marker='o', linewidth='2')
        true_5 = plt.plot(def_true[0:5, 0] * 1330, def_true[0:5, 1] * 1947, color='k', linestyle='solid', marker='o', linewidth='2')
        pred_atr_env = plt.plot(atr_env_pred[:, 0] * 1330, atr_env_pred[:, 1] * 1947, color='r', linestyle='solid', marker='o', linewidth='2')
        plt.savefig('./film/nexus/%d.jpg' % num)
        plt.close()

    # quad
    if i == 7:
        plt.xlim(0, 1983)
        plt.ylim(1088, 0)
        print "============", atr_attr
        pred_def = plt.plot(def_pred[:, 0] * 1983, def_pred[:, 1] * 1088, color='c', linestyle='solid', marker='o', linewidth='2')
        pred_atr = plt.plot(atr_pred[:, 0] * 1983, atr_pred[:, 1] * 1088, color='m', linestyle='solid', marker='o', linewidth='2')
        pred_env = plt.plot(env_pred[:, 0] * 1983, env_pred[:, 1] * 1088, color='b', linestyle='solid', marker='o', linewidth='2')
        true_10 = plt.plot(def_true[4:13, 0] * 1983, def_true[4:13, 1] * 1088, color='g', linestyle='solid', marker='o', linewidth='2')
        true_5 = plt.plot(def_true[0:5, 0] * 1983, def_true[0:5, 1] * 1088, color='k', linestyle='solid', marker='o', linewidth='2')
        pred_atr_env = plt.plot(atr_env_pred[:, 0] * 1983, atr_env_pred[:, 1] * 1088, color='r', linestyle='solid', marker='o', linewidth='2')
        plt.savefig('./film/quad/%d.jpg' % num)
        plt.close()

def plot():
    path = glob('../dataset/image/test/RGB/*.jpg')
    path.sort()
    DATA_NUM = [161, 58, 464, 82, 194, 30, 91, 2]
    j = 0

    # Amount of movement
    f_def = open('./Save_Def/results.pkl', 'rb')

    # Amount of movement + attribute
    f_atr = open('./Save_Atr/results.pkl', 'rb')

    # Amount of movement + environment
    f_env = open('./Save_Env/results.pkl', 'rb')

    # Amount of movement + attribute + environment
    f_atr_env = open('./Save_Atr_Env/results.pkl', 'rb')

    # all data = 1082
    results_def = pickle.load(f_def)
    results_atr = pickle.load(f_atr)
    results_env = pickle.load(f_env)
    results_atr_env = pickle.load(f_atr_env)


    for i in range(len(DATA_NUM)):
        print "===============", path[i]
        for num in range(j, j + DATA_NUM[i]):
            print num, "------------------"
            name = 'sequence' + str(num)
            plot_trajectory(results_def[num][0], results_def[num][1], results_atr[num][0], results_atr[num][1], results_atr[num][2], results_env[num][0], results_env[num][1], results_atr_env[num][0], results_atr_env[num][1], name, num, path[i], i)
        j += DATA_NUM[i]

if __name__ == '__main__':
    plot()

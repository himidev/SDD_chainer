# coding:UTF-8
import argparse
import os
import pickle
import copy
from glob import glob
import cv2

import numpy as np

import chainer
from chainer import optimizers
from chainer import cuda
from chainer import serializers

from net_def import Model_Def
from net_atr import Model_Atr
from net_env import Model_Env
from net_atr_env import Model_Atr_Env
from attribute import Test
from load_test import Test_DataLoader
from load_test_atr import Test_DataLoader_Atr
from image_read import Image_Read
from norm import test_pixel

'''------------------------------------------'''
# MODEL PATH
# Among of movement
MODEL_PATH_DEFAULT = "../default/Train/{}.model"
# Attribute
MODEL_PATH_ATTRIBUTE = "../attribute/Train/{}.model"
# Environment
MODEL_PATH_ENVIRONMENT_ = "../environment/Train/{}.model"
# Attribute_Environment
MODEL_PATH_ATTRIBUTE_ENVIRONMENT_ = '../attribute_environment/Train/50.model'

SEGMENTATION_PATH_DATA = '../dataset/image/test/GLAY/*.png'
DATA_SCENE = ['Bookstore', 'coupa', 'deathCircle', 'gate', 'hyang', 'little', 'nexus', 'quad']
'''------------------------------------------'''


def Euclid_error_pixel(trajectory_pixel, prediction_pixel, obs_length):
    '''
    :param trajectory: true value
    :param prediction: prediction calue
    :param obs_length: observe length
    :return:
    '''
    error = np.zeros(len(prediction_pixel) - obs_length)
    for i in range(obs_length, len(prediction_pixel)):
        # prediction position
        pred_pos = prediction_pixel[i, :]
        # true position
        true_pos = trajectory_pixel[i+2, :]

        # Euclidean distance error
        error[i - obs_length] = np.linalg.norm(true_pos - pred_pos)
    return error


def main():
    '''Parameter Settings'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=int, default=1, help='number of batch')
    parser.add_argument('--sequence', type=int, default=13, help='number of sequence')
    parser.add_argument('--relate_coordinate', type=int, default=12, help='number of relate_coordinate')
    parser.add_argument('--obs_sequence', type=int, default=4, help='number of observe sequence(relate_coordinate)')
    parser.add_argument('--obs_sequence2', type=int, default=3, help='number of observe sequence(relate_coordinate)')
    parser.add_argument('--pred_sequence', type=int, default=7, help='number of prediction sequence')
    parser.add_argument('--pred', type=int, default=11, help='number of prediction sequence')
    parser.add_argument('--learning_rate', type=float, default=0.1, help='number of learning rate')
    parser.add_argument('--i_size_def', type=int, default=2, help='number of default input layer unit')
    parser.add_argument('--i_size_atr', type=int, default=8, help='number of attribute input layer unit')
    parser.add_argument('--i_size_env', type=int, default=290, help='number of environment input layer unit')
    parser.add_argument('--i_size_atr_env', type=int, default=296, help='number of attribute_environment input layer unit')
    parser.add_argument('--h_size', type=int, default=128, help='number of hidden layer unit')
    parser.add_argument('--o_size', type=int, default=2, help='number of output layer unit')
    parser.add_argument('--GPU_ID', type=int, default=0, help='number of GPU')
    sample_args = parser.parse_args()

    #test_def(sample_args)
    #test_atr(sample_args)
    #test_env(sample_args)
    test_atr_env(sample_args)


'''Amount of movement'''
def test_def(sample_args):
    # model call
    model = Model_Def(i_size=sample_args.i_size_def, h_size=sample_args.h_size, o_size=sample_args.o_size, train=False)
    cuda.get_device_from_id(sample_args.GPU_ID).use()
    model.to_gpu()

    save_directory = './Save_Def'

    # optimizer
    optimizer = optimizers.RMSprop()
    optimizer.setup(model)

    # model read
    serializers.load_npz(MODEL_PATH_DEFAULT, model)

    # load test data
    data_test = Test_DataLoader(sample_args.sequence)

    # initial loss
    total_error_0 = 0
    total_error_1 = 0
    total_error_2 = 0
    total_error_3 = 0
    total_error_4 = 0
    total_error_5 = 0
    total_error_6 = 0
    total_error_7 = 0

    loss1 = 0
    loss2 = 0
    loss3 = 0
    loss4 = 0
    loss5 = 0
    loss6 = 0
    loss7 = 0
    loss8 = 0

    # result save
    results_def = []

    for test in range(len(data_test.list)):
        print "============", DATA_SCENE[test]
        for pointer in range(data_test.list[test]):
            pred = []
            trajectory = data_test.list_coordinate[test][pointer]
            index = 0
            count = 1

            trajectory = np.asarray(trajectory, dtype=np.float32)
            trajectory_copy = copy.deepcopy(trajectory)
            # Calculation of movement amount
            trajectory = np.diff(trajectory, axis=0)

            model.reset_state()
            for x, absolutely_coord in zip(trajectory[index:index + sample_args.obs_sequence, :], trajectory_copy[index+1:index + sample_args.obs_sequence + 1, :]):
                x = np.asarray(x, dtype=np.float32)
                absolutely_coord = np.asarray(absolutely_coord, dtype=np.float32)
                # reshape
                x = np.reshape(x, [-1, 2])
                absolutely_coord = np.reshape(absolutely_coord, [-1, 2])
                # GPU
                x = chainer.Variable(cuda.to_gpu(x))

                a = model(x, train=False)
                # Change Variable to numpy
                a = cuda.to_cpu(a.data)
                b = a + absolutely_coord
                # from moving amount to absolute value
                pred.append(b)

                # prediction start
                if count > 3:
                    for _ in range(sample_args.pred_sequence):
                        a = chainer.Variable(cuda.to_gpu(a))

                        a = model(a, train=False)
                        a = cuda.to_cpu(a.data)
                        b = a + b
                        pred.append(b)
                count += 1

            prediction = np.array(pred)
            prediction = np.reshape(prediction, [-1, 2])

            # combine the predicted values with true values
            true_pred = np.vstack((trajectory_copy[:5], prediction[3:sample_args.pred]))
            # find absolute coordinates matching the original image size
            trajectory_pixel = test_pixel(trajectory_copy[:sample_args.sequence], test)
            prediction_pixel = test_pixel(prediction[:sample_args.pred], test)

            # Euclidean distance error
            total_error = np.trunc(Euclid_error_pixel(trajectory_pixel, prediction_pixel, sample_args.obs_sequence2))
            total_error_0 += total_error[0]
            total_error_1 += total_error[1]
            total_error_2 += total_error[2]
            total_error_3 += total_error[3]
            total_error_4 += total_error[4]
            total_error_5 += total_error[5]
            total_error_6 += total_error[6]
            total_error_7 += total_error[7]

            print "Trajectory Number : ", pointer, "out of", data_test.list[test]
            results_def.append((trajectory_copy[:sample_args.sequence], true_pred))

        total_error_0 /= pointer
        total_error_1 /= pointer
        total_error_2 /= pointer
        total_error_3 /= pointer
        total_error_4 /= pointer
        total_error_5 /= pointer
        total_error_6 /= pointer
        total_error_7 /= pointer

        loss1 += total_error_0
        loss2 += total_error_1
        loss3 += total_error_2
        loss4 += total_error_3
        loss5 += total_error_4
        loss6 += total_error_5
        loss7 += total_error_6
        loss8 += total_error_7

    f = open('./Euclid_Loss_Def/Euclid_Error.txt', 'w')
    print >> f, (
        "1_loss:{}, 2_loss:{}, 3_loss:{}, 4_loss:{}, 5_loss:{}, 6_loss:{}, 7_loss:{}, 8_loss:{}, Total_loss:{}".format((np.trunc(loss1 / test)),
                                                                                      np.trunc((loss2 / test)),
                                                                                      np.trunc((loss3 / test)),
                                                                                      np.trunc((loss4 / test)),
                                                                                      np.trunc((loss5 / test)),
                                                                                      np.trunc((loss6 / test)),
                                                                                      np.trunc((loss7 / test)),
                                                                                      np.trunc((loss8 / test)),
                                                                                      ((np.trunc((
                                                                                           loss1 / test) + (
                                                                                           loss2 / test) + (
                                                                                           loss3 / test) + (
                                                                                           loss4 / test) + (
                                                                                           loss5 / test) + (loss6 / test) + (loss7 / test) + (loss8 / test))) / 8)))
    f.close()

    print "Saving results"
    with open(os.path.join(save_directory, 'results.pkl'), 'wb') as f:
        pickle.dump(results_def, f)

'''Amount of movement + attribute'''
def test_atr(sample_args):
    # model call
    model = Model_Atr(i_size=sample_args.i_size_atr, h_size=sample_args.h_size, o_size=sample_args.o_size, train=False)
    cuda.get_device_from_id(sample_args.GPU_ID).use()
    model.to_gpu()

    save_directory = './Save_Atr'

    # optimizer
    optimizer = optimizers.RMSprop()
    optimizer.setup(model)

    # model load
    serializers.load_npz(MODEL_PATH_ATTRIBUTE, model)

    # load test data
    data_test = Test_DataLoader_Atr(sample_args.sequence)

    # initial loss
    total_error_0 = 0
    total_error_1 = 0
    total_error_2 = 0
    total_error_3 = 0
    total_error_4 = 0
    total_error_5 = 0
    total_error_6 = 0
    total_error_7 = 0

    loss1 = 0
    loss2 = 0
    loss3 = 0
    loss4 = 0
    loss5 = 0
    loss6 = 0
    loss7 = 0
    loss8 = 0

    # result save
    results_atr = []

    for test in range(len(data_test.list)):
        print "============", DATA_SCENE[test]
        for pointer in range(data_test.list[test]):
            pred = []
            trajectory = data_test.list_coordinate[test][pointer]
            # extract attribute
            attribute = Test(trajectory)
            index = 0
            count = 1

            trajectory = np.asarray(trajectory, dtype=np.float32)
            trajectory_copy = copy.deepcopy(trajectory)
            # Calculation of movement amount
            trajectory = np.diff(trajectory[:, :2], axis=0)
            t_shape = trajectory.shape

            # target trajectory + attribute
            trajectory = np.c_[trajectory, trajectory_copy[:t_shape[0], 2:9]]

            model.reset_state()
            for x, absolutely_coord in zip(trajectory[index:index + sample_args.obs_sequence, :], trajectory_copy[index+1:index + sample_args.obs_sequence + 1, :]):
                x = np.asarray(x, dtype=np.float32)

                atr = np.copy(x[2:])
                absolutely_coord = np.asarray(absolutely_coord, dtype=np.float32)
                absolutely_coord = absolutely_coord[:2]

                # reshape
                x = np.reshape(x, [-1, 8])

                # GPU
                x = chainer.Variable(cuda.to_gpu(x))

                a = model(x, train=False)
                # Change Variable to numpy
                a = cuda.to_cpu(a.data)
                b = a + absolutely_coord
                # from moving amount to absolute value
                pred.append(b)

                # prediction start
                if count > 3:
                    for _ in range(sample_args.pred_sequence):
                        atr = np.reshape(atr, [-1, 6])
                        a = np.hstack((a, atr))

                        a = chainer.Variable(cuda.to_gpu(a))

                        a = model(a, train=False)
                        a = cuda.to_cpu(a.data)
                        b = a + b
                        pred.append(b)

                count += 1

            prediction = np.array(pred)
            prediction = np.reshape(prediction, [-1, 2])

            # combine the predicted values with true values
            true_pred = np.vstack((trajectory_copy[:, :2][:5], prediction[3:sample_args.pred]))
            # find absolute coordinates matching the original image size
            trajectory_pixel = test_pixel(trajectory_copy[:, :2][:sample_args.sequence], test)
            prediction_pixel = test_pixel(prediction[:sample_args.pred], test)

            # Euclidean distance error
            total_error = np.trunc(Euclid_error_pixel(trajectory_pixel, prediction_pixel, sample_args.obs_sequence2))
            total_error_0 += total_error[0]
            total_error_1 += total_error[1]
            total_error_2 += total_error[2]
            total_error_3 += total_error[3]
            total_error_4 += total_error[4]
            total_error_5 += total_error[5]
            total_error_6 += total_error[6]
            total_error_7 += total_error[7]

            print "Trajectory Number : ", pointer, "out of", data_test.list[test]
            results_atr.append((trajectory_copy[:sample_args.sequence], true_pred, attribute))

        total_error_0 /= pointer
        total_error_1 /= pointer
        total_error_2 /= pointer
        total_error_3 /= pointer
        total_error_4 /= pointer
        total_error_5 /= pointer
        total_error_6 /= pointer
        total_error_7 /= pointer

        loss1 += total_error_0
        loss2 += total_error_1
        loss3 += total_error_2
        loss4 += total_error_3
        loss5 += total_error_4
        loss6 += total_error_5
        loss7 += total_error_6
        loss8 += total_error_7

    f = open('./Euclid_Loss_Atr/Euclid_Error.txt', 'w')
    print >> f, (
        "1_loss:{}, 2_loss:{}, 3_loss:{}, 4_loss:{}, 5_loss:{}, 6_loss:{}, 7_loss:{}, 8_loss:{}, Total_loss:{}".format((np.trunc(loss1 / test)),
                                                                                      np.trunc((loss2 / test)),
                                                                                      np.trunc((loss3 / test)),
                                                                                      np.trunc((loss4 / test)),
                                                                                      np.trunc((loss5 / test)),
                                                                                      np.trunc((loss6 / test)),
                                                                                      np.trunc((loss7 / test)),
                                                                                      np.trunc((loss8 / test)),
                                                                                      np.trunc((((
                                                                                           loss1 / test) + (
                                                                                           loss2 / test) + (
                                                                                           loss3 / test) + (
                                                                                           loss4 / test) + (
                                                                                           loss5 / test) + (loss6 / test) + (loss7 / test) + (loss8 / test))) / 8)))
    f.close()


    print "Saving results"
    with open(os.path.join(save_directory, 'results.pkl'), 'wb') as f:
        pickle.dump(results_atr, f)

'''Amount of movement + environment'''
def test_env(sample_args):
    # test image path
    image_data = glob(SEGMENTATION_PATH_DATA)
    image_data.sort()

    # model call
    model = Model_Env(i_size=sample_args.i_size_env, h_size=sample_args.h_size, o_size=sample_args.o_size, train=False)
    cuda.get_device_from_id(sample_args.GPU_ID).use()
    model.to_gpu()

    save_directory = './Save_Env'

    # optimizer
    optimizer = optimizers.RMSprop()
    optimizer.setup(model)

    # model load
    serializers.load_npz(MODEL_PATH_ENVIRONMENT_, model)

    # data load
    data_test = Test_DataLoader(sample_args.sequence)

    # initial loss
    total_error_0 = 0
    total_error_1 = 0
    total_error_2 = 0
    total_error_3 = 0
    total_error_4 = 0
    total_error_5 = 0
    total_error_6 = 0
    total_error_7 = 0

    loss1 = 0
    loss2 = 0
    loss3 = 0
    loss4 = 0
    loss5 = 0
    loss6 = 0
    loss7 = 0
    loss8 = 0

    # save result
    results_env = []

    for test in range(len(data_test.list)):
        print "============", DATA_SCENE[test]
        for pointer in range(data_test.list[test]):
            pred = []
            # image load
            # Grayscale conversion
            data = cv2.imread(image_data[test], 0)
            data /= 10
            trajectory = data_test.list_coordinate[test][pointer]
            trajectory = np.asarray(trajectory, dtype=np.float32)
            trajectory_copy = copy.deepcopy(trajectory)
            # Calculation of movement amount
            trajectory = np.diff(trajectory, axis=0)

            index = 0
            count = 1
            model.reset_state()
            for x, absolutely_coord in zip(trajectory[index:index + sample_args.obs_sequence, :], trajectory_copy[index+1:index + sample_args.obs_sequence + 1, :]):
                absolutely_coord = np.asarray(absolutely_coord, dtype=np.float32)

                # calculation of target environment
                image = Image_Read(data, absolutely_coord, test, train=False)
                image_ = chainer.Variable(cuda.to_gpu(image.img))

                x = np.asarray(x, dtype=np.float32)
                # reshape
                x = np.reshape(x, [-1, 2])

                # GPU
                x = chainer.Variable(cuda.to_gpu(x))

                a = model(image_, x, train=False)
                # Change Variable to numpy
                a = cuda.to_cpu(a.data)
                b = a + absolutely_coord
                # from moving amount to absolute value
                pred.append(b)

                # prediction start
                if count > 3:
                    for _ in range(sample_args.pred_sequence):
                        a = np.reshape(a, [-1])
                        # calculation of target environment
                        image = Image_Read(data, b[0], test, train=False)
                        image_ = chainer.Variable(cuda.to_gpu(image.img))

                        a = np.asarray(a, dtype=np.float32)
                        a = np.reshape(a, [-1, 2])

                        # GPU
                        a = chainer.Variable(cuda.to_gpu(a))

                        a = model(image_, a, train=False)
                        a = cuda.to_cpu(a.data)
                        b = a + b
                        pred.append(b)
                count += 1

            prediction = np.array(pred)
            prediction = np.reshape(prediction, [-1, 2])

            # combine the predicted values with true values
            true_pred = np.vstack((trajectory_copy[:5], prediction[3:sample_args.pred]))
            # find absolute coordinates matching the original image size
            trajectory_pixel = test_pixel(trajectory_copy[:sample_args.sequence], test)
            prediction_pixel = test_pixel(prediction[:sample_args.pred], test)

            # Euclidean distance error
            total_error = np.trunc(Euclid_error_pixel(trajectory_pixel, prediction_pixel, sample_args.obs_sequence2))
            total_error_0 += total_error[0]
            total_error_1 += total_error[1]
            total_error_2 += total_error[2]
            total_error_3 += total_error[3]
            total_error_4 += total_error[4]
            total_error_5 += total_error[5]
            total_error_6 += total_error[6]
            total_error_7 += total_error[7]

            print "Trajectory Number : ", pointer, "out of", data_test.list[test]
            results_env.append((trajectory_copy[:sample_args.sequence], true_pred))

        total_error_0 /= pointer
        total_error_1 /= pointer
        total_error_2 /= pointer
        total_error_3 /= pointer
        total_error_4 /= pointer
        total_error_5 /= pointer
        total_error_6 /= pointer
        total_error_7 /= pointer

        loss1 += total_error_0
        loss2 += total_error_1
        loss3 += total_error_2
        loss4 += total_error_3
        loss5 += total_error_4
        loss6 += total_error_5
        loss7 += total_error_6
        loss8 += total_error_7

    f = open('./Euclid_Loss_Env/Euclid_Error.txt', 'w')
    print >> f, (
        "1_loss:{}, 2_loss:{}, 3_loss:{}, 4_loss:{}, 5_loss:{}, 6_loss:{}, 7_loss:{}, 8_loss:{}, Total_loss:{}".format(
            (np.trunc(loss1 / test)),
            np.trunc((loss2 / test)),
            np.trunc((loss3 / test)),
            np.trunc((loss4 / test)),
            np.trunc((loss5 / test)),
            np.trunc((loss6 / test)),
            np.trunc((loss7 / test)),
            np.trunc((loss8 / test)),
            np.trunc((((
                           loss1 / test) + (
                           loss2 / test) + (
                           loss3 / test) + (
                           loss4 / test) + (
                           loss5 / test) + (loss6 / test) + (loss7 / test) + (loss8 / test))) / 8)))
    f.close()

    print "Saving results"
    with open(os.path.join(save_directory, 'results.pkl'), 'wb') as f:
        pickle.dump(results_env, f)

'''Amount of movement + attribute+ environment'''
def test_atr_env(sample_args):
    # test image path
    image_data = glob(SEGMENTATION_PATH_DATA)
    image_data.sort()

    # model call
    model = Model_Atr_Env(i_size=sample_args.i_size_atr_env, h_size=sample_args.h_size, o_size=sample_args.o_size,
                          train=False)
    cuda.get_device_from_id(sample_args.GPU_ID).use()
    model.to_gpu()

    save_directory = './Save_Atr_Env'

    # optimizer
    optimizer = optimizers.RMSprop()
    optimizer.setup(model)

    # model load
    serializers.load_npz(MODEL_PATH_ATTRIBUTE_ENVIRONMENT_, model)

    # data load
    data_test = Test_DataLoader_Atr(sample_args.sequence)

    # initial loss
    total_error_0 = 0
    total_error_1 = 0
    total_error_2 = 0
    total_error_3 = 0
    total_error_4 = 0
    total_error_5 = 0
    total_error_6 = 0
    total_error_7 = 0

    loss1 = 0
    loss2 = 0
    loss3 = 0
    loss4 = 0
    loss5 = 0
    loss6 = 0
    loss7 = 0
    loss8 = 0

    # save result
    results_env_atr = []

    for test in range(len(data_test.list)):
        print "============", DATA_SCENE[test]
        for pointer in range(data_test.list[test]):
            pred = []
            # image load
            # Grayscale conversion
            data = cv2.imread(image_data[test], 0)
            data /= 10

            trajectory = data_test.list_coordinate[test][pointer]
            # extract attribute
            attribute = Test(trajectory)

            trajectory = np.asarray(trajectory, dtype=np.float32)
            trajectory_copy = copy.deepcopy(trajectory)

            # Calculation of movement amount
            trajectory = np.diff(trajectory[:, :2], axis=0)
            t_shape = trajectory.shape

            # target trajectory + attribute
            trajectory = np.c_[trajectory, trajectory_copy[:t_shape[0], 2:9]]

            index = 0
            count = 1
            model.reset_state()
            for x, absolutely_coord in zip(trajectory[index:index + sample_args.obs_sequence, :], trajectory_copy[index + 1:index + sample_args.obs_sequence + 1, :]):
                # calculation of target environment
                image = Image_Read(data, absolutely_coord, test, train=False)
                image_ = chainer.Variable(cuda.to_gpu(image.img))

                x = np.asarray(x, dtype=np.float32)

                atr = np.copy(x[2:])
                absolutely_coord = np.asarray(absolutely_coord, dtype=np.float32)
                absolutely_coord = absolutely_coord[:2]

                # reshape
                x = np.reshape(x, [-1, 8])

                # GPU
                x = chainer.Variable(cuda.to_gpu(x))

                a = model(image_, x, train=False)
                # Change Variable to numpy
                a = cuda.to_cpu(a.data)
                b = a + absolutely_coord
                # from moving amount to absolute value
                pred.append(b)

                # prediction start
                if count > 3:
                    for _ in range(sample_args.pred_sequence):
                        a = np.reshape(a, [-1])
                        # calculation of target environment
                        image = Image_Read(data, b[0], test, train=False)
                        image_ = cuda.to_gpu(image.img)

                        a = np.reshape(a, [1, 2])
                        atr = np.reshape(atr, [-1, 6])
                        a = np.hstack((a, atr))

                        a = chainer.Variable(cuda.to_gpu(a))

                        a = model(image_, a, train=False)
                        a = cuda.to_cpu(a.data)
                        b = a + b
                        pred.append(b)
                count += 1

            prediction = np.array(pred)
            prediction = np.reshape(prediction, [-1, 2])
            # combine the predicted values with true values
            true_pred = np.vstack((trajectory_copy[:, :2][:5], prediction[3:sample_args.pred]))
            # find absolute coordinates matching the original image size
            trajectory_pixel = test_pixel(trajectory_copy[:, :2][:sample_args.sequence], test)
            prediction_pixel = test_pixel(prediction[:sample_args.pred], test)

            # Euclidean distance error
            total_error = np.trunc(Euclid_error_pixel(trajectory_pixel, prediction_pixel, sample_args.obs_sequence2))
            total_error_0 += total_error[0]
            total_error_1 += total_error[1]
            total_error_2 += total_error[2]
            total_error_3 += total_error[3]
            total_error_4 += total_error[4]
            total_error_5 += total_error[5]
            total_error_6 += total_error[6]
            total_error_7 += total_error[7]

            print "Trajectory Number : ", pointer, "out of", data_test.list[test]
            results_env_atr.append((trajectory_copy[:sample_args.sequence], true_pred, attribute))

        total_error_0 /= pointer
        total_error_1 /= pointer
        total_error_2 /= pointer
        total_error_3 /= pointer
        total_error_4 /= pointer
        total_error_5 /= pointer
        total_error_6 /= pointer
        total_error_7 /= pointer

        loss1 += total_error_0
        loss2 += total_error_1
        loss3 += total_error_2
        loss4 += total_error_3
        loss5 += total_error_4
        loss6 += total_error_5
        loss7 += total_error_6
        loss8 += total_error_7

    f = open('./Euclid_Loss_Atr_Env/Euclid_Error.txt', 'w')
    print >> f, (
        "1_loss:{}, 2_loss:{}, 3_loss:{}, 4_loss:{}, 5_loss:{}, 6_loss:{}, 7_loss:{}, 8_loss:{}, Total_loss:{}".format((np.trunc(loss1 / test)),
                                                                                      np.trunc((loss2 / test)),
                                                                                      np.trunc((loss3 / test)),
                                                                                      np.trunc((loss4 / test)),
                                                                                      np.trunc((loss5 / test)),
                                                                                      np.trunc((loss6 / test)),
                                                                                      np.trunc((loss7 / test)),
                                                                                      np.trunc((loss8 / test)),
                                                                                      np.trunc((((
                                                                                           loss1 / test) + (
                                                                                           loss2 / test) + (
                                                                                           loss3 / test) + (
                                                                                           loss4 / test) + (
                                                                                           loss5 / test) + (loss6 / test) + (loss7 / test) + (loss8 / test))) / 8)))
    f.close()
    print "Saving results"
    with open(os.path.join(save_directory, 'results.pkl'), 'wb') as f:
        pickle.dump(results_env_atr, f)

if __name__ == '__main__':
    main()

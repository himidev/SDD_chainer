# coding:UTF-8
import time
import argparse

import numpy as np
import matplotlib.pyplot as plt

import chainer
from chainer import optimizers
from chainer import cuda
from chainer import serializers

from net import Model
from load_train import Train_DataLoader
from load_test import Test_DataLoader


def main():
    '''Parameter Settings'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--epoch', type=int, default=100, help='number of epoch')
    parser.add_argument('--batch', type=int, default=10, help='number of batch')
    parser.add_argument('--sequence', type=int, default=10, help='number of sequence')
    parser.add_argument('--relate_coordinate', type=int, default=9, help='number of relate_coordinate')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='number of learning rate')
    parser.add_argument('--i_size', type=int, default=8, help='number of input layer unit')
    parser.add_argument('--h_size', type=int, default=128, help='number of hidden layer unit')
    parser.add_argument('--o_size', type=int, default=2, help='number of output layer unit')
    parser.add_argument('--GPU_ID', type=int, default=0, help='number of GPU')
    args = parser.parse_args()
    train(args)

def train(args):
    # data_load
    data_train = Train_DataLoader(args.sequence)
    data_test = Test_DataLoader(args.sequence)

    # define model
    model = Model(i_size=args.i_size, h_size=args.h_size, o_size=args.o_size, train=True)
    cuda.get_device_from_id(args.GPU_ID).use()
    model.to_gpu()

    # optimizer
    optimizer = optimizers.RMSprop(lr=args.learning_rate)
    optimizer.setup(model)

    # initial value
    train_loss = []
    test_loss = []

    # iteration
    n_iter = 0
    n_iter_test = 0

    for epoch in range(1, args.epoch + 1):
        print 'epoch', epoch
        start = time.time()

        '''TRAIN'''
        print "TRAIN"
        # -5 to delete extra data
        for data_iter in xrange(0, len(data_train.all_data) - 5, args.batch):
            # initial loss
            loss_train = 0

            x = []
            t = []
            n_iter += 1
            model.cleargrads()
            model.reset_state()
            for batch_ in xrange(args.batch):
                list_random = np.random.randint(0, len(data_train.list))
                # coordinate match the scene
                trajectory_random = np.random.randint(0, len(data_train.list_coordinate[list_random]))
                trajectory = data_train.list_coordinate[list_random][trajectory_random]
                # Since -1 is necessary for the target data
                index = np.random.randint(0, len(trajectory) - args.sequence - 1)
                x.append(trajectory[index:index + args.sequence, :])
                t.append(trajectory[index + 1:index + 1 + args.sequence, :])

            x = np.asarray(x, dtype=np.float32)
            t = np.asarray(t, dtype=np.float32)

            # To extract attributes
            x_copy = np.copy(x)
            t_copy = np.copy(t)

            # Calculation of movement amount
            x = np.diff(x[:, :, :2], axis=1)
            t = np.diff(t[:, :, :2], axis=1)

            # Fit dimension
            # Movement amount + Attribute
            x = np.c_[x, x_copy[:, :9, 2:9]]
            t = np.c_[t, t_copy[:, :9, 2:9]]

            for sequence in xrange(args.relate_coordinate):
                xy = x[:, sequence, :]           # input
                training = t[:, sequence, :]     # target

                # Don't use attributes in testing
                training = training[:, :2]
                # reshape
                xy = np.reshape(xy, [-1, 8])
                training = np.reshape(training, [-1, 2])

                # learning by GPU
                xy = chainer.Variable(cuda.to_gpu(xy))
                training = chainer.Variable(cuda.to_gpu(training))

                loss_train += model(xy, training, train=True)

            print "iteration:", n_iter, "loss:", loss_train
            loss_train.backward()
            optimizer.update()

        end = time.time()
        f = open('loss.txt', 'a')
        print >> f, ("epoch:{}, loss:{}, time:{}".format(epoch, loss_train.data, end - start))
        f.close()

        # save epoch
        if epoch % 20 == 0:
            # Move to CPU once to prevent GPU dependence problems during testing
            model.to_cpu()
            serializers.save_npz('./Train/' + str(epoch) + '.model', model)
            serializers.save_npz('./Train/' + str(epoch) + '.state', optimizer)
            model.to_gpu()

        '''TEST'''
        print "TEST"
        # -7 to delete extra data
        for test_iter in xrange(0, len(data_test.all_data) - 7, args.batch):
            # initial loss
            loss_test = 0

            x = []
            t = []
            n_iter_test += 1
            model.cleargrads()
            model.reset_state()
            for batch_test in xrange(args.batch):
                list_random_test = np.random.randint(0, len(data_test.list))
                # coordinate match the scene
                trajectory_random = np.random.randint(0, len(data_test.list_coordinate[list_random_test]))
                trajectory = data_test.list_coordinate[list_random_test][trajectory_random]

                index_test = np.random.randint(0, len(trajectory) - args.sequence - 1)
                x.append(trajectory[index_test:index_test + args.sequence, :])
                t.append(trajectory[index_test + 1:index_test + 1 + args.sequence, :])

            x = np.asarray(x, dtype=np.float32)
            t = np.asarray(t, dtype=np.float32)

            # To extract attributes
            x_copy = np.copy(x)
            t_copy = np.copy(t)

            # Calculation of movement amount
            x = np.diff(x[:, :, :2], axis=1)
            t = np.diff(t[:, :, :2], axis=1)

            # Fit dimension
            # Movement amount + Attribute
            x = np.c_[x, x_copy[:, :9, 2:9]]
            t = np.c_[t, t_copy[:, :9, 2:9]]

            for sequence in xrange(args.relate_coordinate):
                xy = x[:, sequence, :]          # input
                training = t[:, sequence, :]    # target

                training = training[:, :2]

                # reshape
                xy = np.reshape(xy, [-1, 8])
                training = np.reshape(training, [-1, 2])

                # learning by GPU
                xy = chainer.Variable(cuda.to_gpu(xy))
                training = chainer.Variable(cuda.to_gpu(training))

                loss_test += model(xy, training, train=True)

            print "iteration:", n_iter_test, "loss:", loss_test

        # figure
        train_loss.append(loss_train.data)
        test_loss.append(loss_test.data)
        plt.plot(train_loss, label="train_loss")
        plt.plot(test_loss, label="test_loss")
        plt.yscale('log')
        plt.legend()
        plt.grid(True)
        plt.title("loss")
        plt.xlabel("epoch")
        plt.ylabel("loss")
        plt.savefig("Fig/fig_loss.png")
        plt.clf()

if __name__ == '__main__':
    main()

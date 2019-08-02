# coding:UTF-8
import chainer
import chainer.functions as F
import chainer.links as L

class Model_Atr_Env(chainer.Chain):
    def __init__(self, i_size, h_size, o_size, train):
        self.train = train
        super(Model_Atr_Env, self).__init__(
            conv1=L.Convolution2D(None,  16, 5, stride=2),
            conv2=L.Convolution2D(None, 32,  5, stride=1),
            conv3=L.Convolution2D(None, 32,  5, stride=1),
            h_h=L.LSTM(i_size, h_size),
            h_o=L.Linear(h_size, o_size),
        )

    def __call__(self, img, x, t=None, train=False):
        h = F.max_pooling_2d(F.relu(
            F.local_response_normalization(self.conv1(img))), 2, stride=2)
        h = F.max_pooling_2d(F.relu(
            F.local_response_normalization(self.conv2(h))), 2, stride=2)
        h = F.max_pooling_2d(F.relu(self.conv3(h)), 2, stride=2)
        h = F.reshape(h, (-1, 32*3*3))
        h = F.concat((x, h), axis=1)
        h = self.h_h(h)
        y = self.h_o(h)

        if self.train == True:
            loss = F.mean_squared_error(y, t)
            return loss
        elif self.train == False:
            return y

    def reset_state(self):
        self.h_h.reset_state()

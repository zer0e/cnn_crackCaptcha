import tensorflow as tf
from PIL import Image
import os
import time
import random
import numpy as np
from settings import settings


class Model(object):
    def __init__(self, model_name):
        self.image_height = settings.image_height
        self.image_width = settings.image_width
        self.char_set = settings.char_set
        self.char_set_len = len(self.char_set)
        self.captcha_len = settings.captcha_len
        self.train_images_path = settings.train_images_path
        self.test_images_path = settings.test_images_path
        self.sort_identifier = settings.sort_identifier
        self.model_save_dir = settings.model_save_dir
        self.model = None
        self.model_name = model_name
        self.model_exist = self.check_model_exist()

    def check_model_exist(self):
        '''
        判断是否存在模型
        :return:
        '''
        if os.path.exists(os.path.join(self.model_save_dir,self.model_name + ".h5")):
            print("存在同名模型，正在读取该模型....")
            self.model = tf.keras.models.load_model(
                os.path.join(self.model_save_dir, self.model_name + '.h5'))
            if self.model:
                print("模型加载成功....")
                return True
            else:
                print("模型加载失败....")
        print("开始创建模型....")
        self.model = self.cnn_model()
        return False

    def cnn_model(self):
        input_tensor = tf.keras.layers.Input(
            (self.image_height, self.image_width, 3))
        x = input_tensor
        for i in range(2):
            x = tf.keras.layers.Conv2D(
                32*2**i, (3, 3), 3, activation='relu', padding='same')(x)
            x = tf.keras.layers.Conv2D(
                32*2**i, (3, 3), 3, activation='relu', padding='same')(x)
            x = tf.keras.layers.MaxPool2D((2, 2), padding='same')(x)
            x = tf.keras.layers.Dropout(0.25)(x)
        x = tf.keras.layers.Flatten()(x)
        x = tf.keras.layers.Dense(128)(x)
        x = tf.keras.layers.Activation('relu')(x)
        x = tf.keras.layers.Dropout(0.5)(x)
        x = [tf.keras.layers.Dense(self.char_set_len, activation='softmax', name='a%d' % (
            i+1))(x) for i in range(self.captcha_len)]
        model = tf.keras.models.Model(inputs=input_tensor, outputs=x)
        model.compile(loss='categorical_crossentropy',
                      optimizer='adadelta',
                      metrics=['accuracy'])
        return model

    @staticmethod
    def convert2grey(img):
        '''
        图片灰度化
        目前暂时未使用，所以有不必要的计算存在
        :param img:
        :return:
        '''
        imgry = img.convert('1')
        return imgry

    def get_image_and_label(self, img_path, img_name):
        '''
        从本地读取图片 返回图片数组和标签
        :param img_path:
        :param img_name:
        :return:
        '''
        label = img_name.split(self.sort_identifier)[0]
        file = os.path.join(img_path, img_name)
        img = Image.open(file)
        array = np.array(img)
        return array, label

    def label2vec(self, text):
        '''
        标签转为one-hot编码
        :param text:
        :return:
        '''
        label_len = len(text)
        if label_len != self.captcha_len:
            raise ValueError("验证码长度应为%d个字符" % (self.captcha_len))
        vec = np.zeros(self.captcha_len * self.char_set_len)
        for i, ch in enumerate(text):
            idx = i * self.char_set_len + self.char_set.index(ch)
            vec[idx] = 1
        return vec

    def gen_from_local(self, img_path, batch_size=32):
        '''
        从本地获取图片 将数据写入数组
        :param img_path:
        :param batch_size:
        :return:
        '''
        X = np.zeros((batch_size, self.image_height, self.image_width, 3))
        y = [np.zeros((batch_size, self.char_set_len))
             for i in range(self.captcha_len)]
        while True:
            for i in range(batch_size):
                img_array, label = self.get_image_and_label(
                    img_path, random.choice(os.listdir(img_path)))
                X[i, :, :, ] = img_array
                for j, ch in enumerate(label):
                    y[j][i, :] = 0
                    y[j][i, self.char_set.index(ch)] = 1
                yield X, y

    def train(self):
        '''
        训练模型
        callback可以下定时保存
        :return:
        '''
        print("使用训练集为：%s\n使用测试集为：%s" %
              (self.train_images_path, self.test_images_path))
        print("模型保存路径为：%s" % self.model_save_dir)
        print("模型名称为：%s" % self.model_name)
        tf.keras.utils.plot_model(self.model, os.path.join(
            self.model_save_dir, self.model_name+".png"), show_shapes='True')
        callback_list = [
            # tf.keras.callbacks.TensorBoard(log_dir='./logs',
            #                                histogram_freq=0, batch_size=32, write_graph=True,
            #                                write_grads=True, write_images=True, embeddings_freq=0,
            #                                embeddings_layer_names=None, embeddings_metadata=None,
            #                                embeddings_data=None, update_freq='epoch')

        ]
        self.model.fit_generator(self.gen_from_local(self.train_images_path), steps_per_epoch=2000, epochs=5,
                                 validation_data=self.gen_from_local(self.test_images_path), validation_steps=512,
                                 callbacks=callback_list)
        print("训练完成，正在保存模型....")
        self.model.save(os.path.join(
            self.model_save_dir, self.model_name + ".h5"))

    def decode(self, y):
        '''
        从one-hot编码还原为字符
        :param y:
        :return:
        '''
        y = np.argmax(np.array(y), axis=2)[:, 0]
        return ''.join([self.char_set[x] for x in y])

    def predict(self, n):
        print("开始验证模型准确性....")
        now = time.time()
        right = 0
        for i in range(n):
            X, y = next(self.gen_from_local(self.test_images_path, 1))
            y_ = self.model.predict(X)
            y = self.decode(y)
            y_ = self.decode(y_)
            if y == y_:
                right += 1
            else:
                # 对比错误
                print("期待值为%s  但是预测值为%s " % (y, y_))
        print("共测试%d次，其中正确%d次，正确率为%.4f%%" % (n, right, (right/n)*100))
        print("总共耗时：%s秒" % str(time.time() - now))

    def predict_from_img(self, img):
        X = np.zeros((1, self.image_height, self.image_width, 3))
        X[0,:,:,] = img
        y_ = self.model.predict(X)
        y_ = self.decode(y_)
        return y_

def main():
    mymodel = Model("skl_captcha_model")
    mymodel.train()
    mymodel.predict(1000)


if __name__ == "__main__":
    main()

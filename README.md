# cnn_crackCaptcha
use cnn to crack captcha by keras  
本项目使用keras api实现卷积神经网络对验证码进行识别。


## 项目介绍
个人使用验证码识别大多数使用的都是第三方api，但因为付费原因对使用量大的人会带来些许经济压力  
少部分同学会使用tesseract来进行识别，这个库由谷歌开源，但识别率有限，对于干扰较多的验证码得自己手动训练，
并且训练起来相当麻烦。  
而使用卷积神经网络，只需简单进行图片操作，或者甚至不用对图片操作就可以实现对干扰型验证的识别。

### 项目依赖
numpy==1.16.2 
tensorflow==1.13.1 
Pillow==6.0.0 
easydict==1.9 

### 项目结构


### 模型结构
![model](https://github.com/zer0e/cnn_crackCaptcha/raw/master/mymodel.png)


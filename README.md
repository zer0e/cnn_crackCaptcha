# cnn_crackCaptcha
use cnn to crack captcha by keras  
本项目使用keras api实现卷积神经网络对验证码进行识别。  
欢迎提出issues与我交流，共同学习


## 项目介绍
个人使用验证码识别大多数使用的都是第三方api，但因为付费原因对使用量大的人会带来些许经济压力  
少部分同学会使用tesseract来进行识别，这个库由谷歌开源，但识别率有限，对于干扰较多的验证码得自己手动训练，
并且训练起来相当麻烦。  
而使用卷积神经网络，只需简单进行图片操作，或者甚至不用对图片操作就可以实现对干扰型验证的识别。

### 项目依赖
```
numpy==1.16.2 
tensorflow==1.13.1 
Pillow==6.0.0 
easydict==1.9 
```

### 项目结构
```
|-- images
|   |-- origin
|   |-- test
|   |-- train
|-- model
|-- gen_image.py
|-- LICENSE
|-- model.png
|-- model.py
|-- mymodel.png
|-- README.md
|-- requirements.txt
|-- settings.py
|-- sort_images.py
```

### 模型结构
![model](https://github.com/zer0e/cnn_crackCaptcha/raw/master/mymodel.png)

## 使用方法
1.先在images/origin目录下放置需要学习的验证码，例如在测试学习中我准备了两万张纯数字验证码  
验证码以标签开头，并使用"_"做分隔字符(可以在settings修改分隔字符)，具体可参考images/example中的图片  
如果你没有图片，可以调用captcha库生成验证码，但经过测试识别率并不是太高，可能是因为生成机制的原因。
建议使用自己的训练集。    

2.修改settings.py中的部分信息，包括图片的长宽，识别的字符，验证码长度，存放路径等等。  
运行sort_images.py，会自动的以19:1的比例将原始图片分为训练集与验证集，之后便可开始训练。

3.运行model.py便可开始学习，你可以在学习前在model.py中修改保存的模型名称。学习完成后会自动从验证集中识别1000
张验证码，并给出正确率。    

经过测试，在训练类似示例图片中的验证码时，准确率高达98%以上，并且还可以继续训练。


## 日志
1.(2019.07.01)增加了flask api，实现网络调用，并修改了模型。 





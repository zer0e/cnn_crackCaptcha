import os
import random,time
from settings import settings
from PIL import Image
import shutil

def check(origin_images_path):
    print("开始验证原始图片集....")
    time.sleep(3)
    right_size = (settings.image_width, settings.image_height)
    sort_identifier = settings.sort_identifier
    captcha_len = settings.captcha_len
    origin_images_list = os.listdir(origin_images_path)
    total = len(origin_images_list)
    print("原始图片集共有%d张图片"%(total))

    bad_image_list = []
    image_suffix_list = settings.image_suffix_list
    for index, image in enumerate(origin_images_list):
        if not (image.endswith(image_suffix_list[i]) for i in range(len(image_suffix_list))):
            bad_image_list.append((index,image,"图片后缀不正确"))
            continue
        
        prefix = image.split(sort_identifier)[0]
        if len(prefix) != captcha_len:
            bad_image_list.append((index, image, "图片标签错误"))
            continue

        try:
            img = Image.open(os.path.join(origin_images_path,image))
        except OSError:
            bad_image_list.append((index, image, "图片无法打开，可能被占用或者损坏"))
            continue
        

        if right_size == img.size:
            print("第%d张图片通过"%(index + 1))
        else:
            bad_image_list.append((index, image, "图片尺寸异常，为{}".format(img.size)))

    if bad_image_list:
        print("======共有%d张图片存在异常====="%(len(bad_image_list)))
        for bad in bad_image_list:
            print("第%d张图片 名称为%s 异常原因为%s" %(bad[0],bad[1],bad[2]))
    else:
        print("未发现异常图片")
    return bad_image_list


def split(origin_images_path,train_images_path,test_images_path,bad_images_list):

    print("开始分离训练集与测试集，比例为19:1")

    origin_images_list = os.listdir(origin_images_path)
    for bad in bad_images_list:
        origin_images_list.remove(bad)
    total = len(origin_images_list)
    print("共有%d张有效图片，其中有%d张无效图片留在原目录"%(total,len(bad_images_list)))

    if not os.path.exists(train_images_path):
        os.mkdir(train_images_path)
    
    if not os.path.exists(test_images_path):
        os.mkdir(test_images_path)

    test_count = int(total * 0.05)
    test_set = set()

    for i in range(test_count):
        while True:
            file_name = random.choice(origin_images_list)
            if file_name in test_set:
                pass
            else:
                test_set.add(file_name)
                origin_images_list.remove(file_name)
                break
    test_list = list(test_set)
    print("测试集数量为%d张图片"%(len(test_list)))
    for file_name in test_list:
        src = os.path.join(origin_images_path, file_name)
        dst = os.path.join(test_images_path, file_name)
        shutil.move(src, dst)

    train_list = origin_images_list
    print("训练集数量为%d张图片"%(len(train_list)))
    for file_name in train_list:
        src = os.path.join(origin_images_path, file_name)
        dst = os.path.join(train_images_path, file_name)
        shutil.move(src, dst)
        
    print("分离完毕")


def main():
    origin_images_path = settings.origin_images_path
    train_images_path = settings.train_images_path
    test_images_path = settings.test_images_path


    bad_images_info = check(origin_images_path)
    bad_images_list = []

    for info in bad_images_info:
        bad_images_list.append(info[1])
    split(origin_images_path,train_images_path,test_images_path,bad_images_list)

if __name__ == "__main__":
    main()

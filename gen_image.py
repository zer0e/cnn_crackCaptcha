from captcha.image import ImageCaptcha
import random

def gen_image():
    image_width = 100
    image_height = 60
    origin_dir = './images/origin/'
    char_set = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    char_set_len = len(char_set)
    captcha_len = 4
    generator = ImageCaptcha(width=100, height=60, fonts=['images/captcha.ttf'])
    for i in range(20000):
        print("正在生成第%d张图片"%(i + 1))
        random_str = ''.join(random.choice(char_set) for i in range(captcha_len))
        random_num = random.randint(10000,99999)
        img = generator.generate_image(random_str)
        file_name = random_str + "_" + str(random_num) + ".jpg"
        img.save(origin_dir + file_name)
    print("ok")

if __name__ == "__main__":
    gen_image()

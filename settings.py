from easydict import EasyDict


settings = EasyDict()

settings.image_height = 26
settings.image_width = 70
settings.image_suffix_list = ['jpg', 'png', 'jpeg']
settings.sort_identifier = '_'
settings.char_set = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
# settings.num_char_set = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# settings.all_char_set = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
#                          'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 
#                          'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
#                          'V', 'W', 'X', 'Y', 'Z']
settings.captcha_len = 4
settings.origin_images_path = 'images/origin/'
settings.train_images_path = 'images/train/'
settings.test_images_path = 'images/test/'
settings.model_save_dir = 'model/'


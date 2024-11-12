# ver. 2

import os
from PIL import Image
import pillow_avif      # pip3 install pillow-avif-plugin


IMG_EXTENSION_LIST = ['.WEBP', '.PNG', '.AVIF']


#====================================================================================================================


DIR_PATH = "C:\\Users\\zdzit.p.michalowski\\Pictures\\WallPaper_TMP"


#====================================================================================================================


print('DIR_PATH = ' + DIR_PATH)
file_names = [f for f in os.listdir(DIR_PATH) if os.path.isfile(os.path.join(DIR_PATH, f)) and os.path.splitext(f)[1].upper() in IMG_EXTENSION_LIST]
print('file_names = ' + str(file_names) + '\n')
for file_name in file_names:
    im = Image.open(os.path.join(DIR_PATH, file_name)).convert('RGB')
    jpg_file_name = os.path.splitext(file_name)[0] + '.jpg'
    im.save(os.path.join(DIR_PATH, jpg_file_name), 'jpeg')
    print(file_name + ' -> ' + jpg_file_name)


file_names = [f for f in os.listdir(DIR_PATH) if os.path.isfile(os.path.join(DIR_PATH, f)) and os.path.splitext(f)[1].upper() == '.JFIF']
print('file_names = ' + str(file_names) + '\n')
for file_name in file_names:
    jpg_file_name = os.path.splitext(file_name)[0] + '.jpg'
    os.rename(os.path.join(DIR_PATH, file_name), os.path.join(DIR_PATH, jpg_file_name))
    print(file_name + ' -> ' + jpg_file_name)

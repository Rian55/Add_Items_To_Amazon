import os
from PIL import Image

folder_name = r"C:/Users/Yenip/Downloads/grimelange/"
count = 0

for path in os.listdir(folder_name):
    count += 1

for i in range(1, count+10):
    old_name = folder_name + rf"{i}.jpg"
    image = Image.open(old_name)
    image.thumbnail((1100, 1100))
    new_name = folder_name + r"EWPR-SHRT-"
    for j in range(3 - int(len(str(i)))):
        new_name += "0"
    new_name += str(i) + ".jpg"
    print(new_name)
    image.save(new_name)
    os.remove(old_name)

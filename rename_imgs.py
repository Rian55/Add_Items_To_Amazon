import os

for i in range(1, 377):
    old_name = rf"C:/Users/Yenip/Downloads/Boxes/{i}.jpg"
    new_name = r"C:/Users/Yenip/Downloads/Boxes/EWPR-BOXS-"
    for j in range(3-int(len(str(i)))):
        new_name += "0"
    new_name += str(i) + ".jpg"
    print(new_name)
    os.rename(old_name, new_name)

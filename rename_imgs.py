import os

folder_name = r"C:/Users/90531/Downloads/Abajur/"
for i in range(1, 132):
    old_name = folder_name + rf"{i}.jpg"
    new_name = folder_name + r"LAMP-SHDE-"
    for j in range(3-int(len(str(i)))):
        new_name += "0"
    new_name += str(i) + ".jpg"
    print(new_name)
    os.rename(old_name, new_name)

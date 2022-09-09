import os

for i in range(1, 252):
    old_name = rf"C:/Users/Yenip/Downloads/Confetti_kids/{i}.jpg"
    new_name = r"C:/Users/Yenip/Downloads/Confetti_kids/CNFT-KDRG-"
    for j in range(3-int(len(str(i)))):
        new_name += "0"
    new_name += str(i) + ".jpg"
    print(new_name)
    os.rename(old_name, new_name)

from PIL import Image,ImageDraw,ImageFont
import numpy as np
import math
import sys

image_path = input("file_path:").replace("\\","/")
if image_path == "":
    print("The file path of the image was not given.")
    sys.exit()
img = Image.open(image_path)
# img.show()

img_gray = img.convert("L")
# img_gray.show()

img_width = img_gray.width
if img_width > 947:
    img_gray = img_gray.resize(
        (
            947, img_gray.height * 947 // img_gray.width
            )
            )
    img_width = img_gray.width

AA_chars = list(input("chars:"))
if len(AA_chars) < 2:
    print("Characters must be at least 2.")
    sys.exit()
chars_len = len(AA_chars)
print(chars_len)
txt = AA_chars

def make_map(str_list):
    l = []
    font = ImageFont.truetype('msgothic.ttc', 20) #"C:\Windows\Fonts"内の（もしくはパスから書いて）お好きなフォントで #エラーが出なければこのままでOK
    for i in str_list:
        im = Image.new("L",(20,20),"white") #空の白地画像の作成
        draw = ImageDraw.Draw(im)
        draw.text((0,0),i,font=font) #文字入れ
        l.append(np.asarray(im).mean()) #Numpy配列化して平均値を計算、格納
    l_as = np.argsort(l) #密度の指標を昇順ソートしたもののインデックス
    lenl = len(l)
    # l2256 = np.r_[np.repeat(l_as[:-(256%lenl)],256//lenl),np.repeat(l_as[-(256%lenl):],256//lenl+1)] #要素数を256に調節
    # chr_map = np.array(str_list)[l2256] #密度順にソートした文字リスト
    chr_map = np.array(str_list)[l_as]
    return chr_map

AA_chars = make_map(AA_chars)

def pixel_to_AA(image, chars_len):
    bin = math.ceil( 255 / chars_len )
    pixels = image.getdata()
    AA_str = ""
    for pixel in pixels:
        index = math.floor(pixel / bin)
        # print(index)
        AA_str += AA_chars[index]
    return AA_str

print(255 // (chars_len + 1))
AA_str = pixel_to_AA(img_gray, chars_len)

AA_str_len = len(AA_str)
AA_img = ""

for i in range(0, AA_str_len, img_width):
    AA_img += AA_str[i : i + img_width] + "\n"

name = input("filename:")
if name == "":
    txt.append(".txt")
    name = "".join(txt)
elif not name.endswith(".txt"):
    name = name + ".txt"

with open(name, "w") as f:
    f.write(AA_img)
print("\"" + name + "\" is saved.")
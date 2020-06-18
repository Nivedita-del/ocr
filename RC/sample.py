
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import tempfile
from pdf2image import convert_from_path, convert_from_bytes

from RC.failsafeocr import to_unicode

while(True):
    if (os.listdir("data/")):
        continue
    else:
        os.mkdir("./data")

with tempfile.TemporaryDirectory() as path:
    images = convert_from_path('datasets/MktPlace-Myntra.pdf', output_folder='data', fmt='jpg')
images = convert_from_bytes(open('datasets/MktPlace-Myntra.pdf', 'rb').read())

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
                help="type of preprocessing to be done, choose from blur, linear, cubic or bilateral")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

if args["preprocess"] == "thresh":
    gray = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

elif args["preprocess"] == "adaptive":
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

if args["preprocess"] == "linear":
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

elif args["preprocess"] == "cubic":
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

if args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)

elif args["preprocess"] == "bilateral":
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

elif args["preprocess"] == "gauss":
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)


text = pytesseract.image_to_string(Image.open(filename), lang='eng')
os.remove(filename)
#print(text)
from os import listdir
import shutil
dir="data/"
shutil.rmtree(dir)


#temp = os.listdir(dir)
#for files in temp:
#    if files.endswith("*.*"):
#        os.remove(os.path.join(dir, files))
print("deleted files")

#gray = cv2.resize(gray, (1000, 1000))

#cv2.imshow("output", gray)
#cv2.waitKey(0)


ph1 = re.findall(r'\b[6789]\d{9}\b', text, flags=0)
print(ph1[0])

data={}

data["Phone Number"] = ph1

import json
import io

jsondata=json.load(data)


with io.open('data.json', 'w', encoding='utf-8') as outfile:
    str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))

with open('data.json', encoding='utf-8') as data_file:
    data_loaded = json.load(data_file)


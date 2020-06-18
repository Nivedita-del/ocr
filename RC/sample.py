
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import tempfile
from pdf2image import convert_from_path, convert_from_bytes


with tempfile.TemporaryDirectory() as path:
    images = convert_from_path('datasets/MktPlace-Myntra.pdf', output_folder='data')
image = convert_from_bytes(open('datasets/MktPlace-Myntra.pdf', 'rb').read())

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

#gray = cv2.resize(gray, (1000, 1000))

#cv2.imshow("output", gray)
#cv2.waitKey(0)

string = ""

ph1 = re.search(r'\b[6789]\d{9}\b', text, flags=0)
ph2 = re.search(r'\b[7689]\d{9}\b', text, flags=0)
ph3 = re.search(r'\b[8679]\d{9}\b', text, flags=0)
ph4 = re.search(r'\b[9689]\d{9}\b', text, flags=0)

        if ph1:
            p=ph1.group(0)
            print(p)
        elif ph2:
            p = ph2.group(0)
            print(p)
        elif ph3:
            p = ph3.group(0)
            print(p)
        elif ph4:
            p = ph4.group(0)
            print(p)
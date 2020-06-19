
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import io
import json
import ftfy
import tempfile
from pdf2image import convert_from_path, convert_from_bytes


from numpy import unicode
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
# print(text)

# show the output images
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
# cv2.waitKey(0)

text_output = open('outputbase.txt', 'w', encoding='utf-8')
text_output.write(text)
text_output.close()

file = open('outputbase.txt', 'r', encoding='utf-8')
text = file.read()
# print(text)

text = ftfy.fix_text(text)
text = ftfy.fix_encoding(text)

# print(text)


name = None
enino = None
regd = None
vin = None
mfgd = None
nameline = []
eninoline = []
redgline = []
vinline = []
mfgdline = []
text0 = []
text1 = []
text2 = []
text3 = []
text4 = []


# Searching for PAN
lines = text.split('\n')
for lin in lines:
    s = lin.strip()
    s = lin.replace('\n', '')
    s = s.rstrip()
    s = s.lstrip()
    text1.append(s)

text1 = list(filter(None, text1))
# print(text1)

lineno = 0

for wordline in text1:
    xx = wordline.split(',')
    if ([w for w in xx if re.search(
            '(Customer Details| customer detials| costomer| details| detials| datiels|)$',
            w)]):
        text1 = list(text1)
        lineno = text1.index(wordline)
        break

# text1 = list(text1)
text0 = text1[lineno + 1:]
print(text0)


def findtheword(textlist, wordstring):
    lineno = -1
    for wordline in textlist:
        xx = wordline.split()
        if ([w for w in xx if re.search(wordstring, w)]):
            lineno = textlist.index(wordline)
            textlist = textlist[lineno + 1:]
            return textlist
    return textlist

t=re.search("ph:", 'ph')
#print(t)

enino = re.findall(r'\b[6789]\d{9}\b', text, flags=0)
enino = enino[0]

name = re.sub('[^a-zA-Z] +', ' ', text)
if (text.__contains__("Customer Name Billing Address Shipping Address")):
    print('')
try:

    name = text0[11]
    name = name.rstrip()
    name = name.lstrip()
    name = list(name.split(' '))
    name = name[0]
    name = re.sub('[^a-zA-Z] +', ' ', name)

    regd = text0[12]
    regd = regd.rstrip()
    regd = regd.lstrip()
    regd = list(regd.split(','))
    regd = regd[0]

    vin = text0[13]
    vin = vin.rstrip()
    vin = vin.lstrip()
    vin = vin.replace("Customer GSTIN ", "")


except:
    pass

data = {}
data['Name'] = name
data['Ph No'] = enino
data['Address Line 1'] = regd
data['Address Line 2'] = vin
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

with io.open('data.json', 'w', encoding='utf-8') as outfile:
    str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))

with open('data.json', encoding='utf-8') as data_file:
    data_loaded = json.load(data_file)

with open('data.json', 'r', encoding='utf-8') as f:
    ndata = json.load(f)


print('\t', "|+++++++++++++++++++++++++++++++|")
print('\t', '|', '\t', ndata['Name'])
print('\t', "|-------------------------------|")
print('\t', '|', '\t', ndata['Ph No'])
print('\t', "|-------------------------------|")
print('\t', '|', '\t', ndata['Address Line 1'])
print('\t', "|-------------------------------|")
print('\t', '|', '\t', ndata['Address Line 2'])
print('\t', "|-------------------------------|")



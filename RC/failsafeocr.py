
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import io
import json
import ftfy

from numpy import unicode

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
'''for god_damn in text:
    if nonsense(god_damn):
        text.remove(god_damn)
    else:
        print(text)'''
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
    xx = wordline.split('\n')
    if ([w for w in xx if re.search(
            '(Certificate|certificate|of|uf|af|regiestration|registration|regiesteration|regis|redgeNO|regd|no|reged)$',
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


try:

    name = text0[0]
    name = name.rstrip()
    name = name.lstrip()
    name = name.replace("8", "B")
    name = name.replace("0", "D")
    name = name.replace("6", "G")
    name = name.replace("1", "I")
    name = re.sub('[^a-zA-Z] +', ' ', name)

    enino = text0[1]
    enino = enino.rstrip()
    enino = enino.lstrip()
    enino = enino.replace("8", "S")
    enino = enino.replace("0", "O")
    enino = enino.replace("6", "G")
    enino = enino.replace("1", "I")
    enino = enino.replace("\"", "A")
    enino = re.sub('[^a-zA-Z] +', ' ', enino)

    regd = text0[2]
    regd = regd.rstrip()
    regd = regd.lstrip()
    regd = regd.replace('l', '/')
    regd = regd.replace('L', '/')
    regd = regd.replace('I', '/')
    regd = regd.replace('i', '/')
    regd = regd.replace('|', '/')
    regd = regd.replace('\"', '/1')
    regd = regd.replace(" ", "")

    vin = text0[3]
    vin = vin.rstrip()
    vin = vin.lstrip()
    vin = vin.replace('l', '/')
    vin = vin.replace('L', '/')
    vin = vin.replace('I', '/')
    vin = vin.replace('i', '/')
    vin = vin.replace('|', '/')
    vin = vin.replace('\"', '/1')
    vin = vin.replace(" ", "")

    mfgd = text0[4]
    mfgd = mfgd.rstrip()
    mfgd = mfgd.lstrip()
    mfgd = mfgd.replace('l', '/')
    mfgd = mfgd.replace('L', '/')
    mfgd = mfgd.replace('I', '/')
    mfgd = mfgd.replace('i', '/')
    mfgd = mfgd.replace('|', '/')
    mfgd = mfgd.replace('\"', '/1')
    mfgd = mfgd.replace(" ", "")


    text0 = findtheword(text1, '(Certificate|certificate|of|uf|af|regiestration|registration|regiesteration|regis|redgeNO|regd|no|reged)$')
    panline = text0[0]
    pan = panline.rstrip()
    pan = pan.lstrip()
    pan = pan.replace(" ", "")
    pan = pan.replace("\"", "")
    pan = pan.replace(";", "")
    pan = pan.replace("%", "L")

except:
    pass

data = {}
data['Name'] = name
data['Engine number'] = enino
data['Registration data'] = regd
data['Vin no'] = vin
data['Manufacture data'] = mfgd

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

with io.open('data.json', 'w', encoding='utf-8') as outfile:
    str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))

with open('data.json', encoding='utf-8') as data_file:
    data_loaded = json.load(data_file)

# print(data == data_loaded)

with open('data.json', 'r', encoding='utf-8') as f:
    ndata = json.load(f)

print('\t', "|+++++++++++++++++++++++++++++++|")
print('\t', '|', '\t', ndata['Name'])
print('\t', "|-------------------------------|")
print('\t', '|', '\t', ndata['Engine number'])
print('\t', "|-------------------------------|")
print('\t', '|', '\t', ndata['Registration data'])
print('\t', "|-------------------------------|")
print('\t', '|', '\t', ndata['Vin no'])
print('\t', "|-------------------------------|")
print('\t', '|', '\t', ndata['Manufacture data'])
print('\t', "|+++++++++++++++++++++++++++++++|")

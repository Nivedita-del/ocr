import os.path
import json
import io
import sys
import string
import pytesseract
import re
import difflib
import csv
import dateutil.parser as dparser
from numpy import unicode

try:
    from PIL import Image, ImageEnhance, ImageFilter
except:
    print("Please Install PIL - For Python 3 Users the Library is now called Pillow")
    sys.exit()
path = sys.argv[1]

img = Image.open(path)
img = img.convert('RGB')
pix = img.load()

for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
            pix[x, y] = (0, 0, 0, 255)
        else:
            pix[x, y] = (255, 255, 255, 255)

img.save('temp.jpg')

text_in = pytesseract.image_to_string(Image.open('temp.jpg'))
text = list(filter(lambda x: ord(x) < 128, text_in))
print(text_in)

text_output = open('outputbase.txt', 'w')
text_output.write(text_in)
text_output.close()

file = open('outputbase.txt', 'r')
text = file.read()
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


lines = text.split('\n')
for lin in lines:
    s = lin.strip()
    s = s.rstrip()
    s = s.lstrip()
    text1.append(s)

# text1 = list(text1)
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
# print(text0)

with open('namedb.csv', 'r') as f:
    reader = csv.reader(f)
    newlist = list(reader)
newlist = sum(newlist, [])


try:
    for x in text0:
        for y in x.split():
            if (difflib.get_close_matches(y.upper(), newlist)):
                nameline.append(x)
                break
except:
    pass

try:
    name = nameline[0]
    enino = eninoline[1]
    regd = redgline[2]
    vin = vinline[3]
    mfgd = mfgdline[4]

except:
    pass

try:
    redgline = [item for item in text0 if item not in nameline]
    for x in redgline:
        z = x.split()
        z = [s for s in z if len(s) > 3]
        for y in z:
            if (dparser.parse(y, fuzzy=True)):
                dob = y
                vinline = redgline[redgline.index(x) + 1:]
                break
except:
    pass

data = {}
data['Name'] = name
data['Engine number'] = enino
data['Registration data'] = regd
data['Vin no'] = vin
data['Manufacture data'] = mfgd

# print(data)


try:
    to_unicode = unicode
except NameError:
    to_unicode = str

with io.open('data.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(data,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))


with open('data.json') as data_file:
    data_loaded = json.load(data_file)

# print(data == data_loaded)


os.remove('temp.jpg')


with open('data.json', 'r') as f:
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


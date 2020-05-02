import requests
import json
import io
import re
import csv
import string
import dateutil.parser as dparser
from numpy import unicode


def ocr_space_file(filename, overlay=False, api_key='cb1023a29e88957', language='eng'):
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    m = r.content.decode()
    jsonstr = json.loads(m)
    print(jsonstr["ParsedResults"][0]["ParsedText"])

    try:
        to_unicode = unicode
    except NameError:
        to_unicode = str


    with io.open('data_ocr_space.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(jsonstr, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))


with open('data_ocr_space.json') as data_file:
    data_loaded = json.load(data_file)

text = data_loaded["ParsedResults"][0]["ParsedText"]
text_output = open('outputbase_1.txt', 'w')
text_output.write(text)
text_output.close()

file = open('outputbase_1.txt', 'r')
text = file.read()
#print(text)


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

text1 = list(filter(None, text1))
#print(text1)

lineno=0

for wordline in text1:
    xx = wordline.split('\n')
    if ([w for w in xx if re.search('(Certificate|certificate|of|uf|af|regiestration|registration|regiesteration|regis|redgeNO|regd|no|reged)$', w)]):
        text1 = list(text1)
        lineno = text1.index(wordline)
        break

#text1 = list(text1)
text0 = text1[lineno+1:]
#print(text0)

try:
    for x in text0:
        for y in x.split():
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

# Making tuples of data
data = {}
data['Name'] = name
data['Engine number'] = enino
data['Registration data'] = regd
data['Vin no'] = vin
data['Manufacture data'] = mfgd
# Writing data into JSON
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

# Write JSON file
with io.open('data_final.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))

# Read JSON file
with open('data_final.json') as data_file:
    data_loaded = json.load(data_file)

#print(data == data_loaded)

# Reading data back JSON(give correct path where JSON is stored)
with open('data_final.json', 'r') as f:
    ndata = json.load(f)

ocr_space_file(filename='temp1.jpg', language='eng')

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

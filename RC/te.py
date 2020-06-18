import re

text=" this is my ,mobile number 9482127568    this is my mobile number 6361626707 this is my ,mobile number 9482127568this is my ,mobile number 9482127568"

ph1 = re.search(r'\b[6][789]\d{9}\b', text, flags=0)
ph2 = re.search(r'\b[7689]\d{9}\b', text, flags=2)
ph3 = re.search(r'\b[8679]\d{9}\b', text, flags=0)
ph4 = re.search(r'\b[9689]\d{9}\b', text, flags=0)

while text != None:
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
        p = ph4.group(3)
    print(p)
    break
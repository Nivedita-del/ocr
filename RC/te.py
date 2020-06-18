import re

text=" this is my ,mobile number 9482127568 this is my mobile number 6361626707 this is my ,mobile number 9482127568 this is my ,mobile number 9482127568 this is 7893079665"

ph1 = re.findall(r'\b[6789]\d{9}\b', text, flags=0)
ph2 = re.search(r'\b[7689]\d{9}\b', text, flags=2)
ph3 = re.search(r'\b[8679]\d{9}\b', text, flags=0)
ph4 = re.search(r'\b[9689]\d{9}\b', text, flags=0)

print(ph1)

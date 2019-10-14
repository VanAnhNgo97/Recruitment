# -*- coding: utf-8 -*-
from utils.utils import flatten_dict, parse_attribute, date_normalize
from setting import *
import json
from lxml import etree
def __load_standard_attributes(standard_attributes_fn):
    with open(standard_attributes_fn, mode='r', encoding='utf8') as f:
        standard_attributes = parse_attribute(json.load(f))
        print(standard_attributes)
        f.close()
__load_standard_attributes(STANDARD_ATTRIBUTES_FN)
print("Van Anh")
job = {"@context":"http:\/\/schema.org\/","@type":"JobPosting","title":"Chuy\u00ean vi\u00ean t\u01b0 v\u1ea5n kh\u00f3a h\u1ecdc cho tr\u1ebb em (Xoay ca, thu nh\u1eadp h\u1ea5p d\u1eabn)","description":"<h2>M\u00f4 t\u1ea3 c\u00f4ng vi\u1ec7c<\/h2>\n<ul><li>Li\u00ean l\u1ea1c kh\u00e1ch h\u00e0ng ti\u1ec1m n\u0103ng v\u00e0 \u0111\u1eb7t l\u1ecbch h\u1eb9n t\u01b0 v\u1ea5n t\u1ea1i Trung t\u00e2m\r\n<\/li><li>\u0110\u1eb7t l\u1ecbch h\u1eb9n gia h\u1ea1n kh\u00f3a h\u1ecdc v\u1edbi ph\u1ee5 huynh hi\u1ec7n t\u1ea1i\r\n<\/li><li>Ch\u0103m s\u00f3c h\u1ecdc vi\u00ean hi\u1ec7n t\u1ea1i\r\n<\/li><li>Tham gia v\u00e0o c\u00e1c ho\u1ea1t \u0111\u1ed9ng t\u1ea1i Trung t\u00e2m<\/li><\/ul>\n<h2>Y\u00eau c\u1ea7u \u1ee9ng vi\u00ean<\/h2>\n<ul><li>T\u1ef1 tin giao ti\u1ebfp, tr\u00ecnh b\u00e0y qua \u0111i\u1ec7n tho\u1ea1i v\u00e0 tr\u1ef1c ti\u1ebfp\r\n<\/li><li>C\u00f3 tinh th\u1ea7n l\u00e0m vi\u1ec7c tho\u1ea3i m\u00e1i d\u01b0\u1edbi \u00e1p l\u1ef1c \u0111\u1ec3 \u0111\u1ea1t \u0111\u01b0\u1ee3c nh\u1eefng m\u1ee5c ti\u00eau \u0111\u1ec1 ra\r\n<\/li><li>\u0110\u00e1ng tin c\u1eady, c\u00f3 k\u1ef7 lu\u1eadt v\u00e0 c\u00f3 t\u1ed5 ch\u1ee9c, c\u00f3 k\u1ef9 n\u0103ng qu\u1ea3n l\u00fd th\u1eddi gian hi\u1ec7u qu\u1ea3\r\n<\/li><li>N\u0103ng \u0111\u1ed9ng, t\u00edch c\u1ef1c, nhi\u1ec7t t\u00ecnh v\u00e0 nhi\u1ec1u n\u0103ng l\u01b0\u1ee3ng\r\n<\/li><li>Y\u00eau th\u00edch tr\u1ebb em v\u00e0 s\u1eb5n s\u00e0ng ch\u0103m s\u00f3c b\u00e9.<\/li><li>C\u00f3 kh\u1ea3 n\u0103ng l\u00e0m vi\u1ec7c theo ca, bu\u1ed5i t\u1ed1i v\u00e0 cu\u1ed1i tu\u1ea7n (Ngh\u1ec9 c\u1ed1 \u0111\u1ecbnh th\u1ee9 hai v\u00e0 0,5 ng\u00e0y \u0111\u01b0\u1ee3c s\u1eafp x\u1ebfp trong tu\u1ea7n linh \u0111\u1ed9ng)\r\n<\/li><li>\u0110\u1ecba \u0111i\u1ec3m l\u00e0m vi\u1ec7c \u0111\u01b0\u1ee3c s\u1eafp x\u1ebfp theo nhu c\u1ea7u nh\u00e2n s\u1ef1 t\u1ea1i c\u00e1c Trung t\u00e2m (Q. 7, Q. 5, Ph\u00fa Nhu\u1eadn, B\u00ecnh Th\u1ea1nh, B\u00ecnh T\u00e2n, ...)<\/li><\/ul>\n<h2>Quy\u1ec1n l\u1ee3i \u0111\u01b0\u1ee3c h\u01b0\u1edfng<\/h2>\n<ul><li>T\u1ed5ng thu nh\u1eadp h\u00e0ng th\u00e1ng h\u1ea5p d\u1eabn (bao g\u1ed3m l\u01b0\u01a1ng c\u1ed1 \u0111\u1ecbnh, th\u01b0\u1edfng v\u00e0 hoa h\u1ed3ng theo c\u1ea5p b\u1eadc)\r\n<\/li><li>\u0110\u01b0\u1ee3c tham gia c\u00e1c kh\u00f3a \u0111\u00e0o t\u1ea1o k\u1ef9 n\u0103ng, ki\u1ebfn th\u1ee9c s\u1ea3n ph\u1ea9m \u0111\u1ea7u v\u00e0o v\u00e0 c\u00e1c ch\u01b0\u01a1ng tr\u00ecnh \u0111\u00e0o t\u1ea1o ph\u00e1t tri\u1ec3n k\u1ef9 n\u0103ng trong su\u1ed1t qu\u00e1 tr\u00ecnh l\u00e0m vi\u1ec7c.\r\n<\/li><li>C\u00f3 c\u01a1 h\u1ed9i ti\u1ebfp x\u00fac v\u00e0 th\u1ef1c h\u00e0nh giao ti\u1ebfp ti\u1ebfng Anh v\u1edbi gi\u00e1o vi\u00ean b\u1ea3n x\u1ee9\r\n<\/li><li>L\u01b0\u01a1ng th\u00e1ng 13\r\n<\/li><li>12 ng\u00e0y ph\u00e9p\/n\u0103m\r\n<\/li><li>B\u1ea3o hi\u1ec3m x\u00e3 h\u1ed9i b\u1eaft bu\u1ed9c\r\n<\/li><li>B\u1ea3o hi\u1ec3m tai n\u1ea1n\r\n<\/li><li>C\u00e1c ch\u01b0\u01a1ng tr\u00ecnh, ho\u1ea1t \u0111\u1ed9ng g\u1eafn k\u1ebft nh\u00e2n vi\u00ean\r\n<\/li><li>Ti\u1ec7c h\u00e0ng n\u0103m, team building.\r\n<\/li><li>Qu\u00e0 t\u1eb7ng sinh nh\u1eadt\r\n<\/li><li>Quy\u1ec1n l\u1ee3i cho con h\u1ecdc t\u1ea1i I Can Read<\/li><\/ul>","identifier":{"@type":"PropertyValue","name":"I Can Read","value":17698},"datePosted":"2019-10-09","validThrough":"2019-11-30T23:59:59+07:00","employmentType":"FULL_TIME","hiringOrganization":{"@type":"Organization","name":"I Can Read","sameAs":"https:\/\/www.topcv.vn\/cong-ty\/i-can-read\/17698.html","logo":"https:\/\/static.topcv.vn\/company_logos\/i-can-read-5d1c7587834f5.jpg"},"jobLocation":[{"@type":"Place","address":{"@type":"PostalAddress","streetAddress":"TP. HCM","addressLocality":"TP. HCM","addressRegion":"H\u1ed3 Ch\u00ed Minh","postalCode":700000,"addressCountry":"Vi\u1ec7t Nam"}}],"baseSalary":{"@type":"MonetaryAmount","currency":"VND","value":{"@type":"QuantitativeValue","unitText":"MONTH","value":"7-20 tri\u1ec7u","minValue":"7 tri\u1ec7u","maxValue":"20 tri\u1ec7u"}},"skills":"D\u1ecbch v\u1ee5 kh\u00e1ch h\u00e0ng, Kinh doanh \/ B\u00e1n h\u00e0ng, T\u01b0 v\u1ea5n, L\u1eadp k\u1ebf ho\u1ea1ch, K\u1ef9 n\u0103ng giao ti\u1ebfp, Qu\u1ea3n l\u00fd th\u1eddi gian, K\u1ef9 n\u0103ng Thuy\u1ebft ph\u1ee5c, Ti\u1ebfng Anh giao ti\u1ebfp, T\u01b0 v\u1ea5n"}
#print(job)
inital_description = job['description']
if "Yêu cầu ứng viên" in inital_description:
	print("True")
else:
	print("False")

description_dom = etree.HTML(inital_description)
requirement = description_dom.xpath("//h2/text()[contains(.,'Yêu cầu ứng viên')]")
#requirement = description_dom.xpath("//ul//text()")
#dung voi trinh duyet
#requirement = description_dom.xpath("//ul[preceding-sibling::h2/text()[contains(.,'Yêu cầu ứng viên')]][1]")

#requirement = description_dom.xpath("//*[contains(text(),'Yêu cầu ứng viên')]/following-sibling::*[1]")
print(requirement)
#test
content = '''\
<record>
    <nd>First</nd>
    <nd>Second</nd>
    <nd ref="203936110"></nd>
    <nd>Third</nd>
    <nd>Fourth</nd>
    <h2>Yêu cầu công việc</h2>
    <ul
    	<li>ABC</li>
    	<li>BCD</li>
	</ul>
	<h2>Quyền lợi được hưởng</h2>
	<ul>
		<li>A1</li>
		<li>A2</li>
	</ul>   
</record>'''

root = etree.HTML(content)

for elt in root.xpath('''
    //nd[@ref="203936110"]/following-sibling::nd[1]
    |
    //nd[@ref="203936110"]/preceding-sibling::nd[1]'''):
	#print(elt)
    print(elt.text)

for elt in root.xpath("//*[contains(text(),'Yêu cầu công việc')]/following-sibling::*[1]"):
	print(elt[0].text)

text = """                       
<html>
  <head>
    <title>This tag includes 'some_text'</title>
    <h2>A h2 tag</h2>
    <h2>Yêu cầu công việc</h2>
    <ul>
    	<li>ABC</li>
    	<li>BCD</li>
	</ul>
	<h2>Quyền lợi được hưởng</h2>
	<ul>
		<li>A1</li>
		<li>A2</li>
	</ul>   
  </head>
</html>
"""
doc = etree.fromstring(text)
req = doc.xpath("//*[contains(text(),'Yêu cầu')]/following-sibling::*[1]")#//text() ok
#chuyen ve string
for element in req:
	print(etree.tostring(element,method='html'))
'''
fin = []
for str(content) in req:
	if content.strip() != '':
		fin.append(content.strip())
'''
print(req)

print(type(req))
#req_str = "\n".join(req)
#print(req_str)
#req_json = json.loads(req.text, strict=False)
'''
min_max_attributes = {}
min_max_attributes["baseSalary_value_minValue"] = "7 trieu"
min_max_attributes["baseSalary_value_maxValue"] = "10 trieu"
items = list(min_max_attributes.items())
print(items)

v0 = int(re.search(r'\d+', str(items[0][1])).group(0))
print(v0)
v1 = int(re.search(r'\d+', str(items[1][1])).group(0))
'''
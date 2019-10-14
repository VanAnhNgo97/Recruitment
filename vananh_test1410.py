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
test = "Vân Anh"
print(test)
encode_test = test.encode("utf-8")
print(encode_test)
decode_test = encode_test.decode("utf-8")
print(decode_test)
#chay ok
'''
inital_description = job['description']
lower_init_description = inital_description.lower()
print(inital_description)
description_dom = etree.HTML(inital_description)
print("ok")
std_description_str = ""
if "jobBenefits" not in job:
    benefits = description_dom.xpath("//*[contains(text(),'Quyền lợi')]/following-sibling::*[1]")
    #print(benefits)
    #print("------benefits-------")
    #print(len(benefits))
    jobBenefits = etree.tostring(benefits[0],method='html',encoding="unicode")
    #print(jobBenefits)
    job["jobBenefits"] = jobBenefits
    std_description = description_dom.xpath("//*[contains(text(),'Mô tả')]/following-sibling::*[1]")
    std_description_str = etree.tostring(std_description[0],method='html',encoding="unicode")
if "experienceRequirements" not in job:
    requirements = description_dom.xpath("//*[contains(text(),'Yêu cầu')]/following-sibling::*[1]")
    experienceRequirements = etree.tostring(requirements[0],method='html',encoding="unicode")
    job["experienceRequirements"] = experienceRequirements 
#
if std_description_str.strip() != "":
    job["description"] = std_description_str
print("*******************")
print(job)
print("\n\n")
print("**************")
'''
anphabe = """{"@context":"https:\/\/schema.org","@type":"JobPosting","title":"Nh\u00e2n Vi\u00ean L\u01b0u Tr\u1eef (l\u00e0m vi\u1ec7c t\u1ea1i B\u00ecnh \u0110\u1ecbnh)","description":"\n        \u003Cp\u003E\u003C\/p\u003E\n        \u003Cp\u003E\u003Cstrong\u003EJob Description\u003C\/strong\u003E\u003C\/p\u003E\n        \u003Cdiv\u003E\u003Cul\u003E\u003Cli\u003ETi\u1ebfp nh\u1eadn, ph\u00e2n lo\u1ea1i, l\u1eadp danh m\u1ee5c v\u00e0 l\u01b0u tr\u1eef h\u1ed3 s\u01a1 t\u1eadp trung t\u1ea1i kho l\u01b0u tr\u1eef c\u1ee7a C\u00f4ng ty.\u003C\/li\u003E\u003Cli\u003EScan h\u1ed3 s\u01a1, nh\u1eadp li\u1ec7u v\u00e0o ph\u1ea7n m\u1ec1m\/ ch\u01b0\u01a1ng tr\u00ecnh l\u01b0u tr\u1eef theo quy \u0111\u1ecbnh C\u00f4ng ty.\u003C\/li\u003E\u003Cli\u003E\u0110\u1ec1 ngh\u1ecb c\u00e1c Ph\u00f2ng ban\/\u0110\u01a1n v\u1ecb li\u00ean quan b\u00e0n giao h\u1ed3 s\u01a1 theo \u0111\u1ecbnh k\u1ef3\/ ph\u00e1t sinh theo y\u00eau\u00a0c\u1ea7u c\u00f4ng vi\u1ec7c ho\u1eb7c theo ch\u1ec9 \u0111\u1ea1o c\u1ea5p tr\u00ean.\u003C\/li\u003E\u003Cli\u003ETh\u1ef1c hi\u1ec7n c\u00f4ng t\u00e1c truy xu\u1ea5t h\u1ed3 s\u01a1 l\u01b0u tr\u1eef theo y\u00eau c\u1ea7u c\u1ee7a c\u1ea5p tr\u00ean.\u003C\/li\u003E\u003Cli\u003ETheo d\u00f5i, qu\u1ea3n l\u00fd vi\u1ec7c xu\u1ea5t m\u01b0\u1ee3n v\u00e0 thu h\u1ed3i h\u1ed3 s\u01a1 m\u01b0\u1ee3n theo quy tr\u00ecnh \u0111\u01b0\u1ee3c duy\u1ec7t.\u003C\/li\u003E\u003Cli\u003EB\u00e1o c\u00e1o t\u1ed5ng h\u1ee3p li\u00ean quan \u0111\u1ebfn l\u01b0u tr\u1eef h\u1ed3 s\u01a1.\u003C\/li\u003E\u003Cli\u003EC\u00e1c c\u00f4ng vi\u1ec7c c\u1ee5 th\u1ec3 kh\u00e1c s\u1ebd trao \u0111\u1ed5i khi ph\u1ecfng v\u1ea5n\u003C\/li\u003E\u003C\/ul\u003E\u003Cp\u003E\u003Cb\u003EL\u01b0\u01a1ng va\u0300 ca\u0301c khoa\u0309n phu\u0301c l\u01a1\u0323i:\u003C\/b\u003E\u003C\/p\u003E\n\n\u003Cul\u003E\u003Cli\u003EL\u01b0\u01a1ng\u00a0 - Th\u01b0\u01a1\u0309ng cao, nhi\u00ea\u0300u c\u01a1 h\u00f4\u0323i th\u0103ng ti\u1ebfn, m\u00f4i tr\u01b0\u01a1\u0300ng la\u0300m vi\u00ea\u0323c chuy\u00ean nghi\u00ea\u0323p.\u003C\/li\u003E\u003Cli\u003EH\u01b0\u01a1\u0309ng ch\u00ednh s\u00e1ch chi\u1ebft kh\u1ea5u \u01b0u \u0111\u00e3i d\u00e0nh cho CBNV khi mua c\u0103n h\u1ed9 - thu\u1ed9c c\u00e1c do\u0300ng sa\u0309n ph\u00e2\u0309m c\u1ee7a C\u00f4ng ty.\u003C\/li\u003E\u003Cli\u003EH\u01b0\u01a1\u0309ng chi\u0301nh sa\u0301ch h\u00f4\u0303 tr\u01a1\u0323 \u0111\u00f4\u0301i v\u01a1\u0301i CBNV co\u0301 hoa\u0300n ca\u0309nh kho\u0301 kh\u0103n.\u003C\/li\u003E\u003Cli\u003EKha\u0301m s\u01b0\u0301c kho\u0309e \u0111i\u0323nh ky\u0300, \u0111i du l\u1ecbch va\u0300 c\u1ea5p ph\u00e1t \u0111\u1ed3ng ph\u1ee5c h\u0103\u0300ng n\u0103m.\u003C\/li\u003E\u003Cli\u003EMua ba\u0309o hi\u00ea\u0309m s\u01b0\u0301c kho\u0309e, ba\u0309o hi\u00ea\u0309m tai na\u0323n con ng\u01b0\u01a1\u0300i (24\/24).\u003C\/li\u003E\u003Cli\u003ETham gia BHXH, BHYT, BHTN theo \u0111u\u0301ng quy \u0111\u1ecbnh c\u1ee7a ph\u00e1p lu\u1eadt.\u003C\/li\u003E\u003C\/ul\u003E\u003C\/div\u003E\n        \u003Cp\u003E\u003C\/p\u003E\n        \u003Cp\u003E\u003Cstrong\u003EJob Requirement\u003C\/strong\u003E\u003C\/p\u003E\n        \u003Cdiv\u003E\u003Cul\u003E\u003Cli\u003ENam\/ N\u1eef, t\u1eeb 24 - 30 tu\u1ed5i. \u003C\/li\u003E\u003Cli\u003ET\u1ed1t nghi\u1ec7p Trung c\u1ea5p tr\u1edf l\u00ean chuy\u00ean ng\u00e0nh v\u0103n th\u01b0 - l\u01b0u tr\u1eef\u00a0ho\u1eb7c c\u00e1c ng\u00e0nh ngh\u1ec1 li\u00ean quan. \u003C\/li\u003E\u003Cli\u003ET\u1ed1i thi\u1ec3u 04 n\u0103m kinh nghi\u1ec7m l\u00e0m c\u00f4ng t\u00e1c l\u01b0u tr\u1eef t\u1ea1i\u00a0c\u00e1c C\u00f4ng ty b\u1ea5t \u0111\u1ed9ng s\u1ea3n\/x\u00e2y d\u1ef1ng. \u01afu ti\u00ean \u1ee9ng vi\u00ean \u0111\u00e3 t\u1eebng s\u1eed d\u1ee5ng c\u00e1c ph\u1ea7n m\u1ec1m v\u1ec1\u00a0l\u01b0u tr\u1eef.\u003C\/li\u003E\u003Cli\u003ETh\u00e0nh th\u1ea1o tin h\u1ecdc v\u0103n ph\u00f2ng, c\u00e1c ph\u1ea7n m\u1ec1m l\u01b0u tr\u1eef li\u00ean quan.\u003C\/li\u003E\u003Cli\u003EC\u1ea9n th\u1eadn, t\u1ec9 m\u1ec9, b\u1ea3o m\u1eadt th\u00f4ng tin.\u003C\/li\u003E\u003C\/ul\u003E\u003C\/div\u003E\n        \u003Cp\u003E\u003C\/p\u003E\n        \u003Cp\u003E\u003Cstrong\u003EAdditional Information\u003C\/strong\u003E\u003C\/p\u003E\n        \u003Cul\u003E\n            \u003Cli\u003E\u003Cstrong\u003EJob Level:\u003C\/strong\u003E Experienced (Non-manager)\u003C\/li\u003E\n            \u003Cli\u003E\u003Cstrong\u003ESalary:\u003C\/strong\u003E Competitive\u003C\/li\u003E\n            \u003Cli\u003E\u003Cstrong\u003EJob Function:\u003C\/strong\u003E Admin\/Clerical\/Translator\u003C\/li\u003E\n            \u003Cli\u003E\u003Cstrong\u003EIndustry:\u003C\/strong\u003E Civil\/Construction\/Materials, Real Estate\u003C\/li\u003E\n            \u003Cli\u003E\u003Cstrong\u003ELocation:\u003C\/strong\u003E Binh Dinh\u003C\/li\u003E\n            \u003Cli\u003E\u003Cstrong\u003EJob type:\u003C\/strong\u003E Full-Time Permanent\u003C\/li\u003E\n            \u003Cli\u003E\u003Cstrong\u003EPosted:\u003C\/strong\u003E 07 Oct 2019\u003C\/li\u003E            \n        \u003C\/ul\u003E\n        \u003Cp\u003E\u003C\/p\u003E\n        \u003Cp\u003E\u003Cstrong\u003EAbout Hung Thinh Corporation\u003C\/strong\u003E\u003C\/p\u003E\n        \u003Cdiv\u003E\u003Cp style=\u0022text-align:justify;\u0022\u003EH\u01a1n 16 n\u0103m qua, H\u01b0ng Th\u1ecbnh  \u0111\u00e3 ph\u00e1t tri\u1ec3n m\u1ea1nh m\u1ebd v\u1edbi 29 c\u00f4ng ty th\u00e0nh vi\u00ean, 03 v\u0103n ph\u00f2ng \u0111\u1ea1i di\u1ec7n c\u00f9ng h\u1ec7  th\u1ed1ng 08 S\u00e0n giao d\u1ecbch quy m\u00f4 l\u1edbn v\u00e0 \u0111\u1ed9i ng\u0169 h\u01a1n  2.300 nh\u00e2n s\u1ef1 nhi\u1ec7t huy\u1ebft. S\u1edf h\u1eefu ti\u1ec1m l\u1ef1c v\u1eefng ch\u1eafc, H\u01b0ng Th\u1ecbnh \u0111\u00e3 \u0111\u1ea7u  t\u01b0, ph\u00e1t tri\u1ec3n h\u01a1n 50 d\u1ef1 \u00e1n tr\u00ean kh\u1eafp c\u00e1c t\u1ec9nh  th\u00e0nh nh\u01b0 B\u00ecnh \u0110\u1ecbnh, Kh\u00e1nh H\u00f2a, L\u00e2m \u0110\u1ed3ng, B\u00ecnh Thu\u1eadn, B\u00e0 R\u1ecba \u2013 V\u0169ng T\u00e0u, \u0110\u1ed3ng  Nai v\u00e0 TP.HCM. H\u01b0ng Th\u1ecbnh c\u00f2n t\u1ea1o d\u1ea5u \u1ea5n quan tr\u1ecdng v\u00e0 th\u00e0nh c\u00f4ng v\u01b0\u1ee3t tr\u1ed9i v\u1edbi  c\u00e1c th\u01b0\u01a1ng v\u1ee5 M\u0026amp;A v\u00e0 h\u1ee3p t\u00e1c ph\u00e1t tri\u1ec3n n\u1ed5i b\u1eadt tr\u00ean th\u1ecb tr\u01b0\u1eddng.\u003C\/p\u003E\n\u003Cp style=\u0022text-align:justify;\u0022\u003ESong song c\u00f9ng ho\u1ea1t \u0111\u1ed9ng  kinh doanh, T\u1eadp \u0111o\u00e0n lu\u00f4n \u01b0u ti\u00ean th\u1ef1c hi\u1ec7n c\u00e1c ch\u01b0\u01a1ng tr\u00ecnh t\u1eeb thi\u1ec7n c\u0169ng nh\u01b0  c\u00e1c ho\u1ea1t \u0111\u1ed9ng thi\u1ebft th\u1ef1c d\u00e0nh cho x\u00e3 h\u1ed9i \u2013 c\u1ed9ng \u0111\u1ed3ng. \u0110\u00e2y l\u00e0 n\u00e9t v\u0103n h\u00f3a \u0111\u1eadm ch\u1ea5t  nh\u00e2n v\u0103n b\u1eaft ngu\u1ed3n t\u1eeb tri\u1ebft l\u00fd kinh doanh \u201cV\u00ec m\u1ed9t c\u1ed9ng \u0111\u1ed3ng H\u01b0ng Th\u1ecbnh\u201d m\u00e0  ch\u00fang t\u00f4i lu\u00f4n theo \u0111u\u1ed5i. Ch\u1ec9 t\u00ednh t\u1eeb n\u0103m 2016 \u0111\u1ebfn  nay, T\u1eadp \u0111o\u00e0n \u0111\u00e3 d\u00e0nh h\u01a1n 35 t\u1ef7 \u0111\u1ed3ng cho c\u00e1c ho\u1ea1t \u0111\u1ed9ng thi\u1ec7n nguy\u1ec7n.\u003C\/p\u003E\n\u003Cp style=\u0022text-align:justify;\u0022\u003EV\u1edbi nh\u1eefng \u0111\u00f3ng g\u00f3p t\u00edch c\u1ef1c  cho n\u1ec1n kinh t\u1ebf v\u00e0 c\u1ed9ng \u0111\u1ed3ng, H\u01b0ng Th\u1ecbnh \u0111\u00e3 vinh d\u1ef1 \u0111\u00f3n nh\u1eadn nhi\u1ec1u gi\u1ea3i th\u01b0\u1edfng trong n\u01b0\u1edbc v\u00e0 qu\u1ed1c t\u1ebf th\u1ec3 hi\u1ec7n s\u1ef1 ghi nh\u1eadn c\u1ee7a x\u00e3 h\u1ed9i  v\u00e0 c\u00e1c t\u1ed5 ch\u1ee9c uy t\u00edn.\u003C\/p\u003E\u003C\/div\u003E\n        \u003Cp\u003E\u003C\/p\u003E\n        \u003Cp\u003EView more jobs at \u003Ca href=\u0027https:\/\/www.anphabe.com\/big-jobs\u0027 target=\u0027_blank\u0027 title=\u0027https:\/\/www.anphabe.com\/big-jobs\u0027\u003Ehttps:\/\/www.anphabe.com\/big-jobs\u003C\/a\u003E \u003C\/p\u003E\n        \n        ","occupationalCategory":"Experienced (Non-manager)","industry":"Civil\/Construction\/Materials, Real Estate","employmentType":"Full-Time Permanent","datePosted":"2019-10-07","validThrough":"2019-11-06","baseSalary":{"@type":"MonetaryAmount","currency":"USD","value":{"@type":"QuantitativeValue","minValue":500,"maxValue":600,"unitText":"MONTH"}},"hiringOrganization":{"@type":"Organization","name":"Hung Thinh Corporation","logo":"https:\/\/www.anphabe.com\/file-deliver.php?key=hcWDxaBjm7TXnZedhtmlrtKWiG3ZcGmgWteYmaTLlGVkZFtwq3Nln1KXmcdacZtvaGSXaG-Wa6qeaWdqhMnJx8XZztjFpsKl2ciEntegY2agU9anyKKZyXKTZKank56hlJueY5-imIdrrg.."},"jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","streetAddress":"Binh Dinh","addressLocality":"Binh Dinh","addressRegion":"Binh Dinh","addressCountry":{"@type":"Country","name":"Vietnam"},"postalCode":"700000"}},"identifier":{"@type":"PropertyValue","name":"Hung Thinh Corporation","value":227274}}"""
print(anphabe)
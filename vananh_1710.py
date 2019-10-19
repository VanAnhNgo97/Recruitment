# -*- coding: utf-8 -*-
import os
import json
import uuid
import codecs
import pandas as pd
import re
#vananh
from datetime import datetime
#from datetime import timedelta
from dateutil.relativedelta import relativedelta


job = """
{"@context":"http:\/\/schema.org\/","@type":"JobPosting","title":"K\u0129 thu\u1eadt vi\u00ean S\u01a1n, G\u00f2 (8 tri\u1ec7u - 10 tri\u1ec7u)","description":"<h2>M\u00f4 t\u1ea3 c\u00f4ng vi\u1ec7c<\/h2>\n<p>Th\u1ef1c hi\u1ec7n s\u1eefa ch\u1eefa, b\u1ea3o d\u01b0\u1ee1ng xe kh\u00e1ch h\u00e0ng theo ph\u00e2n c\u00f4ng c\u00f4ng vi\u1ec7c c\u1ee7a \u0110\u1ed1c c\u00f4ng\/t\u1ed5 tr\u01b0\u1edfng, th\u1ef1c hi\u1ec7n c\u00f4ng vi\u1ec7c m\u1ed9t c\u00e1ch chuy\u00ean nghi\u1ec7p theo quy tr\u00ecnh d\u1ecbch v\u1ee5 c\u1ee7a MMV.<\/p>\n<h2>Y\u00eau c\u1ea7u \u1ee9ng vi\u00ean<\/h2>\n<p>- T\u1ed1t nghi\u1ec7p Trung c\u1ea5p&nbsp;<\/p><p>- Tr\u00ean 3  n\u0103m kinh nghi\u1ec7m l\u00e0m vi\u1ec7c trong l\u0129nh v\u1ef1c li\u00ean quan&nbsp;<\/p><p>- K\u1ef9 thu\u1eadt S\u01a1n.\r\n<\/p><p>- Ho\u1eb7c K\u1ef9 thu\u1eadt G\u00f2 h\u00e0n c\u01a1 kh\u00ed.<\/p><p>- Hi\u1ec3u bi\u1ebft c\u01a1 b\u1ea3n v\u1ec1 Th\u01b0\u01a1ng  hi\u1ec7u Mitsubishi Motors v\u1ec1 Gami, C\u00f4ng ty\r\n<\/p><p>- Hi\u1ec3u bi\u1ebft c\u01a1 b\u1ea3n v\u1ec1 c\u00e1c s\u1ea3n ph\u1ea9m v\u00e0 d\u1ecbch v\u1ee5 m\u00e0 C\u00f4ng ty \u0111ang cung c\u1ea5p\r\n<\/p><p>- C\u00f3 kh\u1ea3 n\u0103ng l\u00e0m vi\u1ec7c \u0111\u1ed9c l\u1eadp c\u0169ng nh\u01b0 theo nh\u00f3m , ch\u1ecbu \u00e1p l\u1ef1c cao&nbsp;<br><\/p><p>- Y\u00eau c\u1ea7u:\r\n<\/p><p>+ S\u1ee9c kh\u1ecfe t\u1ed1t\r\n<\/p><p>+ Cam k\u1ebft g\u1eafn b\u00f3 l\u00e2u d\u00e0i v\u1edbi C\u00f4ng ty \t\r\n<\/p>\n<h2>Quy\u1ec1n l\u1ee3i \u0111\u01b0\u1ee3c h\u01b0\u1edfng<\/h2>\n<p>- M\u1ee9c l\u01b0\u01a1ng: 8 tri\u1ec7u - 10 tri\u1ec7u<\/p><p>- M\u00f4i tr\u01b0\u1eddng \u0111i\u1ec1u ki\u1ec7n l\u00e0m vi\u1ec7c hi\u1ec7n \u0111\u1ea1i, chuy\u00ean nghi\u1ec7p, n\u0103ng \u0111\u1ed9ng, th\u00e2n thi\u1ec7n.<\/p><p>- Thu nh\u1eadp, \u0111\u00e3i ng\u1ed9 t\u1ed1t.<\/p><p>- \u0110\u01b0\u1ee3c t\u1ea1o \u0111i\u1ec1u ki\u1ec7n t\u1ed1t \u0111\u1ec3 nh\u00e2n vi\u00ean ph\u00e1t huy h\u1ebft n\u0103ng l\u1ef1c.<\/p><p>- Th\u01b0\u1edfng v\u00e0o c\u00e1c d\u1ecbp \u0111\u1eb7c bi\u1ec7t: Ng\u00e0y l\u1ec5, t\u1ebft\u2026<\/p><p>- C\u00f3 c\u01a1 h\u1ed9i th\u0103ng ti\u1ebfn.\u00a0<\/p><p>- BHYT, BHXH, ngh\u1ec9 m\u00e1t h\u00e0ng n\u0103m\u2026.<\/p><p>- \u0110\u01b0\u1ee3c ngh\u1ec9 ( CN ), ngh\u1ec9 ph\u00e9p, th\u01b0\u1edfng l\u1ec5, t\u1ebft theo quy \u0111\u1ecbnh c\u1ee7a C\u00f4ng ty.<\/p><p>- C\u00e1c quy\u1ec1n l\u1ee3i kh\u00e1c theo quy \u0111\u1ecbnh c\u1ee7a lu\u1eadt lao \u0111\u1ed9ng<\/p>","identifier":{"@type":"PropertyValue","name":"C\u00f4ng ty C\u1ed5 ph\u1ea7n \u0110\u1ea7u t\u01b0 th\u01b0\u01a1ng m\u1ea1i An D\u00e2n","value":27390},"datePosted":"2019-10-15","validThrough":"2019-11-14T23:59:59+07:00","employmentType":"FULL_TIME","hiringOrganization":{"@type":"Organization","name":"C\u00f4ng ty C\u1ed5 ph\u1ea7n \u0110\u1ea7u t\u01b0 th\u01b0\u01a1ng m\u1ea1i An D\u00e2n","sameAs":"https:\/\/www.topcv.vn\/cong-ty\/cong-ty-co-phan-dau-tu-thuong-mai-an-dan\/27390.html","logo":"https:\/\/static.topcv.vn\/company_logos\/cong-ty-co-phan-dau-tu-thuong-mai-an-dan-61657902f2cec4bae52c1579a1f9213e-5d9c48fa32277.jpg"},"jobLocation":[{"@type":"Place","address":{"@type":"PostalAddress","streetAddress":"CS1: S\u1ed1 1 Nguy\u1ec5n V\u0103n Linh, Gia Th\u1ee5y, Long Bi\u00ean, H\u00e0 N\u1ed9i; CS2: V\u0129nh Ph\u00fac","addressLocality":"CS1: S\u1ed1 1 Nguy\u1ec5n V\u0103n Linh, Gia Th\u1ee5y, Long Bi\u00ean, H\u00e0 N\u1ed9i; CS2: V\u0129nh Ph\u00fac","addressRegion":"H\u00e0 N\u1ed9i","postalCode":100000,"addressCountry":"Vi\u1ec7t Nam"}},{"@type":"Place","address":{"@type":"PostalAddress","streetAddress":"CS1: S\u1ed1 1 Nguy\u1ec5n V\u0103n Linh, Gia Th\u1ee5y, Long Bi\u00ean, H\u00e0 N\u1ed9i; CS2: V\u0129nh Ph\u00fac","addressLocality":"CS1: S\u1ed1 1 Nguy\u1ec5n V\u0103n Linh, Gia Th\u1ee5y, Long Bi\u00ean, H\u00e0 N\u1ed9i; CS2: V\u0129nh Ph\u00fac","addressRegion":"V\u0129nh Ph\u00fac","postalCode":280000,"addressCountry":"Vi\u1ec7t Nam"}}],"baseSalary":{"@type":"MonetaryAmount","currency":"VND","value":{"@type":"QuantitativeValue","unitText":"MONTH","value":"8-10 tri\u1ec7u","minValue":"8 tri\u1ec7u","maxValue":"10 tri\u1ec7u"}},"skills":"B\u1ea3o tr\u00ec \/ S\u1eefa ch\u1eefa"}
"""
print(job)
def load_dict(dict_file_name):
    if dict_file_name is not None:
        with open(dict_file_name, encoding='utf-8-sig', mode='r') as f:
            d = json.load(f)
            f.close()
        return d
    return None
#18.10
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ini_career_dict = load_dict(os.path.join(DIR_PATH, 'utils/dict/career.json'))
#ini_career_dict = load_dict("career")
career_dict = {}
career_dict_detail = {}
career_list = []
i = 1
for k,v in ini_career_dict.items():
	if v not in career_list:
		career_list.append(v)
		career_dict_detail[v] = i
		i = i + 1
	career_id = career_dict_detail[v]
	career_dict[k] = career_id
#print(career_dict)
'''
#chay ok
with open('career_code.json', mode='w', encoding='utf-8') as f:
    json.dump(career_dict, f,ensure_ascii=False,indent=4, separators=(',', ': '))
    f.close()
'''
'''
#chay ok
with open('career_detail.json', mode='w', encoding='utf-8') as f:
    json.dump(career_dict_detail, f, ensure_ascii=False)
    f.close()
'''
#vananh
def normalize_date(date):
    year_month_date = re.split(r'\/-', date[:10])
    date_str = ""
    if len(year_month_date[0]) == 2:
        date_str =  '-'.join(year_month_date[::-1])
    else:
        date_str = '-'.join(year_month_date)
    day = pd.to_datetime(date_str)
    return day

#vananh
def normalize_date_range(from_date, to_date):
    suitable_date = from_date + relativedelta(months=3)
    print("max date:",suitable_date)
    if suitable_date >= to_date:
        return to_date
    else:
        return suitable_date

datePosted = normalize_date("24-08-2019")
#print("datePosted",datePosted)
validThrough = normalize_date("2019-11-11")
#print("iniValidThrough", validThrough)
validThrough = normalize_date_range(datePosted,validThrough)
#print("finalValidThrough",validThrough)


class Test:
    #attr
    def __init__(self):
        self.attr = 1

    def test_dict(self,job):
        dict_a = {}
        dict_a["Key1"] = "A"
        dict_a["Key2"] = "B"
        return dict_a

    def test_dict2(self,job):
        dict_b = {}
        dict_b["Key3"] = "C"
        dict_b["Key4"] = "D"

    def test_dict3(self):
        job = {}
        job["name"] = "VA"
        job["age"] = 22
        a = self.test_dict(job)
        b = {**self.test_dict2(job), **a}
        print("dict b")
        for k,v in a.items():
            print(k,"----",v)

#x = Test().test_dict3()





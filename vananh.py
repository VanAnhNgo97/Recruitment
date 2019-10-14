import pymongo
from setting import *
import datetime
import pandas as pd
from pyvi import ViTokenizer
import re
def get_filter_data(job):
    title = job['title']
    hiring_organization_name = job['hiringOrganization']['name']
    if type(job['jobLocation']) is list:
        address_region = ','.join([location['address']['addressRegion'] for location in job['jobLocation']])
    else:
        address_region = job['jobLocation']['address']['addressRegion']

    return [title, hiring_organization_name, address_region]

def __is_date(attribute_value):
    return re.match(
        r"^(\d{4}-\d{2}-\d{2} {0,1}((\d{2}:\d{2}:\d{2})|T\d{2}:\d{2}(:\d{2})?(\+\d{2}:\d{2}))?)|(\d{2}\/\d{2}\/\d{4})|(\d{4}\/\d{2}\/\d{2})$",
        str(attribute_value)) is not None

def date_normalize(date):
    year_month_date = re.split(r'\/-', date[:10])
    print(year_month_date)
    if len(year_month_date[0]) == 2:
        return '-'.join(year_month_date[::-1])
    else:
        return '-'.join(year_month_date)

def word_split(text):
    return re.compile("[\\w_]+").findall(ViTokenizer.tokenize(text))



collection = pymongo.MongoClient(MONGO_URI)[MONGO_DATABASE][MONGO_COLLECTION]
jobs = list(collection.find({},
							{'title': 1, 'hiringOrganization.name': 1, 'jobLocation.address.addressRegion': 1,'_id': 0, 'validThrough' : 1}))
print(len(jobs))
job = jobs[0]
print(job)
'''
data = [get_filter_data(job) for job in jobs]
print(data[0][1])
date_str = job["validThrough"]
date_time_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
print(date_time_obj)
#'validThrough': '2019-10-21T23:59:59+07:00',
'''
print(__is_date("30-10-2019"))
print(date_normalize("2019-10-19T23:59:59+07:00"))
"""
#topcv_test
	"datePosted" : "2019-09-19",
	"validThrough" : "2019-10-19T23:59:59+07:00",
"""
d = pd.to_datetime("2019-10-19T23:59:59+07:00")
date_str = str(d.day) + "-" + str(d.month) + "-" + str(d.year)
date_d = pd.to_datetime(date_str)
print(date_d)
print(date_str)
print(d)
test2 = pd.to_datetime("2019/11/20")
print(test2)
print(word_split(job["validThrough"]))
#chenh lech 1 tuan so 
#chinh sua lai du lieu
#tach xpath
#du bao trong bao lau??
#so sanh cac du bao
#xac dinh tham so la gi
import pymongo
from setting import *
import datetime
import pandas as pd
from pyvi import ViTokenizer
import re
from utils.job_normalization import normalize_job
from utils.remove_similar_data.remove_similar_data import *
from py_stringmatching.similarity_measure.soft_tfidf import SoftTfIdf
import math
import pandas as pd

def get_filter_data(job):
    title = job['title']
    hiring_organization_name = job['hiringOrganization']['name']
    if type(job['jobLocation']) is list:
        address_region = ','.join([location['address']['addressRegion'] for location in job['jobLocation']])
    else:
        address_region = job['jobLocation']['address']['addressRegion']
    date_str = job['validThrough']
    validThroughDate = pd.to_datetime(date_str)
    valid_through = str(validThroughDate.day) + "-" + str(validThroughDate.month) + "-" + str(validThroughDate.year)
    return [title, hiring_organization_name, address_region, valid_through]

collection = pymongo.MongoClient(MONGO_URI)[MONGO_DATABASE][MONGO_COLLECTION]
jobs = list(collection.find({},
							{'title': 1, 'hiringOrganization.name': 1, 'jobLocation.address.addressRegion': 1,'validThrough' : 1}))
print(len(jobs))
job = jobs[0].copy()
job["validThrough"] = "31-10-2019"
print(job)
x = get_filter_data(job)
data = [get_filter_data(job) for job in jobs]
data_reduction = DataReduction(3, data)
print(data[0][-1])
'''
x_normalize = [data_reduction.word_nomalize(data_reduction.word_split(x_)) for x_ in x]
print(len(data_reduction.Y_normalize))

Y_size_filtering = data_reduction.size_filtering(x_normalize, data_reduction.Y_normalize)
print(len(Y_size_filtering))
'''
is_match = data_reduction.is_match(get_filter_data(job))
print(is_match)
from scrapy import Spider, Request
import json
import os
import re
import pymongo
from pyMicrodata import pyMicrodata
from lxml import etree

from utils.utils import parse_json
from utils.job_normalization import normalize_job
from utils.utils import flatten_dict
from utils.remove_similar_data.remove_similar_data import DataReduction
from setting import *
import pandas as pd
from langdetect import detect
import seperate
'''
def get_data_reduction(uri, database, collection):
    collection = pymongo.MongoClient(uri)[database][collection]
    #Lay ra ten, noi tuyen dung, dia diem, ko lay id cua danh sach tuyen dung
    jobs = list(collection.find({},
                                {'title': 1, 'hiringOrganization.name': 1, 'jobLocation.address.addressRegion': 1, 'validThrough' : 1,'datePosted' : 1,
                                 '_id': 0}))
    print(len(jobs))
    print(jobs[0])
    data = [get_filter_data(job) for job in jobs]
    data_reduction = DataReduction(3, data)
    return data_reduction

    
def get_filter_data(job):
    title = job['title']
    hiring_organization_name = job['hiringOrganization']['name']
    if type(job['jobLocation']) is list:
        address_region = ','.join([location['address']['addressRegion'] for location in job['jobLocation']])
    else:
        address_region = job['jobLocation']['address']['addressRegion']
    #vananh
    #validThrough = 
    #trong db la date => chuyen ve str
    valid_through = job['validThrough']
    date_posted = job['datePosted']
    #validThroughDate = pd.to_datetime(date_str)
    #valid_through = str(validThroughDate.year) + "-" + str(validThroughDate.month) + "-" + str(validThroughDate.day)
    return [title, hiring_organization_name, address_region, date_posted,valid_through]
'''
'''
TOPCV_COLLECTION = "topcv_2"
collection = pymongo.MongoClient(MONGO_URI)[MONGO_DATABASE][MONGO_COLLECTION]
assurance_jobs = collection.find({'title' : 'Bancassurance'})

job = assurance_jobs[0]

data_reduction = get_data_reduction(MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION)
is_match = data_reduction.is_match(get_filter_data(job))
print(is_match)

x = [1,2,3,4,5,6]
print(x[:-2])
def test(a):
	return a
y = [2 * x_ for x_ in x[:-2]]
print(y)
'''
class TopcvNormailization(object):
	"""docstring for TopcvNormailization"""
	def __init__(self):
		super(TopcvNormailization, self).__init__()
		self.database = pymongo.MongoClient(MONGO_URI)[MONGO_DATABASE]
		self.oldCollection = self.database[MONGO_COLLECTION]
		self.newCollection = self.database["topcv_2"]

	def get_data_reduction(self):
	    #Lay ra ten, noi tuyen dung, dia diem, ko lay id cua danh sach tuyen dung
	    jobs = list(self.newCollection.find({},
	                                {'title': 1, 'hiringOrganization.name': 1, 'jobLocation.address.addressRegion': 1, 'validThrough' : 1,'datePosted' : 1,
	                                 '_id': 0}))
	    #print(len(jobs))
	    data = [self.get_filter_data(job) for job in jobs]
	    data_reduction = DataReduction(3, data)
	    return data_reduction

	def get_filter_data(self,job):
		title = job['title']
		hiring_organization_name = job['hiringOrganization']['name']
		if type(job['jobLocation']) is list:
		    address_region = ','.join([location['address']['addressRegion'] for location in job['jobLocation']])
		else:
		    address_region = job['jobLocation']['address']['addressRegion']
		valid_through = job['validThrough']
		date_posted = job['datePosted']
		return [title, hiring_organization_name, address_region, date_posted,valid_through]
	
	def copy_data(self):
		no_duplicated = 0
		i = 119
		while i < 125: 
			old_data = self.oldCollection.find({}).sort([('_id',-1)]).skip(i*100).limit(100)
			for job in old_data:
				data_reduction = self.get_data_reduction()
				is_match = data_reduction.is_match(self.get_filter_data(job))
				if is_match:
					no_duplicated = no_duplicated + 1
				else:
					self.newCollection.insert_one(job)
			i = i + 1

		print("no_duplicated: ",no_duplicated)

	def insert_data(self):
		old_data = self.oldCollection.find({}).sort([('_id',-1)]).limit(10)
		for job in old_data:
			self.newCollection.insert_one(job)

new_topcv = TopcvNormailization()
new_topcv.copy_data()

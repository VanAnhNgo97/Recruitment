import os,sys
import pymongo
import json
#from ..utils.utils import flatten_dict
from setting import *
import pandas as pd
#vananh
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bson.objectid import ObjectId
import bson

class JobStatistic(object):
	def __init__(self,ini_category,ini_year,ini_month,ini_amount):
		#self._id = ObjectId()
		self.category = ini_category
		self.year = ini_year
		self.month = ini_month
		day_str = str(ini_year) + '-' + str(ini_month) + '-' + str(1)
		self.day = pd.to_datetime(day_str)
		self.amount = ini_amount
		super(JobStatistic, self).__init__()




class JobUitl(object):
	
	"""docstring for JobUitl"""
	def __init__(self):
		super(JobUitl, self).__init__()
		DIR_PATH = os.path.dirname(os.path.realpath(__file__))
		CAREER_CODE_DICT = self.load_dict(os.path.join(DIR_PATH, 'utils/dict/career_detail.json'))
		self.TEMP_MONGO_COLLECTION = "topcv_test"
		self.category_list = [0]
		self.database = pymongo.MongoClient(MONGO_URI)[MONGO_DATABASE]
		#self.collection = pymongo.MongoClient(MONGO_URI)[MONGO_DATABASE][self.TEMP_MONGO_COLLECTION]
		self.collection = self.database["topcv_2"]	
		for k,v in CAREER_CODE_DICT.items():
			self.category_list.append(int(v))
		

	def load_dict(self,dict_file_name):
	    if dict_file_name is not None:
	        with open(dict_file_name, encoding='utf-8-sig', mode='r') as f:
	            d = json.load(f)
	            f.close()
	        return d
	    return None
	def statistic_by_category(self):
		
		today = datetime.today()
		print(today)
		from_date = self.get_first_job()
		start_year = from_date.year
		start_month = from_date.month
		day_str = str(start_year) + "-" + str(start_month) + "-" + str(1)
		ini_day = pd.to_datetime(day_str)
		from_date = ini_day
		while(from_date < today):
			to_date = from_date + relativedelta(months=1)
			#test
			#print("from date ", from_date)
			#print("to date ", to_date)
			#

			for category in self.category_list:
				amount = 0
				jobs = self.collection.find({
						'occupationalCategory' : category,
						'datePosted' :{
							'$lt' : to_date,
							'$gte' : from_date
						}
				})
				for job in jobs:
					amount = amount + job['totalJobOpenings']
				
				current_year = from_date.year
				current_month = from_date.month
				statisctic_doc = JobStatistic(category,current_year,current_month,amount)
				self.save_doc(statisctic_doc)
			from_date = to_date

		#	
		'''
		amount = self.collection.find({
			'occupationalCategory' : no_category
			}).count()
		jobs = self.collection.find({}).sort([('datePosted',1)])
		print(type(jobs))
		print(jobs[0]['datePosted'])
		print(amount)
		self.get_first_job()
		return amount
		'''

	def get_first_job(self):
		'''
		from_date = pd.to_datetime('2019-09-09')
		to_date = pd.to_datetime('2019-09-13')
		'''
		jobs = self.collection.find({}).sort([('datePosted',1)]).limit(1)
		'''
		filtered_jobs = self.collection.find({
			'occupationalCategory' : 8,
			'datePosted' :{
				'$lt' : to_date,
				'$gt' : from_date
			}
		}).count()
		print(filtered_jobs)
		'''
		#print(jobs[0]['datePosted'])
		return jobs[0]['datePosted']

	def save_doc(self,statistic_doc):
		collection = self.database["TVN_MonthlyCategoryStatistic"]
		data = statistic_doc.__dict__
		collection.insert_one(data)

	def get_amount_single_category(self,year,month,category):
		collection = self.database["MonthlyCategoryStatistic"]
		statisctic_doc = collection.find({
			'year' : year,
			'month' : month,
			'category' : category
		})
		return statisctic_doc["amount"]

	def update_job_statistic(self):
		self.collection = self.database["topcv_2"]
		collection = self.database["MonthlyCategoryStatistic"]
		collection.drop()
		new_collection = self.database["MonthlyCategoryStatistic"]
		self.statistic_by_category()
		#statisctic_doc = JobStatistic(8,2019,8,0)
		#self.save_doc(statisctic_doc)
	def statistic_category(self,category):
		collection = self.database["TVN_MonthlyCategoryStatistic"]
		monthly_jobs_amount = collection.find({
			'category' : category
			},{'day' : 1, 'amount' : 1, '_id' : 0}).sort([('day', -1)])
		#print(monthly_jobs_amount[0])
		return monthly_jobs_amount
	def update_job_statistic_tvn(self):
		self.collection = self.database["timviecnhanh"]
		collection = self.database["TVN_MonthlyCategoryStatistic"]
		collection.drop()
		new_collection = self.database["TVN_MonthlyCategoryStatistic"]
		self.statistic_by_category()
	def statistic_job(self,domain):
		self.collection = self.database[domain]
		collection_name = 'MonthlyStatistic_' + domain
		collection = self.database[collection_name]
		collection.drop()
		new_collection = self.database[collection_name]
		today = datetime.today()
		print(today)
		from_date = self.get_first_job()
		start_year = from_date.year
		start_month = from_date.month
		day_str = str(start_year) + "-" + str(start_month) + "-" + str(1)
		ini_day = pd.to_datetime(day_str)
		from_date = ini_day
		while(from_date < today):
			to_date = from_date + relativedelta(months=1)
			amount = 0
			jobs = self.collection.find({
					'datePosted' :{
						'$lt' : to_date,
						'$gte' : from_date
					}
			})
			for job in jobs:
				amount = amount + job['totalJobOpenings']
			
			current_year = from_date.year
			current_month = from_date.month
			category = 'all'
			statisctic_doc = JobStatistic(category,current_year,current_month,amount)
			#save doc
			data = statisctic_doc.__dict__
			collection.insert_one(data)
			from_date = to_date
	def get_monthly_statistic(self,domain):
		collection_name = 'MonthlyStatistic_' + domain
		collection = self.database[collection_name]
		data = collection.find({},{'_id' : 0,'category' : 0,}).sort([('day', -1)])
		return data




job_util = JobUitl()
#posted_date = job_util.get_first_job()
#print(posted_date)
'''
print(len(job_util.category_list))
for i in job_util.category_list:
	print(i)
'''
#job_util.statistic_by_category()
#job_util.update_job_statistic()
#amount_list = job_util.statistic_category(8)
#pd.DataFrame(amount_list).to_csv("test.csv")
#timviecnhanh
#job_util.update_job_statistic_tvn()
#statisctic topcv - timviecnhanh by monthly
#job_util.statistic_job("timviecnhanh")
print("ok")
#data = job_util.get_monthly_statistic("timviecnhanh")
#pd.DataFrame(data).to_csv("timviecnhanh.csv")
#top 10
id_list = [35,14,21,8,6,50,33,27,42,5]
for job_id in id_list:
	amount_list = job_util.statistic_category(job_id)
	file_name = "thongke_nganh" + str(job_id) + ".csv"
	pd.DataFrame(amount_list).to_csv(file_name)






		
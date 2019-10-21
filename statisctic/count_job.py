import os,sys
import pymongo
#from ..utils.utils import flatten_dict
from setting import *
import pandas as pd
#vananh
from datetime import datetime
from dateutil.relativedelta import relativedelta

class JobUitl(object):
	
	"""docstring for JobUitl"""
	def __init__(self):
		super(JobUitl, self).__init__()
		CAREER_CODE_DICT = self.load_dict(os.path.join(DIR_PATH, 'dict/career_detail.json'))
		self.TEMP_MONGO_COLLECTION = "topcv_test"
		self.category_list = []
		for k,v in CAREER_CODE_DICT.items():
			self.category_list.append(int(v))
		
	def load_dict(self,dict_file_name):
	    if dict_file_name is not None:
	        with open(dict_file_name, encoding='utf-8-sig', mode='r') as f:
	            d = json.load(f)
	            f.close()
	        return d
	    return None
	def statistic_by_category(self,no_category):
		collection = pymongo.MongoClient(MONGO_URI)[MONGO_DATABASE][TEMP_MONGO_COLLECTION]
		amount = collection.find({
			'occupationalCategory' : no_category
			}).count()
		print(amount)
		return amount

job_util = JobUitl()
x = job_util.statistic_by_category(8)
		
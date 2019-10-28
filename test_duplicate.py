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
	                                 '_id': 0}).limit(5))
	    #jobs = []
	    print(len(jobs))
	    data = [self.get_filter_data(job) for job in jobs]
	    self.data_reduction = DataReduction(3, data)
	    

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

	def get_sample(self):
		jobs = self.newCollection.find({}).skip(5).limit(1)
		job = jobs[0]
		return job

	def test_duplicate_url(self):
		old_data = list(self.newCollection.find({}).sort([('_id',1)]).skip(10000).limit(5000))
		length = len(old_data)
		print(length)
		duplicate_url = []
		new_data = []
		for data in old_data:
			if data["url"] not in new_data:
				new_data.append(data["url"])
			else:
				duplicate_url.append(data["url"])
		return duplicate_url
		

	def remove_duplicate(self,duplicate_urls):
		print(len(duplicate_urls))
		for url in duplicate_urls:
			print(url)
			duplicate_data = list(self.newCollection.find({'url' : url}).sort([('_id',1)]))
			length = len(duplicate_data)
			if  length > 1:
				data = [self.get_filter_data(job) for job in duplicate_data]
				if length > 2:
					i = 0
					while i < length - 2:
						temp = [data[i]]						
						data_reduction = DataReduction(3, temp)
						j = i + 1
						while j < length - 1:
							is_match = data_reduction.is_match(data[j])
							if is_match:
								print("match")
							else:
								print("no")
							j = j + 1
					i = i + 1
				else:
					temp = [data[0]]
					data_reduction = DataReduction(3, temp)
					is_match = data_reduction.is_match(data[1])
					if is_match:
						print("match")
					else:
						print("no")







new_topcv = TopcvNormailization()
dup_url = new_topcv.test_duplicate_url()
new_topcv.remove_duplicate(dup_url)
'''
#chay ok
new_topcv.get_data_reduction()
job = new_topcv.get_sample()
filtered_job = new_topcv.get_filter_data(job)
print("filterd_job----")
print(filtered_job)
print("----------")
is_match = new_topcv.data_reduction.is_match(filtered_job)
print(is_match)
new_topcv.data_reduction.add_job(filtered_job)
is_match = new_topcv.data_reduction.is_match(filtered_job)
print(is_match)
print("ok")
#new_topcv.copy_data()
'''
'''
def add_job(self,filterd_job):
	self.size = self.size + 1
	y_split = []
    for i in range(self.no_fields):
        y_split.append(self.word_nomalize(self.word_split(filterd_job[i])))
    y_split.append(filterd_job[-2])
    y_split.append(filterd_job[-1])
    self.Y_normalize.append(y_split)
    #rebuild inverted index and soft 
    for i in range(self.no_fields):
    	ini_index = self.Y_index[i]
    	self.Y_index[i]=self.rebuild_invert_index(filterd_job[i],self.size,ini_index)
	#recalculate soft-ifidf
	for i in range(self.no_fields):
		self.Y_fields[i].append(filterd_job[i])
		self.soft_tf_idf[i] = SoftTfIdf(self.Y_fields[i])

    

def rebuild_invert_index(self,word_list,data_index,ini_invert_index):
    inverted = ini_invert_index
    for word in word_list:
        locations = inverted.setdefault(word, [])
        locations.append(data_index)
    return inverted

str_list = [["Lập trình viên phần mềm"], ["Kiểm toán phần xuất"]]
index = invert_index(str_list)
print(index)

'''
'''
duplicate link
'https://www.topcv.vn/viec-lam/chuyen-vien-kinh-doanh-bds-tong-cong-ty-dat-xanh-mien-nam/158923.html', 'https://www.topcv.vn/viec-lam/chuyen-vien-quan-he-khach-hang-ca-nhan/148666.html', 'https://www.topcv.vn/viec-lam/it-system-administrator/149849.html', 'https://www.topcv.vn/viec-lam/it-system-administrator/162221.html', 'https://www.topcv.vn/viec-lam/nhan-vien-kinh-doanh-nha-hang/150448.html', 'https://www.topcv.vn/brand/flc/tuyen-dung/bamboo-airways-tiep-vien-hang-khong-j152494.html', 'https://www.topcv.vn/viec-lam/thuc-tap-sinh-java/147327.html', 'https://www.topcv.vn/viec-lam/nhan-vien-kinh-doanh-du-an/158155.html', 'https://www.topcv.vn/viec-lam/chuyen-vien-marketing/161462.html', 'https://www.topcv.vn/viec-lam/nhan-vien-lap-dat/161194.html', 'https://www.topcv.vn/viec-lam/chuyen-vien-tuyen-dung-recruitment-specialist/150932.html', 'https://www.topcv.vn/brand/flc/tuyen-dung/bamboo-airways-tuyen-dung-tiep-vien-hang-khong-da-nang-j160882.html', 'https://www.topcv.vn/viec-lam/chuyen-vien-marketing/147637.html', 'https://www.topcv.vn/viec-lam/chuyen-vien-ho-tro-kinh-doanh/147973.html', 'https://www.topcv.vn/viec-lam/it-comtor-tai-hcm/148546.html', 'https://www.topcv.vn/viec-lam/nhan-vien-marketting-thiet-ke-chinh-sua-video/148797.html', 'https://www.topcv.vn/viec-lam/nhan-vien-content-marketing/149416.html', 'https://www.topcv.vn/viec-lam/thuc-tap-sinh-quan-he-khach-hang-doanh-nghiep/157357.html', 'https://www.topcv.vn/viec-lam/nhan-vien-thiet-ke-san-pham/148799.html', 'https://www.topcv.vn/viec-lam/sales-executive-digital-marketing/147995.html', 'https://www.topcv.vn/viec-lam/chuyen-vien-cham-soc-khach-hang-online/150263.html', 'https://www.topcv.vn/viec-lam/ky-su-giam-sat-noi-that/156314.html', 'https://www.topcv.vn/viec-lam/chuyen-vien-tu-van-khach-hang/147751.html', 'https://www.topcv.vn/viec-lam/thu-ngan-khu-vuc-ha-dong/157739.html', 'https://www.topcv.vn/viec-lam/phu-ta-nha-khoa/147882.html', 'https://www.topcv.vn/viec-lam/nhan-vien-maketing-online/148537.html', 'https://www.topcv.vn/viec-lam/nhan-vien-hanh-chinh-nhan-su/150484.html', 'https://www.topcv.vn/viec-lam/chuyen-vien-doi-ngoai/150354.html', 'https://www.topcv.vn/viec-lam/ke-toan-thue/150491.html', 'https://www.topcv.vn/viec-lam/quan-ly-tham-my-vien/150495.html', 'https://www.topcv.vn/viec-lam/truong-phong-marketing/150497.html', 'https://www.topcv.vn/viec-lam/nhan-vien-quay-dung/150775.html', 'https://www.topcv.vn/viec-lam/nhan-vien-marketing-content/150779.html', 'https://www.topcv.vn/viec-lam/nhan-vien-tu-van-tham-my/150791.html', 'https://www.topcv.vn/viec-lam/dieu-duong-vien/150796.html', 'https://www.topcv.vn/viec-lam/chuyen-vien-ke-toan-tong-hop/146733.html', 'https://www.topcv.vn/viec-lam/nhan-vien-it-helpdesk/146728.html', 'https://www.topcv.vn/viec-lam/nhan-vien-cham-soc-khach-hang/146720.html', 'https://www.topcv.vn/viec-lam/chuyen-vien-tu-van/153744.html', 'https://www.topcv.vn/viec-lam/ke-toan-tong-hop/149950.html', 'https://www.topcv.vn/viec-lam/nhan-vien-cham-soc-khach-hang/147872.html', 'https://www.topcv.vn/viec-lam/nhan-vien-marketing/155505.html', 'https://www.topcv.vn/viec-lam/tro-ly-ban-hang/149536.html', 'https://www.topcv.vn/viec-lam/qa-tester/155977.html', 'https://www.topcv.vn/viec-lam/nhan-vien-sales-admin/149270.html', 'https://www.topcv.vn/viec-lam/nhan-vien-ke-toan-chi-phi/161409.html', 'https://www.topcv.vn/viec-lam/thuc-tap-sinh-marketting-content/148686.html', 'https://www.topcv.vn/viec-lam/can-tuyen-chuyen-vien-marketing/148715.html', 'https://www.topcv.vn/viec-lam/nhan-vien-kinh-doanh-khong-yeu-cau-kinh-nghiem/162578.html', 'https://www.topcv.vn/viec-lam/nhan-vien-kinh-doanh/153941.html', 'https://www.topcv.vn/viec-lam/ke-toan-vat-tu/150640.html', 'https://www.topcv.vn/viec-lam/tuyen-dung-nhan-vien-kinh-doanh/147617.html', 'https://www.topcv.vn/viec-lam/hanh-chinh-le-tan/148243.html', 'https://www.topcv.vn/viec-lam/phien-dich-tieng-trung/150498.html', 'https://www.topcv.vn/viec-lam/chuyen-vien-quan-tri-van-hanh/160445.html', 'https://www.topcv.vn/viec-lam/nhan-vien-ke-toan/149972.html', 'https://www.topcv.vn/viec-lam/chuyen-vien-xu-ly-no-phap-ly-tin-chap-khcn/160218.html', 'https://www.topcv.vn/viec-lam/quan-ly-kinh-doanh/153747.html', 'https://www.topcv.vn/viec-lam/chuyen-vien-xu-ly-no-the-chap-kh-ca-nhan/148828.html
'''
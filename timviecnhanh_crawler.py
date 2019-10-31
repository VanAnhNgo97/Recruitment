from scrapy import Spider, Request, FormRequest
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
import lxml


class Crawler(Spider):
    name = "crawler"
    microdata = pyMicrodata()
    no_duplicated_items = 0
    context = None
    standard_sample = None
    map_schema = None
    data_reduction = None
    parse_job = None
    #vananh
    currentDomain = ""
    no_not_vi_doc = 0
    home = 0

    custom_settings = {
        # 'FEED_FORMAT': 'json',
        # 'FEED_URI': 'topcv.json',
        'ITEM_PIPELINES': {
            'pipelines.MongoPipeline': 300
        },
        'MONGO_URI': MONGO_URI,
        'MONGO_DATABASE': MONGO_DATABASE,
        'MONGO_COLLECTION': MONGO_COLLECTION,
        'USER_AGENT' : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0",
        'HTTPERROR_ALLOW_ALL' : True,
        'COOKIES_ENABLED' : False,
        
        
        
    }
    handle_httpstatus_list = [404,410] 
    def __init__(self, name=None, **kwargs):
        self.domain = kwargs.get('domain')
        Crawler.currentDomain = self.domain
        super(Crawler, self).__init__(name, **kwargs)

    def start_requests(self):
        if os.path.exists(get_context_file(self.domain)):
            with open(get_context_file(self.domain), mode='r', encoding='utf8') as f:
                self.context = json.load(f)
                f.close()
            if not self.context['is_finished']:
                raise Exception('Context file is not completed')
            else:
                if self.context['data_format'] == 'json+ld':
                    self.parse_job = self.parse_job_json
                else:
                    self.parse_job = self.parse_job_microdata

                self.standard_sample = self.get_standard_sample(STANDARD_ATTRIBUTES_FN)
                self.map_schema = self.get_map_schema(self.context['schema'])
                self.data_reduction = self.get_data_reduction(MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION)
                self.inserted_data = []
                self.inserted_data_reduction = DataReduction(3,self.inserted_data)
                #self.eng_collection = pymongo.MongoClient(MONGO_URI)[MONGO_DATABASE]["english_job"]
        else:
            raise Exception('Context file name not existed: ' + get_context_file(self.domain))
        yield Request(url=self.context['start_url'], callback=self.parse)

    def parse(self, response):
        next_page = response.xpath(self.context['selectors']['next_page'] + '/@href').get()
        #job_urls = response.xpath(self.context['selectors']['job_url'] + '/@href').getall()
        job_urls = []
        default_url = "https://www.timviecnhanh.com/tuyen-nhan-vien-phuc-vu-nha-hang-part-time-ho-chi-minh-"
        #loi 3041291
        for i in range(3031291,3041291):
            job_url = "https://www.timviecnhanh.com/tuyen-ke-toan-tong-hop-ho-chi-minh-" + str(i) + ".html"
            #job_url = 'https://www.timviecnhanh.com/tuyen-nu-nhan-vien-goi-dau-luong-cao-3031521.html'
            #headers = {'User-Agent': 'whatever'}
            yield Request(url=get_correct_url(job_url, response), callback=self.parse_job,errback=self.error_parse)
        
        '''
        for job_url in job_urls:
            # job_url = response.urljoin(job_url)
            yield Request(url=get_correct_url(job_url, response), callback=self.parse_job)
        
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield Request(url=get_correct_url(next_page, response), callback=self.parse)
        '''
    def error_parse(self, response):
        print(response.status)
        print("errrrrr")

    def parse_job_json(self, response):
        job_url = response.request.url
        error_log = response.request.url + '-----' + str(response.status) + '\n'
        self.logger.error(error_log)
        jobs = self.get_json_from_response_json(response)
        job_selectors = self.context['selectors']['job_selectors']
        for job in jobs:
            #neu ko co industry thi tim lan can
            if "industry" not in job:
                print("not in")
                job["url"] = job_url
                yield self.get_from_neighbor(response,job)
                continue
            language = job["language"]
            job = self.change_to_right_form(job)
            if job_selectors is not None:
                for field, selector in job_selectors.items():
                    print(selector)
                    job[field] = ','.join(
                        text.strip() for text in response.xpath(selector + '/text()').extract() if text is not None)
                job = self.normalize(job, job_url)
                if job is not None:
                    job["language"] = language
                    yield job
            
                

    def parse_job_microdata(self, response):
        job_url = response.request.url
        jobs = self.get_json_from_response_microdata(response)
        job_selectors = self.context['selectors']['job_selectors']
        for job in jobs:
            job = self.change_to_right_form(job)
            if job_selectors is not None:
                for field, selector in job_selectors.items():
                    #print(selector)
                    job[field] = ','.join(
                        text.strip() for text in response.xpath(selector + '/text()').extract() if text is not None)
                job = self.normalize(job, job_url)
                yield job

    @staticmethod
    def get_json_from_response_json(response):
        result = []
        #vananh
        ''' #for topcv
        if response.url == "https://www.topcv.vn/viec-lam":
            Crawler.home = Crawler.home + 1
            return result
        '''
        #
        dom = etree.HTML(response.body.decode("utf8"))
        #print("-------raw------------")
        #print(dom.xpath("//title/text()"),'-------',response.url,'-----',response.status)
        #print("---------------------")
        #for timviecnhanh
        raw_title = dom.xpath("//title/text()")[0]
        if raw_title.lower() == "error":
            Crawler.home = Crawler.home + 1
            return result
        json_node = dom.xpath("//script[text()]")
        extract_job = None
        for node in json_node:
            try:
                job = json.loads(node.text, strict=False)
                if job['@type'] == 'JobPosting':
                    #van anh
                    #dich tai day
                    extract_job = job
                    vi_lang = Crawler.is_vi_language(job['description'])
                    if not vi_lang:
                        job["language"] = "en"
                        temp_job = job
                        if Crawler.currentDomain == "topcv":
                            print(response.url)
                            job = Crawler.seperate_attributes_topcv(temp_job,dom,False)
                            Crawler.no_not_vi_doc = Crawler.no_not_vi_doc + 1
                            result.append(job)
                            return result
                        elif Crawler.currentDomain == "timviecnhanh":
                            print(response.url)
                            job = Crawler.extract_job_openings_tvn(temp_job,dom,False)
                            Crawler.no_not_vi_doc = Crawler.no_not_vi_doc + 1
                            result.append(job)
                            return result
                    else:
                        job["language"] = "vi"
                        temp_job = job
                        if Crawler.currentDomain == "topcv":
                            print(response.url)
                            job = Crawler.seperate_attributes_topcv(temp_job,dom)
                        elif Crawler.currentDomain == "timviecnhanh":
                            print(response.url)
                            job = Crawler.extract_job_openings_tvn(temp_job,dom)

                    result.append(job)

            except (ValueError, TypeError):
                pass
        if extract_job is None:
            if Crawler.currentDomain == "timviecnhanh":
                print(response.url)
                job = Crawler.seperate_attributes_timviecnhanh(dom)
                if job is not None:
                    result.append(job)
        return result

    def get_json_from_response_microdata(self, response):
        raw_json = json.loads(self.microdata.rdf_from_source(response.body, 'json-ld').decode('utf8'))
        result = parse_json(raw_json)
        return result

    def change_to_right_form(self, job):
        norm_job = self.standard_sample.copy()
        #print(norm_job)
        flatten_job = flatten_dict(job)

        for key, value in self.map_schema.items():
            real_value = flatten_job.get(key)
            if real_value is None:
                continue
            else:
                attribute = norm_job
                for attribute_level in value[:-1]:
                    attribute = attribute.get(attribute_level)
                if type(real_value) is str:
                    attribute[value[-1]] = re.sub(r'<[^<>]*>', '', str(real_value))
                elif type(attribute[value[-1]]) == dict and type(real_value) == list:
                    attribute[value[-1]] = real_value[0]
                else:
                    attribute[value[-1]] = real_value
        #print("norm_job")
        #print(norm_job)
        return norm_job

    def normalize(self, job, url):
        result = normalize_job(job)
        result['url'] = url

        # Check duplicate
        #phai ktra nhung tin da insert truoc
        if self.data_reduction.is_match(self.get_filter_data(job)):
            self.no_duplicated_items += 1
            result = None
            return result
        else:
            if self.inserted_data_reduction.is_match(self.get_filter_data(job)):
                self.no_duplicated_items += 1
                result = None
                return result
            else:
                #self.inserted_data.append(self.get_filter_data(job))
                self.inserted_data_reduction.add_job(self.get_filter_data(job))
        return result

    @staticmethod
    def get_standard_sample(file_name):
        if os.path.exists(file_name):
            with open(file_name, mode='r', encoding='utf8') as f:
                standard_sample = json.load(f)
                f.close()
        else:
            raise Exception('Not exist standard file: ' + file_name)

        return standard_sample

    @staticmethod
    def get_map_schema(schema):
        return {key: value.split('_') for key, value in schema.items()}

    def get_data_reduction(self, uri, database, collection):
        collection = pymongo.MongoClient(uri)[database][collection]
        #Lay ra ten, noi tuyen dung, dia diem, ko lay id cua danh sach tuyen dung
        jobs = list(collection.find({},
                                    {'title': 1, 'hiringOrganization.name': 1, 'jobLocation.address.addressRegion': 1, 'validThrough' : 1, 'datePosted' : 1,
                                     '_id': 0}))
        data = [self.get_filter_data(job) for job in jobs]

        data_reduction = DataReduction(3, data)
        return data_reduction

    @staticmethod
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
        #validThroughDate = pd.to_datetime(date_str)
        #valid_through = str(validThroughDate.year) + "-" + str(validThroughDate.month) + "-" + str(validThroughDate.day)
        date_posted = job['datePosted']
        return [title, hiring_organization_name, address_region, date_posted,valid_through]
        
    #van anh
    #vananh
    @staticmethod
    def seperate_attributes_topcv(job,dom,is_vi=True):
        '''
        if not is_vi:
            #lay so luong tuyen dung:
            job_available_node = dom.xpath("//div[@id='col-job-right']//div[@id='box-info-job']//div[@class='job-info-item']//*[contains(text(),'cần tuyển')]/following-sibling::*[1]")
            if(len(job_available_node) == 0):
                job_available_node = dom.xpath("///*[@data-original-title='Số lượng cần tuyển']")
            if(len(job_available_node) > 0):
                job_available_text = job_available_node[0].text
                if "không giới hạn" in job_available_text.lower():
                    job["totalJobOpenings"] = 10
                elif "người" in job_available_text.lower():
                    num_job_available = (job_available_text.split(" ")[0])
                    if(num_job_available.isdigit()):
                        job["totalJobOpenings"] = int(num_job_available)
                else:
                    job["totalJobOpenings"] = 2
            else:
                job["totalJobOpenings"] = 2
            job["language"] = "en"
            return job
        '''
        inital_description = job['description']
        description_dom = etree.HTML(inital_description)
        first_benefit = ""
        first_requirement = ""
        if "jobBenefits" not in job:
            raw_benefits = description_dom.xpath("//*[contains(text(),'Quyền lợi')]/following-sibling::*")
            print(len(raw_benefits))
            raw_benefits_str = ""
            for bnf in raw_benefits:
                bnf_str = etree.tostring(bnf,method='html',encoding="unicode")
                raw_benefits_str = raw_benefits_str + bnf_str
            if len(raw_benefits) > 0:
                first_benefit = etree.tostring(raw_benefits[0],method='html',encoding="unicode")
                jobBenefits = raw_benefits_str
                job["jobBenefits"] = jobBenefits
            else:
                job["jobBenefits"] = ""
        if "experienceRequirements" not in job:
            raw_requirements = description_dom.xpath("//*[contains(text(),'Yêu cầu')]/following-sibling::*")
            requirements_str = ""
            req_length = len(raw_requirements)
            i = 0
            while i < req_length:
                req_str = etree.tostring(raw_requirements[i],method='html',encoding="unicode")
                if(first_benefit == req_str):
                    folowing_req_str = etree.tostring(raw_requirements[i-1],method='html',encoding="unicode")
                    requirements_str = requirements_str.replace(folowing_req_str,"")
                    break
                requirements_str = requirements_str + req_str
                i += 1
            if len(raw_requirements) > 1: #neu = 1 la req = "" den benefit luon
                first_requirement =  etree.tostring(raw_requirements[0],method='html',encoding="unicode")
                experienceRequirements = requirements_str
                job["experienceRequirements"] = experienceRequirements
            else:
                job["experienceRequirements"] = ""
        #
        if first_requirement.strip() != "":
            print("hehe")
            std_description = description_dom.xpath("//*[contains(text(),'Mô tả')]/following-sibling::*")
            std_description_str = ""
            i = 0
            std_description_length = len(std_description)
            while i < std_description_length:
                des_str = etree.tostring(std_description[i],method='html',encoding="unicode")
                if first_requirement == des_str:
                    folowing_des_str = etree.tostring(std_description[i-1],method='html',encoding="unicode")
                    std_description_str = std_description_str.replace(folowing_des_str,"")
                    break
                std_description_str = std_description_str + des_str
                i += 1
            job["description"] = std_description_str
        #sua loi out of range
        print("exp ",job["experienceRequirements"])
        print("be ", job["jobBenefits"] == "")
        if job["experienceRequirements"] == "" or job["jobBenefits"] == "":
            job["jobBenefits"] = seperate.extract_info(inital_description,"quyền lợi")
            job["description"] = seperate.extract_info(inital_description,"mô tả")
            job["experienceRequirements"] = seperate.extract_info(inital_description,"yêu cầu")
        if job["experienceRequirements"] == "" and job["jobBenefits"] == "" and job["description"] == "":
            #print("lala")
            meta_description = dom.xpath("//meta[@name='description']")
            for temp in meta_description:
                job["jobBenefits"] = ""
                job["description"] = temp.attrib['content']
                job["experienceRequirements"] = temp.attrib['content']
            '''
            print(meta_description[0])
            content = meta_description[0].attrib['content']
            print("lalal2")
            print(content)
            '''
        #lay so luong tuyen dung:
        job_available_node = dom.xpath("//div[@id='col-job-right']//div[@id='box-info-job']//div[@class='job-info-item']//*[contains(text(),'cần tuyển')]/following-sibling::*[1]")
        if(len(job_available_node) == 0):
            job_available_node = dom.xpath("///*[@data-original-title='Số lượng cần tuyển']")
        if(len(job_available_node) > 0):
            job_available_text = job_available_node[0].text
            if "không giới hạn" in job_available_text.lower():
                job["totalJobOpenings"] = 10
            elif "người" in job_available_text.lower():
                num_job_available = (job_available_text.split(" ")[0])
                if(num_job_available.isdigit()):
                    job["totalJobOpenings"] = int(num_job_available)
            else:
                job["totalJobOpenings"] = 2
        else:
            job["totalJobOpenings"] = 2
        
        if is_vi:
            job["language"] = "vi"
        else:
            job["language"] = "en"

        #print(job["totalJobOpenings"])
        return job
    @staticmethod
    def seperate_attributes_timviecnhanh(dom):
        job = {}
        meta_description = dom.xpath("//meta[@property='og:description']")
        for temp in meta_description:
            job["jobBenefits"] = ""
            job["description"] = temp.attrib['content']
            job["experienceRequirements"] = ""
        vi_lang = Crawler.is_vi_language(job['description'])
        if not vi_lang:
            Crawler.no_not_vi_doc = Crawler.no_not_vi_doc + 1
            return None
        job["language"] = "vi"
        raw_title = dom.xpath("//title/text()")[0]
        raw_title = raw_title.strip()
        title_list = raw_title.split("|")
        if len(title_list) > 1:
            raw_title = title_list[0].strip()
        job["title"] = raw_title
        job["validThrough"] = seperate.extract_info_tvn(job["description"],"ngày hết hạn")
        job["hiringOrganization"] = {}
        job["hiringOrganization"]["name"] = seperate.extract_info_tvn(job["description"],"công ty")
        raw_salary = seperate.extract_info_tvn(job["description"],"lương")
        job["baseSalary"] =  {}
        job["baseSalary"] = seperate.extract_salary_tvn(raw_salary)
        job["totalJobOpenings"] = 2
        job["jobLocation"] = {
            "address" : {}
        }
        job["jobLocation"]["address"]["addressLocality"] = "Việt Nam"
        job["jobLocation"]["address"]["streetAddress"] = "Việt Nam"
        job["jobLocation"]["address"]["addressCountry"] = "Việt Nam"
        #print(job)
        return job

    @staticmethod
    def extract_job_openings_tvn(job,dom):
        jobOpenings = 0
        if "totalJobOpenings" not in job:
            job_available_values = dom.xpath("//*[@id='left-content']//*[contains(text(),'Số lượng tuyển dụng')]/parent::*/text()")
            if len(job_available_values) == 0:
                job_available_values = dom.xpath("//div[@class='info-left']//*[contains(text(),'Số lượng cần tuyển')]/parent::*/text()")
            for value in job_available_values:
                #print("value")
                #print(value)
                temp = value.strip()
                if temp != "" and temp.isdigit():
                    job["totalJobOpenings"] = int(temp)
                    jobOpenings = job["totalJobOpenings"]
                elif temp != "" and "giới hạn" in temp:
                    job["totalJobOpenings"] = 10
                    jobOpenings = job["totalJobOpenings"]
            if jobOpenings == 0:
                job["totalJobOpenings"] = 2
        return job

    @staticmethod
    def is_vi_language(raw_text):
        tag_re = re.compile(r'<[^>]+>')
        text = tag_re.sub('',raw_text)
        text = text.strip()
        result = detect(text)
        if result != "vi":
            return False
        return True

    def get_from_neighbor(self, response,ini_job):
        #print("-----neighbor_job----")
        dom = etree.HTML(response.body.decode("utf8"))
        neighbor_urls = dom.xpath("//*[@id='job-hot-content']//tr[1]//a[1]")
        if len(neighbor_urls) == 0:
            neighbor_urls = dom.xpath("//*[@id='job-week-content']//tr[1]//a[1]")
        result = []
        for neighbor_url in neighbor_urls:
            url = neighbor_url.attrib["href"]
            neighbor_request = Request(url=get_correct_url(url, response),callback=self.get_job_from_neighbor, encoding='utf8')
            neighbor_request.cb_kwargs["ini_job"] = ini_job
            #print("-----ok-----")
            return neighbor_request
            
    def get_job_from_neighbor(self,response,ini_job):
        print("xxxxxxxxxxxxxxxxxxx")
        neighbor_jobs = self.get_json_from_response_json(response)
        for neighbor_job in neighbor_jobs:
            print("neighbor_job")
            ini_job["industry"] = neighbor_job["industry"]
        job_selectors = self.context['selectors']['job_selectors']
        job = ini_job
        language = job["language"]
        job_url = job["url"]
        job = self.change_to_right_form(job)
        if job_selectors is not None:
            for field, selector in job_selectors.items():
                job[field] = ','.join(
                    text.strip() for text in response.xpath(selector + '/text()').extract() if text is not None)
            job = self.normalize(job, job_url)
            if job is not None:
                job["language"] = language
                yield job

    def close(self, spider, reason):
        print("Number of english items: ", self.no_not_vi_doc)
        print("Number of broken items: ", self.home)
        print('Number of duplicated items: %d' % self.no_duplicated_items)
        print("Finished!")

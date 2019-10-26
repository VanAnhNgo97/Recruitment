# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lxml import etree
import json
from pyMicrodata import pyMicrodata
import os
import re
import pymongo

from utils.utils import parse_json
from utils.detect_schema import JobSchemaDetection
from utils.model import NaiveBayesModel, DecisionTreeModel, LogisticRegressionModel
from utils.preprocess import FeaturesTransformer
from utils.job_normalization import normalize_job
from utils.utils import flatten_dict
from utils.remove_similar_data.remove_similar_data import DataReduction
from wrapper.xpath_mapping import XpathMapping
from setting import *
from langdetect import detect


class SchemaCrawler(Spider):
    name = "schema_crawler"
    microdata = pyMicrodata()
    schema = None
    get_job_sample = None
    samples = []
    selectors = {
        # 'job_url': "//*[@id='box-job-result']/div[1]/div/div/div[2]/h4/a",
        # 'next_page': "//*[@id='box-job-result']/div[2]/ul/li[last()]/a",
    }
    # start_url = 'https://www.topcv.vn/viec-lam/moi-nhat.html?utm_source=click-search-job&utm_medium=page-job&utm_campaign=tracking-job'
    context = {}
    domain = ""
    currentDomain = ""

    def __init__(self, name=None, **kwargs):
        self.start_url = kwargs.get('start_url')
        self.selectors['job_url'] = kwargs.get('job_url')
        self.selectors['next_page'] = kwargs.get('next_page')
        self.domain = kwargs.get('domain')
        #self.driver = webdriver.Firefox()
        super(SchemaCrawler, self).__init__(name, **kwargs)

    def start_requests(self):
        self.context['start_url'] = self.start_url
        self.context['domain'] = self.domain
        SchemaCrawler.currentDomain = self.domain
        
        if not os.path.exists(get_context_file(self.domain)):
            if not os.path.exists(STANDARD_ATTRIBUTES_FN):
                raise Exception('Not exist standard file: ' + STANDARD_ATTRIBUTES_FN)
            yield Request(url=self.start_url, callback=self.get_data_format)
        
        #vananh
        #yield Request(url=self.start_url, callback=self.get_data_format)
        
    def parse(self, response):
        pass

    def get_data_format(self, response):
        #chi lay 1 url dau tien
        sample_job_url = response.xpath(self.selectors['job_url'] + '/@href').get()
        #vananh
        #print(len(sample_job_url))
        #print(sample_job_url)
        yield Request(url=get_correct_url(sample_job_url, response), callback=self.decide_data_format)

    def decide_data_format(self, response):
        can_crawl = True
        if self.is_data_json_format(response):
            print("json")
            #buoc gan, chua goi
            self.get_job_sample = self.get_job_sample_json
            self.context['data_format'] = 'json+ld'
        elif self.is_data_microdata_format(response):
            self.get_job_sample = self.get_job_sample_microdata
            self.context['data_format'] = 'microdata'
        else:
            print('Cannot crawl')
            can_crawl = False
        #vananh
        if can_crawl:
            yield Request(url=self.start_url, callback=self.get_job_url_samples)

    def get_job_url_samples(self, response):
        job_urls = response.meta.setdefault('job_urls', [])
        next_page = response.xpath(self.selectors['next_page'] + '/@href').get()
        #print(next_page)
        #Lay 20 job_urls
        job_urls += response.xpath(self.selectors['job_url'] + '/@href').getall()
        #print(job_urls)
        
        if next_page is not None and len(job_urls) < MAX_NO_SAMPLES:
            yield Request(url=get_correct_url(next_page, response), callback=self.get_job_url_samples, meta={'job_urls': job_urls})
        else:
            yield Request(url=get_correct_url(job_urls[0], response), callback=self.get_job_sample, meta={'job_urls': job_urls[1:MAX_NO_SAMPLES]})
        
    def decide_schema(self):
        #print("VanAnh\n\n")
        print("so luong samples: ", len(self.samples))
        schema = JobSchemaDetection(self.samples, MODEL_DIR, STANDARD_ATTRIBUTES_FN,
                                    WEIGHT_MODEL_FN).get_mapping_schema()
        self.context['schema'] = schema
        self.context['selectors'] = self.selectors
        self.context['is_finished'] = False
        self.logger.error(self.context)
        with open(get_context_file(self.domain), mode='w', encoding='utf8') as f:
            json.dump(self.context, f)
            f.close()

    def get_job_sample_json(self, response):
        samples = response.meta.setdefault('samples', [])
        '''
        print("-------")
        print(response.meta['job_urls'])
        print("------")
        '''
        job_urls = response.meta['job_urls']
        #print(response.meta)
        samples += self.get_json_from_response_json(response)
        #print(samples)
        #lay dan cac job_urls de boc tach???
        if len(job_urls) > 0:
            yield Request(url=get_correct_url(job_urls[0], response), callback=self.get_job_sample_json,
                          meta={'samples': samples, 'job_urls': job_urls[1:]})
        else:
            self.samples = samples
            self.decide_schema()
        
    def get_job_sample_microdata(self, response):
        samples = response.meta.setdefault('samples', [])
        job_urls = response.meta['job_urls']
        samples.append(self.get_json_from_response_microdata(response))

        if len(job_urls) > 0:
            yield Request(url=get_correct_url(job_urls[0], response), callback=self.get_job_sample_microdata,
                          meta={'samples': samples, 'job_urls': job_urls[1:]})
        else:
            self.samples = samples
            self.decide_schema()

    def is_data_json_format(self, response):
        return len(self.get_json_from_response_json(response,True)) > 0 #them True

    def is_data_microdata_format(self, response):
        return len(self.get_json_from_response_microdata(response)) > 0

    @staticmethod
    def get_json_from_response_json(response,is_sample=False):
        print("url:")
        print(response.url)
        result = []
        dom = etree.HTML(response.body.decode("utf8"))
        json_node = dom.xpath("//script[text()]")#xac dinh cac doan script json+ld
        for node in json_node:
            try:
                job = json.loads(node.text, strict=False)
                if job['@type'] == 'JobPosting':
                    #van anh
                    if is_sample == False:#minh them vao
                        #dich tai day
                        vi_lang = SchemaCrawler.is_vi_language(job["description"])
                        if not vi_lang:
                            print("tieng anh")
                            print(response.url)
                            print("-----")
                            return result
                        #
                        if SchemaCrawler.currentDomain == "topcv":
                            temp_job = job
                            job = SchemaCrawler.seperate_attributes_topcv(temp_job,dom)
                            #lay ra so luong tuyendung
                        elif SchemaCrawler.currentDomain == "timviecnhanh":
                            temp_job = job
                            job = SchemaCrawler.seperate_attributes_timviecnhanh(temp_job,dom)

                        #print(job)
                    result.append(job)

            except (ValueError, TypeError):
                pass
        return result

    def get_json_from_response_microdata(self, response):
        print("microdata")
        raw_json = json.loads(self.microdata.rdf_from_source(response.body, 'json-ld').decode('utf8'))
        #print(raw_json)
        result = parse_json(raw_json)
        return result
    #vananh
    @staticmethod
    def seperate_attributes_topcv(job,dom):
        print("ok cv")
        inital_description = job['description']
        #kiem tra tieng anh - true return None
        description_dom = etree.HTML(inital_description)
        first_benefit = ""
        first_requirement = ""
        if "jobBenefits" not in job:
            raw_benefits = description_dom.xpath("//*[contains(text(),'Quyền lợi')]/following-sibling::*")
            raw_benefits_str = ""
            for bnf in raw_benefits:
                bnf_str = etree.tostring(bnf,method='html',encoding="unicode")
                raw_benefits_str = raw_benefits_str + bnf_str
            first_benefit = etree.tostring(raw_benefits[0],method='html',encoding="unicode")
            jobBenefits = raw_benefits_str
            job["jobBenefits"] = jobBenefits
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
            first_requirement =  etree.tostring(raw_requirements[0],method='html',encoding="unicode")
            experienceRequirements = requirements_str
            job["experienceRequirements"] = experienceRequirements 
        #
        if first_requirement.strip() != "":
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
        #lay so luong tuyen dung:
        
        job_available_node = dom.xpath("//div[@id='col-job-right']//div[@id='box-info-job']//div[@class='job-info-item']//*[contains(text(),'cần tuyển')]/following-sibling::*[1]")
        #print("so luong:")
        #print(job_available_node)
        if(len(job_available_node) == 0):
            job_available_node = dom.xpath("///*[@data-original-title='Số lượng cần tuyển']")
        if(len(job_available_node) > 0):
            job_available_text = job_available_node[0].text
            if "không giới hạn" in job_available_text.lower():
                job["totalJobOpenings"] = 50
            elif "người" in job_available_text.lower():
                num_job_available = (job_available_text.split(" ")[0])
                if(num_job_available.isdigit()):
                    job["totalJobOpenings"] = int(num_job_available)
            else:
                job["totalJobOpenings"] = 1
        else:
            job["totalJobOpenings"] = 1
        #print(job["totalJobOpenings"])
        return job

    @staticmethod
    def seperate_attributes_timviecnhanh(job,dom):
        '''
        https://www.timviecnhanh.com/dxmbhn/nhan-vien-kinh-doanh-bds-kv-quan-4-quan-7-nha-be-dat-xanh-mien-bac-ho-chi-minh-id4352813.html
        '''
        jobOpenings = 0
        if "totalJobOpenings" not in job:
            job_available_values = dom.xpath("//*[@id='left-content']//*[contains(text(),'Số lượng tuyển dụng')]/parent::*/text()")
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
        #print("timviecnhanh")
        #print(job["totalJobOpenings"])
        #print(job)
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
    #


class XpathCrawler(Spider):
    name = "xpath_crawler"
    context = None
    mismatch_attributes = None

    def __init__(self, name=None, **kwargs):
        self.domain = kwargs.get('domain')
        super(XpathCrawler, self).__init__(name=name, **kwargs)

    def start_requests(self):
        if os.path.exists(get_context_file(self.domain)):
            with open(get_context_file(self.domain), mode='r', encoding='utf-8') as f:
                self.context = json.load(f)
                f.close()

            if not self.context['is_finished']:
                self.mismatch_attributes = self.get_mismatch_attributes()
                yield Request(url=self.context['start_url'], callback=self.get_job_sample_url)
        else:
            raise Exception('Not exist context file: ' + get_context_file(self.domain))

    def parse(self, response):
        pass

    def get_mismatch_attributes(self):
        matched_attributes = self.context['schema'].values()
        mismatch_attributes = []

        for attribute in STANDARD_ATTRIBUTES:
            if attribute not in matched_attributes:
                mismatch_attributes.append(MAPPING_LABEL_NUM[attribute])
        return mismatch_attributes

    def get_job_sample_url(self, response):
        job_urls = response.xpath(self.context['selectors']['job_url'] + "/@href").extract()
        yield Request(url=get_correct_url(job_urls[0], response), callback=self.get_job_sample_xpath_data, meta={'job_urls': ''})

    def get_job_sample_xpath_data(self, response):
        data = self.get_xpath_content_data(response)
        data += response.meta.setdefault('data', [])
        job_urls = response.meta['job_urls']
        if len(job_urls) == 0:
            #lay phan loai nhung truong con thieu gia tri
            # map_xpath = module(self.mismatch_attributes, data) ko phai minh comment
            map_xpath = XpathMapping(data, self.mismatch_attributes).get_xpath_mapping()
            #print("ng")
            #print(map_xpath)
            job_selectors = self.context['selectors'].setdefault('job_selectors', {})
            for attribute, xpath in map_xpath.items():
                job_selectors[MAPPING_NUM_LABEL[attribute]] = xpath

            self.context['is_finished'] = True

            self.save_context()
        else:
            yield Request(url=get_correct_url(job_urls[0], response), callback=self.get_job_sample_xpath_data,
                          meta={'data': data, 'job_urls': job_urls[1:]})

    def save_context(self):
        with open(get_context_file(self.domain), mode='w', encoding='utf8') as f:
            json.dump(self.context, f)
            f.close()

    @staticmethod
    def get_xpath_content_data(response):
        tree = etree.HTML(response.body.decode('utf8'))
        data = []

        for node in tree.xpath('//head | //style | //script | //footer | //nav | //select | //form | //table'):
            node.getparent().remove(node)

        for node in tree.iter():
            if node.text is not None:
                data.append([node.getroottree().getpath(node), node.text])

        return data

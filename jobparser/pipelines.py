# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy1803

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            self.hh_salary_extraction(item)
        else:
            self.sj_salary_extraction(item)
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def sj_salary_extraction(self, item):
        item['salary_min'] = None
        item['salary_max'] = None
        item['salary_cur'] = None
        if 'от' in item['salary']:
            item['salary_min'] = int(re.findall(r'\d+', item['salary'][2].replace('\xa0', ''))[0])
            item['salary_cur'] = item['salary'][2].split('\xa0')[-1]
        elif 'до' in item['salary']:
            item['salary_max'] = int(re.findall(r'\d+', item['salary'][2].replace('\xa0', ''))[0])
            item['salary_cur'] = item['salary'][2].split('\xa0')[-1]
        elif len(item['salary']) > 8:
            item['salary_min'] = int(item['salary'][0].replace('\xa0', '').strip())
            item['salary_max'] = int(item['salary'][4].replace('\xa0', '').strip())
            item['salary_cur'] = item['salary'][6]
        return item

    def hh_salary_extraction(self, item):
        if 'от ' in item['salary']:
            item['salary_min'] = int(''.join(item['salary'][1].split()))
            if 'до ' in item['salary']:
                item['salary_max'] = int(''.join(item['salary'][3].split()))
                item['salary_cur'] = item['salary'][5]
            else:
                item['salary_max'] = None
                item['salary_cur'] = item['salary'][3]
        elif 'до ' in item['salary']:
            item['salary_min'] = None
            item['salary_max'] = int(''.join(item['salary'][1].split()))
            item['salary_cur'] = item['salary'][3]
        else:
            item['salary_min'] = None
            item['salary_max'] = None
            item['salary_cur'] = None
        return item

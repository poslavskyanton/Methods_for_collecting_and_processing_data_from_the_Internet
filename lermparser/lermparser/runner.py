from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from lermparser.lermparser import settings
from lermparser.lermparser.spiders.lmru import LmruSpider

if __name__ == '__main__':
    settings_crawler = Settings()
    settings_crawler.setmodule(settings)
    crawler_process = CrawlerProcess(settings=settings_crawler)
    crawler_process.crawl(LmruSpider, search='краска')
    crawler_process.start()
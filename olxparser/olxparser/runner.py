from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from olxparser.olxparser import settings
from olxparser.olxparser.spiders.olx import OlxSpider


if __name__ == '__main__':
    search_value = 'bmw'
    settings_crawler = Settings()
    settings_crawler.setmodule(settings)
    crawler_process = CrawlerProcess(settings=settings_crawler)
    crawler_process.crawl(OlxSpider, search=search_value)
    crawler_process.start()
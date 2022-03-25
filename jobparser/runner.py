from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.supjobru import SupjobruSpider


if __name__ == '__main__':
    settings_crawler = Settings()
    settings_crawler.setmodule(settings)
    crawler_process = CrawlerProcess(settings=settings_crawler)
    crawler_process.crawl(HhruSpider)
    crawler_process.crawl(SupjobruSpider)
    crawler_process.start()
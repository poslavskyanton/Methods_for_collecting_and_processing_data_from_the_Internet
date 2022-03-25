import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.supjobru import SupjobruSpider



configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)
runner.crawl(HhruSpider)
runner.crawl(SupjobruSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
"""from scrapy.crawler import CrawlerProcess
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
"""
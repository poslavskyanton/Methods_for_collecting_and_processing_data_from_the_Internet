import scrapy
from scrapy.http import HtmlResponse
from olxparser.olxparser.items import OlxparserItem
from scrapy.loader import ItemLoader


class OlxSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ['olx.kz']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.olx.kz/list/q-{kwargs.get('search')}/"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-cy='page-link-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-cy='listing-ad-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=OlxparserItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_xpath("name", "//h1[@data-cy='ad_title']/text()")
        loader.add_xpath("price", "//h3/text()")
        loader.add_xpath("product_description", "//div[@data-cy='ad_description']/div/text()")
        loader.add_xpath("photos", "//div[@class='swiper-wrapper']//@src | //div[@class='swiper-wrapper']//@data-src")
        yield loader.load_item()

import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SupjobruSpider(scrapy.Spider):
    name = 'supjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//span[contains(@class, '_1BiPY')]/a[contains(@href, 'vakansii')]/@href").getall()
        print(links)
        print(len(links))
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name_value = response.xpath("//div[@class='_3MVeX']/h1/text()").get()
        salary_value = response.xpath("//span[@class='_1OuF_ ZON4b']//text()").getall()
        url_value = response.url
        yield JobparserItem(name=name_value, salary=salary_value, url=url_value)
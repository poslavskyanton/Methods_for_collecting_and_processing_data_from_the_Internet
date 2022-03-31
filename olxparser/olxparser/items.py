# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst
from twisted.web.html import output


def clear_price(value):
    value = value.replace(' ', '')
    try:
        value = int(value)
    except:
        return value
    return value


class OlxparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst())
    product_description = scrapy.Field()
    photos = scrapy.Field()
    _id = scrapy.Field()
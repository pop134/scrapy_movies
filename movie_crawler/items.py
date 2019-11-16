# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MovieCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # pass
    actors = scrapy.Field()
    content = scrapy.Field()
    detail = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    images = scrapy.Field()
    image_url = scrapy.Field()


class Image(scrapy.Item):
    # define the fields for your item here like:
    # pass
    image_urls = scrapy.Field()
    images = scrapy.Field()

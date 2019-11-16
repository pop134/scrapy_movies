# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from movie_crawler.items import MovieCrawlerItem
import datetime, time


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['']
    start_urls = ['http://www.phimmoi.net/phim-le/']

    def parse(self, response):
        yield Request(url='http://www.phimmoi.net/phim-le/',
                      callback=self.parsing_pages,
                      dont_filter=True)

    def parsing_pages(self, response):
        yield Request(url=response.url,
                      callback=self.page_info,
                      dont_filter=True)
        next_page_url = response.xpath('//*[@class="pagination pagination-lg"]')
        if next_page_url.xpath('li[3]/a/@href'):
            url = next_page_url.xpath('li[3]/a/@href').extract_first()
        else:
            url = next_page_url.xpath('li/a/@href').extract_first()
        if url is not None:
            yield Request(url='http://www.phimmoi.net/' + url, callback=self.parsing_pages, dont_filter=True)

    def page_info(self, response):
        body = response.xpath('//*[@class="movie-list-index"]/ul')
        for info in body.xpath('li'):
            url = info.xpath('a/@href').extract_first()
            yield Request(url='http://www.phimmoi.net/' + url, callback=self.extract_movie, dont_filter=True)

    def extract_movie(self, response):


        actors = self.actors(response)
        detail, title = self.movie_details(response)

        detail = self.movie_detail_processing(detail, title)
        if detail['Ngày phát hành']:
            date = detail['Ngày phát hành'].split('/')
            time1 = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
            detail.update({
                'Ngày phát hành': str(round(time.mktime(time1.timetuple())))
            })

        content = ''.join(response.xpath('//*[@id="film-content"]/p//text()').extract())
        image = self.image(response)
        movie_title = response.xpath('//*[@class="col-6 movie-detail"]/h1/span/a/text()').extract_first()

        loader = ItemLoader(item=MovieCrawlerItem(), response=response)
        loader.add_value('image_url', image)
        loader.add_value('content', content)
        loader.add_value('actors', actors)
        loader.add_value('detail', detail)
        loader.add_value('title', movie_title)
        loader.add_value('type', 'Phim Lẻ')

        return loader.load_item()

    @staticmethod
    def movie_details(response):
        body = response.xpath('//*[@class="movie-dl"]')
        detail = []
        title = []
        for info in body.xpath('dd'):
            if info.xpath('a'):
                detail.append(info.xpath('a/text()').extract())
            else:
                detail.append(info.xpath('text()').extract())
        for info in body.xpath('dt'):
            if info.xpath('a'):
                title.append(info.xpath('a/text()').extract())
            else:
                title.append(info.xpath('text()').extract())
        return detail, title

    @staticmethod
    def movie_detail_processing(details, titles):
        x = {}
        for i in range(len(details)):
            title = titles[i]
            detail = details[i]
            a = {
                title[0].strip(":"): detail[0]
            }
            x.update(a)
        return x

    @staticmethod
    def actors(response):
        body = response.xpath('//*[@id="list_actor_carousel"]')
        actors = []
        for info in body.xpath('li'):
            actor = info.xpath('.//*[@class="actor-name"]/span/text()').extract()
            pair = {
                'actor_name': actor[0],
                'character': actor[1]
            }
            actors.append(pair)
        return actors

    @staticmethod
    def image(response):
        body = response.xpath('//*[@class="movie-l-img"]')
        return body.xpath('img/@src').extract_first()



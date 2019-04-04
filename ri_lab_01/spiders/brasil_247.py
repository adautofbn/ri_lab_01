# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class Brasil247Spider(scrapy.Spider):
    name = 'brasil_247'
    allowed_domains = ['brasil247.com']
    start_urls = []

    def __init__(self, *a, **kw):
        super(Brasil247Spider, self).__init__(*a, **kw)
        with open('seeds/brasil_247.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def scrap_url(self, response):
        info = yield {
            'title': response.xpath('//*[@id="wrapper"]/div[5]/h1/text()').get(),
            'sub_title': response.xpath('//*[@id="wrapper"]/div[5]/p[2]/text()').get(),
            'author': response.xpath('//*[@id="wrapper"]/div[6]/section[1]/div[1]/p[2]/strong/text()').get(),
            'date': response.xpath('//*[@id="wrapper"]')[0].css('p::text')[0].get(),
            'section': response.css('body::attr(id)').get().split("-")[-1],
            'text': response.xpath('//*[@id="wrapper"]/div[6]')[0].css('p::text').getall(),
            'url': response.url
        }

    def parse(self, response):

        for href in response.css('article a::attr(href)').getall():
            yield response.follow(href, callback = self.scrap_url)

        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

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

    def scrap_date(self,date_string):
	    day,monthStr,year,clock = date_string.lower().replace('de', '').replace('às', '').replace('\n','').replace('  ',' ').split(' ')
	
	    monthForNum = lambda monthStr: {
		    'janeiro' : '01',
		    'fevereiro' : '02',
		    'março' : '03',
		    'abril' : '04',
		    'maio' : '05',
		    'junho' : '06',
		    'julho' : '07',
		    'agosto' : '08',
		    'setembro' : '09',
		    'outubro' : '10',
		    'novembro' : '11',
		    'dezembro' : '12'
	    }.get(monthStr, "noMatch")

	    formatDay = lambda dayStr : '0' + dayStr if len(dayStr) == 1 else dayStr

	    return formatDay(day) +'/'+ monthForNum(monthStr) + '/' +year + ' ' + clock +':00'

    def scrap_url(self, response):
        date_string = response.xpath('//*[@id="wrapper"]')[0].css('p::text')[2].get()
        date_formatted = self.scrap_date(date_string.encode('utf-8'))
        info = yield {
            'title': response.xpath('//*[@id="wrapper"]/div[5]/h1/text()').get(),
            'sub_title': response.xpath('//*[@id="wrapper"]/div[5]/p[2]/text()').get(),
            'author': response.xpath('//*[@id="wrapper"]/div[6]/section[1]/div[1]/p[2]/strong/text()').get(),
            'date': date_formatted,
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

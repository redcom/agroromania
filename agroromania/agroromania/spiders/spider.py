# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['http://agroromania.manager.ro/pesticide/categorie-defolianti-si-desicanti/']

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        table = soup.find('div', {'class': 'content_article'})
        for name_of_plant in table.find_all('div', {'class': 'col3 domeniiLst'})[1:2]: #ToDo убрать срез
            yield scrapy.Request(
                url=name_of_plant.a['href'],
                callback=self.parse_pesticide,
                meta={'name_of_plant': name_of_plant.a.text.strip()})

    def parse_pesticide(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        table = soup.find('div', {'class': 'content'})
        for name_of_pesticide in table.find_all('div', {'class': 'col3 productLst'})[1:2]: #ToDo убрать срез
            yield scrapy.Request(
                url=name_of_pesticide.a['href'],
                callback=self.parse_pesticide,
                meta={'name_of_plant': response.meta['name_of_plant'],
                      'name_of_pesticide': name_of_pesticide.a.text.strip()})

    def parse_content(self, response):
        pass


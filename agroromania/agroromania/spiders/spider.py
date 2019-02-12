# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from collections import OrderedDict

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
                callback=self.parse_content,
                meta={'name_of_plant': response.meta['name_of_plant'],
                      'name_of_pesticide': name_of_pesticide.a.text.strip()})

    def parse_content(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        content = soup.find('div', {'class': 'content_article'})
        article = content.find('h1').text.strip()


        # pes_detailed = content.find('div', {'class': 'pes_detailed'}).find_all('table', {'border': '1'})[0]
        # for specification in pes_detailed.find_all('tr', {'class': 'labelgeneral'}):
        #     try:
        #         category = specification.text.split(':')[0].strip()
        #         value = specification.text.split(':')[1].strip()
        #         print(category, '::', value)
        #     except:
        #         print('-----------', specification.text)




        # pes_detailed = content.find('div', {'class': 'pes_detailed'}).find_all('table', {'border': '1'})[1]
        # for specification in pes_detailed.find_all('tr', {'class': 'labelgeneral'}):
        #     try:
        #         category = specification.text.split(':')[0].strip()
        #         value = specification.text.split(':')[1].strip()
        #         print(category, '::', value)
        #     except:
        #         print('-----------', specification.text)




        # pes_detailed = content.find('div', {'class': 'pes_detailed'}).find_all('table', {'border': '1'})[2]
        # for specification in pes_detailed.find_all('tr', {'class': 'labelgeneral'}):
        #     try:
        #         category = specification.text.split(':')[0].strip()
        #         value = specification.text.split(':')[1].strip()
        #         print(category, '::', value)
        #     except:
        #         print('-----------', specification.text)
        #
        # for specification in pes_detailed.find_all('tr', {'class': 'TabelCellOff'}):
        #     try:
        #         category = specification.text.split(':')[0].strip()
        #         value = specification.text.split(':')[1].strip()
        #         print(category, '::', value)
        #     except:
        #         print('-----------', specification.text)




        # pes_detailed = content.find('div', {'class': 'pes_detailed'}).find_all('table', {'border': '1'})[3]
        # list_of_fileds = [specification.text for specification in pes_detailed.find('tr', {'class': 'TabelCellOn'}).find_all('td')]
        # table_dict = OrderedDict()
        #
        # for specification in pes_detailed.find_all('tr', {'class': 'TabelCellOff'}):
        #     for index, spec in enumerate(specification.find_all('td')):
        #         table_dict[list_of_fileds[index]] = spec.text.strip()
        #
        # for specification in pes_detailed.find_all('tr', {'class': 'TabelCellOn'})[1:]:
        #     for index, spec in enumerate(specification.find_all('td')):
        #         table_dict[list_of_fileds[index]] = spec.text.strip()
        #
        # print(dict(table_dict))


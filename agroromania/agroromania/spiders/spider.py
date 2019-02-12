# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

import scrapy
from bs4 import BeautifulSoup


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['http://agroromania.manager.ro/pesticide/categorie-defolianti-si-desicanti/']
    file = open('result.json', 'w')

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        table = soup.find('div', {'class': 'content_article'})
        for name_of_plant in table.find_all('div', {'class': 'col3 domeniiLst'}):  # ToDo убрать срез
            yield scrapy.Request(
                url=name_of_plant.a['href'],
                callback=self.parse_pesticide,
                meta={'name_of_plant': name_of_plant.a.text.strip()})

    def parse_pesticide(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        table = soup.find('div', {'class': 'content'})
        for name_of_pesticide in table.find_all('div', {'class': 'col3 productLst'}):  # ToDo убрать срез
            yield scrapy.Request(
                url=name_of_pesticide.a['href'],
                callback=self.parse_content,
                meta={'name_of_plant': response.meta['name_of_plant'],
                      'name_of_pesticide': name_of_pesticide.a.text.strip()})

    def parse_content(self, response):
        result_dict = {}
        soup = BeautifulSoup(response.body, 'lxml')
        content = soup.find('div', {'class': 'content_article'})
        article = content.find('h1').text.strip()
        result_dict['article'] = article

        pes_detailed = content.find('div', {'class': 'pes_detailed'}).find_all('table', {'border': '1'})[0]
        for specification in pes_detailed.find_all('tr', {'class': 'labelgeneral'}):
            try:
                category = specification.text.split(':')[0].strip()
                value = specification.text.split(':')[1].strip()
                result_dict[category] = value
            except:
                pass

        pes_detailed = content.find('div', {'class': 'pes_detailed'}).find_all('table', {'border': '1'})[1]
        for specification in pes_detailed.find_all('tr', {'class': 'labelgeneral'}):
            try:
                category = specification.text.split(':')[0].strip()
                value = specification.text.split(':')[1].strip()
                result_dict[category] = value
            except:
                pass

        pes_detailed = content.find('div', {'class': 'pes_detailed'}).find_all('table', {'border': '1'})[2]
        for specification in pes_detailed.find_all('tr', {'class': 'labelgeneral'}):
            try:
                category = specification.text.split(':')[0].strip()
                value = specification.text.split(':')[1].strip()
                result_dict[category] = value

            except:
                pass

        for specification in pes_detailed.find_all('tr', {'class': 'TabelCellOff'}):
            try:
                category = specification.text.split(':')[0].strip()
                value = specification.text.split(':')[1].strip()
                result_dict[category] = value
            except:
                pass

        pes_detailed = content.find('div', {'class': 'pes_detailed'}).find_all('table', {'border': '1'})[3]
        list_of_fileds = [specification.text for specification in
                          pes_detailed.find('tr', {'class': 'TabelCellOn'}).find_all('td')]
        table_dict = OrderedDict()
        result_dict['utilizari'] = []
        for specification in pes_detailed.find_all('tr', {'class': 'TabelCellOff'}):
            for index, spec in enumerate(specification.find_all('td')):
                if index == 0:
                    key = spec.text.strip()
                table_dict[list_of_fileds[index]] = spec.text.strip()
            result_dict['utilizari'].append({f'{key}': table_dict})

        for specification in pes_detailed.find_all('tr', {'class': 'TabelCellOn'})[1:]:
            for index, spec in enumerate(specification.find_all('td')):
                if index == 0:
                    key = spec.text.strip()
                table_dict[list_of_fileds[index]] = spec.text.strip()
            result_dict['utilizari'].append({f'{key}': table_dict})
        result_dict['name_of_pesticide'] = response.meta['name_of_pesticide']

        json.dump({response.meta["name_of_plant"]: result_dict}, self.file, indent=4)

    def spider_closed(self, spider):
        self.file.close()

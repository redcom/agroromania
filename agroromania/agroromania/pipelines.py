# -*- coding: utf-8 -*-
from scrapy.exporters import JsonItemExporter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AgroromaniaPipeline(object):
    def process_item(self, item, spider):
        return item


class ItemPipeline(object):

    file = None

    def open_spider(self, spider):
        self.file = open('item.json', 'w')
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
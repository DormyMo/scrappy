# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrappy.model.test import Test


class ScrappyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

    def handleInsert(self, item):
        return item

    def handleUpdate(self, item):
        return item


class ModelItem(scrapy.Item):
    model = scrapy.Field()

    @classmethod
    def getInstance(cls, model):
        modelItem = cls()
        modelItem['model'] = model
        return modelItem


if __name__ == '__main__':
    print ModelItem.getInstance(Test())

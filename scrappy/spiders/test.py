# coding:utf8
from scrappy.items.items import ModelItem
from scrappy.model.test import Test

__author__ = 'modm'
from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrappy.extensions.scrapy_redis.spiders import RedisSpider


class TestSpider(CrawlSpider):
    # spider name
    name = 'test'
    # custom settings will overwrite default settings
    custom_settings = {
        'CONCURRENT_REQUESTS': 15,
        'DOWNLOAD_TIMEOUT': 30,
    }

    def __init__(self, category=None, *args, **kwargs):
        super(TestSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request('https://github.com/', dont_filter=True)

    def parse(self, response):
        print response.xpath('//title/text()').extract_first()


class TestMysqlSpider(CrawlSpider):
    # spider name
    name = 'test_mysql'
    # custom settins will overwrite default settings
    custom_settings = {
        'CONCURRENT_REQUESTS': 15,
        'DOWNLOAD_TIMEOUT': 30,
        'ITEM_PIPELINES': {
            'scrappy.pipelines.MysqlORMPipeline': 300
        }
    }

    def __init__(self, category=None, *args, **kwargs):
        super(TestMysqlSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request('https://github.com/', dont_filter=True)

    def parse(self, response):
        test = Test()  # orm model
        test.name = response.xpath('//title/text()').extract_first()
        yield ModelItem.getInstance(test)

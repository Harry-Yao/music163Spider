# -*- coding: utf-8 -*-

import datetime
import pymongo
from scrapy import signals
from twisted.internet import task
__author__ = 'harry yao'
__date__ = '2018/3/27 9:07'


class DailyStatsExtension(object):

    def __init__(self, crawler, coll):
        self.crawler = crawler
        self.coll = coll
        self.stats = crawler.stats
        self.items = 0
        self.time = 60.0 * 60.0  # 时间间隔一小时

        crawler.signals.connect(self._spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(self._spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(self._item_scraped, signal=signals.item_scraped)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        try:
            client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
            db = client[settings['MONGO_DB']]
            if db.authenticate(settings['MONGO_USER'], settings['MONGO_PASSWORD']):
                coll = db[settings['MONGO_COUNT_COLL']]  # 获得collection的句柄
        except Exception as e:
            print('Connect Statics Database Fail.')
        return cls(crawler, coll)

    def _spider_opened(self, spider):
        self.task = task.LoopingCall(self._log, spider)
        self.task.start(self.time, now=True)

    def _spider_closed(self, spider):
        if self.task.running:
            self.task.stop()

    def _item_scraped(self):
        self.items += 1

    def _log(self, spider):
        try:
            self.coll.insert({'spider': 'spider3', 'time': datetime.datetime.now(), 'item_counts': self.items})
        except Exception as e:
            print('Insert Data Fail.')




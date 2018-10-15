# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import redis
from .utils.fake_user_agent import FakeUserAgent
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
from scrapy import signals
from scrapy.http import HtmlResponse


class Music163SpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):

    def __init__(self, crawler):
        self.ua = FakeUserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        user_agent = self.ua.get_user_agent()
        # spider.logger.info('Spider Set User-Agent: %s' % user_agent)
        request.headers.setdefault('User-Agent', user_agent)
        # request.headers.setdefault('Referer', 'http://music.163.com/song?id={}'.format(song_id),)


class RandomProxyMiddleware(object):

    def __init__(self, proxy):
        self.proxy = proxy

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy=crawler.settings.get('PROXIES')
        )

    def process_request(self, request, spider):
        proxy = random.choice(self.proxy)
        request.meta['proxy'] = proxy


class RandomProxyMiddleware2(object):

    def __init__(self, host='127.0.0.1', port=6379, proxy_key='useful_proxy'):
        self.conn = redis.StrictRedis(host=host, port=port)
        self.proxy_key = proxy_key

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('REDIS_HOST'),
            port=crawler.settings.get('REDIS_PORT'),
            proxy_key=crawler.settings.get('PROXY_KEY')
        )

    def process_request(self, request, spider):
        proxys = self.conn.hgetall(self.proxy_key)
        proxy = str(random.choice(list(proxys.keys())), encoding='utf-8')
        try:
            if proxy:
                request.meta["proxy"] = f'http://{proxy}'
                spider.logger.info('Set Proxy IP: %s' % proxy)
        except Exception as e:
            print(e)



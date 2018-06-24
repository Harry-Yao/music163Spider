from scrapy.cmdline import execute
import sys
import os

__author__ = 'harry yao'
__date__ = '2018/1/28 15:40'

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "comment"])
# execute(["scrapy", "crawl", "song"])

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# import MySQLdb
# from MySQLdb import cursors
# from twisted.enterprise import adbapi
from .items import CommentItem, SongItem


class Music163SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    def __init__(self, coll):
        self.coll = coll

    @classmethod
    def from_settings(cls, settings):
        try:
            client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
            db = client[settings['MONGO_DB']]  # 获得数据库的句柄
            # 数据库登录需要帐号密码的话
            if db.authenticate(settings['MONGO_USER'], settings['MONGO_PASSWORD']):
                coll = db[settings['MONGO_COLL']]  # 获得collection的句柄
                return cls(coll)
        except Exception as e:
            print('Connect MongoDB Failed.')

    def process_item(self, item, spider):
        # if isinstance(item, SongItem):
        post_item = dict(item)
        self.coll.insert(post_item)
        # msg = '正在爬取用户{}的评论：{}'.format(item['nickname'], item['content'])
        return item  # 会在控制台输出原item数据，可以选择不写

    def handle_error(self, failure, item, spider):
        print(failure)


# 采用异步机制写入mysql
# class MysqlTwistedPipeline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         dbparam = dict(
#             host=settings["MYSQL_HOST"],
#             db=settings["MYSQL_DBNAME"],
#             user=settings["MYSQL_USER"],
#             password=settings["MYSQL_PASSWORD"],
#             charset='utf8',
#             cursorclass=MySQLdb.cursors.DictCursor,
#             use_unicode=True
#         )
#         dbpool = adbapi.ConnectionPool("MySQLdb", **dbparam)
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         # 使用Twisted将Mysql插入变成异步执行
#         if isinstance(item, CommentItem):
#             query = self.dbpool.runInteraction(self.do_insert, item)
#             query.addErrback(self.handle_error, item, spider)  # 处理异常
#
#     def do_insert(self, cursor, item):
#         insert_sql, params = item.get_insert_sql()
#         cursor.execute(insert_sql, params)
#
#     def handle_error(self, failure, item, spider):
#         print(failure)
#
#
# class MysqlPipeLine(object):
#     def __init__(self):
#         self.conn = MySQLdb.connect('192.168.126.134', 'root',
#                                     '123123', 'article_spider',
#                                     charset='utf8', use_unicode=True)
#
#     def process_item(self, item, spider):
#         if isinstance(item, CommentItem):
#             insert_sql, params = item.get_insert_sql()
#             cursor.execute(insert_sql, params)
#             self.conn.commit()

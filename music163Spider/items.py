# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Music163SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CommentItem(scrapy.Item):
    comment_id = scrapy.Field()
    user_id = scrapy.Field()
    nickname = scrapy.Field()
    song_id = scrapy.Field()
    content = scrapy.Field()
    likedCount = scrapy.Field()
    add_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                        insert into comments(comment_id, user_id, song_id, content, likedCount, add_time)
                         VALUES (%s, %s, %s, %s, %s, %s)
                         ON DUPLICATE KEY UPDATE content=VALUES(content), 
                            likedCount=VALUES(likedCount), add_time=VALUES(add_time)
                    """
        params = (self.comment_id, self.user_id, self.song_id, self.content, self.likedCount, self.add_time)
        return insert_sql, params


class SongItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    artists = scrapy.Field()
    album = scrapy.Field()



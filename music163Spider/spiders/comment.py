# -*- coding: utf-8 -*-
import scrapy
import re
import json
from datetime import datetime
from urllib import parse
from scrapy import FormRequest
from scrapy_redis.spiders import RedisSpider
from scrapy.exceptions import CloseSpider

from music163Spider.items import CommentItem
from music163Spider.utils.encrypt import get_data


class CommentSpider(RedisSpider):
    name = 'comment'
    allowed_domains = ['music.163.com']
    redis_key = 'comment:start_urls'

    # custom_settings = {
    #     'MONGO_HOST': '127.0.0.1',
    #     'REDIS_HOST': '127.0.0.1',
    #     'REDIS_PORT': 6379
    # }

    # def start_requests(self):
    #     text = {'rid': '', 'offset': 1, 'total': 'false', 'limit': 100, 'csrf_token': ''}
    #     post_data = get_data(text)
    #     post_url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_531051217/?csrf_token='
    #     yield FormRequest(
    #         url=post_url,
    #         formdata=post_data,
    #         callback=self.parse_comments,
    #     )

    # 获取歌手专辑列表
    def parse(self, response):
        artist_list = response.xpath('//li/a[contains(@class,"nm")]/@href | //a[@class="msk"]/@href').extract()
        i = 1
        for artist_id in artist_list:
            artist_id = re.findall(r'\d+', artist_id)[0]
            print(f'http://music.163.com/artist/album?id={artist_id}', i)
            i += 1
            yield scrapy.Request(
                f'http://music.163.com/artist/album?id={artist_id}',
                callback=self.parse_artist,
                # meta={'artist_id': artist_id},WORKON
                priority=1
            )

    def parse_artist(self, response):
        next_page = response.xpath('//a[contains(@class,"znxt")]/@href').extract_first()
        base_url = 'http://music.163.com'
        album_urls = response.xpath('//a[@class="msk"]/@href').extract()
        if album_urls:
            for url in album_urls:
                url = f'http://music.163.com{url}'
                print(url)
                yield scrapy.Request(url, callback=self.parse_songs, priority=2)
        # else:
        #     print("could not find album")
        if next_page and next_page != 'javascript:void(0)':
            url = parse.urljoin(next_page, base_url)
            print(url)
            yield scrapy.Request(url, callback=self.parse_artist, priority=1)

    # 提交表单请求歌曲评论
    def parse_songs(self, response):
        json_data = response.xpath('//textarea[contains(@style,"display:none;")]/text()').extract_first()
        song_list = json.loads(json_data)
        text = {'rid': '', 'offset': 1, 'total': 'false', 'limit': 100, 'csrf_token': ''}
        post_data = get_data(text)
        for song in song_list:
            post_url = f'http://music.163.com/weapi/v1/resource/comments/{song["commentThreadId"]}/?csrf_token='
            print(post_url)
            yield FormRequest(
                url=post_url,
                formdata=post_data,
                callback=self.parse_comments,
                meta={'song': song},
                priority=3
            )

    # 获取评论
    def parse_comments(self, response):
        json_dict = json.loads(response.text)
        song = response.meta.get("song", "")
        if json_dict['code'] == -460:
            raise CloseSpider

        # 获取所有评论
        if json_dict['code'] == 200:
            comments = json_dict['comments']
            for comment in comments:
                comment_item = CommentItem()
                comment_item['comment_id'] = comment['commentId']
                comment_item['user_id'] = comment['user']['userId']
                comment_item['nickname'] = comment['user']['nickname']
                comment_item['song_id'] = song['id']
                comment_item['content'] = comment['content']
                comment_item['likedCount'] = comment['likedCount']
                timestamp = int(comment['time']) / 1000
                comment_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                comment_item['add_time'] = comment_time
                yield comment_item

        if 'total' in json_dict and int(json_dict['total']) > 100:
            total = int(json_dict['total'])
            offsets = total // 100 + 2 if total % 100 != 0 else total // 100 + 1
            text = {'rid': '', 'offset': 2, 'total': 'false', 'limit': 100, 'csrf_token': ''}
            for offset in range(2, offsets):
                text['offset'] = offset
                post_url = f'http://music.163.com/weapi/v1/resource/comments/{song["commentThreadId"]}/?csrf_token='
                print(post_url)
                yield FormRequest(
                    url=post_url,
                    formdata=get_data(text),
                    callback=self.parse_total_comments,
                    meta={'song': song},
                    priority=3
                )

    def parse_total_comments(self, response):
        json_dict = json.loads(response.text)
        song = response.meta.get("song", "")

        # 获取所有评论
        if json_dict['comments']:
            comments = json_dict['comments']
            for comment in comments:
                comment_item = CommentItem()
                comment_item['comment_id'] = comment['commentId']
                comment_item['user_id'] = comment['user']['userId']
                comment_item['nickname'] = comment['user']['nickname']
                comment_item['song_id'] = song['id']
                comment_item['content'] = comment['content']
                comment_item['likedCount'] = comment['likedCount']
                timestamp = int(comment['time']) / 1000
                comment_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                comment_item['add_time'] = comment_time
                yield comment_item






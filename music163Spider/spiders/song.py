# -*- coding: utf-8 -*-
import scrapy
import re
import json
from urllib import parse
from scrapy import FormRequest, Request
from scrapy_redis.spiders import RedisSpider

from music163Spider.items import SongItem
from music163Spider.utils.encrypt import get_data


class CommentSpider(scrapy.Spider):
    name = 'song'
    allowed_domains = ['music.163.com']

    custom_settings = {
        'MONGO_HOST': '127.0.0.1',
    }

    def start_requests(self):
        url = 'http://music.163.com/#/discover/artist/cat?id=1001&initial=66'
        yield scrapy.Request(url, callback=self.parse)

    # 获取歌手专辑列表
    def parse(self, response):
        artist_list = response.css("ul#m-artist-box a.nm::attr(href)").extract()
        # artist_list_urls = [parse.urljoin(artist_urls, url) for url in artist_list_urls]
        base_url = 'http://music.163.com/artist/album?id='
        for artist_id in artist_list:
            artist_id = re.findall(r'\d+', artist_id)[0]
            yield scrapy.Request(base_url+artist_id, callback=self.parse_artist, meta={'artist_id': artist_id})

    # 获取专辑列表
    def parse_artist(self, response):
        page = response.css("a.zpgi::text").extract()
        if len(page) == 0:
            page = 1
        else:
            page = int(page[-1])
        for i in range(page):
            url = 'http://music.163.com/artist/album?id=6452&limit=12&offset=' + str((i+1)*12) # + response.meta['artist_id'] \
                  # + '&limit=12&offset=' + str((i+1)*12)
            yield scrapy.Request(url, callback=self.parse_album)

    # 获取歌曲列表
    def parse_album(self, response):
        base_url = 'http://music.163.com'
        album_urls = response.css("a.msk::attr(href)").extract()
        if album_urls:
            album_urls = [parse.urljoin(base_url, url) for url in album_urls]
            for url in album_urls:
                yield scrapy.Request(url, callback=self.parse_songs)
        else:
            print("could not find album")

    # 提交表单请求歌曲评论
    def parse_songs(self, response):
        json_data = response.css('textarea[style="display:none;"]::text').extract_first()
        song_list = json.loads(json_data)
        # post_data = get_data()
        for song in song_list:
            post_url = 'http://music.163.com/api/song/media?id={}'.format(song['id'])
            yield Request(url=post_url, callback=self.parse_lyric, meta={'song': song})

    def parse_lyric(self, response):
        song = response.meta['song']
        j = json.loads(response.text)
        lrc = ''
        if not 'nolyric' in j:
            lyric = j['lyric']
            lrc = re.sub(r'\[.*\]', "", lyric).strip()
        song_item = SongItem()
        song_item['song_id'] = song['id']
        song_item['song_name'] = song['name']
        song_item['score'] = song['score']  # 热度
        song_item['artists'] = song['artists']
        song_item['album'] = song['album']['name']
        song_item['lyric'] = lrc

        yield song_item











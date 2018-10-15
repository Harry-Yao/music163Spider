# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
import base64
import os
import requests
import json
import codecs

__author__ = 'harry yao'
__date__ = '2018/3/8 16:42'


def aes_encrypt(txt, sec_key):
    pad = 16 - len(txt) % 16
    txt = txt + pad * chr(pad)
    encryptor = AES.new(sec_key.encode(), 2, b'0102030405060708')
    encrypt_text = encryptor.encrypt(txt.encode())
    encrypt_text = base64.b64encode(encrypt_text)
    encrypt_text = str(encrypt_text, encoding="utf-8")
    return encrypt_text


def rsa_encrypt(txt, pub_key, modulus):
    txt = txt[::-1]
    rs = int(codecs.encode(txt.encode('utf-8'), 'hex_codec'), 16) ** int(pub_key, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def create_secretkey(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16]


def get_encseckey(sec_key, pub_key, modulus):
    return rsa_encrypt(sec_key, pub_key, modulus)


def get_params(txt, sec_key, nonce):
    return aes_encrypt(aes_encrypt(txt, nonce), sec_key)


def get_data(txt):
    txt = json.dumps(txt)
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a' \
              '876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c' \
              '9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e2' \
              '89dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pub_key = '010001'
    # sec_key = create_secretkey(16)
    sec_key = '62275c7863385c78'
    params = get_params(txt, sec_key, nonce)
    enc_seckey = get_encseckey(sec_key, pub_key, modulus)
    return {
        'params': params,
        'encSecKey': enc_seckey
    }


if __name__ == '__main__':
    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_531051217/?csrf_token='
    headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Origin': 'http://music.163.com',
        'Host': 'music.163.com',
        'Referer': f'http://music.163.com/song?id=514761281',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    }
    # url = 'http://music.163.com/discover/artist/cat?id=1001&initial=65'
    # url = 'http://music.163.com/song?id=185613'
    # url = 'http://music.163.com/artist/album?id=2116'
    # url = 'http://music.163.com/album?id=34720827'
    # url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_531051217/?csrf_token='
    # url = 'http://music.163.com/api/song/media?id=519935205'
    # url = 'http://music.163.com/api/artist/albums/519935205?id=519935205&offset=0&total=true&limit=100'
    # url = 'http://music.163.com/weapi/song/lyric?csrf_token='
    # conn = RedisCilent()
    # proxy_url = "http://{0}".format(conn.pop())

    text = {'rid': '', 'offset': 29, 'total': 'false', 'limit': 15, 'csrf_token': ''}
    # text = {'id': '508297601', 'lv': -1, 'tv': -1, 'csrf_token': ''}
    try:
        r = requests.post(url, headers=headers, params=get_data(text))
        # r = requests.get(url, headers=headers)
    except Exception as e:
        # print("invalid ip and port")
        print(e)
    else:
        code = r.status_code
        if 200 <= code < 300:
            j = json.loads(r.text)
            print(j['total'])
            # if 'hotComments' in j:
            #     for comment in j['hotComments']:
            #         print(comment['content'])
            with open('comments.json', 'wb') as f:
                f.write(r.text.encode())
                f.close()

        # else:
        #     j = json.loads(r.text)
        #     comments = j['comments']
        #     print(comments)
            # j = json.loads(r.text)
            # i = 0
            # for comment in j['comments']:
            #     i += 1
            #     timestamp = int(comment['time']) / 1000
            #     comment_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            #     print(i, comment['user']['nickname']+": "+comment['content']+": "+comment_time)
    # r = requests.get(url, headers=headers)


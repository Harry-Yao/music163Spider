# -*- coding: utf-8 -*-

import jieba
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pymongo
import numpy as np
import datetime

min_date_Ymd = '2018-01-18'
max_date_Ymd = '2018-05-13'

client = pymongo.MongoClient(host='210.38.224.115', port=27017)
db = client['Spider']
if db.authenticate('yao', 'cisco@123'):
    # coll = db['music163']
    # coll2 = db['comment_count']
    coll = db['comment_190499']
    # coll = db['comment_count']
    # coll = db['daily_count']

# comments = coll.find({'song_id': 531051217})
# comments = coll.find({'song_id': 418603077})
#
# for i in comments:
#     try:
#         coll2.insert({'_id': i['comment_id'],
#                       'username': i['nickname'],
#                       'song_id': i['song_id'],
#                       'content': i['content'],
#                       'time': i['add_time']})
#     except Exception as e:
#         print(e)
# start_time = datetime.datetime(2018, 1, 18)
# end_time = datetime.datetime(2018, 5, 13)
# delta = datetime.timedelta(days=1)
#
# while start_time < end_time:
#     temp_time = start_time.date().strftime("%Y-%m-%d")
#     comments = coll.find({'date': temp_time})
#     count = comments.count()
#     coll2.insert({'date': temp_time, 'count': count})
#     start_time += delta

# for i in coll.find():
#     itime = i['time'].split(' ')[0]
#     coll2.insert({'content': i['content'], 'time': itime})


# for i in range(5):
#     t = f'0{i+1}'
#     m_count = 0
#     for count in coll.find():
#         m = count['date'].split('-')[1]
#         if t == m:
#             m_count += count['count']
#     coll2.insert({'date': '2018-'+t, 'count': m_count})





# x_date_Ymd_no_repeat = []
# y_date_Ymd_count = []
# x_likedCount_no_repeat = []
# y_likedCount_count = []
#
#
#
# for date in x_date_Ymd:
#     if date not in x_date_Ymd_no_repeat:
#         x_date_Ymd_no_repeat.append(date)
#         y_date_Ymd_count.append(x_date_Ymd.count(date))
#
# for likedCount in x_likedCount:
#     if likedCount not in x_likedCount_no_repeat:
#         x_likedCount_no_repeat.append(likedCount)
#         y_likedCount_count.append(x_likedCount.count(likedCount))

# for i in comments:
#     itime = datetime.datetime.strptime(i['add_time'], '%Y-%m-%d %H:%M:%S')
#     print(i == itime)
#
# x = [datetime.datetime.strptime(i['add_time'], '%Y-%m-%d') for i in comments]
#
# plt.gca().xaxis.set_major_locator(mdates.DayLocator())

# matplotlib.rcParams['font.sans-serif'] = ['SimHei']   # 用黑体显示中文
# matplotlib.rcParams['axes.unicode_minus'] = False
# x = []
# y = []
#
# for count in coll.find():
#     x.append(count['date'])
#     y.append(count['count'])
#
# xs = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in x]
#
# plt.figure()
#
# plt.plot(xs, y, '')
#
# plt.gcf().autofmt_xdate()
#
# plt.xlabel('年月日', fontsize=18)
# plt.ylabel('评论数', fontsize=18)
# plt.show()
result = ''
for i in coll.find():
    cut_text = jieba.cut(i['content'], cut_all=False)
    result += "/".join(cut_text)

image = Image.open(r'E:\git\music163Spider\music163Spider\utils\timg.jpg')
graph = np.array(image)

# 4、产生词云图
# 有自定义背景图：生成词云图由自定义背景图像素大小决定
wc = WordCloud(font_path=r"E:\git\music163Spider\music163Spider\utils\Yahei.ttf",
               background_color='white', max_font_size=50, mask=graph)
wc.generate(result)

# 5、绘制文字的颜色以背景图颜色为参考
image_color = ImageColorGenerator(graph)  # 从背景图片生成颜色值
wc.recolor(color_func=image_color)
wc.to_file(r"E:\git\music163Spider\music163Spider\utils\wordcloud2.png")  # 按照背景图大小保存绘制好的词云图，比下面程序显示更清晰

# 6、显示图片
plt.figure("词云图")  # 指定所绘图名称
plt.imshow(wc)  # 以图片的形式显示词云
plt.axis("off")  # 关闭图像坐标系
plt.show()

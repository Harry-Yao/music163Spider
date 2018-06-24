import pymongo
import datetime
import matplotlib
import numpy as np
import collections

import matplotlib.pyplot as plt

client = pymongo.MongoClient(host='210.38.224.115', port=27017)
db = client['Spider']
if db.authenticate('yao', 'cisco@123'):
    coll = db['music163_item_counts']  # 获得collection的句柄

x1 = []
y1 = []
x2 = []
y2 = []
x3 = []
y3 = []

start_time = datetime.datetime(2018, 5, 12)
end_time = datetime.datetime(2018, 5, 14)

for i in coll.find({'spider': 'spider1', 'time': {'$gte': start_time, '$lte': end_time}}):
    y1.append(i['item_counts'])
    x1.append(i['time'])

for i in coll.find({'spider': 'spider2', 'time': {'$gte': start_time, '$lte': end_time}}):
    y2.append(i['item_counts'])
    x2.append(i['time'])

for i in coll.find({'spider': 'spider3', 'time': {'$gte': start_time, '$lte': end_time}}):
    y3.append(i['item_counts'])
    x3.append(i['time'])

# plot
plt.plot(x1, y1, 'b')
plt.plot(x2, y2, 'r')
plt.plot(x3, y3, 'g')

plt.xlabel('运行时间', fontsize=18)
plt.ylabel('爬取的歌曲评论数', fontsize=18)

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
# beautify the x-labels
plt.gcf().autofmt_xdate()


print('y1:', y1[-1])
print('y2:', y2[-1])
print('y3:', y3[-1])
print('sum:', y1[-1]+y2[-1]+y3[-1])

plt.show()



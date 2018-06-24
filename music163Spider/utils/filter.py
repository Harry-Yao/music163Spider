import pymongo

client = pymongo.MongoClient(host='210.38.224.115', port=27017)
db = client['Spider']
if db.authenticate('yao', 'cisco@123'):
    coll = db['music163']
    # coll2 = db['comment_count']
    coll2 = db['comment_190499']
    # coll = db['comment_count']
    # coll = db['daily_count']


for i in coll.find({'song_id': 190499}):
    itime = i['add_time'].split(' ')[0]
    try:
        coll2.insert({'_id': i['comment_id'],
                      'username': i['nickname'],
                      'song_id': i['song_id'],
                      'content': i['content'],
                      'time': itime})
    except Exception as e:
        print(e)

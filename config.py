# Author : ZhangTong
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client['36ke']
News = db.news



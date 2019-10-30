from wordcloud import WordCloud
from pymongo import MongoClient
import os
import jieba
import matplotlib.pyplot as plt

def create_wc(dbname,keyword,maskjpg):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn[dbname]
    collectionlist = db.collection_names()
    for collection in collectionlist[3:20]:
        word_list = []
        table = db[collection]
        cols = table.find()
        for col in cols:
            word = col[keyword]
            word_list.append(word)
        cut_text = " ".join(word_list)
        bg_pic = plt.imread(maskjpg)
        font = os.path.join(os.path.dirname(__file__), "DroidSansFallbackFull.ttf")
        wc = WordCloud(
            mask=bg_pic,
            font_path=font,
            background_color='white',
            scale=1.5,
            random_state=30,
            max_words=2000,
            max_font_size=150,
        ).generate(cut_text)
        wc.to_file(collection + '.jpg')
        print("视频"+collection+"成功生成词云")

create_wc("bilibilitm","tanmu","3.jpg")
# conn = MongoClient('127.0.0.1', 27017)
# db = conn.bilibilitm
# collectionlist = db.collection_names()
# for collection in collectionlist[1:2]:
#     word_list = []
#     table = db[collection]
#     cols = table.find()
#     for col in cols:
#         word = col['tanmu']
#         word_list.append(word)
#     cut_text = " ".join(word_list)
#     bg_pic = plt.imread('3.jpg')
#     font=os.path.join(os.path.dirname(__file__), "DroidSansFallbackFull.ttf")
#     wc = WordCloud(
#         mask = bg_pic,
#         font_path=font,
#         background_color='white',
#         scale=1.5,
#         random_state = 30,
#         max_words = 2000,
#         max_font_size = 150,
#     ).generate(cut_text)
#     wc.to_file(collection + '.jpg')
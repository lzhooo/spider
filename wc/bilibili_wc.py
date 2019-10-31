from wordcloud import WordCloud
from pymongo import MongoClient
import os
import jieba
import matplotlib.pyplot as plt
import datetime

def create_wc(ip,dbname0,dbname,keyword,maskjpg):
    conn = MongoClient(ip, 27017)
    db0 = conn[dbname0]
    table0 = db0[str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(
            datetime.datetime.now().day)]
    cols0 = table0.find()
    name_list = []
    for col0 in cols0:
        if(col0["jpg"] == "0"):
            lis = []
            lis.append(str(col0["aid"]))
            lis.append(str(col0["title"]))
            name_list.append(lis)
            table0.update({'aid':col0["aid"]},{"$set":{"jpg":"1"}})
    db = conn[dbname]
    for collection in name_list:
        if collection[0] == 'system.indexes':
            continue
        word_list = []
        table = db[collection[0]]
        cols = table.find()
        for col in cols:
            word = col[keyword]
            word_list.append(word)
        try:
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
            wc.to_file('pic/'+collection[1].replace("/","-") + '.jpg')
            print("video <"+collection[0]+"> done")
        except:
            print("video <" + collection[0] + "> error")
if __name__ == '__main__':
    create_wc('0.0.0.0',"bilibilivideo","bilibilitm_gc","tanmu","3.jpg")
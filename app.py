#coding;utf-8

from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime as dt

#自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

#csvからデータを読み取り、リストとして返す関数を作る
# def opencsv(n): #(n-1)百番台のデータを返す
#     #codecs & csv moduleを使ったバージョン
#     with codecs.open('valudata20171101top.csv',"r",encoding="cp932") as f: #csvファイルの指定
#         reader = csv.reader(f)
#         header = next(reader) #ヘッダーを読み飛ばすためのコード
#         data = []
#         count = 0
#         for row in reader:
#             data.append(row)
#             count += 1
#             if count == 1000:
#                 break;
#         return data[(n-1)*100:n*100]

#朝の5時までにデータベースにデータが上がれば大丈夫な設計
tdatetime = dt.datetime.now() + dt.timedelta(hours=4)
tstr = tdatetime.strftime('%Y-%m-%d')


#CloudFirestoreからデータを取得してくる
cred = credentials.Certificate('credential.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

query = db.collection(tstr).order_by(u'jika',direction=firestore.Query.DESCENDING).limit(1000)
results = query.get()

data = []
j = 0
for i in results:
    data.append(i.to_dict())
    data[j].update({'rank':j+1})
    j = j + 1

#ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    num_list = data[0:3]
    return render_template('index.html', message=num_list, today=tstr)

#時価総額ランキングを返す (n-1)百番台
@app.route('/capitalrank/<number>')
def capitalrank(number):
    n = int(number)
    num_list = data[(n-1)*100:n*100]
    return render_template('capitalrank.html', message=num_list,number=n,today=tstr)

#免責事項
@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0')

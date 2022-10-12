from bs4 import BeautifulSoup
import re
import csv

# スクレイピングしたデータの整形
dataset = []
for i in range(47):
    with open("../shugiin2017_basic/"+str(i+1)+".txt", "r") as f:
        soup = BeautifulSoup(f, 'html.parser')

    # 前処理 (機械学習のためのデータが含まれる箇所抜き出し, タグ除去, 空白除去)
    html = soup.find_all(["td", "div"], attrs={ 'class': ["snkH2Box", 'namae', 'num', 'party', "status", "tosenkaisu"] })
    p1 = re.compile(r"<h3>.*</h3>")
    senkyo =  p1.sub("",str(html))
    p2 = re.compile(r'<li.*>.*</li>')
    senkyo =  p2.sub("",str(senkyo))
    p3 = re.compile(r'<a.*>.*</a>')
    senkyo =  p3.sub("",str(senkyo))
    p4 = re.compile(r'<span>')
    senkyo = p4.sub(",", str(senkyo))
    p5 = re.compile(r"<[^>]*?>")
    senkyo = p5.sub("", str(senkyo))
    p6 = re.compile("\s+")
    senkyo = p6.sub("", str(senkyo))
    output = senkyo[1:-1].split(",")

    # 前処理 (中身に対する細かい処理)
    row = []
    win_flag = 0
    votes_flag = 0
    num = 0
    for o in output:
        # 選挙区ごとに処理
        if o[-1] == "区":
            win_flag = 1
        # 人名+年齢が来たら、人名と年齢をばらす
        elif o[-1] == ")":
            row.append(o[:-4])
            row.append(int(o[-3:-1]))
            votes_flag = 1
        # 得票数&得票率計算
        elif votes_flag == 1:
            if o[-1] != "%":
                num = num*1000 + int(o)
            else:
                row.append(num)
                row.append(float(o[:-1]))
                num = 0
                votes_flag = 0
        # 政党、新旧、当選回数
        elif o != "回":
            row.append(o)
        # ラベリング
        elif o == "回":
            row.append(win_flag)
            dataset.append(row)
            row = []
            win_flag = 0

# データセットを書き出し
with open("../dataset/shugiin2017.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(dataset)
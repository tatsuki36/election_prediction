from bs4 import BeautifulSoup
import requests
import re
import time
import csv


base_url = "https://www.asahi.com/senkyo/senkyo2017/kaihyo/"
headers = {
	"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}

for i in range(47):
    if 0 <= i and i <= 8:
        soup = BeautifulSoup(requests.get(base_url+"A0"+str(i+1)+".html", headers = headers).content, 'html.parser')
    else:
        soup = BeautifulSoup(requests.get(base_url+"A"+str(i+1)+".html", headers = headers).content, 'html.parser') 
    with open("../shugiin2017_basic/"+str(i+1)+".txt", "w") as f:
        f.write(str(soup.contents))
    # print(i+1)
    time.sleep(5)

dataset = []
for i in range(47):
    with open("../shugiin2017/"+str(i+1)+".txt", "r") as f:
        soup = BeautifulSoup(f, 'html.parser')

    #前処理
    html = soup.find_all(["td", "div"], attrs={ 'class': ["snkH2Box", 'namae', 'num', 'party', "status", "tosenkaisu"] })
    p1 = re.compile(r"<h3>.*</h3>")
    senkyo =  p1.sub("",str(html))
    p2 = re.compile(r'<li.*>.*</li>')
    senkyo =  p2.sub("",str(senkyo))
    p3 = re.compile(r'<a.*>.*</a>')
    senkyo =  p3.sub("",str(senkyo))
    p4 = re.compile(r'<span>')
    senkyo = p4.sub(",", str(senkyo))
    p5 = re.compile(r"<[^>]*?>") #タグを取る正規表現
    senkyo = p5.sub("", str(senkyo))
    p6 = re.compile("\s+") #タグを取る正規表現
    senkyo = p6.sub("", str(senkyo))
    output = senkyo[1:-1].split(",")

    row = []
    win_flag = 0
    votes_flag = 0
    num = 0
    for o in output:
        #選挙区ごとに処理
        if o[-1] == "区":
            win_flag = 1
        #人名+年齢が来たら、人名と年齢をばらす
        elif o[-1] == ")":
            row.append(o[:-4])
            row.append(int(o[-3:-1]))
            votes_flag = 1
        #得票数&得票率計算
        elif votes_flag == 1:
            if o[-1] != "%":
                num = num*1000 + int(o)
            else:
                row.append(num)
                row.append(float(o[:-1]))
                num = 0
                votes_flag = 0
        #政党、新旧、当選回数
        elif o != "回":
            row.append(o)
        #ラベリング
        elif o == "回":
            row.append(win_flag)
            dataset.append(row)
            row = []
            win_flag = 0

# print(dataset)
# print(len(dataset))
with open("../dataset/shugiin2017.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(dataset)


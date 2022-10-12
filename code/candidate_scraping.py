from bs4 import BeautifulSoup
import requests
import time


base_url = "https://www.asahi.com/senkyo/senkyo2017/kaihyo/" # 朝日新聞デジタル
headers = {
	"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}


# スクレイピング
for i in range(47):
    if 0 <= i and i <= 8:
        soup = BeautifulSoup(requests.get(base_url+"A0"+str(i+1)+".html", headers = headers).content, 'html.parser')
    else:
        soup = BeautifulSoup(requests.get(base_url+"A"+str(i+1)+".html", headers = headers).content, 'html.parser') 
    
    # 何度もスクレイピングする必要はないのでファイルへ出力
    with open("../shugiin2017_basic/"+str(i+1)+".txt", "w") as f:
        f.write(str(soup.contents))
    time.sleep(5) # サーバの負荷を軽減するためにスクレイピングするタイミングの間隔を取る



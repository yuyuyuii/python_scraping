import requests
from bs4 import BeautifulSoup
import csv
from pprint import pprint

'''
# googleのURL
url = 'https://www.google.co.jp/search'
# google検索でpythonを検索
r = requests.get(url, params={'q': 'python'})
# 検索する際のURL
print(r.url)
# 検索結果
print(r.text)
# soup = BeautifulSoup(r.text, 'html.parser')
# s = soup.find("h1").get_text()
# print(s)

'''

# 検索キーワード
keyword = 'python'
# 検索数
num = "100"
# アクセスするurl
# url = 'https://www.google.co.jp/search'
url = 'https://www.google.co.jp/search?hl=ja&num=' + num + '&q=' + keyword
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
headers = {"User-Agent": user_agent}

# urlにアクセスし、pythonを検索し、レスポンスデータを変数に格納
response = requests.get(url, params={'q': keyword}, headers=headers)

# httpステータスコードをチェック(200以外は例外処理を行ってくれる)
response.raise_for_status()

# 取得したHTMLをパース(解析)
# response.textにデータが入っている
soup = BeautifulSoup(response.text, 'html.parser')

# 検索結果のタイトルとリンクを取得
# 実際の検索結果を見てみるとrクラスの下のaタグがタイトルとリンク部分
res_link = soup.select('.r > a')  #selectで取得可能
res_title = soup.select('.r > a > h3')

searchlist = []
url_list = []
title_text = []

# 取得したリンクの個数分ループでまわす
for i in range(len(res_link)):
  title_text = res_title[i].get_text()
  url_link = res_link[i].get('href') # URLを取得
  # リストへ格納
  searchlist.append([title_text, url_link]) #二次元配列になる
# 書き込みモードでファイルオープン
csvfile = open('scraping.csv', 'w', encoding='utf_8_sig') # エクセルでも文字化けしない
# writer = csv.writer(csvfile, lineterminator='\n')  # 改行区切り
writer = csv.writer(csvfile)  # 改行区切り
writer.writerow(['タイトル', 'URL'])
writer.writerows(searchlist)  # titleを書き込み
csvfile.close() #ファイルを閉じる

'''
# 辞書
title_list = []
dic = []
fieldnames = []
# 取得したリンクの個数分ループでまわす
for i in range(len(res_link)):
  title_text = res_link[i].get_text()
  title_list.append(res_link[i].get_text())
  fieldnames.append(res_link[i].get_text())
  # リンクを取得
  dic[title_text] = res_link[i].get('href')

csvfile = open('scraping.csv', 'w', encoding='utf_8_sig')

writer = csv.DictWriter(csvfile, fieldnames)

# # 出力
writer.writeheader()
writer.writerow(dic)


csvfile.close();

'''

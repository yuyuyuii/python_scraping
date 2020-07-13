import requests
from bs4 import BeautifulSoup
import csv
from pprint import pprint
import db

def url_check(url, params, headers):
  try:
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
  except requests.RequestException as e:
    print(e)
  else:
    return response

# 検索キーワード
keyword = 'python'
# 検索数
num = "100"
# アクセスするurl
url = 'https://www.google.co.jp/search?hl=ja&num=' + num + '&q=' + keyword
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
headers = {"User-Agent": user_agent}  # requestsにおくるheader情報
params = {'q': keyword} # requestsにおくる検索キーワード
# urlチェック
response = url_check(url, params, headers)
# 取得したHTMLをパース(解析)
# response.textにデータが入っている
soup = BeautifulSoup(response.text, 'html.parser')
# 検索結果のタイトルとリンクを取得
# class='r'のaタグ
res_urls = soup.select('.r > a')  # selectで取得可能
res_titles = soup.find_all("h3", class_="LC20lb DKV0Md")# h3タグでclassがLC20lb DKV0Md,のものを取得
title_url = [] # aタグを入れるリスト
title_text = [] # タイトルを入れるリスト
searchlists = []  # 検索結果を入れるリスト

# csv書き出し
# zip関数を使えば、複数のリストを同時にループできる。リストの個数が少ない方に合わせてくれる
# enumerate関数はindex番号付き
# for index, (title, url) in enumerate(zip(res_titles, res_urls)):
# # for title, url in zip(res_titles, res_urls):
#   title_text = title.get_text()  # テキストのみを取得
#   title_url = url.get('href')  # URLを取得
#   # index番号付きでリストへ格納
#   searchlists.append([index, title_text, title_url])  # 二次元配列になる

# select文
for title, url in zip(res_titles, res_urls):
  title_text = title.get_text()  # テキストのみを取得
  title_url = url.get('href')  # URLを取得
  searchlists.append([title_text, title_url])
# table = 'scrapings'
# sql = ('select * from ' + table)
# db = db.db_connect()
# cur = db.cursor()
# cur.execute(sql)
# print(cur.fetchall())

# insert文
sql = ("INSERT INTO scrapings (title, url) VALUES (%s, %s);")
db.db_insert(sql, searchlists)

# csv書き込みをwithを使用して書く closeを書かなくて済む
# with open('scraping.csv', 'w', encoding='utf_8_sig') as csvfile:
#   writer = csv.writer(csvfile)
#   writer.writerow(['タイトル', 'URL'])
#   writer.writerows(searchlists)

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

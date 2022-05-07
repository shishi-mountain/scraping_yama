## YAMAP登頂した山のサイトよりリスト取得
import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep
import re

yamap_url = 'https://yamap.com'
member = '22906'
# URLリストを取得
base_url = 'https://yamap.com/users/{}?tab=summits&page={}#tabs'
d_list = []
i=0
while True:
  i += 1
  url = base_url.format(member, i)
  print(url)

  res = requests.get(url, timeout=3)
  print(res.status_code)
  res.raise_for_status()
  if res.status_code != 200:
    break

  soup = BeautifulSoup(res.content, 'html.parser')
  if soup.select_one('.UserSummitList__TableBody') is None:
    break

  post = soup.select('.UserSummitList__TableBody')

  for pp in post:
    yama_url = yamap_url + pp.select_one('a').get('href')
    yama_name = pp.select_one('a').text
    #count = pp.select_one('tr td:last-of-type')
    count = pp.select_one('tr > td:last-of-type').text
    sleep(5)
    #d_list.append(yama_url)
    #print(yama_url)
    #print(yama_name.replace('\r\n','').replace('\n','').replace(' ', ''))
    #print(count)

    c_info = {
      'yama_url': yama_url,
      'name': yama_name.replace('\r\n','').replace('\n','').replace(' ', ''),
      'count': count
    }
    d_list.append(c_info)
    #print(c_info)



# CSV出力
df=pd.DataFrame(d_list)

print(df)

df.to_csv('yama_list.csv', index=None, encoding='utf-8-sig')
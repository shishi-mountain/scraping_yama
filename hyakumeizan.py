## YAMAP九州百名山リストサイトより一覧取得する
import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep
import re

yamap_url = 'https://yamap.com'
# URLリストを取得
base_url = yamap_url + '/mountains/famous/27513?page={}'
d_list = []
i = 0

while True:
  i += 1
  url = base_url.format(i)
  print(url)

  res = requests.get(url, timeout=3)
  print(res.status_code)
  res.raise_for_status()
  if res.status_code != 200:
    break

  soup = BeautifulSoup(res.content, 'html.parser')
  if soup.select_one('.MountainPrefectureItem__Inner') is None:
    break

  post = soup.select('.MountainPrefectureItem__Inner')
  for pp in post:
    yama_url = yamap_url + pp.select_one('a').get('href')
    yama_name = pp.select_one('a').text
    height = pp.select_one('.MountainPrefectureItem__Altitude').text
    prefectures = pp.select_one('.MountainPrefectureItem__List__Item__Text').text
    remarks_list = pp.select_one('ul:nth-of-type(2)').select('a')
    remarks = []
    for tt in remarks_list:
      remarks.append(tt.text)
    bikou = ",".join(remarks)

    sleep(1)
    print(yama_url)
    print(yama_name.replace('\r\n','').replace('\n','').replace(' ', ''))
    print(height.replace('\r\n','').replace('\n','').replace(' ', '').replace('標高：', ''))
    print(prefectures)
    print(bikou)

    c_info = {
      'yama_url': yama_url,
      'name': yama_name.replace('\r\n','').replace('\n','').replace(' ', ''),
      'height': height.replace('\r\n','').replace('\n','').replace(' ', '').replace('標高：', ''),
      'prefectures': prefectures,
      'bikou': bikou
    }
    d_list.append(c_info)



# CSV出力
df=pd.DataFrame(d_list)

print(df)

df.to_csv('hyakumeizan_list.csv', index=None, encoding='utf-8-sig')
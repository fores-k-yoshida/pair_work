from turtle import heading
from unittest import result
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

url = 'https://home.adpark.co.jp/es/pref_city_search_list.php?city%5B%5D=1310%2C1320_1016&city%5B%5D=1310%2C1320_1041&city%5B%5D=1310%2C1320_1059&city%5B%5D=1310%2C1320_1130&city%5B%5D=1310%2C1320_1148&city%5B%5D=1310%2C1320_1156&city%5B%5D=1310%2C1320_1164&tmpl=hap&area=1000&pref=1310_1320&category=chintai&count=30&sortHistory=&sort=sort2a&bldgType%5B%5D=01_03_04&bldgType%5B%5D=02&bldgType%5B%5D=06&moneyL=60000&moneyH=80000&kyoekiIncFlg=1&reikinFlg=1&zeroShikiFlg=1&madori-preset=on&layout%5B%5D=1K&layout%5B%5D=1DK&spaceL=&spaceH=&walk=15&tikunensu=20&newdate=&airconFlg=1&washerFlg=1&bandtFlg=1&cityGassFlg=1'

result = requests.get(url)
c = result.content
soup = BeautifulSoup(c, "html.parser")

#ページ数を取得
disp = soup.find_all("div", {'class':'search_list_nav_bk-count'})
disp_num = int(disp[0].contents[0].getText())
page_num = int(disp_num / 30)

# URLを入れるリストを設定
urls = []
# 1ページ目を格納
urls.append(url)
# 2ページ目以降を格納
for i in range(1, page_num + 1):
    time.sleep(3)

    begin = '&begin=' + str(30 * i)
    url_page = url + begin
    urls.append(url_page)
    
data = []
error = []
for url in urls:
    # print(url)
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c, "html.parser")
    summary = soup.find("div", {'id':'formSeatchList'})
    print(summary)
    cassetteitems = summary.find_all("div",{'class':'dottable -- search_list_result'})
    for cas in cassetteitems:
        try:
            # 情報取得用の変数を用意
            heading = '' # 見出し
            value = '' # 家賃
            manage = '' # 管理費
            floor_count = '' # 階数
            yrs = '' # 築年数
            location = '' # 住所
            station = '' # 最寄り駅
            thumb = '' # 物件のURL

            # 見出し
            heading = cas.find_all("target", "_blank").getText().strip
            print(heading)
            # 家賃
            value = cas.fing_all("")

            data.append([heading, value, manage, floor_count, yrs, location, station, thumb])    
        except Exception as e:
            error.append([e, url, len(data)])
            pass
    time.sleep(1)

print(data)
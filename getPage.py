from os import link
from turtle import heading
from unittest import result
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from styleframe import StyleFrame, Styler, utils

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
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c, "html.parser")
    summary = soup.find('section',{'class':'search_list_main'})
    cassetteitems = summary.find_all("li",{'class':'search_list_item_v3-2'})
    for cas in cassetteitems:
        try:
            # 情報取得用の変数を用意
            heading = '' # 見出し
            value = '' # 家賃
            manage = '' # 管理費
            building_info = '' # 建物情報
            location = '' # 住所
            station = '' # 最寄り駅
            thumb = '' # 物件のURL

            # 見出し
            heading = cas.find_all("h3", class_="search_list_item_bk-title_v3-2")[0].select("a")[0].string
            # 家賃
            value_before = cas.find_all("h4", class_="search_list_item_price-price_v3-2")[0].select("em")[0].string
            value = value_before.replace('\t', '').replace('\n', '')
            # 管理費
            manage = cas.find_all("p", class_="search_list_item_price-kanri_v3-2")[0].string
            # 建物情報
            building_info = cas.find_all("li", class_="search_list_item_status_v3-2")[0].text
            # 住所
            location = cas.find_all("h4", class_="search_list_item_address_v3-2")[0].text
            # 最寄り駅
            station = cas.find_all("p", class_="search_list_item_traffic_v3-2")[0].text
            # 物件のURL
            thumb = cas.find("a")
            thumb_link = thumb.get("href")

            data.append([heading, value + '万円', manage, building_info, location, station, thumb_link])
        except Exception as e:
            error.append([e, url, len(data)])
            pass
    time.sleep(1)

# data listを DataFrameに変換
df = pd.DataFrame(data, columns=['見出し', '家賃', '管理費', '建物情報', '住所', '最寄り駅', '物件のURL'])
with StyleFrame.ExcelWriter('data_adpark_bukken.xlsx') as writer:
    sf = StyleFrame(df)
    # 列幅の調整
    sf.set_column_width(columns=[1,5], width=30)
    sf.set_column_width(columns=2, width=10)
    sf.set_column_width(columns=3, width=20)
    sf.set_column_width(columns=4, width=36)
    sf.set_column_width(columns=6, width=53)
    # 行幅の調整
    sf.set_row_height(rows=list(range(2, len(data)+2)), height=30)
    # ヘッダー用：セル背景と文字色と太字の設定
    style_backColor = Styler(bg_color=utils.colors.dark_blue, font_color=utils.colors.white, bold=True)
    # 物件のURL用：左揃え、折り返しなし
    style_left_wrap = Styler(horizontal_alignment=utils.horizontal_alignments.left, wrap_text=False, shrink_to_fit=False)

    # 列に適用
    sf.apply_column_style(cols_to_style=['見出し', '物件のURL'], styler_obj=style_left_wrap)
    # 行に適用
    sf.apply_headers_style(styler_obj=style_backColor)

    # Excelファイルとして保存
    sf.to_excel(writer, index=False, sheet_name='物件リスト')
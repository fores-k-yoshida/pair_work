import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

urls = []
url = 'https://home.adpark.co.jp/es/pref_city_search_list.php?pref=1310&city=1310_1041-1310_1148-1310_1164-1310_1172-1310_1199-1310_1202&tmpl=hap&area=1000&pref=1310&category=chintai&count=30&sortHistory=&sort=sort2a&bldgType%5B%5D=01_03_04&bldgType%5B%5D=02&bldgType%5B%5D=06&moneyL=50000&moneyH=70000&reikinFlg=1&zeroShikiFlg=1&madori-preset=on&preset_disp=off&layout%5B%5D=1R&layout%5B%5D=1K&layout%5B%5D=1DK&layout%5B%5D=1LDK&spaceL=&spaceH=&walk=15&tikunensu=15&newdate=&airconFlg=1&washerFlg=1&bandtFlg=1'
urls.append(url)
res = requests.get(url) 
soup = BeautifulSoup(res.text, "html.parser")
disp = soup.find_all("div", {'class':'search_list_nav_bk-count'})

disp_num = int(disp[0].contents[0].getText())
page_num = int(disp_num / 30)

for i in range(1, page_num + 1):
    time.sleep(3)

    begin = '&begin=' + str(30 * i)
    url = 'https://home.adpark.co.jp/es/pref_city_search_list.php?pref=1310&city=1310_1041-1310_1148-1310_1164-1310_1172-1310_1199-1310_1202&tmpl=hap&area=1000&pref=1310&category=chintai&count=30&sortHistory=&sort=sort2a&bldgType%5B%5D=01_03_04&bldgType%5B%5D=02&bldgType%5B%5D=06&moneyL=50000&moneyH=70000&reikinFlg=1&zeroShikiFlg=1&madori-preset=on&preset_disp=off&layout%5B%5D=1R&layout%5B%5D=1K&layout%5B%5D=1DK&layout%5B%5D=1LDK&spaceL=&spaceH=&walk=15&tikunensu=15&newdate=&airconFlg=1&washerFlg=1&bandtFlg=1' + begin
    urls.append(url)
    
print(urls)
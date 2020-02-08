#### モジュールのインポート ####
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import module

#### 初期変数設定 ####
### 取得路線URL
url = "https://transit.yahoo.co.jp/traininfo/detail/132/0/" # 東京メトロ銀座線（YAHOO路線情報の確認したい路線のURLを記載する）

### 運行状況判定
normal_operation_flg = "[○]"
delay_operation_flg = "[!]"

#### 関数 ####
# module.pyに記載

#### メイン処理 ####

### データ取得(from URL)
req = Request(url)
try:
    res = urlopen(req)
except URLError as e:
    if hasattr(e, 'reason'):
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        module.error_processing()
    elif hasattr(e, 'code'):
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        module.error_processing()
else:
    print(res.status)
    print(res.read(100))
    html = res.read().decode("utf-8")
    res.close()

### データ抽出（運行情報取得）

soup = BeautifulSoup(html, "html.parser")
operation_info = soup.select_one("#mdServiceStatus")
operation_info_text = operation_info.select_one("dl > dt").text.replace('\n', '')
operation_info_text = str(operation_info.select_one("dl > dt").text.replace('\n', ''))
operation_info_detail_text = str(operation_info.select_one("dl > dd > p").text)

### Line通知処理（正常運行でない場合に通知） 

## 正常運行の場合の処理
if operation_info_text[:3] == normal_operation_flg:
    print(operation_info_text)
    print("Line通知なし")

## 正常運行でない場合の処理
elif operation_info_text[:3] == delay_operation_flg:
    print(operation_info_text)
    print("Line通知あり")
    module.line_bot(operation_info_detail_text) 

## 異常処理
else:
    module.error_processing()
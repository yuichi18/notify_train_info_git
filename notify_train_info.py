#### モジュールのインポート ####
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import requests
import sys

#### 初期変数設定 ####

### 取得路線URL
url = "https://transit.yahoo.co.jp/traininfo/detail/132/0/" # 東京メトロ銀座線

# TODO:複数路線選択

# ### line通知判断
# line_notice = "notice"
# line_non_notice = "non_notice"

### 異常値通知メッセージ
error_message = "異常終了。管理者に問い合わせてください。"

### 運行状況判定
normal_operation_flg = "[○]"
delay_operation_flg = "[!]"

### Lineapi,アクセストークン設定
line_api = 'https://notify-api.line.me/api/notify'
line_token = 'line-notify-token入力'

#### 関数 ####

### LINE通知
def line_bot(msg):
    line_notify_token = line_token
    line_notify_api = line_api
    message = msg
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token} 
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
    return line_notify

### 異常時処理（ライン通知、処理終了）
def error_processing():
    line_bot(error_message) 
    sys.exit(1)

#### メイン処理 ####

### データ取得(from URL)
req = Request(url)
try:
    res = urlopen(req)
except URLError as e:
    if hasattr(e, 'reason'):
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        error_processing()
    elif hasattr(e, 'code'):
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        error_processing()
else:
    print(res.status)
    print(res.read(100))
    html = res.read().decode("utf-8")
    res.close()

### データ抽出（運行情報取得）

soup = BeautifulSoup(html, "html.parser")
# print(soup)
# mdServiceStatus
operation_info = soup.select_one("#mdServiceStatus")
# print(operation_info)
operation_info_text = operation_info.select_one("dl > dt").text.replace('\n', '')
operation_info_text = str(operation_info.select_one("dl > dt").text.replace('\n', ''))
operation_info_detail_text = str(operation_info.select_one("dl > dd > p").text)
# print(operation_info_text)
# print(operation_info_detail_text)

### Line通知処理（正常運行でない場合に通知） 

## 正常運行の場合の処理
if operation_info_text[:3] == normal_operation_flg:
    print(operation_info_text)
    # line_notice_flg = line_non_notice
    print("Line通知なし")

## 正常運行でない場合の処理
elif operation_info_text[:3] == delay_operation_flg:
    print(operation_info_text)
    # line_notice_flg = line_notice
    print("Line通知あり")
    line_bot(operation_info_detail_text) 

## 異常処理
else:
    print(error_message)
    error_processing()

# ## LIne通知


# if line_notice_flg == line_notice:
#     print("Line通知")
#     msg = operation_info_detail_text
#     LINE_BOT(msg)

# else:
#     print("Line通知なし")

# ## TODO:異常処理通知

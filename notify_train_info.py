## モジュールのインポート
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

## 初期変数設定

# 取得路線URL
url = "https://transit.yahoo.co.jp/traininfo/detail/132/0/" # 東京メトロ銀座線

# TODO:複数路線選択

# line通知判断
line_notice = "notice"
line_non_notice = "non_notice"

# 運行状況判定
normal_operation_flg = "[○]"
delay_operation_flg = "[!]"

# Lineアクセストークンキー格納ファイル
line_api = 'https://notify-api.line.me/api/notify'
line_token = 'line-notify-token入力'

## 運行情報取得
with urlopen(url) as res:
    html = res.read().decode("utf-8")
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

## 通知可否判断 

# 正常運行の場合の処理
if operation_info_text[:3] == normal_operation_flg:
    print(operation_info_text)
    line_notice_flg = line_non_notice

# 正常運行でない場合の処理
elif operation_info_text[:3] == delay_operation_flg:
    print(operation_info_text)
    line_notice_flg = line_notice

# 異常処理
else:
    print("異常終了！コードを見直してください")
    line_notice_flg = line_non_notice

## LIne通知

#LINEにメッセージを送信する関数
def LINE_BOT(msg):
   line_notify_token = line_token
   line_notify_api = line_api
   message = msg
   payload = {'message': message}
   headers = {'Authorization': 'Bearer ' + line_notify_token} 
   line_notify = requests.post(line_notify_api, data=payload, headers=headers)
   
   return line_notify

if line_notice_flg == line_notice:
    print("Line通知")
    msg = operation_info_detail_text
    LINE_BOT(msg)

else:
    print("Line通知なし")

## TODO:異常処理通知
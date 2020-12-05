import requests
import sys
import settings

### LINE通知
def line_bot(msg):
    line_notify_api = 'https://notify-api.line.me/api/notify'
    # line_notify_token = 'line-notify-token入力'
    line_notify_token = settings.line_notify_token
    message = msg
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token} 
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
    return line_notify

### 異常時処理（ライン通知、処理終了）
def error_processing():
    error_message = "異常終了。管理者に問い合わせてください。"
    print(error_message)
    line_bot(error_message) 
    sys.exit(1)
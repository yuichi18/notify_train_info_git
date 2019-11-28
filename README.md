# notify_train_info_git

・アプリ名
電車遅延通知アプリ

・仕様
特定のyahoo路線の運行情報をスクレイピングし、
正常運行以外の場合にLine notifyにて運行情報を通知する

・主な使用技術
スクレイピング：Beautiful Soup
ライン通知：Line notify

・その他
Heroku等のサーバーにアップし、スケジューラーを用いて定期的に実行する

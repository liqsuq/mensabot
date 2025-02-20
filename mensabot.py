#!/usr/bin/python3

# 1時間毎に日本メンサ試験ページ(https://mensa.jp/exam/)をスクレイピングして、
# 新着情報があればメールに送信するスクリプト

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import time	# スリープ用
import datetime

# メール送信用の設定
URL = 'https://mensa.jp/exam/'
FROM_ADDRESS = '送信元メールアドレス'
MY_PASSWORD = '送信元メールアドレスのパスワード'
TO_ADDRESS = '送信先メールアドレス'
SUBJECT = '日本メンサ試験ページ更新情報'
BODY = '日本メンサ試験ページに更新がありました。\n' + URL

# メッセージ作成関数
def create_message(from_addr, to_addr, subject, body):
	msg = MIMEText(body)
	msg['Subject'] = subject
	msg['From'] = from_addr
	msg['To'] = to_addr
	msg['Date'] = formatdate()
	return msg

# メール送信関数
def send(from_addr, to_addrs, msg):

	# GmailのSMTPサーバを使う場合
	smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
	smtpobj.ehlo()
	smtpobj.starttls()
	smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
	smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
	smtpobj.close()

# メイン処理
def main():
	# 1時間毎に実行
	while True:
		# 日本メンサ試験ページをスクレイピング
		response = requests.get(URL)
		response.encoding = response.apparent_encoding
		soup = BeautifulSoup(response.text, 'html.parser')
		news = soup.find_all('div', class_='news')
		if len(news) > 0:
			# 更新情報があればメール送信
			print('Updated: ' + URL)
			msg = create_message(FROM_ADDRESS, TO_ADDRESS, SUBJECT, BODY)
			send(FROM_ADDRESS, [TO_ADDRESS], msg)
		else:
			print('No updates')
		# 1時間スリープ
		time.sleep(3600)

if __name__ == '__main__':
	main()

# このスクリプトを実行すると、1時間毎に日本メンサ試験ページをスクレイピングして、
# 更新情報があればメールに送信します。
# メール送信にはGmailのSMTPサーバを使用しています。
# 送信元メールアドレスと送信先メールアドレス、パスワードを設定してください。
# メール送信に成功すると、コンソールに"No updates"と表示されます。
# 更新情報があれば、日本メンサ試験ページのURLが表示されます。

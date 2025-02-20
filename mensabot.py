#!/usr/bin/python3

import requests
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import time

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
	smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
	smtpobj.ehlo()
	smtpobj.starttls()
	smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
	smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
	smtpobj.close()

# メイン処理
def main():
	oldres = requests.get(URL)
	while True:
		newres = requests.get(URL)
		if newres.status_code != 200:
			print('Connection Error')
			time.sleep(10)
			continue
		if newres.text != oldres.text:
			print('Updated')
			msg = create_message(FROM_ADDRESS, TO_ADDRESS, SUBJECT, BODY)
			send(FROM_ADDRESS, [TO_ADDRESS], msg)
		else:
			print('No updates')
		oldres = newres
		time.sleep(3600)

if __name__ == '__main__':
	main()
	
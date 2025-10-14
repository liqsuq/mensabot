#!/usr/bin/python3

import requests
import time

STRF = "[%y/%m/%d %H:%M]"
TARGET_URL = "https://mensa.jp/exam/"
NOTIFY_URL = "https://ntfy.sh/mensabot"
HEAD = "MensaBot"
BODY = "Mensa試験情報が更新されました。".encode('utf-8')
TAGS = "tada"

def send_msg():
	r = requests.post(
		NOTIFY_URL,
		headers = {"Title": HEAD, "Click": TARGET_URL, "Tags": TAGS},
		data = BODY,
	)
	if r.status_code != 200:
		print(time.strftime(STRF), "Failed to send: ", r.reason)

def main():
	print(time.strftime(STRF), "MensaBot started")
	old = None
	while True:
		while (r := requests.get(TARGET_URL)).status_code != 200:
			print(time.strftime(STRF), "Failed to fetch: ", r.reason)
			time.sleep(5)
		new = '\n'.join(l.strip() for l in r.text.splitlines() if l.strip())
		if old is None:
			old = new
			continue
		if new != old:
			print(time.strftime(STRF), 'Updated')
			send_msg()
		else:
			print(time.strftime(STRF), 'No updates')
		old = new
		time.sleep(300)

if __name__ == '__main__':
	main()
	
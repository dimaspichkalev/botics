from flask import Flask, request
import requests 
import sys
import json
from bot_main import analyze_message

token = 'AVNTHE50Q3YU1M7CA6IZWDVAWWSKYNF3'
url = "https://dev.greendatasoft.ru/api/authentication"
post_url = "https://dev.greendatasoft.ru/"
payload = {'j_username': 'dimaspichkalev@gmail.com', 'j_password': 'asuchatbot145'}

headers = {'Content-type': 'application/json',  # Определение типа данных
           'Accept': 'application/json',
           'Content-Encoding': 'utf-8'}

app = Flask(__name__)

@app.route("/index")
def hello():
	return "hello"

@app.route('/', methods = ['POST'])

def message():

	if request.method == 'POST':	

		data = request.json
		
		# print(data)

		# author = data["body"]["author"]
		authorIsBot = data["body"]["authorIsBot"]
		chat = data["body"]["chat"]
		message = data["body"]["payload"]

		if not (authorIsBot):
			body = { "text": analyze_message(message) }
				

		# url_get = 'https://dev.greendatasoft.ru/api/bot/%s/me' % (token)

		url_post = 'https://dev.greendatasoft.ru/api/bot/%s/chat/%d/post' % (token, chat)

		with requests.session() as session:
			session.post(url, payload)
			# answer = s.get(url_get)
			if not (authorIsBot):
				res = session.post(url_post, headers=headers, data=json.dumps(body))
				
		return "True"

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=4567, debug=True)
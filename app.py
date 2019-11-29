from flask import Flask, request
import requests
import json
from utils.bot_work import analyze_message
import os


token = os.environ['GREENDATA_TOKEN']
url = os.environ['AUTH_URL']
post_url = "https://dev.greendatasoft.ru/"
payload = {
	'j_username': os.environ['GREENDATA_USER'], 
	'j_password': os.environ['GREENDATA_PWD']
	}
headers = {
	'Content-type': 'application/json',  # Определение типа данных
	'Accept': 'application/json',
	'Content-Encoding': 'utf-8'
	}


app = Flask(__name__)

@app.before_request
def before_request():
	if request.url.startswith('http://'):
		url = request.url.replace('http://', 'https://', 1)


@app.route('/', methods = ['POST'])
def message():
	if request.method == 'POST':	
		data = request.json
		authorisbot = data["body"]["authorIsBot"]
		chat = data["body"]["chat"]
		message = data["body"]["payload"]
		if not authorisbot:
			body = {
				"text": analyze_message(message)
			}
		url_post = "https://dev.greendatasoft.ru/api/bot/{0}/chat/{1}/post".format(token, chat)
		with requests.session() as session:
			session.post(url, payload)
			if not (authorisbot):
				session.post(url_post, headers=headers, data=json.dumps(body))
		return "True"


if __name__ == "__main__":
	app.run(port=33507, debug=True)
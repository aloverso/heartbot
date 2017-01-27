from flask import Flask
import poplib
from email import parser
import json
import os
app = Flask(__name__)

messages = []

@app.route('/')
def home():
	return 'home'

@app.route('/mail')
def get_mail():
	messages.extend(pop3_connect())
	print(messages)
	return json.dumps(messages)

def pop3_connect():
	pop_conn = poplib.POP3_SSL('pop.gmail.com')
	pop_conn.user(os.environ['HEARTBOT_USERNAME'])
	pop_conn.pass_(os.environ['HEARTBOT_PASSWORD'])
	messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]

	joined_mssgs=[]	
	for mssg in messages:
		decoded_items=[]
		for item in mssg[1]:
			decoded_items.append(item.decode(encoding='UTF-8'))
		joined_mssgs.append("\n".join(decoded_items))

	parsed_mssgs = [parser.Parser().parsestr(mssg) for mssg in joined_mssgs]
	pop_conn.quit()
	return [m['subject'] for m in parsed_mssgs]


if __name__ == '__main__':
    app.run(debug=True)
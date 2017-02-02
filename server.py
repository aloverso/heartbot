from flask import Flask, render_template
from flask import jsonify
import json
import os
import redis

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/nextmessage')
def get_next_message():
	# assuming we are storing messages in a redis list called messages
	# rpop removes right-end of list (least-recently added, queue)
	new_message = r.rpop('messages')
	resend_old_message = False

	if new_message==None:
		new_message = r.get('lastmessage')
		resend_old_message = True

	r.set('lastmessage', new_message)
	new_message_json = json.loads(new_message.decode(encoding='UTF-8'))
	new_message_json['resend_old_message'] = resend_old_message
	return jsonify(new_message_json)

if __name__ == '__main__':
    app.run(debug=True)
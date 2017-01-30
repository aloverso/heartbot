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

	if new_message==None:
		new_message = r.get('lastmessage')

	r.set('lastmessage', new_message)
	return jsonify(json.loads(new_message.decode(encoding='UTF-8')))

if __name__ == '__main__':
    app.run(debug=True)
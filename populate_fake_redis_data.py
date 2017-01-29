import json
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

for i in range(20):
	m = json.dumps({'subject':'subject'+str(i), 'size':0})
	r.rpush('messages', m)

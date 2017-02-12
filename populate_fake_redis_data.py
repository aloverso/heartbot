import json
import redis
import random
r = redis.StrictRedis(host='localhost', port=6379, db=0)

for i in range(20):
    m = json.dumps({"subject":'subject'+str(i), "size":random.uniform(1000, 1000000), 'sentiment': random.uniform(-1, 1)})
    r.rpush('messages', m)

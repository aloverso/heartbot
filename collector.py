import os
import sys
import time
import redis
import poplib
from email import parser

def get_mail():
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

    ret = [{"subject": m['subject'], 'size': 0} for m in parsed_mssgs]
    return ret


if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    while True:
        print("Fetching mail...", end="")
        mail = get_mail()
        print(" got {} messages.".format(len(mail)))

        for m in mail:
            r.rpush("messages", m)

        time.sleep(5)

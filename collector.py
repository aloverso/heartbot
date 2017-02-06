import os
import sys
import time
import redis
import poplib
import json
from email import parser

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_mail():
    """ fetches new messages from a gmail account using POP, then parses it
    into a JSON blob and returns it:
    {"subject": string, "date": string, "size": int, "sentiment": int} """

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

    def parse_msg(msg):
        """ takes a msg object from Python's email parser and formats it into
        a dictionary (which then becomes JSON that we can put in Redis) """
        analyzer = SentimentIntensityAnalyzer()
        subject = msg.get("Subject")
        return {
            "subject":   subject,
            "date":      msg.get("Date"),
            "size":      len(bytes(msg)),
            "sentiment": analyzer.polarity_scores(subject)['compound']
        }

    ret = [json.dumps(parse_msg(m)) for m in parsed_mssgs]

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

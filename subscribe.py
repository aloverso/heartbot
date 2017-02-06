from splinter import Browser
import os
import sys
import time
import redis
import poplib
import json
from email import parser

with Browser() as browser:
    # # Visit URL
    # url = "https://lists.olin.edu/mailman/listinfo/acro"
    # browser.visit(url)
    # browser.fill('email', 'olinheartbot@gmail.com')
    # # Find and click the 'search' button
    # button = browser.find_by_name('email-button')
    # # Interact with elements
    # button.click()
    # if browser.is_text_present('Subscription results'):
    #     print("subscribed")

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
        subject = msg.get("Subject")
        return {
            "subject":   subject,
            "sender":    msg.get("Sender"),
            "date":      msg.get("Date"),
            "size":      len(bytes(msg)),
        }


    ret = [parse_msg(m) for m in parsed_mssgs]

    print(ret)
    for msg in ret:
        subj = msg['subject']
        if 'confirm' in subj:
            uid = subj[8:]

            sender = msg['sender']
            i = sender.index(' ')
            slist = sender[:i]

            try:

                url = "https://lists.olin.edu/mailman/confirm/"+slist+"/"+uid
                print(url)
                browser.visit(url)
                # Find and click the 'search' button
                button = browser.find_by_name('submit')
                # Interact with elements
                button.click()
            except:
                print(sender)
                print(subj)

    print(ret)
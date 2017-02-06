import re
from robobrowser import RoboBrowser

# Browse to Rap Genius
browser = RoboBrowser(history=True, user_agent="olin heartbot")
browser.open('https://lists.olin.edu/mailman/listinfo/')

# Look up the various lists
lists = browser.select('body > table td a')
for mailing_list in lists[2:]: # skip a couple of mailto: links
    print("Subscribing to {}...".format(mailing_list.text))
    browser.follow_link(mailing_list)

    try:
        subscribe_form = browser.get_form(action=re.compile("../subscribe/"))
        subscribe_form['email'].value = 'olinheartbot@gmail.com'
        browser.submit_form(subscribe_form)
    except:
        print("Unable to subscribe to {}!".format(mailing_list.text))

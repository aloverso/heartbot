# heartbot
A visualization of Olin's email heartbeat

![a diagram of heartbot](https://github.com/aloverso/heartbot/blob/master/heartbot.png)

The collector simply queries a set email account using Python's POP library, then pushes a JSON string `{"subject": "subject line of message", "date": "date from the message's `Date` header", "size": int size of message in bytes}` to Redis for each message it finds. The Flask API has one endpoint that, when queried, attempts to retreive and return one of those JSON blobs from Redis, or returns an empty JSON `{}` if there's no message waiting.

## To Run

Make sure you have redis installed and available on `localhost:6379` (the default).

First time:
  - `virtualenv venv --python=python3`
  - `pip install -r requirements.txt`

After that, whenever you open a new terminal:
  - `source venv/bin/activate` (you should see `(venv)` prepended before your command prompt)

Then, `python collector.py` and `python server.py`.

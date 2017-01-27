# heartbot
A visualization of Olin's email heartbeat

![a diagram of heartbot](https://github.com/aloverso/heartbot/blob/master/heartbot.png)

The collector simply queries a set email account using Python's POP library, then pushes a JSON string `{"subject": "subject line of message", "size": int size of message in bytes}` to Redis for each message it finds. The Flask API has one endpoint that, when queried, attempts to retreive and return one of those JSON blobs from Redis, or returns an empty JSON `{}` if there's no message waiting.

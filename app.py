from flask import Flask, send_file, request
import datetime
import os

app = Flask(__name__)

@app.route('/track/<name>')
def track(name):

    ip = request.remote_addr
    ua = request.headers.get("User-Agent")

    log = f"""
OPENED Mail:
Name: {name}
Time: {datetime.datetime.now()}
IP: {ip}
UA: {ua}
-----------------------
"""

    print(log)

    with open("email_stats.txt", "a", encoding="utf-8") as f:
        f.write(log)

    return send_file("like.png", mimetype="image/png")


@app.route('/')
def home():
    return "Tracker running."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
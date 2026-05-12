from flask import Flask, send_file, request
import datetime
import uuid
import os

app = Flask(__name__)

LOG_FILE = "email_stats.txt"

# -----------------------------
# Simple in-memory dedupe (upgrade later to DB/Redis)
# -----------------------------
seen_events = set()

# -----------------------------
# BOT / PROXY FILTERS
# -----------------------------
BLOCKED_UA_KEYWORDS = [
    "googleimageproxy",
    "bot",
    "crawler",
    "spider",
    "preview",
]

def is_bot(user_agent: str) -> bool:
    ua = (user_agent or "").lower()
    return any(x in ua for x in BLOCKED_UA_KEYWORDS)


# -----------------------------
# TRACK ROUTE
# -----------------------------
@app.route('/track/<track_id>')
def track(track_id):

    ua = request.headers.get("User-Agent", "")
    ip = request.remote_addr

    # Ignore bots / email scanners
    if is_bot(ua):
        print("🚫 Bot/proxy ignored:", ua)
        return send_file("like.png", mimetype="image/png")

    # Deduplicate (prevents multiple opens from same cache)
    if track_id in seen_events:
        print("🔁 Duplicate open ignored:", track_id)
        return send_file("like.png", mimetype="image/png")

    seen_events.add(track_id)

    timestamp = datetime.datetime.now()

    log = f"""
OPEN EVENT
Track ID: {track_id}
Time: {timestamp}
IP: {ip}
User-Agent: {ua}
-----------------------
"""

    print(log)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log)

    return send_file("like.png", mimetype="image/png")


# -----------------------------
# HOME
# -----------------------------
@app.route('/')
def home():
    return "Tracker running."


# -----------------------------
# RUN
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
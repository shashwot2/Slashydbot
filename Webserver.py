from flask import Flask
from threading import Thread

#python discord bot code above ^^
app = Flask('')


@app.route('/')
def index():
    return "Bot up and running"


def run():
    app.run(host="0.0.0.0", port=8080)


def Webserver():
    t = Thread(target=run)
    t.start()

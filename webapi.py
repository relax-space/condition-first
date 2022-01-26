
'''
说明: 启动命令 python webapi.py
'''
import time

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(app, default_limits=[
                  '2/second'], key_func=get_remote_address)


@app.route('/<id>')
def index(id):
    time.sleep(1)
    return id


@app.route('/delay/<second>/<id>')
def delay(second, id):
    second = int(second)
    time.sleep(second)
    return id


@app.route('/free/<sleep_time>')
@limiter.exempt
def free(sleep_time):
    sleep_time = float(sleep_time)
    time.sleep(sleep_time)
    print(sleep_time)
    return sleep_time


if __name__ == '__main__':
    app.run(debug=True)

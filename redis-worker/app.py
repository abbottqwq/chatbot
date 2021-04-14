from flask import Flask, url_for, request, jsonify
import config
import redis
import random

app = Flask(__name__)

redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

@app.route('/', methods=['GET', 'POST'])
def getResponse():
    return jsonify(message="helloworld")


def random_time(time, scope):
    return time + random.randint(-scope, scope)


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
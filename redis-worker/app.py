from flask import Flask, url_for, request, jsonify, abort
import config
import redis
import random
import requests
from datetime import timedelta
import logging

app = Flask(__name__)

redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)


@app.route('/', methods=['POST'])
def getResponse():
    logging.warning(request.get_json())
    message = request.get_json()['message']
    logging.warning(message)
    print(message)
    if not message:
        abort(400)
    res = get_from_cache(message)
    logging.warning("res is --------------->")
    logging.warning(res)
    if not res:
        res = requests.post(config.CHATBOT_API_URL,
                            json={"message": message}).json()["res"]
        logging.warning(res)
        state = set_to_cache(message, res, config.TIME, config.SCOPE)
        if not state:
            return jsonify({"res": res, "error": "REDIS_WRITE_ERROR"})
    else:
        res = res.decode("utf-8")
        logging.info(res)
    return jsonify({"res": res})


@app.route('/add', methods=['POST'])
def teach_me():
    message = request.get_json()['message']
    res = request.json['res']
    logging.warning(message)
    logging.warning(res)
    state = set_to_cache(message, res, config.TIME, config.SCOPE)
    logging.warning(state)
    if state==False:
        return jsonify({'err': 'REDIS_WRITE_ERROR'})
    else:
        return jsonify({'success': '1'})


def set_to_cache(message: str, res: str, time: int, scope: int):
    state = redis_client.setex(message, timedelta(
        seconds=random_time(time, scope)), res)
    return state


def get_from_cache(message: str) -> str:
    return redis_client.get(message)


def random_time(time: int, scope: int) -> int:
    r_time = time + random.randint(-scope, scope)
    if r_time < 0:
        r_time = 0
    return r_time


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

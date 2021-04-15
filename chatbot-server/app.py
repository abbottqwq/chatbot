from flask import Flask, url_for, request, jsonify, abort
import requests
import config
from functools import wraps
import logging
app = Flask(__name__)


def debug_only(f):
    @wraps(f)
    def wrapped(**kwargs):
        if not config.DEBUG:
            abort(404)
        return f(**kwargs)
    return wrapped


@app.route('/message', methods=['POST'])
def hello():
    message = request.json['message']
    if not message:
        abort(400)
    res = requests.post(config.REDIS_WORKER_URL, json={
                        "message": message}).json()["res"]
    print(res)
    return jsonify({"res": res})


@app.route('/message', methods=['GET'])
@debug_only
def test_message():
    message = request.args['message']
    print(message)
    if not message:
        abort(400)
    res = requests.post(config.REDIS_WORKER_URL, json={
                        "message": message}).json()["res"]

    return jsonify({"res": res})


@app.route('/teachme', methods=['POST'])
def teachme():
    message = request.json['message']
    res = request.json['res']
    if not message or not res:
        abort(400)
    res = requests.post(config.MONGO_WORKER_URL, json={
                        "message": message, "res": res})
    logging.warning(res)
    return res


@app.route('/teachme', methods=['GET'])
@debug_only
def teachme_test():
    # logging.warning(request.json)
    message = request.args['message']
    res = request.args['res']
    if not message or not res:
        abort(400)
    res = requests.post(config.MONGO_WORKER_URL, json={
                        "message": message, "res": res})
    logging.warning(res)
    return res


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

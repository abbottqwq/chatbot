from flask import Flask, url_for, request, jsonify, abort
import requests
import config
from functools import wraps
app = Flask(__name__)

def debug_only(f):
    @wraps(f)
    def wrapped(**kwargs):
        if not config.DEBUG:
            abort(404)
        return f(**kwargs)
    return wrapped

@app.route('/', methods=['POST'])
def hello():
    message = request.json['message']
    if not message:
        abort(400)
    res = requests.post("http://redis-worker-service.api:5000", json={"message":message}).json()["res"]
    print(res)
    return jsonify({"res":res})

@app.route('/', methods=['GET'])
@debug_only
def test():
    message = request.args['message']
    print(message)
    if not message:
        abort(400)
    res = requests.post("http://redis-worker-service.api:5000", json={"message":message}).json()["res"]
    print(res)
    return jsonify({"res":res})

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
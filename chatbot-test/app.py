from flask import Flask, url_for, request, jsonify, abort
import requests
import config
from functools import wraps
import logging
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def test():
    
    redis_status = requests.get(config.REDIS_WORKER_URL + "/test_connection").json()
    
    return jsonify()



if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

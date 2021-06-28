from flask import Flask, request, jsonify
import pymongo
import config
import requests
import json
import logging
from pymongo.errors import ConnectionFailure
app = Flask(__name__)
mongo_client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)
db = mongo_client.db

def is_mongo_avaliable(m):
    try:
        m.admin.command('ismaster')
        logging.info("mongodb connected")
        return True
    except ConnectionFailure:
        logging.error("mongo connection error")
        return False

@app.route('/test_connection', methods=['GET', 'POST'])
def test():
    if is_mongo_avaliable(mongo_client):
        return jsonify({'success':1})
    else:
        return jsonify({'error':1})

@app.route('/', methods=['POST'])
def teach_me():
    message = request.get_json()['message']
    res = request.json['res']
    err = {}
    if not add_to_db(message, res):
        err['mongo_error'] = 1
        err['error'] = 1
    if not add_to_redis(message, res):
        err['redis_error'] = 1
        err["error"] = 1
    if not err:
        return json.dumps({"success": 1})
    return json.dumps(err)


def add_to_db(message: str, res: str):
    result = db.things.insert_one({"message": message, "res": res})
    return result


def add_to_redis(message: str, res: str):
    state = requests.post(config.REDIS_WORKER_URL +
                          "/add", json={
                              "message": message, "res": res}).json()
    logging.warning(state)
    return 'success' in state


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

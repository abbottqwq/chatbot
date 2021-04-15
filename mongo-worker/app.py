from flask import Flask, request, jsonify
import pymongo
import config
import requests

app = Flask(__name__)
mongo_client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)
db = mongo_client().db


@app.route('/', methods=['POST'])
def teach_me():
    message = request.json['message']
    res = request.json['res']
    err = {}
    if not add_to_db(message, res):
        err['mongo_error':1]
    if not add_to_redis(message, res):
        err['redis_error': 1]
    return err


def add_to_db(message: str, res: str):
    result = db.things.insert_one({"message": message, "res": res})
    return len(result.inserted_ida) > 0


def add_to_redis(message: str, res: str):
    state = requests.post(config.REDIS_WORKER_URL, json={
                          "message": message}).json()
    return state['error'] is None


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

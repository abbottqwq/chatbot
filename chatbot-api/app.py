from predict import pred
from flask import Flask, url_for, request, jsonify, abort
import config
import requests
import logging

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def getResponse():
    message = request.get_json()['message']
    logging.info("message is " + message)
    if not message:
        abort(400)
    logging.warning('before predict')
    res = pred(message)
    logging.warning(res)
    return jsonify({'res': res})

# str = input()
# print(pred(str))



if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

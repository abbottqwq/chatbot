from flask import Flask, url_for, request, jsonify, abort
import config
import requests


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def getResponse():
    message = request.json['message']
    if not message:
        abort(400)
    return jsonify(res="helloworld + " + message)


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


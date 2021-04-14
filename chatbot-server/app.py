from flask import Flask, url_for, request, jsonify
import requests
import config
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def hello():
    x = requests.get("http://redis-worker-service.api:5000").json()
    print(x)
    return x
if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
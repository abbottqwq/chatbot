from flask import Flask, url_for, request, jsonify
import config
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def hello():
    return "Hello World!"
if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=80, debug=config.DEBUG)
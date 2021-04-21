from flask import Flask, url_for, request, jsonify, abort
import config
import requests
import numpy as np
import tensorflow as tf
from tensorflow import keras
import json
from keras.models import Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import logging

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def getResponse():
    message = request.get_json()['message']
    if not message:
        abort(400)
    return jsonify(res=pred(message))


with open('word_index.json', 'r') as f:
    word_index = json.load(f)


j = {}
with open("parameters.json",'r') as f:
  j = json.load(f)
jj = json.loads(j)
print(jj)
VOCAB_SIZE = jj['VOCAB_SIZE']
HIDDEN_DIM = jj['HIDDEN_DIM']
maxlen_questions = jj['maxlen_questions']
maxlen_answers = jj['maxlen_answers']
with open('word_index.json', 'r') as f:
  word_index = json.load(f)
model = keras.models.load_model('model', compile=False)
enc_model = keras.models.load_model('enc_model', compile=False)
dec_model = keras.models.load_model('dec_model', compile=False)




def str_to_tokens(sentence: str):
    words = sentence.lower().split()
    tokens_list = list()
    for current_word in words:
        result = word_index.get(current_word, '')
        if result != '':
            tokens_list.append(result)
    return pad_sequences([tokens_list],
                         maxlen=maxlen_questions,
                         padding='post')


def pred(message: str) -> str:
    states_values = enc_model.predict(str_to_tokens(message))
    empty_target_seq = np.zeros((1, 1))
    empty_target_seq[0, 0] = word_index['start']
    stop_condition = False
    decoded_translation = ''
    while not stop_condition:
        dec_outputs, h, c = dec_model.predict([empty_target_seq]
                                              + states_values)
        sampled_word_index = np.argmax(dec_outputs[0, -1, :])
        sampled_word = None
        for word, index in word_index.items():
            if sampled_word_index == index:
                if word != 'end':
                    decoded_translation += ' {}'.format(word)
                sampled_word = word

        if sampled_word == 'end' \
                or len(decoded_translation.split()) \
                > maxlen_answers:
            stop_condition = True

        empty_target_seq = np.zeros((1, 1))
        empty_target_seq[0, 0] = sampled_word_index
        states_values = [h, c]
    # logging.warning(decoded_translation)
    # print(len(decoded_translation))
    if len(decoded_translation) == 0:
        decoded_translation = "Sorry, I can't understand it"
    return decoded_translation
    
# print(pred('hello'))
# for _ in tf.range(10):
#     print(pred(input()))


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

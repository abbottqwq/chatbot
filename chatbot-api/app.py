from flask import Flask, url_for, request, jsonify, abort
import config
import requests
import numpy as np
import tensorflow as tf
import json
from tensorflow import keras
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dense, Flatten, Conv1D, MaxPooling1D, Input, LSTM
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


with open('word_index.txt', 'r') as f:
    word_index = json.load(f)


HIDDEN_DIM = config.HIDDEN_DIM
VOCAB_SIZE = config.VOCAB_SIZE
maxlen_answers = config.MAXLEN_ANSWERS
maxlen_questions = config.MAXLEN_QUESTIONS
enc_inputs = Input(shape=(None,))
enc_embedding = Embedding(VOCAB_SIZE, HIDDEN_DIM, mask_zero=True)(enc_inputs)
_, state_h, state_c = LSTM(HIDDEN_DIM, return_state=True)(enc_embedding)
enc_states = [state_h, state_c]

dec_inputs = Input(shape=(None,))
dec_embedding = Embedding(VOCAB_SIZE, HIDDEN_DIM, mask_zero=True)(dec_inputs)
dec_lstm = LSTM(HIDDEN_DIM, return_state=True, return_sequences=True)
dec_outputs, _, _ = dec_lstm(dec_embedding, initial_state=enc_states)
dec_dense = Dense(VOCAB_SIZE, activation=tf.keras.layers.Softmax())
output = dec_dense(dec_outputs)

model = keras.models.load_model('my_model')


dec_state_input_h = Input(shape=(HIDDEN_DIM,))
dec_state_input_c = Input(shape=(HIDDEN_DIM,))
dec_states_inputs = [dec_state_input_h, dec_state_input_c]
dec_outputs, state_h, state_c = dec_lstm(dec_embedding,
                                         initial_state=dec_states_inputs)
dec_states = [state_h, state_c]
dec_outputs = dec_dense(dec_outputs)
dec_model = Model(
    inputs=[dec_inputs] + dec_states_inputs,
    outputs=[dec_outputs] + dec_states)
enc_model = Model(inputs=enc_inputs, outputs=enc_states)


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
    logging.warning(decoded_translation)
    return decoded_translation
# print(pred('hello'))
# for _ in tf.range(10):
#     pred(input())


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

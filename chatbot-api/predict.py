import numpy as np
import tensorflow as tf
from tensorflow import keras
import json
from keras.models import Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import wordnet
from bs4 import BeautifulSoup
from collections import Counter
from functools import reduce
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import nltk
import logging
with open('word_index.json', 'r') as f:
    word_index = json.load(f)


j = {}
with open("parameters.json", 'r') as f:
    j = json.load(f)
jj = json.loads(j)
print(jj)
VOCAB_SIZE = jj['VOCAB_SIZE']
HIDDEN_DIM = jj['HIDDEN_DIM']
maxlen_questions = jj['maxlen_questions']
maxlen_answers = jj['maxlen_answers']
with open('word_index.json', 'r') as f:
    word_index = json.load(f)
# model = keras.models.load_model('model', compile=False)
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


nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('words')
nltk.download('punkt')


def remove_useless_thing(text: str) -> str:
    text = re.sub('http://\S+|https://\S+', ' ', text)
    text = re.sub('@\S+', ' ', text)
    text = re.sub('[^a-zA-Z]+', ' ', text)
    return text


lemmatizer = WordNetLemmatizer()


def pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def lemmatize_words(text):
    pos_tagged = nltk.pos_tag(nltk.word_tokenize(text))
    wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            # if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:
            # else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return " ".join(lemmatized_sentence)


words = set(nltk.corpus.words.words())


def remove_non_english_words(text):
    new_text = [w for w in nltk.wordpunct_tokenize(
        text) if w.lower() in words or not w.isalpha()]
    new_text = " ".join(new_text)
    return new_text


message_preprocessing = [remove_useless_thing, lemmatize_words, remove_non_english_words]


def preprocessing(message: str) -> str:
    return reduce(lambda res, f: f(res), message_preprocessing, message)


def pred(message: str) -> str:
    logging.warning('in predict')
    preprocessed_str = preprocessing(message)
    logging.warning('after preprocessed ' + preprocessed_str)
    states_values = enc_model.predict(str_to_tokens(preprocessed_str))
    empty_target_seq = np.zeros((1, 1))
    empty_target_seq[0, 0] = word_index['<sos>']
    stop_condition = False
    decoded_translation = ''
    count = 0
    while not stop_condition:
        dec_outputs, h, c = dec_model.predict([empty_target_seq]
                                              + states_values)
        sampled_word_index = np.argmax(dec_outputs[0, -1, :])
        # print(sampled_word_index)
        sampled_word = None
        for word, index in word_index.items():
            if sampled_word_index == index:
                if word != '<eos>':
                    decoded_translation += ' {}'.format(word)
                sampled_word = word
        print(sampled_word)
        if sampled_word == '<eos>'  or len(decoded_translation.split()) > maxlen_answers:
            stop_condition = True

        empty_target_seq = np.zeros((1, 1))
        empty_target_seq[0, 0] = sampled_word_index
        states_values = [h, c]
    # logging.warning(decoded_translation)
    # print(len(decoded_translation))
    if len(decoded_translation) == 0:
        decoded_translation = "Sorry, I can't understand it"
    logging.warning(decoded_translation)
    return decoded_translation

# print(pred('hello'))
# for _ in tf.range(10):
#     print(pred(input()))


if __name__ == '__main__':
    print(pred('hello'))
    for _ in tf.range(10):
        print(pred(input()))

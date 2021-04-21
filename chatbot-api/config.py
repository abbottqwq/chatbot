import os
DEBUG = os.environ.get('DEBUG', '0')=="1"
PORT = int(os.environ.get('PORT', '5000'))
HOST = os.environ.get('HOST', '0.0.0.0')
VOCAB_SIZE = int(os.environ.get('VOCAB_SIZE', '12897'))
HIDDEN_DIM = int(os.environ.get('HIDDEN_DIM', '300'))
MAXLEN_ANSWERS = int(os.environ.get('MAXLEN_ANSWERS', '32'))
MAXLEN_QUESTIONS = int(os.environ.get('MAXLEN_QUESTIONS', '34'))


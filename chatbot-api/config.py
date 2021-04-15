import os
DEBUG = os.environ.get('DEBUG', '0')=="1"
PORT = int(os.environ.get('PORT', '5000'))
HOST = os.environ.get('HOST', '0.0.0.0')

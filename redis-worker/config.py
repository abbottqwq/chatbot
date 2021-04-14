import os
DEBUG = os.environ.get('DEBUG', '0')=="1"
PORT = os.environ.get('PORT', 5000)
HOST = os.environ.get('HOST', '0.0.0.0')
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
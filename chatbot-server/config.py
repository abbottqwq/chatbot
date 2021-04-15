import os
DEBUG = os.environ.get('DEBUG', '0') == "1"
PORT = os.environ.get('PORT', 5000)
HOST = os.environ.get('HOST', '0.0.0.0')
REDIS_WORKER_SERVICE = os.environ.get(
    "REDIS_WORKER_SERVICE", "redis-worker-service")
REDIS_WORKER_NAMESPACE = os.environ.get("REDIS_WORKER_NAMESPACE", "api")
REDIS_WORKER_PORT = os.environ.get("REDIS_WORKER_PORT", "5000")
REDIS_WORKER_PROTOCOL = os.environ.get("REDIS_WORKER_PROTOCOL", "http")
REDIS_WORKER_URL = "{}://{}.{}:{}".format(REDIS_WORKER_PROTOCOL,
                                          REDIS_WORKER_SERVICE, REDIS_WORKER_NAMESPACE, REDIS_WORKER_PORT)

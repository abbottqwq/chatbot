import os
DEBUG = os.environ.get('DEBUG', '0') == "1"
PORT = int(os.environ.get('PORT', 5000))
HOST = os.environ.get('HOST', '0.0.0.0')
REDIS_WORKER_SERVICE = os.environ.get(
    "REDIS_WORKER_SERVICE", "redis-worker-service")
REDIS_WORKER_NAMESPACE = os.environ.get("REDIS_WORKER_NAMESPACE", "api")
REDIS_WORKER_PORT = int(os.environ.get("REDIS_WORKER_PORT", "5000"))
REDIS_WORKER_PROTOCOL = os.environ.get("REDIS_WORKER_PROTOCOL", "http")
REDIS_WORKER_URL = "{}://{}.{}:{}".format(REDIS_WORKER_PROTOCOL,
                                          REDIS_WORKER_SERVICE, REDIS_WORKER_NAMESPACE, REDIS_WORKER_PORT)


MONGO_WORKER_SERVICE = os.environ.get(
    "MONGO_WORKER_SERVICE", "mongo-worker-service")
MONGO_WORKER_NAMESPACE = os.environ.get("MONGO_WORKER_NAMESPACE", "api")
MONGO_WORKER_PORT = int(os.environ.get("MONGO_WORKER_PORT", "5000"))
MONGO_WORKER_PROTOCOL = os.environ.get("MONGO_WORKER_PROTOCOL", "http")
MONGO_WORKER_URL = "{}://{}.{}:{}".format(MONGO_WORKER_PROTOCOL,
                                          MONGO_WORKER_SERVICE, MONGO_WORKER_NAMESPACE, MONGO_WORKER_PORT)                                          

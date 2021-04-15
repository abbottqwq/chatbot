import os
DEBUG = os.environ.get('DEBUG', '0')=="1"
PORT = int(os.environ.get('PORT', '5000'))
HOST = os.environ.get('HOST', '0.0.0.0')
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
TIME = int(os.environ.get('TIME', 1200))
SCOPE = int(os.environ.get('SCOPE', 300))

CHATBOT_API_SERVICE = os.environ.get(
    "CHATBOT_API_SERVICE", "chatbot-api-service")
CHATBOT_API_NAMESPACE = os.environ.get("CHATBOT_API_NAMESPACE", "api")
CHATBOT_API_PORT = int(os.environ.get("CHATBOT_API_PORT", "5000"))
CHATBOT_API_PROTOCOL = os.environ.get("CHATBOT_API_PROTOCOL", "http")
CHATBOT_API_URL = "{}://{}.{}:{}".format(CHATBOT_API_PROTOCOL,
                                          CHATBOT_API_SERVICE, CHATBOT_API_NAMESPACE, CHATBOT_API_PORT)
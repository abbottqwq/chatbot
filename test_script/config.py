import os
MINIKUBE_IP= os.environ.get('MINIKUBE_IP', '192.168.68.16')
TEST_PORT = int(os.environ.get('PORT', 32100))
TEST_URL = "http://" + MINIKUBE_IP + ":" + str(TEST_PORT)

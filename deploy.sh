PWD
ls
docker build -t abbottqwq/chatbot-client:lastest -t abbottqwq/chatbot-client:$SHA -f ./chatbot-client/Dockerfile ./chatbot-client
docker build -t abbottqwq/chatbot-api:lastest -t abbottqwq/chatbot-api:$SHA -f ./chatbot-api/Dockerfile ./chatbot-api
# docker build -t abbottqwq/chatbot-client:lastest -t abbottqwq/chatbot-client:$SHA -f ./chatbot-client/Dockerfile ./chatbot-client
docker build -t abbottqwq/chatbot-server:lastest -t abbottqwq/chatbot-server:$SHA -f ./chatbot-server/Dockerfile ./chatbot-server

docker build -t abbottqwq/mongo-worker:lastest -t abbottqwq/mongo-worker:$SHA -f ./mongo-worker/Dockerfile ./mongo-worker
docker build -t abbottqwq/redis-worker:lastest -t abbottqwq/redis-worker:$SHA -f ./redis-worker/Dockerfile ./redis-worker

docker push abbottqwq/chatbot-api:lastest
docker push abbottqwq/chatbot-client:lastest
docker push abbottqwq/chatbot-server:lastest

docker push abbottqwq/mongo-worker:lastest
docker push abbottqwq/redis-worker:lastest

docker push abbottqwq/chatbot-api:$SHA
docker push abbottqwq/chatbot-client:$SHA
docker push abbottqwq/chatbot-server:$SHA

docker push abbottqwq/mongo-worker:$SHA
docker push abbottqwq/redis-worker:$SHA

kubectl apply -f namespace
kubectl apply -f k8s


kubectl set image deployments/chatbot-api-deployment chatbot-api=abbottqwq/chatbot-api:lastest
kubectl set image deployments/chatbot-client-deployment chatbot-api=abbottqwq/chatbot-client:lastest
kubectl set image deployments/chatbot-server-deployment chatbot-api=abbottqwq/chatbot-server:lastest
kubectl set image deployments/redis-worker-deployment chatbot-api=abbottqwq/rediskubectl set image deployments/redis-worker:lastest
kubectl set image deployments/mongo-worker-deployment chatbot-api=abbottqwq/mongo-worker:lastest
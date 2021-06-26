docker build -t abbottqwq/chatbot-client:latest -t abbottqwq/chatbot-client:$SHA -f ./chatbot-client/Dockerfile ./chatbot-client
docker build -t abbottqwq/chatbot-api:latest -t abbottqwq/chatbot-api:$SHA -f ./chatbot-api/Dockerfile ./chatbot-api
# docker build -t abbottqwq/chatbot-client:latest -t abbottqwq/chatbot-client:$SHA -f ./chatbot-client/Dockerfile ./chatbot-client
docker build -t abbottqwq/chatbot-server:latest -t abbottqwq/chatbot-server:$SHA -f ./chatbot-server/Dockerfile ./chatbot-server

docker build -t abbottqwq/mongo-worker:latest -t abbottqwq/mongo-worker:$SHA -f ./mongo-worker/Dockerfile ./mongo-worker
docker build -t abbottqwq/redis-worker:latest -t abbottqwq/redis-worker:$SHA -f ./redis-worker/Dockerfile ./redis-worker

docker push abbottqwq/chatbot-api:latest
docker push abbottqwq/chatbot-client:latest
docker push abbottqwq/chatbot-server:latest

docker push abbottqwq/mongo-worker:latest
docker push abbottqwq/redis-worker:latest

docker push abbottqwq/chatbot-aapi:$SHA
docker push abbottqwq/chatbot-client:$SHA
docker push abbottqwq/chatbot-server:$SHA

docker push abbottqwq/mongo-worker:$SHA
docker push abbottqwq/redis-worker:$SHA

kubectl apply -f namespace
kubectl apply -f k8s


kubectl set image deployments/chatbot-api-deployment chatbot-api=abbottqwq/chatbot-api:latest
kubectl set image deployments/chatbot-client-deployment chatbot-client=abbottqwq/chatbot-client:latest
kubectl set image deployments/chatbot-server-deployment chatbot-server=abbottqwq/chatbot-server:latest
kubectl set image deployments/redis-worker-deployment redis-worker=abbottqwq/redis-worker:latest
kubectl set image deployments/mongo-worker-deployment mongo-worker=abbottqwq/mongo-worker:latest
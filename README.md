# chatbot
api: <br>
POST /api/message json: {message: "my message"} return {"res": "response message"} or {"res": "response message", "error": "REDIS_WRITE_ERROR"} if something wrong with redis <BR>
GET /api/message debug only

POST /api/teachme json: {message: "my message", res: "the ideal response"} return {} if everything is ok. {'mongo_error':1} if mongodb has error; {'redis_error':1} if redis error <br>
GET /api/teachme debug only

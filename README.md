# chatbot
api: <br>
POST /api/message json: {message: "my message"} return {"res": "response message"} or {"res": "response message", "error": "REDIS_WRITE_ERROR"} if something wrong with redis
GET /api/message debug only


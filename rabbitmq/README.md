Start Server
```
uvicorn main:app --reload
```

Send message
```
curl -X POST "http://127.0.0.1:8000/send/" -H "Content-Type: application/json" -d '{"message": "Hello, RabbitMQ!"}'
```

Start consuming messages
```
curl "http://127.0.0.1:8000/consume/"
```
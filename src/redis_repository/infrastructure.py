import redis

client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

try:
    response = client.ping()
    print(f'Connect to Redis: {response}')
except redis.ConnectionError as e:
        print(f'Connect failed: {e}')

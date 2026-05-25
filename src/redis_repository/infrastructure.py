import redis

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

try:
    response = redis_client.ping()
    print(f'Connect to Redis: {response}')
except redis.ConnectionError as e:
        print(f'Connect failed: {e}')



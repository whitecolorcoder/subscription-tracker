
docker pull redis
docker pull postgres

# Start a Redis container
docker run --name my-redis -p 6379:6379 -d redis

# Start a PostgreSQL container
docker run --name my-postgres -e POSTGRES_PASSWORD=12345 -p 5432:5432 -d postgres


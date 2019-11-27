## Python Echo Server with Redis client.

Consists of:
1. Docker installation for TCP echo server based on python listening on port 5000;
2. Redis startup.sh script to run redis container;
3. Redis-py client to write echoed messages to Redis.

### Installation

1. Run ```docker network create --driver bridge echo-net``` to create network for inter-container communication;
2. Run ```redis_startup.sh``` to start Redis container listening on port 6379;
3. Run ```docker build -t socket_echo:1.0 .``` to build python-echo image;
4. Run ```docker run --name socket_echo --network echo-net -p 5000:5000 -d socket_echo:1.0``` to start python-echo container.

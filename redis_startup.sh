#!/bin/bash
docker run --name redis-for-echo --network echo-net -p 6379:6379 -d redis:latest

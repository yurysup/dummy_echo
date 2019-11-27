#!/usr/bin/env python

import sys
import socket
import selectors
import types
import redis
from datetime import datetime

sel = selectors.DefaultSelector()

try:
    # Use connection pool not to handle connection closure; 6379 standard Redis port
    pool = redis.ConnectionPool(host='redis-for-echo', port=6379, db=0)
    red = redis.Redis(connection_pool=pool)
except Exception:
    print("Can't connect to Redis!")

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    #print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            # Send data also to Redis
            red_key = echo_prefix + str(int(datetime.now().timestamp()))
            red_value = str(data.outb.decode("utf-8"))
            red.set(red_key, red_value)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
echo_prefix = 'echo:'

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()

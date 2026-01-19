import time
import uuid
import threading
import socket


users = {}


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8080))
server.listen(5)

lock = threading.Lock()


def accept_connections():
    while True:
        conn, _ = server.accept()
        id = str(uuid.uuid4())
        with lock:
            users[id] = {"tokens": 10, "last_refill": time.time()}
        t1 = threading.Thread(target=listen_connection, args=(id, conn), daemon=True)
        t1.start()


def listen_connection(id, conn):
    while True:
        _ = conn.recv(1024).decode()
        with lock:
            time_now = time.time()
            time_elapsed = time_now - users[id]["last_refill"]
            tokens = users[id]["tokens"] + time_elapsed * (10 / 60)
            tokens = min(10, tokens)
            users[id]["tokens"] = tokens
            users[id]["last_refill"] = time_now
            if users[id]["tokens"] >= 1:
                users[id]["tokens"] -= 1
                response = f"Yes allowed. {users[id]['tokens']}/10".encode()
                conn.sendall(response)
            else:
                conn.sendall("You have hit the limit. Try again later.".encode())


t = threading.Thread(target=accept_connections, daemon=True)
t.start()

while True:
    time.sleep(1)

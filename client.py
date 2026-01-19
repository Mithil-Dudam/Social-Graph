import socket
import threading
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 8080))


def send_requests():
    while True:
        request = input("").encode()
        client.sendall(request)


def listen_responses():
    while True:
        response = client.recv(1024).decode()
        print(f"Server response: {response}")


t = threading.Thread(target=send_requests, daemon=True)
t1 = threading.Thread(target=listen_responses, daemon=True)
t.start()
t1.start()

while True:
    time.sleep(1)

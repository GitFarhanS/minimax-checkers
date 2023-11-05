import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))


print("hello")

def handle_conn():
    print("test")


x = 0

while x==0:
    handle_conn()
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

def check_database(username, password):
    client.send(username.encode())
    client.send(password.encode())
    confirmation = (client.recv(1024).decode())
    print(confirmation)
    if confirmation == "Login successful":
        return True
    else:
        return False

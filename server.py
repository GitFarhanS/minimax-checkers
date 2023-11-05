import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

server.listen(5)


def handle_conn(c):
    username = c.recv(1024).decode()
    password = c.recv(1024)
    password = hashlib.sha256(password).hexdigest()

    conn = sqlite3.connect("userdata.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

    if cursor.fetchall():
        c.send("Login successful".encode())

    else:
        c.send("Login failed".encode())

    c.close()


while True:
    client, addr = server.accept()
    threading.Thread(target=handle_conn, args=(client,)).start()

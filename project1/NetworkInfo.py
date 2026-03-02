import socket
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
print("Computer Name :", hostname)
print("IP Address :", ip)
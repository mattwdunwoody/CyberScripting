import socket
import time
import threading
from queue import Queue

# ANSI color codes
RESET = "\033[0m"
BOLD  = "\033[1m"
BLUE  = "\033[38;5;39m"   # Kali blue

# set  default socket timeout in seconds
socket.setdefaulttimeout(0.55)

# lock thread during print so we get cleaner outputs
thread_lock = threading.Lock()

def banner():
    print(BLUE + BOLD + r"""
 __  __  _    _    ____  _____  _____  __    ___ 
(  \/  )( \/\/ )  (_  _)(  _  )(  _  )(  )  / __)
 )    (  )    (     )(   )(_)(  )(_)(  )(__ \__ \
(_/\/\_)(__/\__)   (__) (_____)(_____)(____)(___/
""" + RESET)

# get target ip and port range as input from the user
print("="*50)
print("Simple Port Scanner")
print("="*50)
banner()
target_ip = input("Enter Target IP: ")
port_start = eval(input("Enter Target Port to start (Eg. 01: "))
port_stop = eval(input("Enter Target Port to end (Eg. 065535: "))
print("-"*50)

print("Scanning Host for Open Ports", target_ip)

def portscan(port):

    # create socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # try to connect
    try:
        # create/open connection
        conx = s.connect((target_ip, port))

        # don't let thread to screw up printing
        with thread_lock:
            print(port, "is open")

        # close connection
        conx.close()
    except:
        pass

# handles port threading
def portThreader():
    while True:
        # gets a port from the queue
        thisPortToScan = q.get()

        # run job with available port in queue (thread)
        portscan(thisPortToScan)

        # mark job as complete in queue
        q.task_done()

# create queue
q = Queue()

# start time
startTime = time.time()

# 200 threads
for x in range(200):
    # thread id
    t = threading.Thread(target=portThreader)

    # classifying as a daemon so they will die when the main dies
    t.daemon = True

    # begins, must come after daemon definition
    t.start()

# ports passed to queue
for thisPort in range(port_start, port_stop):
    q.put(thisPort)

# wait until the thread terminates
q.join()

# print run time
print("="*50)
print("Run Time: ", round(time.time() - startTime, 2), "seconds")
print("="*50)
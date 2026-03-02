import time

def main():
    start_port = eval(input("Enter the port number to stort: "))
    stop_port = eval(input("Enter the port number to stop: "))

    for i in range(start_port, stop_port+1):
        time.sleep(5)
        print(i)

main()
# How to use these programs

## Port Scanner
###### This port scanner steps through a user-provided range of ports on a user-given target IP address and outputs which ports are currently open.
### DO NOT use this to scan IP addresses outside of your network or any hardware that you do not own!
1. Run file
2. Enter target IP
3. Enter the port to start at (eg. 0)
4. Enter the port to end at (eg. 065535)
5. The program should run and may take a while. Use discretion when selecting a target.

## Folder Security Scanner
###### This scanner scans text file within a given folder for specific suspicious words using YARA rules.
Instructions:
1. Run file
2. Select a folder to scan by clicking the "Select Folder" button
3. Once the folder has been selected, click the "Scan Selected Folder" button
4. List of suspicious words can be updated in the source code

## TCP Reverse Shell
###### This is a reverse shell program that allows a server to remotely exucute commands on a client machine. This includes directory scanning and traversal, sending and grabbing files to and from the victim machine, and remote screen capture. It also has persistence features to hide itself within the registry and persist even if the victim restarts their machine.
### Setup Instructions
1. Install the client script onto the victim machine
2. Install the server script to a kali server
3. Configure the IP address in both files to the IP address of the kali machine
4. Run the server file to wait for incoming connections from the client
5. Run the client file on the client to initialize the connection
### Commands and Features
terminate: terminates connection

```dir```: shows current directory and its contents

```cd```: allows for changing directories. Format: ```cd <path>``` Example: ```cd C:\Users\user\Desktop```

```grab```: grabs a file from the victim's machine. Format: ```grab*<File Path>``` Example: ```grab*C:\Users\John\Desktop\photo.jpg```

```send```: sends a file to the victim's machine. Format: ```send*<destination path>*<File name>``` Example: ```send*C:\Users\John\Desktop\*photo.jpg```

```screencap```: captures a screenshot of the victim's machine and sends it to the kali server. Output files can be found in ```/home/kali/Desktop/```

```checkUserLevel```: determines the privilege level that the client is running on. (whether or not you have admin privileges)

Some default windows commands such as ```whoami```, ```ipconfig```, etc.

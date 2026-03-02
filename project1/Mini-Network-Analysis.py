import psutil
for conn in psutil.net_connections():
    if conn.status == 'LISTEN':
        print("Listening on port : ", conn.laddr.port)

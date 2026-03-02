import psutil

for conn in psutil.net_connections(kind='inet'):
    print(conn)
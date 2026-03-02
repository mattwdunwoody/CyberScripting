import psutil
import ipaddress

print("=" * 50)
print("     Suspicious Connection Check     ")
print("=" * 50)

for conn in psutil.net_connections(kind="inet"):
    if conn.raddr:
        remote_ip = conn.raddr.ip
        remote_port = conn.raddr.port

    try:
        ip_obj = ipaddress.ip_address(remote_ip)
        if ip_obj.is_global:  # public internet IP

            if remote_port not in [80, 443, 53]:
                print("Suspicious:", remote_ip, "Port:", remote_port, "Status:", conn.status)
    except:
        pass


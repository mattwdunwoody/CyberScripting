import psutil
import time
from datetime import datetime

print("Network monitor running...\n")

old = psutil.net_io_counters()

while True:
    time.sleep(1)
    new = psutil.net_io_counters()
    up = (new.bytes_sent - old.bytes_sent) / 1024
    down = (new.bytes_recv - old.bytes_recv) / 1024
    old = new

    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] UP: {round(up, 2)} KB/s | DOWN: {round(down, 2)} KB/s")

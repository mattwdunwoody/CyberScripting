import psutil
from datetime import datetime

# Get system boot time
bootTime = psutil.boot_time()
print(bootTime)

# Convert timestamp to readable date-time
readable_boot_time = datetime.fromtimestamp(bootTime)
print(readable_boot_time)
print("System Boot Time: ", readable_boot_time.strftime('%Y-%m-%d %H:%M:%S'))
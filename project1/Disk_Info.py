import psutil

disk = psutil.disk_usage("C:\\")
print("Total: ", round(disk.total / (1024**3), 2), "GB")
print("Used (GB) : ", round(disk.used / (1024**3), 2), "GB")
print("Free (GB) : ", round(disk.free / (1024**3), 2), "GB")
print("Disk Usage (%): ", disk.percent, "%")
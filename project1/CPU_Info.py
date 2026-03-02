import psutil
import platform

# powerful library, can be used to do much more
print("Processor: ", platform.processor())

print("Physical cores: ", psutil.cpu_count(logical=False))
print("Logical  cores: ", psutil.cpu_count(logical=True))
print("CPU Usage:      ", psutil.cpu_percent(interval=1), "%")

import psutil
ram = psutil.virtual_memory()
print("Total: ", round(ram.total / (1024**3), 2), "GB")
print("Available: ", round(ram.available / (1024**3), 2), "GB")
print("Used: ", round(ram.used / (1024**3), 2), "GB")
print("Percentage: ", ram.percent, "%")
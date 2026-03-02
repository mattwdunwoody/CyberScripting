import os

# ANSI color codes
RESET = "\033[0m"
BOLD  = "\033[1m"
BLUE  = "\033[38;5;39m"   # Kali blue
WHITE = "\033[97m"
GRAY  = "\033[90m"
RED   = "\033[91m"

def banner():
    print(BLUE + BOLD + r"""
 __  __       _   _   _                     _____           _     
|  \/  | __ _| |_| |_| |__   _____      __ |_   _|__   ___ | |___ 
| |\/| |/ _` | __| __| '_ \ / _ \ \ /\ / /   | |/ _ \ / _ \| / __|
| |  | | (_| | |_| |_| | | |  __/\ V  V /    | | (_) | (_) | \__ \
|_|  |_|\__,_|\__|\__|_| |_|\___| \_/\_/     |_|\___/ \___/|_|___/
""" + RESET)

def main():
    banner()
    print(GRAY + "=" * 50 + RESET)
    print("hi")
    print(GRAY + "=" * 50)

main()

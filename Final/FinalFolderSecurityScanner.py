#import tkinter for GUI
import tkinter as tk
#import file dialog to select folders
from tkinter import filedialog
#import os to work with files and folders
import os
# import datetime to calculate start and end times
import datetime

# global variable to store selected folder path
selected_folder = ""

# handles obtaining the file directory to scan
def fetch_folder():
    global selected_folder

    # opens the dialog to select a folder
    folder_path = filedialog.askdirectory()

    # if the path exists, update the selected_folder varaible and the GUI
    if folder_path:
        selected_folder = folder_path
        folder_label.config(text=f"Selected Folder:{selected_folder}")

    else:
        folder_label.config(text="No Folder Selected")

def scan_folder():
    global selected_folder

    #if no folder is selected, show error message and stop
    if not selected_folder:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "[ERROR] Please select a folder.\n")
        return

    #clear previous results from the text box
    result_text.delete("1.0", tk.END)

    #List of suspicious keywords to scan for
    suspicious_words = [
        # Urgency / Pressure
        "urgent", "immediately", "asap", "action required", "important", "alert",

        # Account / Security
        "account", "account suspended", "account locked", "verify", "verification",
        "confirm", "security alert", "unauthorized", "suspicious activity",

        # Credentials
        "password", "username", "login", "signin", "credentials", "reset password",

        # Financial / Banking
        "bank", "credit card", "debit card", "payment", "transaction",
        "billing", "invoice", "refund", "transfer", "wire", "deposit",

        # Threat / Fear
        "suspended", "terminated", "blocked", "restricted", "penalty",
        "legal action", "fine", "court", "lawsuit",

        # Links / Actions
        "click here", "click below", "open link", "download", "attachment",
        "update", "upgrade", "install", "access now",

        # Personal Info Requests
        "ssn", "social security", "date of birth", "dob", "pin",
        "otp", "verification code", "security code",

        # Prize / Scam
        "winner", "won", "prize", "lottery", "free", "gift",
        "claim now", "limited offer",

        # Email Tricks
        "dear user", "dear customer", "official notice", "final warning",

        # Tech / IT Scams
        "virus detected", "malware", "system infected", "technical support",
        "remote access", "support team"
    ]

    # record the starting time and totals
    start_time = datetime.datetime.now()
    total_bad_files = 0
    total_bad_words = 0

    #loop through all files in selected folder
    for filename in os.listdir(selected_folder):
        #check only txt files
        if filename.endswith(".txt"):
            # calculate the full path
            file_path = os.path.join(selected_folder, filename)

            try:
                # open and read the content
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read().lower()

                # create an array of found suspicous words in the file content
                found = [word for word in suspicious_words if word in content]

                # if the array has data:
                if found:
                    # add an entry in the output for the file and all suspicious words
                    result_text.insert(tk.END, f"[WARNING] {filename}: {', '.join(found)}\n", "warning")

                    # update totals
                    total_bad_files += 1
                    total_bad_words += len(found)

                # if no suspicious words found, mark as safe
                else:
                    result_text.insert(tk.END, f"[SAFE] {filename}\n", "safe")

            except Exception as e:
                result_text.insert(tk.END, f"[ERROR] {filename} : {str(e)}\n", "error")

    # record the end time and the elapsed time as well as print totals
    end_time = datetime.datetime.now()
    result_text.insert(tk.END, f"[INFO] Start time: {start_time} \nEnd Time: {end_time} \nElapsed time: {end_time - start_time}\nTotal number of suspicious files: {total_bad_files}\nTotal number of suspicious text: {total_bad_words}", "info")


# GUI setup
myapp = tk.Tk()
myapp.title('Folder Security Scanner')
myapp.geometry('600x400')
myapp.configure(bg='lightblue')

# title label
title_label = tk.Label(myapp, text="Scan Folder for Suspicious Text", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

# button to select a folder
fetch_btn = tk.Button(myapp, text="Select Folder", command=fetch_folder)
fetch_btn.pack(pady=5)

# label to show the selected path
folder_label = tk.Label(myapp, text="No folder selected", wraplength=650, fg="blue")
folder_label.pack(pady=5)

# button to start the scan
scan_btn = tk.Button(myapp, text="Scan Selected Folder", command=scan_folder)
scan_btn.pack(pady=10)

#create text box to display results
result_text = tk.Text(myapp, width=80, height=20)
result_text.pack(pady=10, padx=10)

# configuring tags and colors
result_text.tag_config("warning", foreground="red")
result_text.tag_config("safe", foreground="green")
result_text.tag_config("error", foreground="red")
result_text.tag_config("info", foreground="blue")

# start main loop
myapp.mainloop()
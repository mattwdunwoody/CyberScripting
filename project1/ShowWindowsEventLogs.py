import os
os.system('powershell "Get-EventLog -LogName System -Newest 40 | Format-Table -AutoSize"')
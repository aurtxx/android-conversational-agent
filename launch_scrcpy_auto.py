"""
Auto-launcher for scrcpy.
Monitors ADB connection and launches scrcpy desktop mirror window
immediately when the device becomes online/authorized.
"""

import time
import subprocess

ADB = r"C:\Program Files\platform-tools\adb.exe"
SCRCPY = r"C:\Users\aurtx\AppData\Local\Microsoft\WinGet\Packages\Genymobile.scrcpy_Microsoft.Winget.Source_8wekyb3d8bbwe\scrcpy-win64-v4.1\scrcpy.exe"
SERIAL = "dc3e96b9"

print("[*] Waiting for device dc3e96b9 to become online for scrcpy...", flush=True)

while True:
    res = subprocess.run([ADB, "devices"], capture_output=True, text=True)
    lines = res.stdout.strip().splitlines()
    is_online = False
    for line in lines[1:]:
        if SERIAL in line and "\tdevice" in line:
            is_online = True
            break

    if is_online:
        print("[+] Device is ONLINE! Launching scrcpy window...", flush=True)
        cmd = [SCRCPY, "-s", SERIAL, "-w", "--no-audio"]
        subprocess.run(cmd)
        break

    time.sleep(1.5)

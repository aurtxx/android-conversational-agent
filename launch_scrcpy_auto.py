#!/usr/bin/env python3
"""
Auto-launcher for scrcpy.
Monitors ADB connection and launches scrcpy desktop mirror window
automatically when an authorized Android device is connected.
"""

import time
import subprocess
from core.device import find_adb
from core.mirror import find_scrcpy

ADB = find_adb()
SCRCPY = find_scrcpy()

print("[*] Waiting for any authorized Android device to become online for scrcpy...", flush=True)

while True:
    try:
        res = subprocess.run([ADB, "devices"], capture_output=True, text=True, timeout=5)
        lines = res.stdout.strip().splitlines()
        connected_serial = None
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) >= 2 and parts[1] == "device":
                connected_serial = parts[0]
                break

        if connected_serial:
            print(f"[+] Device {connected_serial} is ONLINE! Launching scrcpy window...", flush=True)
            cmd = [SCRCPY, "-s", connected_serial, "-w", "--no-audio"]
            subprocess.run(cmd)
            break
    except Exception as e:
        pass

    time.sleep(2.0)

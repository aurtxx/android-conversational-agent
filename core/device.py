"""
Device Connection & Control Module.
Handles ADB discovery, health check, and strict User Permission Gating.
"""

import os
import re
import subprocess
import sys
import time

ADB_SEARCH_PATHS = [
    r"C:\Program Files\platform-tools\adb.exe",
    os.path.expanduser(r"~\AppData\Local\Android\Sdk\platform-tools\adb.exe"),
    "adb"
]

def find_adb():
    for path in ADB_SEARCH_PATHS:
        try:
            r = subprocess.run([path, "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if r.returncode == 0:
                return path
        except Exception:
            continue
    return "adb"

ADB_BIN = find_adb()

class DeviceManager:
    def __init__(self, serial=None, auto_approve=False):
        self.adb = ADB_BIN
        self.serial = serial
        self.auto_approve = auto_approve
        self.device_info = {}

    def scan_devices(self):
        try:
            res = subprocess.run([self.adb, "devices", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            lines = res.stdout.strip().splitlines()[1:]
            devices = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 2 and parts[1] == "device":
                    devices.append(parts[0])
            return devices
        except Exception as e:
            print(f"[-] ADB Error scanning devices: {e}", file=sys.stderr)
            return []

    def get_device_metadata(self, serial):
        def _get_prop(prop):
            r = subprocess.run([self.adb, "-s", serial, "shell", "getprop", prop], stdout=subprocess.PIPE, text=True)
            return r.stdout.strip()

        brand = _get_prop("ro.product.brand")
        model = _get_prop("ro.product.model")
        version = _get_prop("ro.build.version.release")
        
        # Screen size
        size_res = subprocess.run([self.adb, "-s", serial, "shell", "wm", "size"], stdout=subprocess.PIPE, text=True).stdout
        m = re.search(r"(\d+)x(\d+)", size_res)
        screen_size = f"{m.group(1)}x{m.group(2)}" if m else "Unknown"

        # Battery
        bat_res = subprocess.run([self.adb, "-s", serial, "shell", "dumpsys", "battery"], stdout=subprocess.PIPE, text=True).stdout
        bat_match = re.search(r"level:\s*(\d+)", bat_res)
        battery = f"{bat_match.group(1)}%" if bat_match else "Unknown"

        return {
            "serial": serial,
            "brand": brand or "Android",
            "model": model or "Device",
            "android_version": version or "Unknown",
            "screen_size": screen_size,
            "battery": battery
        }

    def connect(self):
        devices = self.scan_devices()
        if not devices:
            print("[!] No authorized USB debugging Android devices found.")
            print("[*] Please connect phone via USB and enable 'USB Debugging' in Developer Options.")
            return False

        if self.serial and self.serial in devices:
            target_serial = self.serial
        else:
            target_serial = devices[0]

        self.device_info = self.get_device_metadata(target_serial)
        self.serial = target_serial

        # Strict User Permission Gate
        if not self.auto_approve:
            print("\n" + "=" * 50)
            print("🔐 ANDROID DEVICE PERMISSION GATE")
            print("=" * 50)
            print(f"Device Brand:    {self.device_info['brand']}")
            print(f"Device Model:    {self.device_info['model']}")
            print(f"Serial ID:       {self.device_info['serial']}")
            print(f"Android Version: {self.device_info['android_version']}")
            print(f"Display:         {self.device_info['screen_size']}")
            print(f"Battery Level:   {self.device_info['battery']}")
            print("=" * 50)
            
            prompt = input("Do you grant this agent permission to connect and control this device? [y/N]: ").strip().lower()
            if prompt not in ["y", "yes"]:
                print("[X] Permission denied by user. Aborting device control.")
                return False

        print(f"[+] Device control granted for {self.device_info['model']} ({self.serial})")
        # Keep awake
        subprocess.run([self.adb, "-s", self.serial, "shell", "svc", "power", "stayon", "true"], stdout=subprocess.DEVNULL)
        return True

    def run_cmd(self, args, timeout=15):
        cmd = [self.adb, "-s", self.serial] + args
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)

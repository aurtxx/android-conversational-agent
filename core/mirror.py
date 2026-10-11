"""
Screen Mirroring Controller via scrcpy.
Allows live PC view and human-in-the-loop control alongside automated agents.
"""

import os
import subprocess

SCRCPY_PATHS = [
    os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Packages\Genymobile.scrcpy_Microsoft.Winget.Source_8wekyb3d8bbwe\scrcpy-win64-v4.1\scrcpy.exe"),
    os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Microsoft\WinGet\Packages\Genymobile.scrcpy_Microsoft.Winget.Source_8wekyb3d8bbwe\scrcpy-win64-v4.1\scrcpy.exe"),
    "scrcpy"
]

def find_scrcpy():
    for p in SCRCPY_PATHS:
        try:
            r = subprocess.run([p, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if r.returncode == 0:
                return p
        except Exception:
            continue
    return "scrcpy"

SCRCPY_BIN = find_scrcpy()

def launch_scrcpy(serial=None, stay_awake=True, turn_screen_off=False, no_audio=True):
    cmd = [SCRCPY_BIN]
    if serial:
        cmd.extend(["-s", serial])
    if stay_awake:
        cmd.append("-w")
    if turn_screen_off:
        cmd.append("-S")
    if no_audio:
        cmd.append("--no-audio")

    try:
        proc = subprocess.Popen(cmd)
        print(f"[+] scrcpy mirror window started (PID: {proc.pid})")
        return proc
    except Exception as e:
        print(f"[-] Could not launch scrcpy: {e}")
        return None

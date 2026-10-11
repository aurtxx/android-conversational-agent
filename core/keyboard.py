"""
Android Soft Keyboard Manager & Safe Input Guard.
Provides reliable keyboard visibility detection, safe dismissal via KEYCODE_BACK,
and ASCII text sanitization for ADB input without shell truncation or crashes.
"""

import re
import subprocess
import time

class KeyboardGuard:
    def __init__(self, device_serial=None, adb_path="adb"):
        self.device_serial = device_serial
        self.adb = adb_path

    def _cmd(self, args):
        cmd = [self.adb]
        if self.device_serial:
            cmd.extend(["-s", self.device_serial])
        cmd.extend(args)
        return subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=8
        )

    def is_keyboard_open(self):
        """Checks dumpsys input_method to verify if the soft keyboard is currently visible."""
        try:
            res = self._cmd(["shell", "dumpsys", "input_method"])
            raw = res.stdout.decode("utf-8", errors="ignore")
            return "mInputShown=true" in raw
        except Exception:
            return False

    def dismiss_keyboard(self, verify=True, delay=0.3):
        """
        Safely dismisses the soft keyboard only if it is currently open.
        Prevents accidental back-navigation out of the conversation.
        """
        if self.is_keyboard_open():
            self._cmd(["shell", "input", "keyevent", "KEYCODE_BACK"])
            time.sleep(delay)
            if verify and self.is_keyboard_open():
                # Second attempt if keyboard is stubborn
                self._cmd(["shell", "input", "keyevent", "KEYCODE_BACK"])
                time.sleep(delay)
            return True
        return False

    @staticmethod
    def sanitize_adb_text(text):
        """
        Sanitizes text for 'adb shell input text':
        - Replaces spaces with '%s'
        - Escapes special shell characters (?, &, ', !, (, ))
        - Strips unsupported non-ASCII / emoji characters that crash Android shell
        """
        if not text:
            return ""
        
        # Strip or convert emojis / non-ascii to avoid 'Killed' error in adb shell input text
        ascii_text = text.encode("ascii", "ignore").decode("ascii")
        
        escaped = (
            ascii_text.replace(" ", "%s")
            .replace("?", "\\?")
            .replace("&", "\\&")
            .replace("'", "\\'")
            .replace("!", "\\!")
            .replace("(", "\\(")
            .replace(")", "\\)")
            .replace("\"", "\\\"")
            .replace("`", "")
            .replace("$", "\\$")
            .replace(";", "\\;")
        )
        return escaped

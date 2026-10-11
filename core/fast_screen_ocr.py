"""
Fast Sub-Second OCR & Screen Extraction Engine for WhatsApp.
Captures live screen, runs RapidOCR, extracts dialogue bubbles,
and pipes them directly into SmolLM2 Memory Manager.
"""

import io
import os
import re
import sys
import time
import subprocess
import numpy as np
from PIL import Image

ADB_BIN = r"C:\Program Files\platform-tools\adb.exe"
DEVICE = "dc3e96b9"

class FastScreenExtractor:
    def __init__(self, target_name="Krupali", device=DEVICE):
        self.target_name = target_name
        self.device = device
        self.ocr = None
        self._init_ocr()

    def _init_ocr(self):
        try:
            from rapidocr_onnxruntime import RapidOCR
            self.ocr = RapidOCR()
            print("[+] RapidOCR engine initialized.")
        except Exception as e:
            print(f"[-] RapidOCR init error: {e}")
            self.ocr = None

    def capture_screenshot(self):
        cmd = [ADB_BIN, "-s", self.device, "exec-out", "screencap", "-p"]
        t0 = time.time()
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elapsed = time.time() - t0
        if res.returncode == 0 and len(res.stdout) > 1000:
            return res.stdout, elapsed
        return None, elapsed

    def extract_bubbles_ocr(self, img_bytes):
        if not self.ocr:
            return []

        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        width, height = img.size

        # Ignore top status/action bar (y < 120) and bottom keyboard/entry (y > 1180)
        top_crop = 130
        bottom_crop = 1180

        result, _ = self.ocr(np.array(img))
        if not result:
            return []

        bubbles = []
        for item in result:
            box, text, score = item[0], item[1], float(item[2])
            text = text.strip()
            if score < 0.65 or not text:
                continue

            x0, y0 = box[0][0], box[0][1]

            if y0 < top_crop or y0 > bottom_crop:
                continue

            # Ignore timestamps (e.g. 22:34, 13:51)
            if re.match(r"^\d{1,2}:\d{2}$", text):
                continue
            # Ignore date chips
            if any(d in text for d in ["September", "October", "November", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
                continue
            if text in ["Message", "TODAY", "YESTERDAY"]:
                continue

            # Left side (x < 150) is Target (Krupali), Right side is You
            is_incoming = (x0 < 150)
            sender = self.target_name if is_incoming else "You"

            bubbles.append({
                "sender": sender,
                "text": text,
                "is_incoming": is_incoming,
                "x": x0,
                "y": y0,
                "score": score
            })

        bubbles.sort(key=lambda b: b["y"])
        return bubbles

    def read_screen_live(self):
        t0 = time.time()
        img_bytes, cap_t = self.capture_screenshot()
        if not img_bytes:
            return [], time.time() - t0

        bubbles = self.extract_bubbles_ocr(img_bytes)
        return bubbles, time.time() - t0

if __name__ == "__main__":
    ext = FastScreenExtractor("Krupali")
    bubbles, duration = ext.read_screen_live()
    print(f"\n[+] Extracted {len(bubbles)} bubbles in {duration:.2f}s:")
    for b in bubbles:
        side = "IN " if b["is_incoming"] else "OUT"
        print(f"[{side}] {b['sender']}: {b['text']}")

"""
Krupali Conversational Assistant.
Integrates:
1. Fast OCR sub-second screen extraction (RapidOCR)
2. SmolLM2 Local Memory Manager (SmolLM2-135M)
3. Semi-autonomous / interactive execution loop for Krupali Ni.
"""

import os
import sys
import time
import subprocess
from core.fast_screen_ocr import FastScreenExtractor
from brain.memory_manager import SmolMemoryManager

if sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ADB_BIN = r"C:\Program Files\platform-tools\adb.exe"
DEVICE = "dc3e96b9"

OPENER_MESSAGE = "Hey Krupali, thoda time hai kya casual baat karne ka? Kuch interesting puchna tha actually"
CHOICE_C_MESSAGE = "Bas ye confirm karna tha: 1st year me aake Google/Microsoft phodne ka josh bacha hai ya already mann bana liya hai ki 'bhai bas pass karwa do'? Haha"

def send_whatsapp_text(message):
    print(f"\n[*] Typing message: '{message}'", flush=True)
    # Tap entry box
    subprocess.run([ADB_BIN, "-s", DEVICE, "shell", "input", "tap", "250", "1222"])
    time.sleep(0.3)

    # Format text for adb input text
    formatted = (message.replace(" ", "%s")
                 .replace("?", "\\?")
                 .replace("&", "\\&")
                 .replace("'", "\\'")
                 .replace("!", "\\!")
                 .replace("(", "\\(")
                 .replace(")", "\\)"))
    subprocess.run([ADB_BIN, "-s", DEVICE, "shell", "input", "text", formatted])
    time.sleep(0.5)

    # Tap send button
    subprocess.run([ADB_BIN, "-s", DEVICE, "shell", "input", "tap", "653", "719"])
    time.sleep(0.5)
    print("[+] Message sent successfully!", flush=True)

def main():
    print("=" * 60)
    print("[*] KRUPALI CONVERSATION ASSISTANT (SmolLM2 + Fast OCR)")
    print("=" * 60)

    extractor = FastScreenExtractor("Krupali")
    memory = SmolMemoryManager("Krupali")

    # Initial screen read
    print("\n[*] Reading current chat screen via OCR...")
    bubbles, elapsed = extractor.read_screen_live()
    added = memory.arrange_and_update(bubbles)
    print(f"[+] Loaded baseline memory ({len(memory.history)} turns in {elapsed:.2f}s).")
    print("\nCurrent Memory State:")
    print(memory.get_formatted_context(max_turns=4))

    print("\n" + "=" * 60)
    print(f"Ready to send Opener (Option 3):")
    print(f"👉 \"{OPENER_MESSAGE}\"")
    print(f"Follow-up queued (Choice C):")
    print(f"👉 \"{CHOICE_C_MESSAGE}\"")
    print("=" * 60)

if __name__ == "__main__":
    main()

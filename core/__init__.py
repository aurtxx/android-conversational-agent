"""
Core hardware, ADB, screen OCR, and WhatsApp automation modules.
"""

from core.device import DeviceManager, find_adb
from core.whatsapp import WhatsAppController
from core.keyboard import KeyboardGuard
from core.mirror import launch_scrcpy
from core.fast_screen_ocr import FastScreenExtractor

__all__ = [
    "DeviceManager",
    "find_adb",
    "WhatsAppController",
    "KeyboardGuard",
    "launch_scrcpy",
    "FastScreenExtractor"
]

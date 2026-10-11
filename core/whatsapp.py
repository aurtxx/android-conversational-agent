"""
WhatsApp Automation Engine via ADB UIAutomator.
Handles dynamic coordinate detection, multiline input expansion,
live chat extraction, boundary-aware incoming/outgoing classification,
and safe keyboard dismissal.
"""

import os
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from core.keyboard import KeyboardGuard

class WhatsAppController:
    def __init__(self, device_manager):
        self.device = device_manager
        self.keyboard_guard = KeyboardGuard(
            device_serial=self.device.serial,
            adb_path=self.device.adb
        )

    def open_chat_by_phone(self, phone_number):
        """Opens WhatsApp conversation via phone number deep-link."""
        clean_num = re.sub(r"[^\d+]", "", phone_number)
        url = f"https://api.whatsapp.com/send?phone={clean_num}"
        self.device.run_cmd(["shell", "input", "keyevent", "KEYCODE_WAKEUP"])
        time.sleep(0.3)
        self.device.run_cmd(["shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url, "com.whatsapp"])
        time.sleep(2.0)
        self.keyboard_guard.dismiss_keyboard()

    def open_chat_by_search(self, contact_name, tap_pos=(195, 230)):
        """Navigates to WhatsApp home and taps target contact."""
        self.device.run_cmd(["shell", "input", "keyevent", "KEYCODE_BACK"])
        time.sleep(0.4)
        self.device.run_cmd(["shell", "input", "tap", str(tap_pos[0]), str(tap_pos[1])])
        time.sleep(1.2)
        self.keyboard_guard.dismiss_keyboard()

    def dump_ui(self):
        """Dumps current screen hierarchy using fast exec-out with safe file fallback."""
        # 1. Fast stream dump
        try:
            res = self.device.run_cmd(["exec-out", "uiautomator", "dump", "/dev/tty"], timeout=8)
            raw = res.stdout
            if "<hierarchy" in raw:
                xml_clean = raw[raw.find("<?xml"):]
                return xml_clean[:xml_clean.rfind(">") + 1]
        except Exception:
            pass

        # 2. Resilient file dump fallback
        try:
            self.device.run_cmd(["shell", "uiautomator", "dump", "/sdcard/window_dump.xml"], timeout=8)
            res2 = self.device.run_cmd(["shell", "cat", "/sdcard/window_dump.xml"], timeout=8)
            raw2 = res2.stdout
            if "<hierarchy" in raw2:
                xml_clean2 = raw2[raw2.find("<?xml"):]
                return xml_clean2[:xml_clean2.rfind(">") + 1]
        except Exception:
            pass

        return ""

    def get_chat_history(self, boundary_x2=620):
        """
        Extracts all visible chat bubbles on the screen.
        Incoming vs Outgoing classification:
          - Incoming messages: right edge bounds x2 < 620
          - Outgoing messages: right edge bounds x2 >= 620
        """
        xml_data = self.dump_ui()
        if not xml_data or "<hierarchy" not in xml_data:
            return {"contact": "", "status": "", "messages": [], "draft": ""}

        try:
            root = ET.fromstring(xml_data)
        except Exception:
            return {"contact": "", "status": "", "messages": [], "draft": ""}

        contact = ""
        status_text = ""
        draft = ""
        messages = []

        for node in root.iter("node"):
            res_id = node.attrib.get("resource-id", "")
            text = node.attrib.get("text", "").strip()
            bounds = node.attrib.get("bounds", "")

            if "conversation_contact_name" in res_id and text:
                contact = text
            if "conversation_contact_status" in res_id and text:
                status_text = text
            if res_id.endswith(":id/entry"):
                draft = text if text != "Message" else ""

            # Only genuine chat bubble text
            if "message_text" in res_id and text:
                m = re.findall(r"\[(\d+),(\d+)\]", bounds)
                if len(m) == 2:
                    x1, y1 = int(m[0][0]), int(m[0][1])
                    x2, y2 = int(m[1][0]), int(m[1][1])
                    
                    # Filter pure timestamps (e.g., 22:48)
                    if re.match(r"^\d{1,2}:\d{2}(\s*[ap]m)?$", text, re.IGNORECASE):
                        continue

                    is_incoming = (x2 < boundary_x2)
                    sender = contact if (is_incoming and contact) else ("Target" if is_incoming else "You")

                    messages.append({
                        "sender": sender,
                        "text": text,
                        "is_incoming": is_incoming,
                        "y": y1,
                        "bounds": bounds
                    })

        messages.sort(key=lambda m: m["y"])
        return {
            "contact": contact,
            "status": status_text,
            "messages": messages,
            "draft": draft
        }

    def send_message(self, message, input_tap=(250, 1222)):
        """Types and dispatches message with dynamic send-button calculation & keyboard dismissal."""
        if not message:
            return False

        # 1. Tap message entry box
        self.device.run_cmd(["shell", "input", "tap", str(input_tap[0]), str(input_tap[1])])
        time.sleep(0.35)

        # 2. Type sanitized message text
        formatted = KeyboardGuard.sanitize_adb_text(message)
        self.device.run_cmd(["shell", "input", "text", formatted])
        time.sleep(0.45)

        # 3. Dynamic send button position lookup
        send_x, send_y = 653, 719  # Default coordinate with active soft keyboard
        xml_after = self.dump_ui()
        if xml_after:
            try:
                root = ET.fromstring(xml_after)
                for node in root.iter("node"):
                    res_id = node.attrib.get("resource-id", "")
                    if any(k in res_id for k in ["send", "conversation_entry_action_button"]):
                        m = re.findall(r"\[(\d+),(\d+)\]", node.attrib.get("bounds", ""))
                        if len(m) == 2:
                            send_x = (int(m[0][0]) + int(m[1][0])) // 2
                            send_y = (int(m[0][1]) + int(m[1][1])) // 2
                            break
            except Exception:
                pass

        # 4. Tap send button
        self.device.run_cmd(["shell", "input", "tap", str(send_x), str(send_y)])
        time.sleep(0.4)

        # 5. Safely dismiss keyboard immediately
        self.keyboard_guard.dismiss_keyboard()
        return True

    def exit_chat(self):
        """Safely dismisses keyboard and returns to home screen."""
        self.keyboard_guard.dismiss_keyboard()
        self.device.run_cmd(["shell", "input", "keyevent", "KEYCODE_HOME"])

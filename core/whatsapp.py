"""
WhatsApp Automation Engine via ADB UIAutomator.
Handles dynamic coordinate detection, multiline input expansion, and live chat extraction.
"""

import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET

class WhatsAppController:
    def __init__(self, device_manager):
        self.device = device_manager

    def open_chat(self, phone_number):
        clean_num = re.sub(r"[^\d+]", "", phone_number)
        url = f"https://api.whatsapp.com/send?phone={clean_num}"
        self.device.run_cmd(["shell", "input", "keyevent", "KEYCODE_WAKEUP"])
        time.sleep(0.3)
        self.device.run_cmd(["shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url, "com.whatsapp"])
        time.sleep(2.0)

    def dump_ui(self):
        self.device.run_cmd(["shell", "uiautomator", "dump", "/sdcard/window_dump.xml"], timeout=12)
        res = self.device.run_cmd(["shell", "cat", "/sdcard/window_dump.xml"], timeout=12)
        return res.stdout

    def get_chat_history(self):
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
            text = node.attrib.get("text", "")
            bounds = node.attrib.get("bounds", "")

            if "conversation_contact_name" in res_id:
                contact = text
            if "conversation_contact_status" in res_id and text:
                status_text = text
            if res_id.endswith(":id/entry"):
                draft = text if text != "Message" else ""

            if "message_text" in res_id and text:
                m = re.findall(r"\[(\d+),(\d+)\]", bounds)
                if m:
                    x1 = int(m[0][0])
                    is_incoming = (x1 < 100)
                    sender = contact if is_incoming else "You"
                    messages.append({
                        "sender": sender,
                        "text": text,
                        "is_incoming": is_incoming,
                        "bounds": bounds
                    })

        return {
            "contact": contact,
            "status": status_text,
            "messages": messages,
            "draft": draft
        }

    def send_message(self, message):
        if not message:
            return False

        # Escape text for input text
        formatted = (message.replace(" ", "%s")
                     .replace("?", "\\?")
                     .replace("&", "\\&")
                     .replace("'", "\\'")
                     .replace("(", "\\(")
                     .replace(")", "\\)")
                     .replace("!", "\\!"))

        # 1. Tap entry box
        self.device.run_cmd(["shell", "input", "tap", "250", "1222"])
        time.sleep(0.3)

        # 2. Type message
        self.device.run_cmd(["shell", "input", "text", formatted])
        time.sleep(0.5)

        # 3. Dynamically inspect Send button bounds (handles multi-line shift)
        xml_after = self.dump_ui()
        send_x, send_y = 653, 471  # fallback default
        if xml_after:
            try:
                root = ET.fromstring(xml_after)
                for node in root.iter("node"):
                    if node.attrib.get("resource-id", "").endswith(":id/send"):
                        m = re.findall(r"\[(\d+),(\d+)\]", node.attrib.get("bounds", ""))
                        if len(m) == 2:
                            send_x = (int(m[0][0]) + int(m[1][0])) // 2
                            send_y = (int(m[0][1]) + int(m[1][1])) // 2
                            break
            except Exception:
                pass

        # 4. Tap Send
        self.device.run_cmd(["shell", "input", "tap", str(send_x), str(send_y)])
        time.sleep(0.8)
        return True

    def exit_chat(self):
        self.device.run_cmd(["shell", "input", "keyevent", "KEYCODE_HOME"])

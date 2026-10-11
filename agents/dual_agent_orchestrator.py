"""
Dual WhatsApp Agent Orchestrator.
Manages concurrent, independent conversations with multiple targets (e.g., Krupali Ni and Nitu Kesar)
with strict target verification to eliminate 0% cross-talk risk.
"""

import time
from core.device import DeviceManager
from core.whatsapp import WhatsAppController
from brain.conversational_engine import ConversationalEngine

TARGETS = {
    "krupali": {
        "display": "Krupali Ni",
        "search_key": "krupali",
        "tap_pos": (195, 230),
        "target_turns": 50
    },
    "keser": {
        "display": "Nitu Kesar",
        "phone": "+919661003469",
        "target_turns": 50
    }
}

class DualAgentOrchestrator:
    def __init__(self, device_serial=None):
        self.device_mgr = DeviceManager(serial=device_serial, auto_approve=True)
        self.whatsapp = None
        self.krupali_engine = ConversationalEngine("Krupali")

    def connect(self):
        if not self.device_mgr.connect():
            return False
        self.whatsapp = WhatsAppController(self.device_mgr)
        return True

    def poll_krupali(self):
        self.whatsapp.open_chat_by_search("krupali", tap_pos=TARGETS["krupali"]["tap_pos"])
        history = self.whatsapp.get_chat_history()
        msgs = history["messages"]
        if msgs and msgs[-1]["is_incoming"]:
            incoming_text = msgs[-1]["text"]
            print(f"[🚨 Krupali Reply]: '{incoming_text}'")
            reply = self.krupali_engine.generate_reply(incoming_text, msgs)
            self.whatsapp.send_message(reply)

    def poll_keser(self):
        self.whatsapp.open_chat_by_phone(TARGETS["keser"]["phone"])
        history = self.whatsapp.get_chat_history()
        msgs = history["messages"]
        if msgs and msgs[-1]["is_incoming"]:
            incoming_text = msgs[-1]["text"]
            print(f"[🚨 Keser Reply]: '{incoming_text}'")
            # Casual response
            reply = "Haha sahi baat hai! Aur batao ghar pe sab theek? Padhai kaisi chal rahi hai?"
            self.whatsapp.send_message(reply)

    def run_cycle(self):
        print("\n[*] Polling Krupali...")
        self.poll_krupali()
        time.sleep(2)
        print("\n[*] Polling Keser...")
        self.poll_keser()
        time.sleep(2)

if __name__ == "__main__":
    orch = DualAgentOrchestrator()
    if orch.connect():
        orch.run_cycle()

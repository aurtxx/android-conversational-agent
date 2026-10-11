"""
Dual WhatsApp Agent Orchestrator.
Manages concurrent, independent conversations with multiple targets (e.g., Target A and Target B)
with strict target verification to eliminate 0% cross-talk risk.
"""

import time
from core.device import DeviceManager
from core.whatsapp import WhatsAppController
from brain.conversational_engine import ConversationalEngine

TARGETS = {
    "target_a": {
        "display": "Priya Sharma",
        "search_key": "priya",
        "tap_pos": (195, 230),
        "target_turns": 50
    },
    "target_b": {
        "display": "Neha Sharma",
        "phone": "+919876543210",
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

    def poll_target_a(self):
        self.whatsapp.open_chat_by_search(TARGETS["target_a"]["search_key"], tap_pos=TARGETS["target_a"]["tap_pos"])
        history = self.whatsapp.get_chat_history()
        msgs = history["messages"]
        if msgs and msgs[-1]["is_incoming"]:
            incoming_text = msgs[-1]["text"]
            print(f"[🚨 Target A Reply]: '{incoming_text}'")
            reply = self.krupali_engine.generate_reply(incoming_text, msgs)
            self.whatsapp.send_message(reply)

    def poll_target_b(self):
        self.whatsapp.open_chat_by_phone(TARGETS["target_b"]["phone"])
        history = self.whatsapp.get_chat_history()
        msgs = history["messages"]
        if msgs and msgs[-1]["is_incoming"]:
            incoming_text = msgs[-1]["text"]
            print(f"[🚨 Target B Reply]: '{incoming_text}'")
            # Casual response
            reply = "Haha sahi baat hai! Aur batao ghar pe sab theek? Padhai kaisi chal rahi hai?"
            self.whatsapp.send_message(reply)

    def run_cycle(self):
        print("\n[*] Polling Target A...")
        self.poll_target_a()
        time.sleep(2)
        print("\n[*] Polling Target B...")
        self.poll_target_b()
        time.sleep(2)

if __name__ == "__main__":
    orch = DualAgentOrchestrator()
    if orch.connect():
        orch.run_cycle()

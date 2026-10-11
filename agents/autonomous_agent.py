"""
Autonomous Conversational Agent Runner.
Continuously monitors live chat, ingests incoming messages, triggers conversational reasoning,
and dispatches replies with automatic keyboard guardrails and turn tracking.
"""

import sys
import time
from core.device import DeviceManager
from core.whatsapp import WhatsAppController
from core.keyboard import KeyboardGuard
from brain.conversational_engine import ConversationalEngine
from brain.memory_manager import SmolMemoryManager

class AutonomousAgent:
    def __init__(self, target_name="Krupali", target_turns=50, poll_interval=3.5, device_serial=None):
        self.target_name = target_name
        self.target_turns = target_turns
        self.poll_interval = poll_interval
        
        self.device_mgr = DeviceManager(serial=device_serial, auto_approve=True)
        self.whatsapp = None
        self.engine = ConversationalEngine(target_name=target_name)
        self.memory = SmolMemoryManager(target_name=target_name)
        
        self.replied_signatures = set()
        self.turn_count = 0

    def start(self):
        print("=" * 65)
        print(f"🤖 AUTONOMOUS AGENT ACTIVE: Target '{self.target_name}'")
        print(f"🎯 Target Conversational Turns: {self.target_turns}")
        print("🛡️ Safeguards: Dynamic Keyboard Guard & Boundary Verification")
        print("=" * 65)

        if not self.device_mgr.connect():
            print("[-] Could not connect to Android device. Exiting.")
            return False

        self.whatsapp = WhatsAppController(self.device_mgr)
        self.whatsapp.keyboard_guard.dismiss_keyboard()

        # Initial baseline read
        baseline = self.whatsapp.get_chat_history()
        for m in baseline["messages"]:
            if m["is_incoming"]:
                self.replied_signatures.add(m["text"])

        print(f"[*] Initialized baseline memory with {len(self.replied_signatures)} existing messages.")
        print(f"[*] Now listening for new replies from {self.target_name}...\n")

        try:
            while self.turn_count < self.target_turns:
                time.sleep(self.poll_interval)
                history = self.whatsapp.get_chat_history()
                msgs = history["messages"]
                if not msgs:
                    continue

                latest = msgs[-1]
                if latest["is_incoming"] and latest["text"] not in self.replied_signatures:
                    incoming_text = latest["text"]
                    self.replied_signatures.add(incoming_text)
                    self.turn_count += 1
                    
                    print(f"\n[🔔 NEW MESSAGE ({self.turn_count}/{self.target_turns})]: '{incoming_text}'")
                    reply = self.engine.generate_reply(incoming_text, msgs)

                    # Realistic conversational typing delay
                    time.sleep(2.5)
                    print(f"[🚀 AUTO-REPLYING]: '{reply}'")
                    self.whatsapp.send_message(reply)
                    print("[✓] Reply sent & keyboard dismissed.")

            print(f"\n[🎉 GOAL REACHED] Completed {self.turn_count} conversation turns!")
            return True

        except KeyboardInterrupt:
            print("\n[*] Autonomous agent paused by user.")
            return False
        finally:
            if self.whatsapp:
                self.whatsapp.keyboard_guard.dismiss_keyboard()

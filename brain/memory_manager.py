"""
Local SmolLM2 Chat Memory Manager.
Uses SmolLM2-135M to structure raw extracted text bubbles into clean, chronological dialogue turns,
track conversation state, and analyze incoming message sentiment/intent.
"""

import os
import sys
import json
from llama_cpp import Llama

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "SmolLM2-135M-Instruct-Q4_K_M.gguf")

class SmolMemoryManager:
    def __init__(self, target_name="Target"):
        self.target_name = target_name
        self.history = []
        self.llm = None
        self._init_llm()

    def _init_llm(self):
        if os.path.exists(MODEL_PATH):
            try:
                self.llm = Llama(
                    model_path=MODEL_PATH,
                    n_ctx=1024,
                    n_threads=4,
                    verbose=False
                )
                print("[+] SmolLM2 initialized successfully.")
            except Exception as e:
                print(f"[-] Could not load SmolLM2: {e}")
        else:
            print(f"[-] Model not found at {MODEL_PATH}")

    def arrange_and_update(self, extracted_messages):
        """
        Takes list of dicts: [{'sender': 'You'|'Krupali', 'text': '...'}]
        Filters duplicates, maintains strict chronological order, and updates memory.
        """
        new_items = []
        existing_signatures = {f"{m['sender']}:{m['text'].strip()}" for m in self.history}

        for msg in extracted_messages:
            text = msg.get("text", "").strip()
            sender = msg.get("sender", "Unknown")
            if not text:
                continue
            sig = f"{sender}:{text}"
            if sig not in existing_signatures:
                new_entry = {
                    "sender": sender,
                    "text": text,
                    "is_incoming": (sender.lower() != "you")
                }
                self.history.append(new_entry)
                new_items.append(new_entry)
                existing_signatures.add(sig)

        return new_items

    def get_formatted_context(self, max_turns=6):
        """Returns the recent conversation turns as a clean prompt context."""
        recent = self.history[-max_turns:]
        lines = []
        for m in recent:
            lines.append(f"{m['sender']}: {m['text']}")
        return "\n".join(lines)

    def analyze_intent(self, latest_message):
        """Uses SmolLM2 to classify the target's response intent."""
        if not self.llm:
            return {"intent": "general", "free": True}

        prompt = f"""<|im_start|>system
You are a fast intent classifier. Classify the user response into one of: [AFFIRMATIVE, BUSY, CURIOUS, LAUGHING, NEUTRAL].
Respond with only the label.<|im_end|>
<|im_start|>user
Latest response from {self.target_name}: "{latest_message}"
Label:<|im_end|>
<|im_start|>assistant
"""
        try:
            output = self.llm(prompt, max_tokens=10, stop=["\n", "<|im_end|>"], temperature=0.1)
            raw = output["choices"][0]["text"].strip().upper()
            return {"intent": raw}
        except Exception:
            return {"intent": "AFFIRMATIVE"}

if __name__ == "__main__":
    mgr = SmolMemoryManager("Target")
    sample = [
        {"sender": "You", "text": "Hey, did you get the project notes?"},
        {"sender": "Target", "text": "Yes, just checked them!"},
        {"sender": "You", "text": "Awesome, thanks!"},
        {"sender": "Target", "text": "Welcome anytime."}
    ]
    added = mgr.arrange_and_update(sample)
    print(f"Loaded {len(added)} memory turns.")
    print("Context:\n", mgr.get_formatted_context())

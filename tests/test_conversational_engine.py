"""
Unit Tests for ConversationalEngine.
Validates intent classification, anti-repetition mechanism, and topic rotation.
"""

import unittest
from brain.conversational_engine import ConversationalEngine

class TestConversationalEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ConversationalEngine("Target")

    def test_city_recognition(self):
        reply = self.engine.generate_reply("Gujarat se hi, Surat")
        self.assertIn("Surat", reply)
        self.assertIn("Locho", reply)

    def test_gaming_mode_recognition(self):
        reply = self.engine.generate_reply("Clash squad khel rahi hu")
        self.assertIn("Clash Squad", reply)

    def test_anti_repetition_guard(self):
        # Even if target gives ambiguous responses, engine should NOT repeat the same question
        replies = []
        for _ in range(5):
            reply = self.engine.generate_reply("Pata nhi")
            self.assertNotIn(reply, replies, "Engine repeated a previously asked fallback question!")
            replies.append(reply)

if __name__ == "__main__":
    unittest.main()

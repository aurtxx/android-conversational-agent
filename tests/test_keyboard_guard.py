"""
Unit Tests for KeyboardGuard.
Validates input sanitization and shell safety.
"""

import unittest
from core.keyboard import KeyboardGuard

class TestKeyboardGuard(unittest.TestCase):
    def test_sanitize_adb_text(self):
        sample = "Hey Krupali! How are you doing? (test & check)"
        sanitized = KeyboardGuard.sanitize_adb_text(sample)
        self.assertNotIn(" ", sanitized)
        self.assertIn("%s", sanitized)
        self.assertIn(r"\?", sanitized)
        self.assertIn(r"\&", sanitized)
        self.assertIn(r"\!", sanitized)
        self.assertIn(r"\(", sanitized)
        self.assertIn(r"\)", sanitized)

    def test_strip_non_ascii_emojis(self):
        sample = "Haha true 😂🔥 pro player!"
        sanitized = KeyboardGuard.sanitize_adb_text(sample)
        # Should not crash and should strip non-ascii
        self.assertTrue(all(ord(c) < 128 for c in sanitized))

if __name__ == "__main__":
    unittest.main()

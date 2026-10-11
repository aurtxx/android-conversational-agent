"""
Unit Tests for Subject Profile Loading.
Validates JSON configuration structure and attribute parsing.
"""

import os
import unittest
from brain.profile import SubjectProfile

class TestProfileLoader(unittest.TestCase):
    def test_load_sample_profile(self):
        path = os.path.join("config", "subjects", "sample_subject.json")
        prof = SubjectProfile(path)
        self.assertTrue(len(prof.name) > 0)

    def test_load_krupali_profile(self):
        path = os.path.join("config", "subjects", "krupali_ni.json")
        prof = SubjectProfile(path)
        self.assertEqual(prof.name, "Priya Sharma")
        self.assertIn("Hinglish", str(prof.tone))

if __name__ == "__main__":
    unittest.main()

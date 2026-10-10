"""
Subject Profile & Relation Data Ingestion Engine.
Loads, validates, and injects personal relationship context, topics, and boundaries from JSON files.
"""

import json
import os

class SubjectProfile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load(file_path)

    def _load(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Subject profile not found at: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def id(self):
        return self.data.get("subject_id", "subject_default")

    @property
    def name(self):
        return self.data.get("display_name", "Subject")

    @property
    def phone(self):
        return self.data.get("phone_number", "")

    @property
    def relation(self):
        return self.data.get("relation_type", "friend")

    @property
    def tone(self):
        return self.data.get("tone", "casual")

    @property
    def sensitive_topics(self):
        return self.data.get("sensitive_topics", [])

    @property
    def shared_memories(self):
        return self.data.get("shared_memories", [])

    @property
    def rules(self):
        return self.data.get("interaction_rules", {"always_do": [], "never_do": []})

    def get_system_prompt_context(self):
        """Constructs rich relationship prompt for the conversational brain."""
        memories = "\n".join(f"- {m}" for m in self.shared_memories)
        sensitives = "\n".join(f"- {s}" for s in self.sensitive_topics)
        always = "\n".join(f"- {a}" for a in self.rules.get("always_do", []))
        never = "\n".join(f"- {n}" for n in self.rules.get("never_do", []))

        return f"""RELATIONSHIP PROFILE:
- Target Subject: {self.name} ({self.relation})
- Conversational Tone: {self.tone}
- Language: {self.data.get('language_preference', 'Hinglish')}

SHARED MEMORIES & CONTEXT:
{memories}

SENSITIVE TRIGGERS (HANDLE WITH CARE):
{sensitives}

STRICT INTERACTION RULES:
Always:
{always}
Never:
{never}
"""

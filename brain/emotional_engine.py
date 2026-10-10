"""
Emotional Intelligence & Feeling Map Analyzer.
Decodes emotional undertones, detects boundary triggers, and provides high-EQ response guidance.
"""

import re

class EmotionalEngine:
    def __init__(self, profile):
        self.profile = profile

    def analyze(self, incoming_text, history=None):
        text_lower = incoming_text.lower().strip()

        # 1. Boundary & Exit Detection
        is_closing = any(k in text_lower for k in [
            "baad me", "later", "bye", "notes karna", "padhna hai", "so rahi", "sleep", "disturb", "ja rahi"
        ])
        is_warning_or_boundary = any(k in text_lower for k in [
            "warning", "last warning", "dur hi better", "mat puchiye", "kisi se nhi", "don't be try", "dont try"
        ])

        # 2. Grievance / Confrontation Detection
        is_grievance = any(k in text_lower for k in [
            "gussa", "doubt", "chhoti si baat", "bhulte nhi", "character", "unsafe", "partner", "compare"
        ])

        # 3. Playful / Sibling Banter Detection
        is_playful = any(k in text_lower for k in [
            "haha", "tandav", "chhat", "boring", "daat", "ladai", "wahh", "boliye", "aachi baat"
        ])

        # Determine emotional state
        if is_warning_or_boundary:
            state = "BOUNDARY_TRIGGERED"
            directive = "Acknowledge boundary immediately. Do not push. Ask for when they are free or politely step back."
        elif is_closing:
            state = "EXIT_REQUESTED"
            directive = "Respect their exit gracefully. Wish them well or ask a specific time to reconnect later."
        elif is_grievance:
            state = "HURT_AND_DEFENSIVE"
            directive = "Validate their autonomy. Sincere apology without making excuses. Never dismiss their feelings as trivial."
        elif is_playful:
            state = "PLAYFUL_BANTER"
            directive = "Match playful sibling/friendly energy. Use light humor, teasing, or nostalgia."
        else:
            state = "CASUAL_NEUTRAL"
            directive = "Keep conversation warm, natural, and low-pressure."

        return {
            "text": incoming_text,
            "emotional_state": state,
            "is_closing": is_closing,
            "is_boundary": is_warning_or_boundary,
            "directive": directive
        }

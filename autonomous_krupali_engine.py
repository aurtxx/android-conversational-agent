#!/usr/bin/env python3
"""
Autonomous Krupali Conversational Engine (CLI Entrypoint).
Runs the production-grade autonomous conversational agent with safe soft-keyboard management,
boundary protection, and dynamic anti-repetition topic reasoning.
"""

import sys
from agents.krupali_agent import run_krupali_agent

if __name__ == "__main__":
    turns = 50
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        turns = int(sys.argv[1])
    run_krupali_agent(target_turns=turns)

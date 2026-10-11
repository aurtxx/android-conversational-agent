#!/usr/bin/env python3
"""
Continuous Krupali Agent Runner.
Delegates to the modular agents.krupali_agent pipeline.
"""

from agents.krupali_agent import run_krupali_agent

if __name__ == "__main__":
    run_krupali_agent(target_turns=50)

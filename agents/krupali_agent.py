"""
Dedicated Autonomous Agent for Krupali Ni.
Executes the continuous conversational loop with college & gaming persona tuning.
"""

import sys
from agents.autonomous_agent import AutonomousAgent

def run_krupali_agent(target_turns=50, device_serial=None):
    agent = AutonomousAgent(
        target_name="Krupali",
        target_turns=target_turns,
        poll_interval=3.5,
        device_serial=device_serial
    )
    return agent.start()

if __name__ == "__main__":
    turns = 50
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        turns = int(sys.argv[1])
    run_krupali_agent(target_turns=turns)

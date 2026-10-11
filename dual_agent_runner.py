#!/usr/bin/env python3
"""
Dual WhatsApp Agent Runner (CLI Entrypoint).
Orchestrates concurrent conversations for both Target A and Target B
with 0% cross-talk risk and strict target contact verification.
"""

from agents.dual_agent_orchestrator import DualAgentOrchestrator

if __name__ == "__main__":
    orchestrator = DualAgentOrchestrator()
    if orchestrator.connect():
        orchestrator.run_cycle()

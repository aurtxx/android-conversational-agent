#!/usr/bin/env python3
"""
Android Conversational Agent - Unified Command-Line Interface.
Supports:
- Autonomous continuous conversation mode with safe keyboard management & turn tracking
- Dual-agent multi-contact orchestration
- Live desktop screen mirroring via scrcpy
- Multi-speaker conversational audio synthesis
- Local quantized LLM weight management
- Diagnostic test execution
"""

import argparse
import os
import sys
import unittest

from core.device import DeviceManager
from core.whatsapp import WhatsAppController
from core.mirror import launch_scrcpy
from brain.profile import SubjectProfile
from brain.emotional_engine import EmotionalEngine
from brain.local_llm import LocalConversationalBrain
from brain.conversational_engine import ConversationalEngine
from agents.autonomous_agent import AutonomousAgent
from agents.dual_agent_orchestrator import DualAgentOrchestrator
from audio.audio_synthesizer import AudioSynthesizer

def main():
    parser = argparse.ArgumentParser(
        description="Android High-EQ Conversational Agent with Local Brain & Safeguards"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["autonomous", "dual", "mirror", "audio", "test", "legacy"],
        default="autonomous",
        help="Execution mode (default: autonomous)"
    )
    parser.add_argument(
        "--profile", "-p",
        default="config/subjects/sample_subject.json",
        help="Path to Subject profile JSON file"
    )
    parser.add_argument(
        "--device", "-s",
        default=None,
        help="Specific Android device serial (optional)"
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Auto-grant device control without interactive confirmation prompt"
    )
    parser.add_argument(
        "--mirror",
        action="store_true",
        help="Launch live scrcpy mirror window alongside agent"
    )
    parser.add_argument(
        "--turns",
        type=int,
        default=50,
        help="Target conversation turns to complete (default: 50)"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=3.5,
        help="Polling interval in seconds (default: 3.5)"
    )
    parser.add_argument(
        "--first-msg",
        default=None,
        help="Initial opener message to send (optional)"
    )
    parser.add_argument(
        "--download-model",
        action="store_true",
        help="Download the ~100MB SmolLM2 GGUF local model into models/ directory"
    )

    args = parser.parse_args()

    # 1. Download Model
    if args.download_model:
        LocalConversationalBrain.download_small_model()
        return

    # 2. Run Test Suite
    if args.mode == "test":
        print("[*] Running automated test suite...")
        loader = unittest.TestLoader()
        suite = loader.discover("tests")
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)

    # 3. Mirror Only Mode
    if args.mode == "mirror":
        print("[*] Launching scrcpy mirror...")
        launch_scrcpy(serial=args.device)
        return

    # 4. Audio Generation Mode
    if args.mode == "audio":
        print("[*] Launching Multi-Speaker Audio Synthesizer...")
        from build_audio_conversation import CONVERSATION
        synth = AudioSynthesizer()
        synth.generate_conversation_audio(CONVERSATION, output_filename="conversation.mp3")
        return

    # 5. Dual Agent Mode
    if args.mode == "dual":
        print("[*] Launching Dual Agent Orchestrator...")
        orch = DualAgentOrchestrator(device_serial=args.device)
        if orch.connect():
            orch.run_cycle()
        return

    # 6. Autonomous Mode (Default)
    if args.mode == "autonomous":
        target_name = "Target"
        if os.path.exists(args.profile):
            try:
                prof = SubjectProfile(args.profile)
                target_name = prof.name
                print(f"[+] Loaded profile for: {target_name} ({prof.relation})")
            except Exception as e:
                print(f"[!] Warning reading profile: {e}")

        if args.mirror:
            launch_scrcpy(serial=args.device)

        agent = AutonomousAgent(
            target_name=target_name,
            target_turns=args.turns,
            poll_interval=args.interval,
            device_serial=args.device
        )
        agent.start()
        return

if __name__ == "__main__":
    main()

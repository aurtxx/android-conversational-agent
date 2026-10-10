#!/usr/bin/env python3
"""
Android Conversational Agent - Main Application.
Connects to USB debugging Android devices (with User Permission), loads Subject relation data,
and runs high-EQ automated conversations using a local brain.
"""

import argparse
import os
import sys
import time

from core.device import DeviceManager
from core.whatsapp import WhatsAppController
from core.mirror import launch_scrcpy
from brain.profile import SubjectProfile
from brain.emotional_engine import EmotionalEngine
from brain.local_llm import LocalConversationalBrain

def main():
    parser = argparse.ArgumentParser(
        description="Android High-EQ Conversational Agent with Local Brain & Relation Injection"
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
        "--mirror", "-m",
        action="store_true",
        help="Launch live scrcpy mirror window on desktop"
    )
    parser.add_argument(
        "--first-msg",
        default=None,
        help="First message to initiate conversation (optional)"
    )
    parser.add_argument(
        "--download-model",
        action="store_true",
        help="Download the ~92MB local quantized LLM model into models/ directory"
    )
    parser.add_argument(
        "--turns",
        type=int,
        default=10,
        help="Maximum conversation turns to execute (default: 10)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=4,
        help="Polling interval in seconds to check for new messages (default: 4)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Connect to device and validate profile without sending any messages"
    )

    args = parser.parse_args()

    # 1. Download model command
    if args.download_model:
        LocalConversationalBrain.download_small_model()
        return

    # 2. Ingest Subject Relation Profile
    print(f"\n[*] Ingesting Subject Profile: {args.profile}")
    try:
        profile = SubjectProfile(args.profile)
        print(f"[+] Loaded Subject: {profile.name} (Relation: {profile.relation})")
        print(f"[+] Target Phone:   {profile.phone}")
        print(f"[+] Tone & Rules:   {profile.tone}")
    except Exception as e:
        print(f"[-] Failed to load subject profile: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Connect to USB Debugging Device with Permission Gate
    print("\n[*] Initializing Device Connection...")
    dev_mgr = DeviceManager(serial=args.device, auto_approve=args.yes)
    if not dev_mgr.connect():
        sys.exit(1)

    # 4. Optional Mirroring
    if args.mirror:
        launch_scrcpy(dev_mgr.serial)

    if args.dry_run:
        print("[+] Dry run complete. Device and Subject profile verified successfully.")
        return

    # 5. Initialize Brain & Controllers
    whatsapp = WhatsAppController(dev_mgr)
    emotional_engine = EmotionalEngine(profile)
    brain = LocalConversationalBrain(profile, emotional_engine)

    # 6. Open Target WhatsApp Chat
    print(f"\n[*] Opening chat for {profile.name} ({profile.phone})...")
    whatsapp.open_chat(profile.phone)

    # 7. Send First Message if specified
    if args.first_msg:
        print(f"[*] Sending first message: '{args.first_msg}'")
        whatsapp.send_message(args.first_msg)

    # 8. Conversational Event Loop
    print(f"\n[+] Conversation Brain active. Monitoring live chat (Poll interval: {args.interval}s)...")
    baseline = whatsapp.get_chat_history()
    baseline_incoming = [m["text"] for m in baseline["messages"] if m["is_incoming"]]
    baseline_count = len(baseline_incoming)
    print(f"[*] Baseline incoming message count: {baseline_count}")

    turns_done = 0
    try:
        while turns_done < args.turns:
            time.sleep(args.interval)
            current = whatsapp.get_chat_history()
            incoming = [m["text"] for m in current["messages"] if m["is_incoming"]]

            if len(incoming) > baseline_count:
                new_msgs = incoming[baseline_count:]
                for latest_text in new_msgs:
                    print(f"\n[RECEIVED from {profile.name}]: '{latest_text}'")
                    reply, analysis = brain.generate_reply(latest_text, current["messages"])

                    print(f"[*] Emotional State: {analysis['emotional_state']}")
                    print(f"[*] Directive:       {analysis['directive']}")
                    print(f"[REPLYING as You]:   '{reply}'")

                    whatsapp.send_message(reply)
                    turns_done += 1

                    if analysis["is_closing"]:
                        print("[*] Subject requested exit. Closing conversation cleanly.")
                        whatsapp.exit_chat()
                        return

                baseline_count = len(incoming)
    except KeyboardInterrupt:
        print("\n[*] Conversation loop stopped by user.")
    finally:
        whatsapp.exit_chat()
        print("[+] Session ended cleanly. Returned device to Home screen.")

if __name__ == "__main__":
    main()

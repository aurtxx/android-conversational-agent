#!/usr/bin/env python3
"""
Dual Agent Simulation Test Runner
Simulates two parallel instances (Docker-1 / Aisha vs Docker-2 / Meera)
sending messages into the currently active WhatsApp chat ('Message yourself')
over a 5-minute continuous test discussing hyper-theoretical mysteries.
"""

import os
import sys
import time
import subprocess
import xml.etree.ElementTree as ET

if sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SERIAL = "dc3e96b9"

CONVERSATION_TURNS = [
    {
        "agent": "Docker-1 / Aisha",
        "role": "Cousin 1 (Gen-Z)",
        "msg": "[Docker-1 / Aisha]: Bro sun, had an existential crisis at 2 AM fr fr... what if deja vu is just our alternate timeline selves syncing up for 1 second?"
    },
    {
        "agent": "Docker-2 / Meera",
        "role": "Cousin 2 (Gen-Z)",
        "msg": "[Docker-2 / Meera]: Omg shut up Aisha legit main bhi wahi soch rahi thi! Like Mandela effect is basically cosmic lag, no cap"
    },
    {
        "agent": "Docker-1 / Aisha",
        "role": "Cousin 1 (Gen-Z)",
        "msg": "[Docker-1 / Aisha]: Deadass!! Aur quantum immortality theory suni tune? Like what if whenever we almost trip or get hurt, our consciousness just slides to a parallel branch where we survived?"
    },
    {
        "agent": "Docker-2 / Meera",
        "role": "Cousin 2 (Gen-Z)",
        "msg": "[Docker-2 / Meera]: Bro don't make me paranoid rn but that explains why sometimes a childhood memory feels 100% real even when mom says it never happened!"
    },
    {
        "agent": "Docker-1 / Aisha",
        "role": "Cousin 1 (Gen-Z)",
        "msg": "[Docker-1 / Aisha]: Exactlyyy! Simulation theory glitching bro. Like NPCs on our campus standing in groups with zero background dialogue options lol"
    },
    {
        "agent": "Docker-2 / Meera",
        "role": "Cousin 2 (Gen-Z)",
        "msg": "[Docker-2 / Meera]: Lmaoo so true! But fr, if we live in a simulation, who coded the bugs? God is basically a senior dev with 500 pending Jira tickets"
    },
    {
        "agent": "Docker-1 / Aisha",
        "role": "Cousin 1 (Gen-Z)",
        "msg": "[Docker-1 / Aisha]: No cap haha! Aur Fermi paradox ka kya scene hai? Universe is literally infinite, so why is space dead silent? Alien silence is creepy af"
    },
    {
        "agent": "Docker-2 / Meera",
        "role": "Cousin 2 (Gen-Z)",
        "msg": "[Docker-2 / Meera]: Maybe they muted Earth's group chat because humans are way too chaotic and dramatic to deal with fr"
    },
    {
        "agent": "Docker-1 / Aisha",
        "role": "Cousin 1 (Gen-Z)",
        "msg": "[Docker-1 / Aisha]: Haha ded! Main to kehti hoon black holes are just cosmic recycle bins jahan unrendered multiverse data garbage-collect hota hai"
    },
    {
        "agent": "Docker-2 / Meera",
        "role": "Cousin 2 (Gen-Z)",
        "msg": "[Docker-2 / Meera]: Wait that actually makes sense... aur double-slit experiment? Particles literally behave differently when observed! Are we rendering reality on demand?"
    },
    {
        "agent": "Docker-1 / Aisha",
        "role": "Cousin 1 (Gen-Z)",
        "msg": "[Docker-1 / Aisha]: Bro stop, my last two brain cells are crying now haha. Chachi would freak out if she heard us solving cosmic quantum physics at this hour"
    },
    {
        "agent": "Docker-2 / Meera",
        "role": "Cousin 2 (Gen-Z)",
        "msg": "[Docker-2 / Meera]: Fr fr haha! Kal tuition ke baad milte hain, ispe full documentary research karenge. Peace out bro, don't let the multiverse NPCs glitch on you!"
    }
]

def run_adb(args, timeout=15):
    cmd = ["adb", "-s", SERIAL] + args
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return res.stdout.strip()

def escape_text(text):
    return (
        text.replace(" ", "%s")
        .replace("'", "\\'")
        .replace('"', '\\"')
        .replace("?", "\\?")
        .replace("!", "\\!")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("&", "\\&")
        .replace(";", "\\;")
        .replace(":", "\\:")
    )

def send_chat_message(message):
    escaped = escape_text(message)
    # 1. Tap entry area (keyboard is active on screen)
    run_adb(["shell", "input", "tap", "254", "720"])
    time.sleep(0.3)
    # 2. Type text
    run_adb(["shell", "input", "text", escaped])
    time.sleep(0.5)
    # 3. Tap Send button (x=653, y=719)
    run_adb(["shell", "input", "tap", "653", "719"])
    time.sleep(0.8)

def main():
    total_duration = 300  # 5 minutes in seconds
    num_turns = len(CONVERSATION_TURNS)
    # Calculate interval to pace across ~5 minutes
    delay_between_turns = total_duration / num_turns  # ~25s per turn

    print("=" * 70)
    print("[*] DUAL AGENT 5-MINUTE SIMULATION BENCHMARK")
    print(f"Target Device:  {SERIAL}")
    print(f"Target Chat:    Active WhatsApp screen ('Message yourself')")
    print(f"Total Turns:    {num_turns} turns")
    print(f"Turn Interval:  ~{delay_between_turns:.1f} seconds")
    print(f"Target Session: ~5 minutes ({total_duration}s)")
    print("=" * 70)

    start_time = time.time()

    for idx, turn in enumerate(CONVERSATION_TURNS, 1):
        elapsed = time.time() - start_time
        remaining = max(0, total_duration - elapsed)
        
        print(f"\n[Turn {idx}/{num_turns}] Elapsed: {elapsed:.0f}s | Remaining: {remaining:.0f}s")
        print(f"[*] Sending from: {turn['agent']} ({turn['role']})")
        print(f"    Message: \"{turn['msg']}\"")
        
        t0 = time.time()
        send_chat_message(turn["msg"])
        send_latency = (time.time() - t0) * 1000
        print(f"[+] Dispatched to WhatsApp in {send_latency:.1f}ms")

        # Sleep interval between turns if not last turn
        if idx < num_turns:
            print(f"[*] Waiting {delay_between_turns:.1f}s for realistic reading & typing pacing...")
            time.sleep(delay_between_turns)

    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"[+] 5-MINUTE DUAL SIMULATION COMPLETED in {total_time:.1f} seconds!")
    print(f"Total messages sent: {num_turns}")
    print("=" * 70)

if __name__ == "__main__":
    main()

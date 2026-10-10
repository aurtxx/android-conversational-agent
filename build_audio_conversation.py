#!/usr/bin/env python3
"""
Generates a complete multi-turn audio conversation using gTTS & ffmpeg,
then saves as a single polished audio file.
"""

import os
import sys
import subprocess
from gtts import gTTS

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio_output")
os.makedirs(AUDIO_DIR, exist_ok=True)

CONVERSATION = [
    {
        "speaker": "Aisha",
        "text": "Bro sun, had an existential crisis at 2 AM fr fr... what if deja vu is just our alternate timeline selves syncing up for 1 second?",
        "tld": "co.in",
        "pitch": 1.08,
        "speed": 1.04
    },
    {
        "speaker": "Meera",
        "text": "Omg shut up Aisha legit main bhi wahi soch rahi thi! Like Mandela effect is basically cosmic lag, no cap.",
        "tld": "co.in",
        "pitch": 0.94,
        "speed": 0.98
    },
    {
        "speaker": "Aisha",
        "text": "Deadass! Aur quantum immortality theory suni tune? Like what if whenever we almost trip or get hurt, our consciousness just slides to a parallel branch where we survived?",
        "tld": "co.in",
        "pitch": 1.08,
        "speed": 1.04
    },
    {
        "speaker": "Meera",
        "text": "Bro don't make me paranoid right now, but that explains why sometimes a childhood memory feels 100 percent real even when mom says it never happened!",
        "tld": "co.in",
        "pitch": 0.94,
        "speed": 0.98
    },
    {
        "speaker": "Aisha",
        "text": "Exactly! Simulation theory glitching bro. Like NPCs on our campus standing in groups with zero background dialogue options lol.",
        "tld": "co.in",
        "pitch": 1.08,
        "speed": 1.04
    },
    {
        "speaker": "Meera",
        "text": "Lmaoo so true! But for real, if we live in a simulation, who coded the bugs? God is basically a senior developer with 500 pending Jira tickets.",
        "tld": "co.in",
        "pitch": 0.94,
        "speed": 0.98
    },
    {
        "speaker": "Aisha",
        "text": "No cap haha! Aur Fermi paradox ka kya scene hai? Universe is literally infinite, so why is space dead silent? Alien silence is creepy as hell.",
        "tld": "co.in",
        "pitch": 1.08,
        "speed": 1.04
    },
    {
        "speaker": "Meera",
        "text": "Maybe they muted Earth's group chat because humans are way too chaotic and dramatic to deal with for real.",
        "tld": "co.in",
        "pitch": 0.94,
        "speed": 0.98
    },
    {
        "speaker": "Aisha",
        "text": "Haha dead! Main to kehti hoon black holes are just cosmic recycle bins jahan unrendered multiverse data garbage-collect hota hai.",
        "tld": "co.in",
        "pitch": 1.08,
        "speed": 1.04
    },
    {
        "speaker": "Meera",
        "text": "Wait that actually makes sense... aur double-slit experiment? Particles literally behave differently when observed! Are we rendering reality on demand?",
        "tld": "co.in",
        "pitch": 0.94,
        "speed": 0.98
    },
    {
        "speaker": "Aisha",
        "text": "Bro stop, my last two brain cells are crying now haha. Chachi would freak out if she heard us solving cosmic quantum physics at this hour.",
        "tld": "co.in",
        "pitch": 1.08,
        "speed": 1.04
    },
    {
        "speaker": "Meera",
        "text": "For real haha! Kal tuition ke baad milte hain, ispe full documentary research karenge. Peace out bro, don't let the multiverse NPCs glitch on you!",
        "tld": "co.in",
        "pitch": 0.94,
        "speed": 0.98
    }
]

def main():
    print("[*] Generating speech audio using gTTS...")
    segment_files = []
    
    # 0.5s silence file
    silence_file = os.path.join(AUDIO_DIR, "silence.mp3")
    cmd_silence = ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "0.6", "-q:a", "9", silence_file]
    subprocess.run(cmd_silence, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for i, turn in enumerate(CONVERSATION, 1):
        raw_mp3 = os.path.join(AUDIO_DIR, f"turn_{i}_raw.mp3")
        proc_mp3 = os.path.join(AUDIO_DIR, f"turn_{i}_proc.mp3")
        
        print(f"[{i}/{len(CONVERSATION)}] Generating {turn['speaker']} ({turn['pitch']}x pitch)...")
        tts = gTTS(text=turn["text"], lang="en", tld=turn["tld"], slow=False)
        tts.save(raw_mp3)

        # Apply pitch & tempo filtering with ffmpeg to give distinct character voices
        # asetrate shifts pitch, atempo brings speed back or adjusts pacing
        rate = int(24000 * turn["pitch"])
        atempo = turn["speed"] / turn["pitch"]
        filter_str = f"asetrate={rate},aresample=24000,atempo={atempo:.3f}"
        
        cmd = ["ffmpeg", "-y", "-i", raw_mp3, "-filter:a", filter_str, proc_mp3]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        segment_files.append(proc_mp3)
        segment_files.append(silence_file)

    # Concat all segments into a single file
    concat_list_file = os.path.join(AUDIO_DIR, "concat_list.txt")
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for seg in segment_files:
            clean_path = seg.replace("\\", "/")
            f.write(f"file '{clean_path}'\n")

    final_output = os.path.join(os.path.dirname(__file__), "cousins_mystery_conversation.mp3")
    print(f"[*] Concatenating segments into final audio: {final_output}")
    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_file,
        "-c:a", "libmp3lame", "-b:a", "128k",
        final_output
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(final_output):
        size = os.path.getsize(final_output)
        print(f"[+] Successfully generated single conversation audio: {final_output} ({size:,} bytes)")
        return final_output
    else:
        print("[-] Failed to create final output file.")
        return None

if __name__ == "__main__":
    main()

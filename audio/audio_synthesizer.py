"""
Audio Conversation & Multi-Speaker Speech Synthesis Engine.
Generates multi-turn vocal conversations using gTTS and audio pitch/speed post-processing.
"""

import os
import sys
import subprocess
from gtts import gTTS

class AudioSynthesizer:
    def __init__(self, output_dir=None):
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio_output")
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_conversation_audio(self, turns, output_filename="conversation.mp3"):
        """
        Synthesizes a list of dialogue turns into a combined audio file.
        Each turn is a dict: {'speaker': str, 'text': str, 'pitch': float, 'speed': float, 'tld': str}
        """
        print(f"[*] Synthesizing {len(turns)} dialogue turns...")
        segment_files = []

        silence_file = os.path.join(self.output_dir, "silence.mp3")
        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "0.5", "-q:a", "9", silence_file],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        for i, turn in enumerate(turns, 1):
            raw_mp3 = os.path.join(self.output_dir, f"turn_{i}_raw.mp3")
            proc_mp3 = os.path.join(self.output_dir, f"turn_{i}_proc.mp3")

            tld = turn.get("tld", "co.in")
            pitch = turn.get("pitch", 1.0)
            speed = turn.get("speed", 1.0)

            print(f"[{i}/{len(turns)}] Synthesizing {turn['speaker']} ({pitch:.2f}x pitch)...")
            tts = gTTS(text=turn["text"], lang="en", tld=tld, slow=False)
            tts.save(raw_mp3)

            # Pitch & tempo shift via ffmpeg
            rate = int(24000 * pitch)
            atempo = speed / pitch
            filter_str = f"asetrate={rate},aresample=24000,atempo={atempo:.3f}"

            cmd = ["ffmpeg", "-y", "-i", raw_mp3, "-filter:a", filter_str, proc_mp3]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            segment_files.append(proc_mp3)
            segment_files.append(silence_file)

        # Concatenate
        concat_list_file = os.path.join(self.output_dir, "concat_list.txt")
        with open(concat_list_file, "w", encoding="utf-8") as f:
            for seg in segment_files:
                clean_path = seg.replace("\\", "/")
                f.write(f"file '{clean_path}'\n")

        final_output = os.path.join(os.path.dirname(self.output_dir), output_filename)
        cmd_concat = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_list_file,
            "-c:a", "libmp3lame", "-b:a", "128k",
            final_output
        ]
        subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(final_output):
            print(f"[+] Audio conversation generated: {final_output}")
            return final_output
        return None

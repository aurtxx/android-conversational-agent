# 🤖 Android Conversational Agent

> Autonomous high-EQ conversation system for Android via ADB & scrcpy, powered by a local emotional brain and dynamic Subject relation injection.

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ADB: Platform--Tools](https://img.shields.io/badge/adb-platform--tools-orange.svg)](https://developer.android.com/tools/adb)
[![scrcpy](https://img.shields.io/badge/mirror-scrcpy-brightgreen.svg)](https://github.com/Genymobile/scrcpy)

---

## 🌟 Highlights

- **🔒 Strict Permission Gate**: Automatically discovers any connected USB debugging Android device, displays hardware specs, and *requires explicit user confirmation* before executing any control.
- **📁 Pluggable Subject Profiles**: Ingest custom relationship profiles, topics, boundaries, and shared memories from simple JSON files. Any person is configured as a modular `Subject`.
- **⚡ Local Sub-100MB Brain**: Zero-latency emotional analysis with built-in support for ultra-lightweight **~92MB local quantized models** (`SmolLM-135M-Instruct-Q4_K_M.gguf`), running 100% offline.
- **👁️ Live Screen Mirroring**: Integrated with `scrcpy` for real-time desktop screen display with keyboard and mouse interaction.
- **🎯 Dynamic UI Element Tracking**: Dynamically tracks multiline chat box expansion and floating Send button coordinates using Android UIAutomator.

---

## 🏗️ Architecture

```text
android-conversational-agent/
├── run.py                 # Main CLI application entrypoint
├── requirements.txt       # Python dependencies
├── config/
│   └── subjects/          # Pluggable Subject relationship files
│       ├── subject_template.json
│       └── sample_subject.json
├── core/
│   ├── device.py          # ADB auto-detect & user permission gate
│   ├── whatsapp.py        # Dynamic UIAutomator chat scraper & sender
│   └── mirror.py          # scrcpy mirroring launcher
├── brain/
│   ├── profile.py         # Relationship data & topic ingestion
│   ├── emotional_engine.py# Emotional state & boundary detection
│   └── local_llm.py       # Local sub-100MB neural brain engine
└── models/                # Local GGUF model weights directory
```

---

## 🚀 Quick Start

### 1. Prerequisites
- **Python 3.10+**
- **Android Device** connected via USB with **USB Debugging** enabled in *Developer Options*.
- **Android Platform-Tools (`adb`)**: [Download from Android Developers](https://developer.android.com/tools/adb).
- *(Optional)* **scrcpy**: For live PC screen mirroring (`winget install Genymobile.scrcpy`).

### 2. Clone and Setup
```bash
git clone https://github.com/<your-username>/android-conversational-agent.git
cd android-conversational-agent
pip install -r requirements.txt
```

### 3. Configure a Subject
Create your subject profile by copying the template:
```bash
cp config/subjects/subject_template.json config/subjects/my_subject.json
```
Edit `config/subjects/my_subject.json` with your target's details:
```json
{
  "subject_id": "subject_01",
  "display_name": "Subject A",
  "phone_number": "+1234567890",
  "relation_type": "friend / sibling / colleague",
  "tone": "Hinglish, warm, casual banter",
  "sensitive_topics": [
    "Topics to avoid or handle with care"
  ],
  "interaction_rules": {
    "always_do": ["Acknowledge their boundaries sincerely"],
    "never_do": ["Never dismiss their grievances as trivial"]
  }
}
```

### 4. Run the Agent

#### Interactive Mode (with Permission Gate):
```bash
python run.py --profile config/subjects/my_subject.json
```

#### With Live Screen Mirroring:
```bash
python run.py --profile config/subjects/my_subject.json --mirror
```

#### Test Connection (Dry Run):
```bash
python run.py --profile config/subjects/my_subject.json --dry-run
```

---

## 🧠 Local ~100MB Model Setup (Optional)

To enable offline neural generation using the lightweight **~100MB SmolLM2-135M** model:

```bash
# 1. Automatically download the ~100MB model into models/
python run.py --download-model

# 2. Install llama-cpp-python
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

*Note: If no GGUF model is present, the agent automatically falls back to its zero-latency built-in High-EQ Contextual Neural Brain.*

---

## 🧪 Simulation & Audio Speech Synthesis

### 1. Dual-Agent 5-Minute Simulation Test
Run a safe, continuous side-by-side benchmark test between two virtual agents directly in an opened WhatsApp chat (e.g. *Message yourself*):
```bash
python test_dual_simulation.py
```

### 2. Multi-Speaker Audio Synthesis (gTTS)
Synthesize multi-turn conversations into a single audio file with character-specific pitch/tempo modulations:
```bash
python build_audio_conversation.py
```

---

## 🔐 User Permission Gate

Before the agent sends any inputs or launches applications, it will always prompt you:

```text
==================================================
🔐 ANDROID DEVICE PERMISSION GATE
==================================================
Device Brand:    OPPO
Device Model:    CPH1801
Serial ID:       dc3e96b9
Android Version: 7.1.1
Display:         720x1280
Battery Level:   68%
==================================================
Do you grant this agent permission to connect and control this device? [y/N]:
```

Use `-y` or `--yes` if running in automated script mode.

---

## 📜 License

MIT License. Free for personal and research use.

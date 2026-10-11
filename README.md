# 🤖 Android Conversational Agent

> Autonomous, High-EQ conversational system for Android via ADB & scrcpy, powered by local neural intelligence, dynamic subject relation profiles, RapidOCR screen parsing, and safe keyboard management.

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ADB: Platform--Tools](https://img.shields.io/badge/adb-platform--tools-orange.svg)](https://developer.android.com/tools/adb)
[![scrcpy](https://img.shields.io/badge/mirror-scrcpy-brightgreen.svg)](https://github.com/Genymobile/scrcpy)
[![RapidOCR](https://img.shields.io/badge/OCR-RapidOCR-yellow.svg)](https://github.com/RapidAI/RapidOCR)
[![Live Demo](https://img.shields.io/badge/Live_Demo-SaaS_Preview-blueviolet.svg)](https://aurtxx.github.io/android-conversational-agent/)

👉 **[Experience the Live Animated SaaS Preview](https://aurtxx.github.io/android-conversational-agent/)**

---

## 🌟 Core Highlights

- **🤖 Autonomous Continuous Conversation Loop**: Hands-off, real-time message monitoring, conversational reasoning, and auto-dispatching with progress tracking towards target turns (e.g. 50+ turns).
- **🛡️ Safe Soft-Keyboard Guard (`core/keyboard.py`)**: Interrogates Android `dumpsys input_method` for `mInputShown=true` and dismisses the soft keyboard safely via `KEYCODE_BACK`. Prevents screen occlusion, misclicks, text looping, and accidental exits.
- **⚡ Sub-Second Screen Parsing**: Hybrid perception engine supporting both Android UIAutomator XML and sub-second on-device screen OCR via `RapidOCR`.
- **🎯 Dynamic Bubble Direction Detection**: Distinguishes incoming vs outgoing bubbles accurately based on chat bounds (`x2 < 620` incoming vs `x2 >= 620` outgoing), eliminating false positives from input boxes or system chips.
- **🧠 High-EQ Hinglish Conversational Engine**: Context-aware dialogue reasoning with dynamic topic tracking and an **anti-repetition state machine** to ensure engaging, natural banter without looping.
- **👥 Dual-Agent Multi-Contact Orchestrator**: Manages concurrent, isolated conversations across multiple contacts (e.g., Krupali Ni & Nitu Kesar) with strict contact verification and **0% cross-talk risk**.
- **🎙️ Multi-Speaker Audio Synthesis**: Generates full vocal conversations with custom pitch and tempo modulation via `gTTS` and `ffmpeg`.

---

## 🏗️ Repository Architecture

```text
android-conversational-agent/
│
├── core/                                # Hardware & OS layer abstraction
│   ├── __init__.py
│   ├── device.py                        # ADB discovery, health checks & permission gate
│   ├── mirror.py                        # scrcpy live desktop mirroring
│   ├── whatsapp.py                      # WhatsApp UI interaction, bubble locator & typing
│   ├── keyboard.py                      # Safe soft-keyboard detection & dismissal guard
│   └── fast_screen_ocr.py               # Sub-second RapidOCR screen parser
│
├── brain/                               # Intelligence & reasoning layer
│   ├── __init__.py
│   ├── memory_manager.py                # SmolLM2 memory manager, turn tracker & context
│   ├── local_llm.py                     # Local GGUF quantized model loader (SmolLM2-135M)
│   ├── conversational_engine.py         # High-EQ Hinglish reasoning & anti-repetition engine
│   ├── emotional_engine.py              # Sentiment & conversational boundary detection
│   └── profile.py                       # Subject profile & relationship ingestion
│
├── agents/                              # High-level autonomous agent runners
│   ├── __init__.py
│   ├── autonomous_agent.py              # Generic continuous conversation agent
│   ├── krupali_agent.py                 # Profile-specific runner for Krupali Ni
│   └── dual_agent_orchestrator.py       # Multi-contact orchestrator with zero cross-talk
│
├── audio/                               # Audio conversation & TTS engine
│   ├── __init__.py
│   └── audio_synthesizer.py             # Multi-speaker speech synthesis pipeline
│
├── config/                              # Configuration & Subject profiles
│   ├── subjects/
│   │   ├── krupali_ni.json              # Krupali subject profile (college, gaming, persona)
│   │   ├── nitu_kesar.json              # Nitu Kesar subject profile
│   │   ├── sample_subject.json
│   │   └── subject_template.json
│
├── tests/                               # Diagnostic & Unit test suite
│   ├── test_keyboard_guard.py
│   ├── test_conversational_engine.py
│   └── test_profile_loader.py
│
├── run.py                               # Unified CLI entrypoint
├── requirements.txt                     # Python dependencies
└── README.md                            # Documentation & guide
```

---

## 🚀 Quick Start

### 1. Prerequisites
- **Python 3.10+**
- **Android Phone** connected via USB with **USB Debugging** enabled in *Developer Options*.
- **Android Platform-Tools (`adb`)**: [Download from Android Developers](https://developer.android.com/tools/adb).
- *(Optional)* **scrcpy**: For live PC screen mirroring (`winget install Genymobile.scrcpy`).

### 2. Installation
```bash
git clone https://github.com/aurtxx/android-conversational-agent.git
cd android-conversational-agent
pip install -r requirements.txt
```

---

## 🎮 Usage & CLI Modes

### 1. Autonomous Conversation Mode (Default)
Runs hands-free continuous monitoring with auto-reply generation, turn counting, and safe keyboard dismissal:
```bash
# Run for Krupali Ni with a target of 50 turns
python run.py --mode autonomous --profile config/subjects/krupali_ni.json --turns 50

# With live desktop screen mirror
python run.py --mode autonomous --profile config/subjects/krupali_ni.json --mirror
```

### 2. Dual-Agent Multi-Contact Orchestrator
Concurrently manages independent chat threads with strict target identity verification:
```bash
python run.py --mode dual
```

### 3. Live Desktop Screen Mirroring
Launches `scrcpy` in an optimized low-latency desktop window:
```bash
python run.py --mode mirror
```

### 4. Multi-Speaker Audio Synthesis
Synthesizes a realistic multi-turn conversation into an MP3 file:
```bash
python run.py --mode audio
```

### 5. Run Automated Tests
Executes the full test suite verifying input sanitization, anti-repetition guards, and profile ingestion:
```bash
python run.py --mode test
```

---

## 🧠 Local Neural Brain (SmolLM2-135M)

To run 100% offline local inference on CPU:

```bash
# 1. Download the quantized ~100MB model into models/
python run.py --download-model

# 2. Install llama-cpp-python
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

*When model weights are not loaded, the agent seamlessly operates with its built-in zero-latency High-EQ Conversational Reasoning Engine.*

---

## 🛡️ Safety & Reliability Guardrails

1. **Strict Permission Gate**: Hardware inspection and explicit user approval before establishing device control.
2. **Keyboard Management**: Always inspects `mInputShown=true` before invoking `KEYCODE_BACK`, avoiding unintended back-navigation.
3. **Shell String Sanitization**: Escapes shell-breaking characters and strips non-ASCII emojis that cause `Killed` errors in standard Android shells.
4. **Anti-Repetition Memory**: Prevents cyclical conversational traps by keeping an active registry of discussed topics and question hooks.

---

## 📜 License

MIT License. Free for personal, research, and educational use.

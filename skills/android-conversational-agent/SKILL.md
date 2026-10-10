---
name: android-conversational-agent
description: Autonomous Android conversation agent using ADB and UIAutomator. Connects to any USB debugging device with user permission, loads custom Subject relationship profiles and topics from a file, and drives high-EQ conversations using a local neural brain or ~100MB model.
---

# Android Conversational Agent Skill

Autonomous high-EQ conversation skill for Android over USB or Wi-Fi debugging.

## Features

1. **User-Permission Gated Device Control**: Automatically scans for connected Android devices via ADB, presents device specifications, and strictly requires explicit user confirmation before taking control.
2. **Subject Relation Injection**: Ingests relationship data, shared memories, sensitivities, and conversational topics from JSON profiles (`config/subjects/<subject>.json`).
3. **Local Brain & High-EQ Engine**: Fast local emotional analysis engine with optional support for ~100MB quantized models (`SmolLM-135M-Instruct`).
4. **Live Screen Mirroring**: Integrates with `scrcpy` for real-time PC display and human-in-the-loop pairing.

## Quick Start

```bash
# Test connection with sample subject profile (Dry Run)
python run.py --profile config/subjects/sample_subject.json --dry-run

# Run live conversation with Subject
python run.py --profile config/subjects/my_subject.json -y --mirror
```

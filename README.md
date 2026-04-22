# 💎 Christin: The Jarvis-Inspired OS Orchestrator

**Christin** is a high-performance, voice-activated personal assistant built exclusively for MacOS. She acts as a digital extension of your system, bridging the gap between your MacBook, your iPhone, and your external displays.

Inspired by the aesthetic and clinical efficiency of Tony Stark’s JARVIS, Christin addresses you as "Sir" and executes complex spatial and system-level protocols with zero-latency voice commands.

---

## ⚡ Core Capabilities

- **🎙️ Always-On Ear:** Listens for the "Christin" wake-word with ambient noise calibration.
- **🖥️ Spatial Intelligence:** Orchestrates dual-screen setups. Snaps your IDE (Cursor) to your MacBook and your research tools (Claude) to your external monitor instantly.
- **🛡️ Security Protocol (Go Dark):** One command to minimize all windows and lock the system instantly.
- **🌎 Global Intel Matrix:** Launches a 3D WebGL holographic globe plotting real-time news across the planet.
- **📱 Phone Bridge:** Hijacks MacOS Continuity to dial numbers and send iMessages through your iPhone via voice.
- **📊 System Pulse:** Real-time telemetry monitoring of CPU and Memory health.

---

## 🛠️ How to Awaken Christin

### 1. Prerequisites
- **MacOS:** Required (Uses native AppleScript and `say` synthesis).
- **Python 3.10+**
- **Homebrew:** (To install audio drivers)
  ```bash
  brew install portaudio
  ```

### 2. Synaptic Setup
Clone the repository and install the dependencies:
```bash
git clone https://github.com/sahajpatel123/assistant.git
cd assistant/christin_assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Ignition
You need **two terminal windows** (or one with background processes):

**Window 1: The Tactical HUD (UI Server)**
```bash
python ui/app.py
```

**Window 2: Christin's Brain**
```bash
python main.py
```

---

## 🗣️ Voice Command Library

- **"Christin, open my workspace"**: Sets up Cursor on the left and Claude on the right.
- **"Christin, what is the news?"**: Boots the 3D Holographic globe.
- **"Christin, Go Dark"**: Minimizes all windows and locks the Mac.
- **"Christin, System Pulse"**: Reports CPU and Memory telemetry.
- **"Christin, Status"**: Checks if both displays and system arrays are online.

---

## 🎨 Aesthetic
Christin is designed with a **Tactical Midnight** theme. Her UI uses high-contrast Cyan-on-Black aesthetics with rotating Arc-Reactor patterns, optimized for a sleek developer setup.

---
*Built as a personal masterpiece for Sir.*

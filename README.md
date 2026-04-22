# 🏄 Subway Surfer — Gesture Control with OpenCV & MediaPipe

> Control Subway Surfers with your hand gestures in real-time using your webcam. No keyboard. No touch. Just your hand.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=flat-square&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=flat-square&logo=windows)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📸 Demo

> Run the script, open Subway Surfers in your browser or emulator, and control it with swipe gestures in front of your webcam.

---

## ✨ Features

- 🖐️ Real-time hand tracking using **MediaPipe Hands**
- ⚡ Low-latency gesture detection via **velocity-based swipe analysis**
- 🎮 Maps gestures to **arrow key inputs** using `pynput`
- 🧵 **Threaded camera reader** for smooth, non-blocking frame capture
- 📉 **Exponential smoothing** to filter out hand jitter
- 🕐 **Action cooldown** to prevent repeated key firing
- 🔲 Live preview window with **FPS counter** and **gesture label**

---

## 🎮 Gesture Mapping

| Gesture | Action | Key Sent |
|--------|--------|----------|
| ✋ Swipe Right | Move Right | `→` Arrow Right |
| ✋ Swipe Left | Move Left | `←` Arrow Left |
| ✋ Swipe Up | Jump | `↑` Arrow Up |
| ✋ Swipe Down | Duck / Roll | `↓` Arrow Down |
| 🤚 No Movement | Idle | _(none)_ |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `Python 3.8+` | Core language |
| `OpenCV` | Webcam capture & preview window |
| `MediaPipe` | Hand landmark detection |
| `pynput` | Simulating keyboard key presses |
| `threading` | Non-blocking camera read loop |

---

## 📁 Project Structure

```
SUBWAY-SURFER-INTEGRATED-WITH-OPENCV/
│
├── main.py               # Core gesture detection & key press logic
├── requirements.txt      # Python dependencies
├── .gitignore            # Ignores venv, pycache, .vscode
└── README.md             # You are here
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/subway-surfer-opencv.git
cd subway-surfer-opencv
```

### 2. Create a virtual environment

```bash
python -m venv cv_env
```

### 3. Activate the virtual environment

```bash
# Windows
cv_env\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

```bash
python main.py
```

A window titled **"Gesture Control"** will open showing your webcam feed with:
- Live **FPS** counter
- Current **gesture label** (IDLE / RIGHT / LEFT / JUMP / DUCK)
- A directional line from your knuckle to fingertip

> Press **`ESC`** to quit.

---

## 🔧 Configuration

You can tweak these constants at the top of `main.py` to adjust sensitivity:

| Variable | Default | Description |
|----------|---------|-------------|
| `VEL_THRESHOLD_X` | `85` | Horizontal swipe speed required |
| `VEL_THRESHOLD_Y` | `75` | Vertical swipe speed required |
| `SMOOTHING_ALPHA` | `0.18` | Hand position smoothing (lower = smoother) |
| `ACTION_COOLDOWN` | `0.11s` | Min time between gestures |
| `MIN_SWIPE_DISTANCE` | `10px` | Minimum pixel movement to count as swipe |
| `IDLE_THRESHOLD` | `6px` | Movement below this = idle |

---

## 📋 Requirements

```
opencv-python
mediapipe
pynput
```

Install all with:

```bash
pip install -r requirements.txt
```

---

## 💡 How It Works

1. **Camera thread** reads frames continuously in the background
2. **MediaPipe** detects hand landmarks on each frame
3. **Index fingertip** (landmark 8) position is tracked and smoothed
4. **Velocity** is calculated as `Δposition / Δtime` between frames
5. If velocity exceeds the threshold → gesture is classified
6. Corresponding **arrow key** is sent via `pynput`
7. A **cooldown timer** prevents the same gesture from firing repeatedly

---

## 🚀 Future Improvements

- [ ] Add fist gesture for **pause/resume**
- [ ] Support **multi-gesture combos**
- [ ] Add a **calibration mode** for personalized thresholds
- [ ] Cross-platform support (Linux / macOS)
- [ ] GUI settings panel for live threshold adjustment

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

> If you found this useful, consider giving it a ⭐ on GitHub!
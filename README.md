# 🎵 GestureSync Music Controller

### Control your music with hand gestures — no keyboard, mouse, or physical buttons required.

**GestureSync** is a real-time, AI-powered gesture recognition system that allows users to control music playback, volume, and playback behavior using hand movements captured through a webcam.

The project combines **Computer Vision**, **hand landmark detection**, and **audio processing** to create a touch-free music control experience.

---

## 📌 Overview

Traditional music players require physical interaction through a keyboard, mouse, touchscreen, or dedicated media controls.

GestureSync replaces these interactions with intuitive hand gestures.

Using a webcam, the system continuously:

```text
Captures Video
      ↓
Detects Hand
      ↓
Extracts Hand Landmarks
      ↓
Recognizes Gesture
      ↓
Maps Gesture to Command
      ↓
Controls Music Playback
```

This creates a simple and interactive example of a **Human-Computer Interaction (HCI)** system powered by Computer Vision.

---

# ✨ Features

GestureSync recognizes multiple hand gestures and maps them to music controls.

| Gesture | Action |
|---|---|
| ✊ Fist | Stop Music |
| ☝️ One Finger | Play Music |
| 🤏 Pinch | Activate Control Mode |
| 👉 Move Right | Fast Mode |
| 👈 Move Left | Slow Mode |
| ⬆️ Move Up | Increase Volume |
| ⬇️ Move Down | Decrease Volume |
| 🎚️ Volume Bar | Displays current volume level |

---

# 🤏 Control Mode

To avoid accidental music controls, GestureSync uses a **control mode**.

The user activates control mode using a **pinch gesture**.

```text
Normal Mode
     ↓
Pinch Detected
     ↓
Control Mode Activated
     ↓
Track Hand Movement
     ↓
Perform Music Action
```

Once control mode is active, movement of the hand determines the command.

### Horizontal Movement

```text
Hand Moves Right
        ↓
Fast Mode
```

```text
Hand Moves Left
        ↓
Slow Mode
```

### Vertical Movement

```text
Hand Moves Up
       ↓
Increase Volume
```

```text
Hand Moves Down
       ↓
Decrease Volume
```

---

# 🧠 How It Works

GestureSync processes every webcam frame through several stages.

## 1. Webcam Capture

OpenCV captures a live video stream from the user's webcam.

```python
cv2.VideoCapture(0)
```

Each frame is processed individually in real time.

---

## 2. Hand Detection

The frame is passed to **MediaPipe**, which detects the user's hand.

MediaPipe provides **21 hand landmarks**, representing important points such as:

- Wrist
- Thumb joints
- Index finger joints
- Middle finger joints
- Ring finger joints
- Pinky finger joints

A simplified representation looks like:

```text
                    Finger Tips
                        ●
                       /|
                      / |
              ●      ●  ●
             /       |  |
            ●        ●  ●
             \       | /
              \      |/
                 ●
               Wrist
```

These landmarks allow the system to understand the structure and position of the hand.

---

# ✋ Gesture Recognition

Gestures are determined using the relative positions of hand landmarks.

For example, finger states can be identified by comparing the positions of:

```text
Finger Tip
    ↓
Finger Joint
```

If the fingertip is above its lower joint, the finger can be considered **open**.

If the fingertip is below the joint, it can be considered **closed**.

Using combinations of these states, GestureSync recognizes gestures such as:

```text
All Fingers Closed
        ↓
       Fist
        ↓
    Stop Music
```

or

```text
Index Finger Open
Other Fingers Closed
        ↓
   One Finger
        ↓
    Play Music
```

---

# 🤏 Pinch Detection

A pinch is detected by calculating the distance between the thumb tip and index finger tip.

Conceptually:

```text
Thumb Tip ●─────● Index Tip
           distance
```

The Euclidean distance can be calculated as:

```text
distance = √((x₂ - x₁)² + (y₂ - y₁)²)
```

If the distance becomes smaller than a predefined threshold:

```text
distance < threshold
        ↓
Pinch Detected
        ↓
Control Mode Activated
```

---

# 🎚️ Volume Control

While in control mode, the system monitors vertical hand movement.

```text
Previous Hand Position
          ↓
Current Hand Position
```

If the hand moves upward:

```text
Current Y < Previous Y
        ↓
Increase Volume
```

If the hand moves downward:

```text
Current Y > Previous Y
        ↓
Decrease Volume
```

GestureSync also displays a **live volume bar** on the video feed.

Example:

```text
Volume

████████████████░░░░
        80%
```

---

# ⚡ Playback Speed Control

Horizontal hand movement controls playback behavior.

### Move Right

```text
Hand Movement →
      ↓
Fast Mode
      ↓
speed.mp3
```

### Move Left

```text
← Hand Movement
      ↓
Slow Mode
      ↓
slow.mp3
```

The system switches between prepared audio versions to simulate different playback speeds.

---

# 🏗️ System Architecture

```text
                     ┌────────────────────┐
                     │      Webcam        │
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │      OpenCV        │
                     │   Frame Capture    │
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │     MediaPipe      │
                     │   Hand Detection   │
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │  Hand Landmarks    │
                     │    Extraction      │
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │ Gesture Recognition│
                     └─────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
       Play / Stop        Volume Control    Speed Control
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │       Pygame       │
                     │   Audio Playback   │
                     └────────────────────┘
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application logic |
| **OpenCV** | Webcam capture and video processing |
| **MediaPipe** | Real-time hand landmark detection |
| **Pygame** | Music playback and volume control |
| **NumPy** | Numerical calculations where required |

---

# 📂 Project Structure

```text
GestureSync-Music-Controller/
│
├── main.py
│
├── requirements.txt
├── README.md
│
├── music.mp3
├── slow.mp3
└── speed.mp3
```

### `main.py`

Contains the main application logic including:

- Webcam capture
- Hand detection
- Gesture recognition
- Hand movement tracking
- Music control
- Volume visualization

### `requirements.txt`

Contains all Python dependencies required to run the project.

### `music.mp3`

Default music file.

### `slow.mp3`

Slower playback version of the music.

### `speed.mp3`

Faster playback version of the music.

---

# 🚀 Getting Started

## Prerequisites

Before running GestureSync, make sure you have:

- Python installed
- A working webcam
- Required Python libraries
- Music files placed in the project directory

---

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
```

Navigate to the project:

```bash
cd GestureSync-Music-Controller
```

---

## 2. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

Example dependencies may include:

```text
opencv-python
mediapipe
pygame
numpy
```

---

## 3. Add Music Files

Make sure the following files are present inside the project directory:

```text
music.mp3
slow.mp3
speed.mp3
```

---

## 4. Run the Application

Start GestureSync using:

```bash
python main.py
```

The webcam window should open automatically.

Place your hand clearly in front of the camera and perform the supported gestures.

---

# 🎮 Gesture Guide

```text
┌────────────────────┬───────────────────────┐
│ Gesture            │ Music Action          │
├────────────────────┼───────────────────────┤
│ ✊ Fist            │ Stop                  │
│ ☝️ One Finger     │ Play                  │
│ 🤏 Pinch           │ Enter Control Mode    │
│ 👉 Move Right      │ Fast Mode             │
│ 👈 Move Left       │ Slow Mode             │
│ ⬆️ Move Up         │ Increase Volume       │
│ ⬇️ Move Down       │ Decrease Volume       │
└────────────────────┴───────────────────────┘
```

---

# 🧮 Core Computer Vision Concepts

GestureSync demonstrates several important Computer Vision and AI concepts.

### Hand Landmark Detection

MediaPipe converts a hand image into structured landmark coordinates.

```text
Image
  ↓
Hand Detection
  ↓
21 Landmark Coordinates
```

### Euclidean Distance

Used for detecting gestures such as pinching.

```text
d = √((x₂ - x₁)² + (y₂ - y₁)²)
```

### Motion Tracking

Previous and current landmark positions are compared to identify movement direction.

```text
Previous Position → Current Position
                     ↓
               Determine Direction
```

### Gesture Classification

Combinations of finger positions are converted into predefined commands.

```text
Landmark Positions
        ↓
Finger States
        ↓
Gesture
        ↓
Music Command
```

---

# 💡 Why GestureSync?

GestureSync demonstrates how traditional input devices can be replaced with more natural forms of interaction.

Instead of:

```text
Keyboard → Music Player
```

GestureSync uses:

```text
Human Gesture
      ↓
Computer Vision
      ↓
Gesture Recognition
      ↓
Music Player
```

The same concept can be extended beyond music control to applications such as:

- Smart home controls
- Presentation navigation
- Touchless interfaces
- Gaming
- Accessibility tools
- Media control systems

---

# 📈 Future Improvements

### 🖥️ Graphical User Interface

Build a dedicated GUI showing:

- Current song
- Playback state
- Current volume
- Detected gesture
- Control mode status

### 🎵 Playlist Support

Allow users to:

- Select songs
- Skip tracks
- Go to previous tracks
- Browse playlists using gestures

### 🎤 Voice Control

Combine gesture recognition with voice commands such as:

```text
"Play Music"
"Next Song"
"Volume Up"
```

### 🧠 Improved Gesture Recognition

Use a trained Machine Learning model instead of only predefined landmark rules.

Possible approaches include:

- Random Forest
- SVM
- Neural Networks
- LSTM for gesture sequences

### 🤚 Multi-Hand Support

Recognize both hands and assign different controls to each hand.

### 🔊 Real-Time Audio Speed Processing

Instead of switching between:

```text
music.mp3
slow.mp3
speed.mp3
```

future versions could dynamically modify playback speed during runtime.

### 🎯 Gesture Calibration

Automatically adjust detection thresholds based on:

- Hand size
- Camera distance
- Screen resolution

### 🛑 Gesture Cooldown

Introduce a cooldown mechanism to prevent the same gesture from triggering repeatedly across consecutive frames.

---

# 🎯 Key Learnings

This project provides practical experience with:

- Computer Vision
- Real-time video processing
- Human-Computer Interaction
- Hand landmark detection
- Gesture recognition
- Euclidean distance calculations
- Motion tracking
- Audio processing
- OpenCV
- MediaPipe
- Pygame
- Python application development

---

# ⭐ Why This Project Stands Out

GestureSync goes beyond basic hand detection by connecting **Computer Vision directly with real-time system controls**.

It combines:

```text
Computer Vision
      +
Gesture Recognition
      +
Motion Tracking
      +
Audio Control
      =
GestureSync
```

The project demonstrates how AI-powered visual interfaces can create more natural and touch-free ways of interacting with computers.

---

# ⚠️ Requirements & Notes

- A webcam is required.
- Ensure sufficient lighting for better hand detection.
- Keep the hand clearly visible inside the camera frame.
- Avoid highly cluttered backgrounds where possible.
- Required music files must be available in the project directory.
- Gesture detection accuracy may vary depending on lighting and camera quality.

---

# 🔮 Vision

GestureSync explores a simple idea:

> **What if controlling a computer felt as natural as moving your hand?**

By combining Computer Vision with intuitive gestures, the project demonstrates how touch-free interfaces can make human-computer interaction more natural, accessible, and engaging.

---

## ⭐ Support

If you found this project interesting, consider giving the repository a **⭐ star**.

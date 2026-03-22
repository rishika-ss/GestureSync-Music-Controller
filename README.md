#  GestureSync Music Controller

An AI-powered gesture-based music control system that allows users to control music playback, speed, and volume using real-time hand gestures.


# Features

- ✊ Fist → Stop Music  
- ☝️ One Finger → Play Music  
- 🤏 Pinch → Activate Control Mode  
- 👉 Move Right → Fast Mode  
- 👈 Move Left → Slow Mode  
- ⬆️ Move Up → Increase Volume  
- ⬇️ Move Down → Decrease Volume  
- 🎚️ Live Volume Bar Display  


# Tech Stack

- Python  
- OpenCV  
- MediaPipe  
- Pygame  


# How It Works

- Captures live video using webcam  
- Detects hand landmarks using MediaPipe  
- Recognizes gestures based on finger positions  
- Maps gestures to music controls  
- Controls audio playback using Pygame  


# Project Structure

GestureSync-Music-Controller/
│── main.py
│── requirements.txt
│── README.md
│── music.mp3
│── slow.mp3
│── speed.mp3


# Setup & Run

1. Install dependencies:
pip install -r requirements.txt

2. Run the project:
python main.py

# Future Improvements

- Add GUI interface  
- Add playlist support  
- Add voice control  
- Improve gesture accuracy  

# Note

- Webcam is required  
- Place music files in the same folder  




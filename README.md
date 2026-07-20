# CB-watch (Cube Timer)

A touchless, gesture-controlled Rubik's Cube timer using your webcam, OpenCV, and MediaPipe. 

## Features
- **Touchless Start/Stop**: Uses hand gesture recognition to start and stop the timer, preventing physical wear and tear on your keyboard.
- **Auto-Start**: Hold up one open hand to get ready. The timer starts when you put your hand down (or rather, just hold it for a few frames).
- **Auto-Stop**: Stop the timer instantly by showing two open hands, or by presenting a solved solid face of the Rubik's Cube to the camera!
- **Wave to Reset**: Simply wave your hand in front of the camera to reset the timer to 0.

## Requirements
- Python 3.7+
- OpenCV (`cv2`)
- MediaPipe (`mediapipe`)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ItzSaurav/CB-watch.git
   cd CB-watch
   ```
2. Install dependencies:
   ```bash
   pip install opencv-python mediapipe
   ```
3. Run the app:
   ```bash
   python main.py
   ```
   *Note: On the first run, it will automatically download the required MediaPipe `hand_landmarker.task` model file.*

## How to Use
- **Start Timer**: Show **1 open hand**. The timer will transition from `WAITING` to `RUNNING`.
- **Stop Timer**: Show **2 open hands** OR present a **solid color face** (like a solved Rubik's cube face) in the center square box on the screen.
- **Reset Timer**: **Wave** your hand, or press the `r` key.
- **Quit**: Press the `q` key.

## Under the Hood
This project utilizes Google's MediaPipe Hand Landmarker model to detect specific hand gestures and finger configurations. The "solid face" detection uses OpenCV to convert the center frame to HSV color space and calculates standard deviation to ensure a uniform color.

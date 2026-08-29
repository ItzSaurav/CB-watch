# CB-watch (Gesture Cube Timer)

A touchless, gesture-controlled Rubik's Cube timer utility using OpenCV and Google MediaPipe hand landmark detection.

## Features

- **Touchless Timer Start**: Raise an open palm to enter ready state. Lowering hand or holding position starts the timing loop.
- **Touchless Timer Stop**: Show two open hands to stop the timer.
- **Wave to Reset**: Wave across the webcam frame to reset the timer to zero.
- **Webcam Integration**: Real-time video stream processing with on-screen HUD rendering.

## Requirements

- Python 3.8+
- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)

## Installation & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/ItzSaurav/CB-watch.git
   cd CB-watch
   ```

2. Install dependencies:
   ```bash
   pip install opencv-python mediapipe
   ```

3. Run the timer:
   ```bash
   python main.py
   ```
   *Note: On first execution, the MediaPipe `hand_landmarker.task` model file is automatically downloaded if not already present in the directory.*

## Controls

- **1 Open Hand**: Ready / Start timer
- **2 Open Hands**: Stop timer
- **Wave Hand**: Reset timer to 00:00.00
- **`q` key**: Exit application

## License

MIT License.

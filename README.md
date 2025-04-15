# Yoga Pose Analysis Web Application

A web-based application that provides real-time feedback on yoga poses using computer vision and machine learning.

## Features

- Real-time pose detection using MediaPipe
- Support for three yoga poses:
  - Warrior II
  - Tree Pose
  - Triangle Pose
- Real-time feedback on pose alignment
- Modern, responsive web interface
- Live video feed with pose overlay

## Requirements

- Python 3.8 or higher
- Webcam

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd yoga-pose-analysis
```

2. Create a virtual environment (not necessary, might not work):
```bash
python -m venv venv
source venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Allow camera access when prompted by your browser.

4. Select a pose from the buttons on the right side of the screen.

5. Follow the on-screen feedback to improve your pose.

## Controls

- Click the pose buttons to select which pose you want to practice
- The application will provide real-time feedback on your pose alignment
- The current pose is displayed at the top of the video feed

## Notes

- Make sure you have good lighting and avoid very baggy clothing
- Stand at a reasonable distance from the camera (frame should contain full body)
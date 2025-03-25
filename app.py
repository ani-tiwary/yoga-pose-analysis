from flask import Flask, render_template, Response, jsonify, request
import cv2
import numpy as np
import mediapipe as mp
from enum import Enum
import math
from yogurt import PoseAnalyzer, YogaPose
app = Flask(__name__)
pose_analyzer = PoseAnalyzer()
camera = None
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def get_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
    return camera

def generate_frames():
    while True:
        camera = get_camera()
        success, frame = camera.read()
        if not success:
            break
        else:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            try:
                landmarks = results.pose_landmarks.landmark
                if pose_analyzer.current_pose:
                    feedback = pose_analyzer.analyze_pose(landmarks)
                    y_position = 30
                    for tip in feedback:
                        cv2.putText(image, tip, (10, y_position), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                        y_position += 30
            except:
                pass
            mp.solutions.drawing_utils.draw_landmarks(
                image, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                mp.solutions.drawing_utils.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                mp.solutions.drawing_utils.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
            )
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_pose', methods=['POST'])
def set_pose():
    pose_name = request.json.get('pose')
    if pose_name == 'warrior2':
        pose_analyzer.current_pose = YogaPose.WARRIOR2
    elif pose_name == 'tree':
        pose_analyzer.current_pose = YogaPose.TREE
    elif pose_name == 'triangle':
        pose_analyzer.current_pose = YogaPose.TRIANGLE
    return jsonify({'status': 'success'})

@app.route('/get_current_pose')
def get_current_pose():
    return jsonify({'pose': pose_analyzer.current_pose.value if pose_analyzer.current_pose else 'None'})

if __name__ == '__main__':
    app.run(debug=True) 
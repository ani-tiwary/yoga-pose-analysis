from flask import Flask, render_template, Response, jsonify, request, session
import cv2
import numpy as np
import mediapipe as mp
from enum import Enum
import math
from yogurt import PoseAnalyzer, YogaPose
import logging
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key
pose_analyzer = PoseAnalyzer()

# Configure logging
logging.basicConfig(
    filename='yoga_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Global variables for camera and pose detection
camera = None
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def get_camera():
    global camera
    if camera is None:
        try:
            camera = cv2.VideoCapture(0)
            if not camera.isOpened():
                raise Exception("Failed to open camera")
            logging.info("Camera initialized successfully")
        except Exception as e:
            logging.error(f"Camera initialization error: {str(e)}")
            raise
    return camera

def generate_frames():
    while True:
        try:
            camera = get_camera()
            success, frame = camera.read()
            if not success:
                logging.error("Failed to read frame from camera")
                break
            else:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = pose.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                # Draw pose landmarks without text overlay
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
        except Exception as e:
            logging.error(f"Error in generate_frames: {str(e)}")
            break

@app.route('/')
def index():
    session['last_visit'] = datetime.now().isoformat()
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    try:
        return Response(generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        logging.error(f"Error in video_feed: {str(e)}")
        return jsonify({'error': 'Failed to start video feed'}), 500

@app.route('/get_feedback')
def get_feedback():
    try:
        camera = get_camera()
        success, frame = camera.read()
        if not success:
            return jsonify({'error': 'Failed to read frame'}), 500
            
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            feedback = pose_analyzer.analyze_pose(landmarks)
            
            # Determine if pose is correct (no feedback means good form)
            is_correct = len(feedback) == 0
            
            return jsonify({
                'feedback': feedback,
                'is_correct': is_correct,
                'current_pose': pose_analyzer.current_pose.value if pose_analyzer.current_pose else 'None'
            })
        else:
            return jsonify({
                'feedback': ['No pose detected. Please stand in front of the camera.'],
                'is_correct': False,
                'current_pose': pose_analyzer.current_pose.value if pose_analyzer.current_pose else 'None'
            })
            
    except Exception as e:
        logging.error(f"Error getting feedback: {str(e)}")
        return jsonify({'error': 'Failed to get feedback'}), 500

@app.route('/set_pose', methods=['POST'])
def set_pose():
    try:
        pose_name = request.json.get('pose')
        if not pose_name:
            return jsonify({'error': 'No pose specified'}), 400
            
        if pose_name == 'warrior2':
            pose_analyzer.current_pose = YogaPose.WARRIOR2
        elif pose_name == 'tree':
            pose_analyzer.current_pose = YogaPose.TREE
        elif pose_name == 'triangle':
            pose_analyzer.current_pose = YogaPose.TRIANGLE
        else:
            return jsonify({'error': 'Invalid pose'}), 400
            
        logging.info(f"Pose set to: {pose_analyzer.current_pose.value}")
        return jsonify({'status': 'success'})
    except Exception as e:
        logging.error(f"Error setting pose: {str(e)}")
        return jsonify({'error': 'Failed to set pose'}), 500

@app.route('/get_current_pose')
def get_current_pose():
    try:
        return jsonify({'pose': pose_analyzer.current_pose.value if pose_analyzer.current_pose else 'None'})
    except Exception as e:
        logging.error(f"Error getting current pose: {str(e)}")
        return jsonify({'error': 'Failed to get current pose'}), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True) 
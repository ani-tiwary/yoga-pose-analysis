import cv2
import numpy as np
import mediapipe as mp
from enum import Enum
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class YogaPose(Enum):
    WARRIOR2 = "Warrior II"
    TREE = "Tree Pose"
    TRIANGLE = "Triangle Pose"

class PoseAnalyzer:
    def __init__(self):
        self.current_pose = None
        self.feedback_cooldown = 0
        
    def calculate_angle(self, a, b, c): # get angle btwn three things
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360-angle
            
        return angle

    def get_coordinates(self, landmarks, part): # get xy for body part
        return [landmarks[part.value].x, landmarks[part.value].y]

    def analyze_warrior2(self, landmarks): # bilateral warriorii analysis
        feedback = []
        
        right_shoulder = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_SHOULDER)
        right_hip = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_HIP)
        right_knee = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_KNEE)
        right_ankle = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_ANKLE)
        right_wrist = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_WRIST)
        
        left_shoulder = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
        left_hip = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
        left_knee = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_KNEE)
        left_ankle = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE)
        left_wrist = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_WRIST)
        
        right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
        left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        
        if right_knee_angle < left_knee_angle:
            front_knee_angle = right_knee_angle
            back_knee_angle = left_knee_angle
            front_leg = "right"
        else:
            front_knee_angle = left_knee_angle
            back_knee_angle = right_knee_angle
            front_leg = "left"
        
        if front_knee_angle < 75 or front_knee_angle > 105:
            feedback.append("Adjust front knee bend (aim for roughly 90 degrees)")
            
        if back_knee_angle < 140:
            feedback.append("Straighten back leg more")
            
        hip_shoulder_angle = self.calculate_angle(right_shoulder, right_hip, left_hip)
        hip_shoulder_angle_alt = self.calculate_angle(left_shoulder, left_hip, right_hip)
        
        better_hip_angle = min(abs(hip_shoulder_angle - 90), abs(hip_shoulder_angle_alt - 90))
        if better_hip_angle > 25:
            feedback.append("Square hips to the side")
        
        right_arm_height_diff = abs(right_wrist[1] - right_shoulder[1])
        left_arm_height_diff = abs(left_wrist[1] - left_shoulder[1])
        
        if right_arm_height_diff > 0.1 or left_arm_height_diff > 0.1:
            feedback.append("Bring arms more parallel to ground")
            
        return feedback

    def analyze_tree(self, landmarks): # bilateral tree analysis
        feedback = []
        
        right_hip = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_HIP)
        right_knee = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_KNEE)
        right_ankle = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_ANKLE)
        right_wrist = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_WRIST)
        right_shoulder = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_SHOULDER)
        
        left_hip = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
        left_knee = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_KNEE)
        left_ankle = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE)
        left_wrist = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_WRIST)
        left_shoulder = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
        
        right_leg_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
        left_leg_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        
        if right_leg_angle > left_leg_angle:
            standing_leg_angle = right_leg_angle
            raised_foot = left_ankle
            knee_reference = right_knee
        else:
            standing_leg_angle = left_leg_angle
            raised_foot = right_ankle
            knee_reference = left_knee
        
        if standing_leg_angle < 160:
            feedback.append("Straighten standing leg more")
            
        hip_angle = self.calculate_angle(right_hip, 
                                       [(right_hip[0] + left_hip[0])/2, right_hip[1]], 
                                       left_hip)
        if abs(hip_angle - 180) > 25:
            feedback.append("Keep hips level")
            
        foot_height = abs(raised_foot[1] - knee_reference[1])
        if foot_height > 0.15:
            feedback.append("Raise foot higher on inner thigh")
        
        right_hands_height = right_wrist[1] < right_shoulder[1]
        left_hands_height = left_wrist[1] < left_shoulder[1]
        
        if not (right_hands_height and left_hands_height):
            feedback.append("Raise your hands above your head")
            
        return feedback

    def analyze_triangle(self, landmarks): # bilateral triangle analysis
        feedback = []
        
        right_shoulder = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_SHOULDER)
        right_hip = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_HIP)
        right_knee = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_KNEE)
        right_ankle = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_ANKLE)
        right_wrist = self.get_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_WRIST)
        
        left_shoulder = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
        left_hip = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
        left_knee = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_KNEE)
        left_ankle = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE)
        left_wrist = self.get_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_WRIST)

        stance_width = abs(right_ankle[0] - left_ankle[0])
        if stance_width < 0.3:
            feedback.append("Widen your stance")

        right_leg_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
        left_leg_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        
        if right_leg_angle < 160 or left_leg_angle < 160:
            feedback.append("Straighten both legs")

        spine_angle = self.calculate_angle(
            [(right_shoulder[0] + left_shoulder[0])/2, right_shoulder[1]],
            [(right_hip[0] + left_hip[0])/2, right_hip[1]],
            [right_hip[0] + 0.1, right_hip[1]]
        )
        
        if abs(spine_angle - 90) > 20:
            feedback.append("Tilt your torso more to the side")

        wrist_distance = abs(right_wrist[0] - left_wrist[0])
        if wrist_distance > 0.15:
            feedback.append("Align arms in a vertical line")

        return feedback

    def analyze_pose(self, landmarks): # analyses current pose, gives feedback
        if self.current_pose == YogaPose.WARRIOR2:
            return self.analyze_warrior2(landmarks)
        elif self.current_pose == YogaPose.TREE:
            return self.analyze_tree(landmarks)
        elif self.current_pose == YogaPose.TRIANGLE:
            return self.analyze_triangle(landmarks)
        return []

def main():
    pose_analyzer = PoseAnalyzer()
    
    cap = cv2.VideoCapture(0)
    
    cv2.namedWindow("Yoga Pose Analysis", cv2.WINDOW_NORMAL)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('1'):
                pose_analyzer.current_pose = YogaPose.WARRIOR2
            elif key == ord('2'):
                pose_analyzer.current_pose = YogaPose.TREE
            elif key == ord('3'):
                pose_analyzer.current_pose = YogaPose.TRIANGLE
            elif key == ord('q'):
                break
            
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
            
            mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
            )
            
            cv2.putText(image, f"Current Pose: {pose_analyzer.current_pose.value if pose_analyzer.current_pose else 'None'}", 
                       (10, image.shape[0] - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(image, "Press: 1-Warrior II, 2-Tree Pose, 3-Triangle Pose, Q-Quit", 
                       (10, image.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            cv2.imshow('Yoga Pose Analysis', image)
            
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
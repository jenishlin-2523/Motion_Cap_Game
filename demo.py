import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

st.title("🎮 Motion Control Subway Game (Streamlit Version)")

# Use webcam
cap = cv2.VideoCapture(0)
stframe = st.empty()

# Movement state
movement = "Stand"

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize and convert for processing
        image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

            # Example logic: left-right motion control
            if left_wrist.x < 0.3:
                movement = "Left 🏃‍♂️⬅️"
            elif right_wrist.x > 0.7:
                movement = "Right 🏃‍♂️➡️"
            else:
                movement = "Stand 🧍"

        except:
            pass

        # Draw pose landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Convert back to BGR for OpenCV to show
        final = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        stframe.image(final, channels="BGR", use_column_width=True)
        st.write(f"**Movement Detected:** {movement}")

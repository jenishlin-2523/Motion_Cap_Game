import streamlit as st
import cv2
import mediapipe as mp
import time

# Title
st.title("🕺 Real-time Pose Detection with Webcam")
st.markdown("This app uses your webcam to detect human pose using MediaPipe.")

# Run/Stop toggle
run = st.checkbox("Turn ON Camera")

# MediaPipe Pose setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Webcam feed processing
FRAME_WINDOW = st.image([])

if run:
    cap = cv2.VideoCapture(0)  # Use the first webcam
    st.info("Press the checkbox to turn off the camera.")
    
    while run:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to access webcam.")
            break

        # Flip, convert color
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # MediaPipe processing
        results = pose.process(rgb)

        # Draw keypoints
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        FRAME_WINDOW.image(frame, channels="BGR")

    cap.release()
    st.success("Camera turned off.")
else:
    st.warning("Turn on the camera using the checkbox above.")

import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import mediapipe as mp
import cv2

# Initialize MediaPipe pose detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

class PoseDetector(VideoProcessorBase):
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        # Process the image and detect pose
        results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Streamlit App Interface
st.title("🕺 Real-time Pose Detection with Webcam")
st.write("This app uses your webcam to detect human pose using MediaPipe + Streamlit WebRTC.")

webrtc_streamer(
    key="pose",
    video_processor_factory=PoseDetector,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

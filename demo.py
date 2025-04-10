import cv2
import mediapipe as mp
import pyautogui
import time

# Mediapipe pose setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Setup webcam
cap = cv2.VideoCapture(0)
pyautogui.FAILSAFE = False

# Cooldown to prevent rapid key presses
cooldown = 1.0
last_action_time = time.time()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip image and convert to RGB
    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_image)

    # Draw landmarks
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Extract landmarks
        landmarks = results.pose_landmarks.landmark
        right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

        now = time.time()

        # Jump: Raise right hand above shoulder
        if right_hand.y < right_shoulder.y and now - last_action_time > cooldown:
            pyautogui.press("up")
            print("Jump")
            last_action_time = now

        # Slide: Lower right hand below hip
        elif right_hand.y > right_hip.y and now - last_action_time > cooldown:
            pyautogui.press("down")
            print("Slide")
            last_action_time = now

    # Show webcam
    cv2.imshow('Pose Controlled Subway Surfer', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

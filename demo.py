import cv2
import mediapipe as mp
import pyautogui
import win32gui
import time

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Lower lag

# Window size
screen_width, screen_height = 640, 480

# Cooldown
last_trigger_time = 0
cooldown = 0.3  # seconds

# FPS counter
prev_frame_time = 0

# Get foreground window title
def get_active_window_title():
    try:
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)
    except:
        return ""

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.resize(frame, (screen_width, screen_height))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    # Define grid zones regardless of face detection
    left_zone = int(screen_width * 0.4)
    right_zone = int(screen_width * 0.6)
    top_zone = int(screen_height * 0.4)
    bottom_zone = int(screen_height * 0.6)

    # Check game window
    active_window = get_active_window_title()
    if "subway" not in active_window.lower():
        cv2.putText(frame, "❌ Game not active.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow('AI Subway Controller', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        continue

    # Face tracking
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            nose = face_landmarks.landmark[1]
            nose_x = int(nose.x * screen_width)
            nose_y = int(nose.y * screen_height)
            cv2.circle(frame, (nose_x, nose_y), 5, (0, 255, 0), -1)

            current_time = time.time()
            if current_time - last_trigger_time > cooldown:
                if nose_x < left_zone:
                    pyautogui.press('right')
                    print("🎮 Triggered: RIGHT")
                    last_trigger_time = current_time
                elif nose_x > right_zone:
                    pyautogui.press('left')
                    print("🎮 Triggered: LEFT")
                    last_trigger_time = current_time
                elif nose_y < top_zone:
                    pyautogui.press('up')
                    print("🎮 Triggered: UP")
                    last_trigger_time = current_time
                elif nose_y > bottom_zone:
                    pyautogui.press('down')
                    print("🎮 Triggered: DOWN")
                    last_trigger_time = current_time

    # Draw grid (always)
    cv2.line(frame, (left_zone, 0), (left_zone, screen_height), (255, 0, 0), 1)
    cv2.line(frame, (right_zone, 0), (right_zone, screen_height), (255, 0, 0), 1)
    cv2.line(frame, (0, top_zone), (screen_width, top_zone), (255, 0, 0), 1)
    cv2.line(frame, (0, bottom_zone), (screen_width, bottom_zone), (255, 0, 0), 1)

    # FPS overlay
    new_frame_time = time.time()
    fps = int(1 / (new_frame_time - prev_frame_time + 0.0001))
    prev_frame_time = new_frame_time
    cv2.putText(frame, f'FPS: {fps}', (10, screen_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imshow('AI Subway Controller', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

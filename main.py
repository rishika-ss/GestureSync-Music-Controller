import cv2
import mediapipe as mp
import pygame
import math
import time

# ------------------ PYGAME INIT ------------------
pygame.mixer.init()
tracks = {
    "normal": "music.mp3",
    "slow": "slow.mp3",
    "fast": "speed.mp3"
}

current_mode = None
volume_level = 0.5  # 50%
track_start_time = 0  # Keep track of position in seconds

def play_mode(mode):
    global current_mode, track_start_time

    if mode == current_mode:
        return

    # Get current playback time in seconds
    if current_mode is not None:
        # get_pos() returns milliseconds since music started
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms != -1:
            track_start_time += pos_ms / 1000.0

    # Stop current track
    pygame.mixer.music.stop()

    # Load new track
    pygame.mixer.music.load(tracks[mode])
    # Start from the same timestamp
    pygame.mixer.music.play(-1, start=track_start_time)
    pygame.mixer.music.set_volume(volume_level)

    current_mode = mode

def stop_music():
    global current_mode, track_start_time
    pygame.mixer.music.stop()
    current_mode = None
    track_start_time = 0

# ------------------ MEDIAPIPE INIT ------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
movement_threshold = 40
cooldown_time = 0.4
last_action_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, c = frame.shape

            # -------- PINCH DETECTION --------
            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]
            thumb_x, thumb_y = int(thumb.x * w), int(thumb.y * h)
            index_x, index_y = int(index.x * w), int(index.y * h)
            distance = math.hypot(index_x - thumb_x, index_y - thumb_y)
            pinch_active = distance < 40

            # -------- FINGER COUNT --------
            fingers = 0
            tips = [8, 12, 16, 20]
            for tip in tips:
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                    fingers += 1

            # -------- FIST (STOP) --------
            if fingers == 0:
                stop_music()
                cv2.putText(frame, "STOP", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # -------- ONE FINGER (PLAY NORMAL) --------
            elif fingers == 1 and not pinch_active:
                play_mode("normal")
                cv2.putText(frame, "PLAY", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # -------- PINCH CONTROL MODE --------
            if pinch_active:
                cv2.putText(frame, "CONTROL MODE", (20, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

                wrist = hand_landmarks.landmark[0]
                current_x = int(wrist.x * w)
                current_y = int(wrist.y * h)
                current_time = time.time()

                if prev_x != 0 and (current_time - last_action_time > cooldown_time):

                    # RIGHT - FAST
                    if current_x - prev_x > movement_threshold:
                        play_mode("fast")
                        last_action_time = current_time

                    # LEFT - SLOW
                    elif prev_x - current_x > movement_threshold:
                        play_mode("slow")
                        last_action_time = current_time

                    # UP - VOLUME UP
                    elif prev_y - current_y > movement_threshold:
                        volume_level = min(1.0, volume_level + 0.1)
                        pygame.mixer.music.set_volume(volume_level)
                        last_action_time = current_time

                    # DOWN - VOLUME DOWN
                    elif current_y - prev_y > movement_threshold:
                        volume_level = max(0.0, volume_level - 0.1)
                        pygame.mixer.music.set_volume(volume_level)
                        last_action_time = current_time

                prev_x = current_x
                prev_y = current_y

    # -------- DRAW VOLUME BAR --------
    bar_x, bar_y = 50, 400
    bar_width, bar_height = 300, 20

    # Background bar
    cv2.rectangle(frame, (bar_x, bar_y),
                  (bar_x + bar_width, bar_y + bar_height),
                  (100, 100, 100), -1)

    # Filled bar
    filled_width = int(bar_width * volume_level)
    # Color changes with volume
    if volume_level < 0.3:
        color = (0, 0, 255)  # Red
    elif volume_level < 0.7:
        color = (0, 255, 255)  # Yellow
    else:
        color = (0, 255, 0)  # Green

    cv2.rectangle(frame, (bar_x, bar_y),
                  (bar_x + filled_width, bar_y + bar_height),
                  color, -1)

    # Volume text
    cv2.putText(frame, f"VOLUME: {int(volume_level * 100)}%",
                (bar_x, bar_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Mode indicator
    if current_mode:
        cv2.putText(frame, f"MODE: {current_mode.upper()}",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 255), 2)

    cv2.imshow("Smart Gesture DJ Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()

import cv2
import mediapipe as mp
import pygame
import math
import time

pygame.mixer.init()

TRACKS = {
    "normal": "music.mp3",
    "slow": "slow.mp3",
    "fast": "speed.mp3"
}

current_mode = None
volume_level = 0.5
track_start_time = 0


def play_mode(mode):
    global current_mode, track_start_time

    if mode == current_mode:
        return

    if current_mode is not None:
        pos = pygame.mixer.music.get_pos()
        if pos != -1:
            track_start_time += pos / 1000

    pygame.mixer.music.stop()
    pygame.mixer.music.load(TRACKS[mode])
    pygame.mixer.music.play(-1, start=track_start_time)
    pygame.mixer.music.set_volume(volume_level)

    current_mode = mode


def stop_music():
    global current_mode, track_start_time
    pygame.mixer.music.stop()
    current_mode = None
    track_start_time = 0


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
movement_threshold = 40
cooldown_time = 0.4
last_action_time = 0

while True:
    success, frame = cap.read()
    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:

            draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape

            thumb = hand.landmark[4]
            index = hand.landmark[8]

            tx, ty = int(thumb.x * w), int(thumb.y * h)
            ix, iy = int(index.x * w), int(index.y * h)

            # distance between thumb and index finger (used for pinch detection)
            dist = math.hypot(ix - tx, iy - ty)
            pinch = dist < 40

            fingers = 0
            tips = [8, 12, 16, 20]

            # count how many fingers are raised
            for tip in tips:
                if hand.landmark[tip].y < hand.landmark[tip - 2].y:
                    fingers += 1

            if fingers == 0:
                stop_music()
                cv2.putText(frame, "STOP", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            elif fingers == 1 and not pinch:
                play_mode("normal")
                cv2.putText(frame, "PLAY", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if pinch:
                cv2.putText(frame, "CONTROL MODE", (20, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

                wrist = hand.landmark[0]
                cx, cy = int(wrist.x * w), int(wrist.y * h)
                now = time.time()

                if prev_x != 0 and (now - last_action_time > cooldown_time):

                    # horizontal movement → change music speed
                    if cx - prev_x > movement_threshold:
                        play_mode("fast")
                        last_action_time = now

                    elif prev_x - cx > movement_threshold:
                        play_mode("slow")
                        last_action_time = now

                    # vertical movement → control volume
                    elif prev_y - cy > movement_threshold:
                        volume_level = min(1.0, volume_level + 0.1)
                        pygame.mixer.music.set_volume(volume_level)
                        last_action_time = now

                    elif cy - prev_y > movement_threshold:
                        volume_level = max(0.0, volume_level - 0.1)
                        pygame.mixer.music.set_volume(volume_level)
                        last_action_time = now

                prev_x, prev_y = cx, cy

    bar_x, bar_y = 50, 400
    bar_w, bar_h = 300, 20

    cv2.rectangle(frame, (bar_x, bar_y),
                  (bar_x + bar_w, bar_y + bar_h),
                  (100, 100, 100), -1)

    filled = int(bar_w * volume_level)

    if volume_level < 0.3:
        color = (0, 0, 255)
    elif volume_level < 0.7:
        color = (0, 255, 255)
    else:
        color = (0, 255, 0)

    cv2.rectangle(frame, (bar_x, bar_y),
                  (bar_x + filled, bar_y + bar_h),
                  color, -1)

    cv2.putText(frame, f"Volume: {int(volume_level * 100)}%",
                (bar_x, bar_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    if current_mode:
        cv2.putText(frame, f"Mode: {current_mode.upper()}",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 255), 2)

    cv2.imshow("GestureSync Music Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()

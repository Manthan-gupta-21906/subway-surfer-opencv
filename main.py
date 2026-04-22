import cv2
import mediapipe as mp
import time
import threading
from pynput.keyboard import Controller, Key

# ================= CONFIG =================
VEL_THRESHOLD_X = 85
VEL_THRESHOLD_Y = 75
SMOOTHING_ALPHA = 0.18
ACTION_COOLDOWN = 0.11
IDLE_THRESHOLD = 6
lastMoveTime = time.time()

CAMERA_WIDTH = 424
CAMERA_HEIGHT = 240
MIN_SWIPE_DISTANCE = 10

# ================= KEYBOARD =================
keyboard = Controller()
KEY_HOLD_DURATION = 0.08

def send_key(key):
    key_map = {
        'right': Key.right,
        'left': Key.left,
        'up': Key.up,
        'down': Key.down,
        'space': Key.space
    }
    keyboard.press(key_map[key])
    time.sleep(KEY_HOLD_DURATION)
    keyboard.release(key_map[key])
    time.sleep(0.02)

# ================= SHARED FRAME =================
frame = None
lock = threading.Lock()
running = True

def camera_reader(cap):
    global frame, running
    while running:
        success, img = cap.read()
        if not success:
            continue
        img = cv2.flip(img, 1)
        with lock:
            frame = img.copy()

# ================= MEDIAPIPE =================
mp_hands = mp.solutions.hands

# ================= CAMERA =================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, CAMERA_WIDTH)
cap.set(4, CAMERA_HEIGHT)
cap.set(cv2.CAP_PROP_FPS, 30)

threading.Thread(target=camera_reader, args=(cap,), daemon=True).start()

# ================= VARIABLES =================
smoothX, smoothY = 0, 0
prevPosX, prevPosY = 0, 0
prevTime = 0
lastActionTime = 0
prevCX, prevCY = 0, 0

actionText = "IDLE"
prevActionText = "IDLE"

# ================= FPS =================
fps = 0
frameCount = 0
fpsTimer = time.time()

cv2.namedWindow("Gesture Control", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Gesture Control", 640, 480)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    while True:
        with lock:
            if frame is None:
                continue
            img = frame.copy()

        h, w, _ = img.shape
        currentTime = time.time()

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]

            px = int(hand.landmark[8].x * w)
            py = int(hand.landmark[8].y * h)

            # -------- SMOOTH --------
            if smoothX == 0:
                smoothX, smoothY = px, py
            else:
                smoothX = int(SMOOTHING_ALPHA * smoothX + (1 - SMOOTHING_ALPHA) * px)
                smoothY = int(SMOOTHING_ALPHA * smoothY + (1 - SMOOTHING_ALPHA) * py)

            cx, cy = smoothX, smoothY

            # Direction line (index MCP → index fingertip)
            bx = int(hand.landmark[5].x * w)
            by = int(hand.landmark[5].y * h)
            cv2.line(img, (bx, by), (cx, cy), (0, 200, 255), 2)

            # ================= SWIPE DETECTION =================
            if prevTime == 0:
                prevPosX, prevPosY = cx, cy
                prevTime = currentTime
            else:
                dt = currentTime - prevTime
                distX = abs(cx - prevPosX)
                distY = abs(cy - prevPosY)

                if dt > 0:
                    vx = (cx - prevPosX) / dt
                    vy = (cy - prevPosY) / dt

                    if currentTime - lastActionTime > ACTION_COOLDOWN:

                        if vx > VEL_THRESHOLD_X and (distX > MIN_SWIPE_DISTANCE or abs(vx) > VEL_THRESHOLD_X*1.6):
                            actionText = "RIGHT"
                            lastActionTime = currentTime

                        elif vx < -VEL_THRESHOLD_X and (distX > MIN_SWIPE_DISTANCE or abs(vx) > VEL_THRESHOLD_X*1.6):
                            actionText = "LEFT"
                            lastActionTime = currentTime

                        elif vy < -VEL_THRESHOLD_Y and (distY > MIN_SWIPE_DISTANCE or abs(vy) > VEL_THRESHOLD_Y*1.6):
                            actionText = "JUMP"
                            lastActionTime = currentTime

                        elif vy > VEL_THRESHOLD_Y and (distY > MIN_SWIPE_DISTANCE or abs(vy) > VEL_THRESHOLD_Y*1.6):
                            actionText = "DUCK"
                            lastActionTime = currentTime

                prevPosX, prevPosY = cx, cy
                prevTime = currentTime

            # -------- IDLE --------
            moveSpeed = abs(cx - prevCX) + abs(cy - prevCY)
            if moveSpeed > IDLE_THRESHOLD:
                lastMoveTime = currentTime

            if currentTime - lastMoveTime > 0.18:
                actionText = "IDLE"

            prevCX, prevCY = cx, cy

        else:
            actionText = "IDLE"
            smoothX, smoothY = 0, 0
            prevTime = 0

        # ================= KEY PRESS =================
        if actionText != prevActionText and actionText != "IDLE":
            key_to_send = None

            if actionText == "RIGHT":
                key_to_send = 'right'
            elif actionText == "LEFT":
                key_to_send = 'left'
            elif actionText == "JUMP":
                key_to_send = 'up'
            elif actionText == "DUCK":
                key_to_send = 'down'

            if key_to_send is not None:
                threading.Thread(target=send_key, args=(key_to_send,), daemon=True).start()

            prevActionText = actionText

        elif actionText == "IDLE":
            prevActionText = "IDLE"

        # ================= FPS =================
        frameCount += 1
        if time.time() - fpsTimer >= 1:
            fps = frameCount
            frameCount = 0
            fpsTimer = time.time()

        preview = cv2.resize(img, (640, 480))

        cv2.putText(preview, f'FPS:{fps}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

        color = (0, 255, 0)
        if actionText == "RIGHT":
            color = (255, 0, 0)
        elif actionText == "LEFT":
            color = (0, 165, 255)
        elif actionText == "JUMP":
            color = (0, 255, 255)
        elif actionText == "DUCK":
            color = (0, 0, 255)

        cv2.putText(preview, actionText, (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)

        cv2.imshow("Gesture Control", preview)

        if cv2.waitKey(1) & 0xFF == 27:
            running = False
            break

cap.release()
cv2.destroyAllWindows()

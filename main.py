import cv2, time, os, urllib.request, ctypes, math
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "hand_landmarker.task"
if not os.path.exists(MODEL_PATH):
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
        MODEL_PATH)

detector = vision.HandLandmarker.create_from_options(vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=MODEL_PATH), num_hands=2,
    running_mode=vision.RunningMode.VIDEO))

CONN = [(0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,7),(7,8),(5,9),(9,10),(10,11),(11,12),
        (9,13),(13,14),(14,15),(15,16),(13,17),(17,18),(18,19),(19,20),(0,17)]
TIP_MCP = [(8,5),(12,9),(16,13),(20,17)]

dist = lambda a, b: math.hypot(a.x-b.x, a.y-b.y)
is_open = lambda hnd: sum(dist(hnd[0],hnd[t]) > dist(hnd[0],hnd[m])*1.3 for t,m in TIP_MCP) >= 3

def is_waving(hist, rev=4, amp=0.06):
    if len(hist) < 10:
        return False
    diffs = [hist[i+1]-hist[i] for i in range(len(hist)-1)]
    reversals, last = 0, 0
    for d in diffs:
        if abs(d) < 0.005:
            continue
        s = 1 if d > 0 else -1
        if last and s != last:
            reversals += 1
        last = s
    return reversals >= rev and max(hist)-min(hist) >= amp

def face_solid(frame, box, hue_std=9, sat_min=60):
    x1, y1, x2, y2 = box
    hsv = cv2.cvtColor(frame[y1:y2, x1:x2], cv2.COLOR_BGR2HSV)
    p = hsv[::8, ::8].reshape(-1, 3)
    return p[:,1].mean() >= sat_min and p[:,0].std() < hue_std

def draw_panel(frame, text, sub, color):
    overlay = frame.copy()
    cv2.rectangle(overlay, (20,20), (430,140), (30,30,30), -1)
    frame[:] = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
    cv2.putText(frame, text, (40,90), cv2.FONT_HERSHEY_SIMPLEX, 1.6, color, 3)
    cv2.putText(frame, sub, (40,125), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

def draw_ring(frame, center, pct, color):
    cv2.ellipse(frame, center, (40,40), -90, 0, 360*pct, color, 4)

STATE_COLOR = {"WAITING": (0,200,255), "RUNNING": (0,255,0), "STOPPED": (0,120,255)}

state, start_time, elapsed = "WAITING", 0, 0
g_hold, c_hold, HOLD, C_HOLD = 0, 0, 6, 15
wave_hist = []

cap = cv2.VideoCapture(0)
cap.set(3, 960); cap.set(4, 540)
u = ctypes.windll.user32
cv2.namedWindow("Cube Timer", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Cube Timer", u.GetSystemMetrics(0), u.GetSystemMetrics(1))
cv2.moveWindow("Cube Timer", 0, 0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    box = (w//2-100, h//2-100, w//2+100, h//2+100)

    small = cv2.resize(frame, (320, 240))
    result = detector.detect_for_video(
        mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(small, cv2.COLOR_BGR2RGB)),
        int(time.time()*1000))

    open_hands = 0
    if result.hand_landmarks:
        wave_hist.append(result.hand_landmarks[0][0].x)
        wave_hist[:] = wave_hist[-15:]
        for hnd in result.hand_landmarks:
            open_hands += is_open(hnd)
            for lm in hnd:
                cv2.circle(frame, (int(lm.x*w), int(lm.y*h)), 4, (0,255,0), -1)
            for a, b in CONN:
                cv2.line(frame, (int(hnd[a].x*w), int(hnd[a].y*h)),
                          (int(hnd[b].x*w), int(hnd[b].y*h)), (255,255,255), 2)
    else:
        wave_hist.clear()

    if state == "WAITING" and open_hands == 1:
        g_hold += 1
        if g_hold >= HOLD:
            state, start_time, g_hold = "RUNNING", time.perf_counter(), 0
    elif state != "RUNNING":
        g_hold = 0

    if state == "RUNNING":
        elapsed = time.perf_counter() - start_time
        g_hold = g_hold+1 if open_hands == 2 else 0
        c_hold = c_hold+1 if face_solid(frame, box) else 0
        if g_hold >= HOLD or c_hold >= C_HOLD:
            state, elapsed = "STOPPED", time.perf_counter()-start_time
            g_hold = c_hold = 0

    if state != "RUNNING" and is_waving(wave_hist):
        state, elapsed, g_hold, c_hold, wave_hist = "WAITING", 0, 0, 0, []

    # --- UI ---
    color = STATE_COLOR[state]
    pulse = int(4 + 3*math.sin(time.time()*4)) if state == "RUNNING" else 4
    cv2.rectangle(frame, box[:2], box[2:], color, 2)
    if state == "RUNNING" and c_hold:
        draw_ring(frame, ((box[0]+box[2])//2, (box[1]+box[3])//2), c_hold/C_HOLD, color)
    cv2.rectangle(frame, (0,0), (w-1,h-1), color, pulse)

    mins, secs = int(elapsed//60), elapsed % 60
    draw_panel(frame, f"{mins:02d}:{secs:06.3f}", state, color)

    cv2.imshow("Cube Timer", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('r'):
        state, elapsed, g_hold, c_hold, wave_hist = "WAITING", 0, 0, 0, []

cap.release()
cv2.destroyAllWindows()
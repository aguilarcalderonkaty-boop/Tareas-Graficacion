import cv2
import mediapipe as mp
import numpy as np
import time


# MediaPipe

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
#Cámara
cap = cv2.VideoCapture(0)


# Estado calculadora

num_a = ""
num_b = ""
operator = ""
result = ""
state = "A"  # Estado actual: A o B
last_press_time = 0
PRESS_DELAY = 0.6  # segundos para que no rebote


# Botones

buttons = []

# Números
x0, y0 = 50, 50
w, h = 80, 80

for i in range(10):
    buttons.append({
        "label": str(i),
        "x": x0 + i * (w + 5),
        "y": y0,
        "w": w,
        "h": h,
        "type": "num"
    })

# Operadores
ops = ["+", "-", "*", "/", "^"]
for i, op in enumerate(ops):
    buttons.append({
        "label": op,
        "x": 50,
        "y": 160 + i * (h + 10),
        "w": w,
        "h": h,
        "type": "op"
    })

# Igual
buttons.append({
    "label": "=",
    "x": 50,
    "y": 160 + len(ops) * (h + 10),
    "w": w,
    "h": h,
    "type": "eq"
})


# Funciones

def draw_button(img, b):
    cv2.rectangle(
        img,
        (b["x"], b["y"]),
        (b["x"] + b["w"], b["y"] + b["h"]),
        (200, 200, 200),
        2
    )
    cv2.putText(
        img,
        b["label"],
        (b["x"] + 25, b["y"] + 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (255, 255, 255),
        2
    )

def inside(x, y, b):
    return b["x"] < x < b["x"] + b["w"] and b["y"] < y < b["y"] + b["h"]


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (1200, 800), interpolation=cv2.INTER_LINEAR)
    h_img, w_img, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    # Dibujar botones
    for b in buttons:
        draw_button(frame, b)

    # Mostrar estado
    display = f"{num_a} {operator} {num_b}"
    cv2.putText(frame, display, (50, h_img - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 255), 2)

    if res.multi_hand_landmarks:
        for hand in res.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            index_tip = hand.landmark[8]
            x = int(index_tip.x * w_img)
            y = int(index_tip.y * h_img)

            cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)

            now = time.time()
            if now - last_press_time > PRESS_DELAY:
                for b in buttons:
                    if inside(x, y, b):

                        if b["type"] == "num":
                            if state == "A":
                                num_a += b["label"]
                            elif state == "B":
                                num_b += b["label"]

                        elif b["type"] == "op" and num_a != "":
                            operator = b["label"]
                            state = "B"

                        elif b["type"] == "eq" and num_b != "":
                            try:
                                expr = num_a + operator + num_b
                                result = str(eval(expr))
                                num_a = result
                                num_b = ""
                                operator = ""
                                state = "A"
                            except:
                                num_a = ""
                                num_b = ""
                                operator = ""
                                result = "Error"

                        last_press_time = now

    if result != "":
        cv2.putText(frame, f"Resultado: {result}",
                    (300, h_img - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4,
                    (255, 100, 0), 2)

    cv2.imshow("Calculadora con dedo", frame) 

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

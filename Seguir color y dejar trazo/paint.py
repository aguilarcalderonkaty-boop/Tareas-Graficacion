import cv2
import numpy as np
import mediapipe as mp

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Variables globales
color = (0,255,0) # Color inicial (verde)
opcion = 0 # 0: nada, 1: pintar

# Inicializar la captura de video desde la cámara web
cap = cv2.VideoCapture(0)
cv2.waitKey(2000) # Esperar 2 segundos para que la cámara se estabilice

pizarra = None   # lienzo donde pintaremos
mano=False
mano_actual=None
mx2,my2=0,0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame2 = frame.copy()
    if pizarra is None:
        pizarra = np.zeros_like(frame)  # inicializar lienzo negro

    # Opciones en pantalla para seleccionar color
    cv2.rectangle(frame2, (30, 30), (100, 100), (0, 255, 0), -1) # verde
    cv2.rectangle(frame2, (110,30), (180,100),(0,0,255) , -1) # rojo
    cv2.rectangle(frame2, (190,30), (260,100), (255,0,140), -1)   # morado
    cv2.rectangle(frame2, (270,30), (340,100), (0,136,255), -1) # naranja
    cv2.rectangle(frame2, (350,30), (420,100), (0,255,255) , -1) # amarillo
    cv2.rectangle(frame2, (430,30), (500,100),(255,0,0), -1) # azul
    
    # Botón de borrar
    cv2.rectangle(frame2, (30,140), (100,200), (250,250,250), -1)   

    # Detectar objeto azul
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 80, 40])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Detectar mano para cambiar color o borrar
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_drawing.draw_landmarks(frame2, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            indice = hand_landmarks.landmark[8]
            mx2, my2 = int(indice.x * w), int(indice.y * h)

            # Paleta de colores
            if 30<my2<100:
                if 30<mx2<100: color=(0,255,0)
                elif 110<mx2<180: color=(0,0,255)
                elif 190<mx2<260: color=(255,0,140)
                elif 270<mx2<340: color=(0,136,255)
                elif 350<mx2<420: color=(0,255,255)
                elif 430<mx2<500: color=(255,0,0)

            # Borrar lienzo
            if 140<my2<200 and 30<mx2<100:
                pizarra[:] = 0 

    # Pintar con el objeto azul detectado
    coords = np.column_stack(np.where(mask==255))
    for y,x in coords:
        pizarra[y,x] = color

    # Superponer lienzo
    combined = cv2.addWeighted(frame2, 0.7, pizarra, 0.3, 0)

    cv2.imshow("Paint", combined)
    cv2.imshow("mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty("Paint", cv2.WND_PROP_VISIBLE) < 1:
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

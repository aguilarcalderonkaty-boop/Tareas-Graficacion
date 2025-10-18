import cv2
import mediapipe as mp

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Configurar el detector de manos
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Voltear la imagen para que parezca un espejo
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convertir a RGB para MediaPipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Variables para almacenar las posiciones de los dedos índices
    index_left = None
    index_right = None

    # Procesar las manos detectadas
    if results.multi_hand_landmarks:
        for hand_landmarks, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Dibujar los landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Identificar si es la mano izquierda o derecha
            label = hand_info.classification[0].label  # 'Left' o 'Right'
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            if label == "Left":
                index_left = (x, y)
            else:
                index_right = (x, y)

    # Dibujar el rectángulo solo si ambas manos están detectadas
    if index_left and index_right:
        cv2.rectangle(frame, index_left, index_right, (0, 255, 0), -1)

    # Mostrar el resultado
    cv2.imshow("Rectángulo entre dedos", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe as mp

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Crear el detector de manos
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Iniciar captura de video
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    # Voltear la imagen (efecto espejo)
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convertir a RGB (MediaPipe trabaja en RGB)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Verificar si hay dos manos detectadas
    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
        # Obtener las dos manos detectadas
        hand1, hand2 = results.multi_hand_landmarks

        # Dibujar ambas manos
        mp_draw.draw_landmarks(frame, hand1, mp_hands.HAND_CONNECTIONS)
        mp_draw.draw_landmarks(frame, hand2, mp_hands.HAND_CONNECTIONS)

        # Coordenadas de los dedos índices
        x1 = int(hand1.landmark[8].x * w)
        y1 = int(hand1.landmark[8].y * h)
        x2 = int(hand2.landmark[8].x * w)
        y2 = int(hand2.landmark[8].y * h)

        # Determinar esquinas del rectángulo
        x_min, x_max = min(x1, x2), max(x1, x2)
        y_min, y_max = min(y1, y2), max(y1, y2)

        # Calcular color dinámico según distancia (opcional)
        distancia = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        color = (0, int(min(255, distancia)), 255 - int(min(255, distancia)))

        # Dibujar rectángulo escalado
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, -1)

    # Mostrar imagen
    cv2.imshow("Rectángulo entre dedos", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar cámara
cap.release()
cv2.destroyAllWindows()

import cv2
import numpy as np

# Rango de color verde en HSV (puedes ajustarlo)
lower_color = np.array([40, 70, 70])
upper_color = np.array([80, 255, 255])

# Inicializar cámara
cap = cv2.VideoCapture(0)

# Lista para guardar posiciones anteriores
trail_points = []

# Tamaño máximo del rastro
max_trail_length = 50

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Máscara del color objetivo
    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=2)

    # Buscar contornos del objeto detectado
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > 3:
            # Agregar punto actual al rastro
            center = (int(x), int(y))
            trail_points.append(center)

            # Limitar longitud del rastro
            if len(trail_points) > max_trail_length:
                trail_points.pop(0)

    # Dibujar rastro como líneas conectadas
    for i in range(1, len(trail_points)):
        if trail_points[i - 1] is None or trail_points[i] is None:
            continue

        # Crear un gradiente de color púrpura → rosa
        alpha = i / len(trail_points)
        r = int(255 * (1 - alpha) + 255 * alpha)
        g = int(0 * (1 - alpha) + 105 * alpha)
        b = int(255 * (1 - alpha) + 180 * alpha)

        cv2.line(frame, trail_points[i - 1], trail_points[i], (b, g, r), 4)

    # Mostrar ventana
    cv2.imshow("Rastro con Lógica Diferente", frame)

    # Salir con ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Liberar cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()

import cv2
import numpy as np

# Abrir la cámara externa (en este caso se usa el índice 0, que corresponde a la primera cámara detectada)
cap = cv2.VideoCapture(0)

# Pausa inicial para que el dispositivo de video se ajuste antes de comenzar
cv2.waitKey(2000)

# Tomar una captura que servirá como referencia del fondo
ret, background = cap.read()
if not ret:
    print("No fue posible obtener la imagen de fondo.")
    cap.release()
    exit()
# Si la lectura falla, se liberan los recursos y se termina el programa

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # Mientras la cámara esté activa, se leen los cuadros en tiempo real.
    # Si ocurre un error en la lectura, se interrumpe el ciclo.

    # Convertir el frame al espacio de color HSV para facilitar la detección de tonos
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir el rango de color que se quiere ocultar (verde en este ejemplo)
    lower_green = np.array([80, 80, 80])
    upper_green = np.array([140, 255, 255])

    # Crear una máscara binaria que marca las zonas verdes
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Invertir la máscara para obtener las áreas que no corresponden al color elegido
    mask_inv = cv2.bitwise_not(mask)

    # Conservar las regiones que no son verdes en la imagen original
    res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Rellenar las zonas verdes con el fondo previamente capturado
    res2 = cv2.bitwise_and(background, background, mask=mask)

    # Combinar ambas imágenes para lograr el efecto de invisibilidad
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    # Mostrar el resultado en pantalla
    cv2.imshow("Capa de Invisibilidad", final_output)
    cv2.imshow("mask", mask)

    # Salir del programa si se presiona la tecla 'q' o si la ventana se cierra manualmente
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty("Capa de Invisibilidad", cv2.WND_PROP_VISIBLE) < 1:
        break

# Liberar la cámara y cerrar todas las ventanas abiertas
cap.release()
cv2.destroyAllWindows()

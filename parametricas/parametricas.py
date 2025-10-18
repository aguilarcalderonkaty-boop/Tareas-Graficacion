import math
import cv2 as cv
import numpy as np
import random as ran

# Tamaño de las imágenes (anchura y altura)
width, height = 800, 800
center_x, center_y = width // 2, height // 2

# Crear tres imágenes negras donde dibujaremos las curvas
img_cardioide = np.zeros((height, width, 3), np.uint8)
img_hipocicloide = np.zeros((height, width, 3), np.uint8)
img_lissajous = np.zeros((height, width, 3), np.uint8)

# Parámetro para tamaño general de las figuras
scale = 170

# Ángulo que irá aumentando para trazar las curvas
angle = 0

# Parámetros para la hipocicloide (curva con 'n' puntas)
num_points = 10  # número de "puntas" o lóbulos de la hipocicloide
R_big = scale    # radio del círculo mayor (fijo)
r_small = scale / num_points  # radio del círculo menor que rueda dentro del mayor

while True:
    # Generar un color RGB aleatorio para los puntos de cada frame
    color = (ran.randint(0, 255), ran.randint(0, 255), ran.randint(0, 255))
    
    # 1. Cardioide usando coordenadas polares
    # rCardioide = a * (0.7 - cos(theta)) es la fórmula polar modificada
    r_cardioide = scale * (0.7 - math.cos(angle))
    
    # Convertimos de coordenadas polares a cartesianas para dibujar
    x_card = int(center_x - r_cardioide * math.cos(angle))
    y_card = int(center_y - r_cardioide * math.sin(angle))
    
    # Dibujamos un pequeño círculo en la posición calculada
    cv.circle(img_cardioide, (x_card, y_card), 3, color, -1)


    # 2. Hipocicloide con fórmula paramétrica
    # El círculo menor rueda dentro del círculo mayor y genera la curva
    x_hipo = int(center_x + (R_big - r_small) * math.cos(angle) + r_small * math.cos(((R_big - r_small) / r_small) * angle))
    y_hipo = int(center_y + (R_big - r_small) * math.sin(angle) - r_small * math.sin(((R_big - r_small) / r_small) * angle))
    
    cv.circle(img_hipocicloide, (x_hipo, y_hipo), 3, color, -1)

    # 3. Curva de Lissajous con frecuencia diferente en X y Y
    # Se usa la función seno para generar movimiento periódico
    x_liss = int(center_x + 150 * math.sin(3 * angle))  # frecuencia 3 en X
    y_liss = int(center_y + 150 * math.cos(5 * angle))  # frecuencia 5 en Y
    
    cv.circle(img_lissajous, (x_liss, y_liss), 3, color, -1)

    # Incrementar el ángulo para que las curvas vayan avanzando
    angle += 0.008

    # Mostrar las tres imágenes en ventanas separadas
    cv.imshow("Curva de Lissajous", img_lissajous)
    cv.imshow(f"Hipocicloide con {num_points} puntas", img_hipocicloide)
    cv.imshow("Cardioide", img_cardioide)

    # Salir si se presiona la tecla ESC (código 27)
    if cv.waitKey(2) & 0xFF == 27:
        break

# Cuando se salga del bucle, cerrar todas las ventanas
cv.destroyAllWindows()

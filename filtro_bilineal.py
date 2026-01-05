import cv2 as cv
import numpy as np
import math


# Imagen original
imagen_original = cv.imread("ejemplo.jpg", cv.IMREAD_GRAYSCALE)

alto, ancho = imagen_original.shape


# Imágenes para guardar
img_escalada = np.zeros((alto, ancho), dtype=np.uint8)
img_rotada = np.zeros((alto, ancho), dtype=np.uint8)

img_escalada_suave = np.zeros((alto, ancho), dtype=np.uint8)
img_rotada_suave = np.zeros((alto, ancho), dtype=np.uint8)


# Parámetros
factor_escala = 2
angulo = 45
rad = math.radians(angulo)


# Escalado 
for fila in range(alto):
    for col in range(ancho):
        nuevo_x = col * factor_escala
        nuevo_y = fila * factor_escala

        if 0 <= nuevo_x < ancho and 0 <= nuevo_y < alto:
            img_escalada[nuevo_y, nuevo_x] = imagen_original[fila, col]


# Suavizado
for i in range(1, alto - 1):
    for j in range(1, ancho - 1):
        vecindad = (
            img_escalada[i, j] +
            img_escalada[i, j + 1] +
            img_escalada[i + 1, j] +
            img_escalada[i + 1, j + 1] +
            img_escalada[i - 1, j] +
            img_escalada[i - 1, j - 1] +
            img_escalada[i - 1, j + 1] +
            img_escalada[i + 1, j - 1] +
            img_escalada[i, j - 1]
        )
        img_escalada_suave[i, j] = int(vecindad / 9)


# Rotación
for i in range(alto):
    for j in range(ancho):
        x_rot = int(i * math.cos(rad) + j * math.sin(rad))
        y_rot = int(j * math.cos(rad) - i * math.sin(rad))

        if 0 <= x_rot < ancho and 0 <= y_rot < alto:
            img_rotada[y_rot, x_rot] = img_escalada[i, j]


# Suavizado post-rotación

for i in range(1, alto - 1):
    for j in range(1, ancho - 1):
        vecinos = (
            img_rotada[i, j] +
            img_rotada[i, j + 1] +
            img_rotada[i + 1, j] +
            img_rotada[i + 1, j + 1] +
            img_rotada[i - 1, j] +
            img_rotada[i - 1, j - 1] +
            img_rotada[i - 1, j + 1] +
            img_rotada[i + 1, j - 1] +
            img_rotada[i, j - 1]
        )
        img_rotada_suave[i, j] = int(vecinos / 9)


# Mostrar 
cv.imshow("Imagen base en escala de grises", imagen_original)
cv.imshow("Imagen ampliada sin interpolacion", img_escalada)
cv.imshow("Imagen ampliada con suavizado", img_escalada_suave)
cv.imshow("Imagen ampliada y rotada", img_rotada)
cv.imshow("Imagen ampliada, rotada y suavizada", img_rotada_suave)

cv.waitKey(0)
cv.destroyAllWindows()

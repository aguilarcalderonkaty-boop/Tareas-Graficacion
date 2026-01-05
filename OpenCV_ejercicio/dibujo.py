import cv2
import numpy as np

def draw_car(img, pos=(150, 220), scale=1.0, body_color=(60, 120, 255), wheel_color=(30, 30, 30)):
    x, y = pos #coordenadas superior izquierda
    s = scale # escala

    # Parte del cuerpo 
    body_w, body_h = int(180*s), int(50*s)
    body_tl = (x, y)
    body_br = (x + body_w, y + body_h)
    cv2.rectangle(img, body_tl, body_br, body_color, -1, cv2.LINE_AA)

    #Parte de arrba
    cab_w, cab_h = int(90*s), int(40*s)
    cab_tl = (x + int(60*s), y - cab_h)
    cab_br = (x + int(150*s), y)
    cv2.rectangle(img, cab_tl, cab_br, body_color, -1, cv2.LINE_AA)

    # Ventanas 
    ven_color = (200, 230, 255)
    cv2.rectangle(img,
                  (x + int(70*s), y - cab_h + int(5*s)),
                  (x + int(100*s), y - int(5*s)),
                  ven_color, -1, cv2.LINE_AA)
    cv2.rectangle(img,
                  (x + int(110*s), y - cab_h + int(5*s)),
                  (x + int(140*s), y - int(5*s)),
                  ven_color, -1, cv2.LINE_AA)

    # Ruedas
    r = int(18*s)
    wheel_y = y + body_h
    cv2.circle(img, (x + int(45*s), wheel_y), r, wheel_color, -1, cv2.LINE_AA)
    cv2.circle(img, (x + int(135*s), wheel_y), r, wheel_color, -1, cv2.LINE_AA)

    # Luces
    cv2.circle(img, (x + body_w, y + int(5*s)), int(6*s),
               (0, 255, 255), -1, cv2.LINE_AA)  # luz delantera
    cv2.circle(img, (x, y + int(5*s)), int(6*s),
               (0, 0, 255), -1, cv2.LINE_AA)  # luz trasera


# Lienzo
h, w = 400, 600
img = np.full((h, w, 3), 240, dtype=np.uint8)

# Fondo: carretera y cielo
cv2.rectangle(img, (0, int(h*0.65)), (w, h), (70, 70, 70), -1)      # carretera
cv2.rectangle(img, (0, 0), (w, int(h*0.65)), (255, 255, 0), -1)   # cielo
cv2.line(img, (0, int(h*0.8)), (w, int(h*0.8)), (255, 255, 255), int(2))  # línea carretera

# Dibuja los autos
draw_car(img, pos=(160, 230), scale=1.0)
draw_car(img, pos=(360, 250), scale=0.8, body_color=(0, 180, 120))

# Mostrar
cv2.imshow("Autito con primitivas", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

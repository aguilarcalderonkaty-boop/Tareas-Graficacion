import cv2 as cv

# Cargar clasificadores
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
bocaCascade = cv.CascadeClassifier('haarcascade_mcs_mouth.xml')
cap = cv.VideoCapture(0)

# Animaciones
modificadorOjos = 0
vueltaOjos = 3
modificadorLengua = 0
vueltaLengua = 1

while True:
    ret, img = cap.read()
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)

    for (x, y, w, h) in rostros:
        # Marco rostro
        img = cv.rectangle(img, (x, y), (x + w, y + h), (204, 0, 255), 3)

        # División superior e inferior
        mitad = int(y + h / 2)
        img = cv.rectangle(img, (x, y), (x + w, mitad), (153, 0, 204), 2)
        img = cv.rectangle(img, (x, mitad), (x + w, y + h), (255, 153, 255), 3)

        # Ojos
        cx_izq = x + int(w * 0.3)
        cx_der = x + int(w * 0.7)
        cy_ojo = y + int(h * 0.4)
        radio_pupila = 5
        limite_ojo = 10

        img = cv.circle(img, (cx_izq, cy_ojo), 20, (255, 255, 255), -1)
        img = cv.circle(img, (cx_der, cy_ojo), 20, (255, 255, 255), -1)
        # Contorno ojo
        img = cv.circle(img, (cx_izq, cy_ojo), 21, (204, 0, 255), 2)
        img = cv.circle(img, (cx_der, cy_ojo), 21, (204, 0, 255), 2)
        # Pupilas con movimiento
        img = cv.circle(img, (cx_izq + modificadorOjos, cy_ojo), radio_pupila, (0, 0, 255), -1)
        img = cv.circle(img, (cx_der + modificadorOjos, cy_ojo), radio_pupila, (0, 0, 255), -1)

        modificadorOjos += vueltaOjos
        if modificadorOjos > limite_ojo or modificadorOjos < -limite_ojo:
            vueltaOjos *= -1

        # Nariz 
        nariz_top = y + int(h * 0.45)
        nariz_bottom = y + int(h * 0.65)
        nariz_left = x + int(w * 0.4)
        nariz_right = x + int(w * 0.6)
        img = cv.rectangle(img, (nariz_left, nariz_top), (nariz_right, nariz_bottom), (255, 102, 255), -1)
        img = cv.rectangle(img, (nariz_left, nariz_top), (nariz_right, nariz_bottom), (153, 0, 204), 2)

        # Boca 
        cx_boca = x + int(w * 0.5)
        cy_boca = y + int(h * 0.8)
        radio_boca = int(w * 0.08)
        img = cv.circle(img, (cx_boca, cy_boca), radio_boca, (60, 0, 60), -1)  # base boca

        # Detectar boca abierta 
        roi_gray = gris[y + int(h * 0.6):y + h, x:x + w]
        boca = bocaCascade.detectMultiScale(roi_gray, 1.7, 11)

        if len(boca) == 0:
            # Mostrar lengua animada
            lengua_top = cy_boca
            lengua_bottom = cy_boca + modificadorLengua
            lengua_izq = cx_boca - int(w * 0.04)
            lengua_der = cx_boca + int(w * 0.04)

            img = cv.rectangle(img, (lengua_izq, lengua_top), (lengua_der, lengua_bottom), (255, 130, 200), -1)
            img = cv.rectangle(img, (lengua_izq, lengua_top), (lengua_der, lengua_bottom), (255, 255, 255), 1)

            modificadorLengua += vueltaLengua
            if modificadorLengua > 20 or modificadorLengua < 0:
                vueltaLengua *= -1
        else:
            modificadorLengua = 0  # No lengua si detecta boca

    # Mostrar ventana
    cv.imshow('ProyectoU2', img)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

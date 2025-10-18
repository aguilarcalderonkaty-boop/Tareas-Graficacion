import cv2 as cv  # Importa la biblioteca OpenCV para procesamiento de imágenes


# Cargar clasificadores Haar
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')  # Clasificador para detectar rostros
bocaCascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_smile.xml')  # Clasificador para detectar bocas
cap = cv.VideoCapture(0)  # Abre la cámara web (índice 0)


# Variables de animación
modificadorOjos = 0      # Posición de la pupila (horizontal)
vueltaOjos = 3           # Dirección del movimiento de los ojos
modificadorLengua = 0    # Altura de la lengua 
vueltaLengua = 1         # Dirección de movimiento de la lengua


while True:
    ret, img = cap.read()  # Captura un frame de la cámara
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Convierte a escala de grises para detección
    rostros = rostro.detectMultiScale(gris, 1.3, 5)  # Detecta rostros en la imagen

    for (x, y, w, h) in rostros:  # Itera sobre los rostros detectados
        # Marco del rostro
        img = cv.rectangle(img, (x, y), (x + w, y + h), (204, 0, 255), 3)


        # División superior/inferior del rostro
        mitad = int(y + h / 2)
        img = cv.rectangle(img, (x, y), (x + w, mitad), (153, 0, 204), 2)       # Parte superior
        img = cv.rectangle(img, (x, mitad), (x + w, y + h), (255, 153, 255), 3) # Parte inferior

        # Ojos
        cx_izq = x + int(w * 0.3)  # Centro del ojo izquierdo
        cx_der = x + int(w * 0.7)  # Centro del ojo derecho
        cy_ojo = y + int(h * 0.4)  # Altura de los ojos

        radio_pupila = 5      # Tamaño de la pupila
        limite_ojo = 10       # Límite del movimiento de los ojos

        # Globo ocular (blanco)
        img = cv.circle(img, (cx_izq, cy_ojo), 20, (255, 255, 255), -1)
        img = cv.circle(img, (cx_der, cy_ojo), 20, (255, 255, 255), -1)

        # Contorno del ojo
        img = cv.circle(img, (cx_izq, cy_ojo), 21, (204, 0, 255), 2)
        img = cv.circle(img, (cx_der, cy_ojo), 21, (204, 0, 255), 2)

        # Pupilas con movimiento horizontal animado
        img = cv.circle(img, (cx_izq + modificadorOjos, cy_ojo), radio_pupila, (0, 0, 255), -1)
        img = cv.circle(img, (cx_der + modificadorOjos, cy_ojo), radio_pupila, (0, 0, 255), -1)

        # Lógica para que las pupilas se muevan de un lado al otro
        modificadorOjos += vueltaOjos
        if modificadorOjos > limite_ojo or modificadorOjos < -limite_ojo:
            vueltaOjos *= -1  # Cambia dirección

       
        # Nariz
        nariz_top = y + int(h * 0.45)
        nariz_bottom = y + int(h * 0.65)
        nariz_left = x + int(w * 0.4)
        nariz_right = x + int(w * 0.6)

        # Dibuja la nariz como un rectángulo rosa
        img = cv.rectangle(img, (nariz_left, nariz_top), (nariz_right, nariz_bottom), (255, 102, 255), -1)
        img = cv.rectangle(img, (nariz_left, nariz_top), (nariz_right, nariz_bottom), (153, 0, 204), 2)

     
        # Boca
        cx_boca = x + int(w * 0.5)        # Centro horizontal de la boca
        cy_boca = y + int(h * 0.8)        # Altura de la boca
        radio_boca = int(w * 0.08)        # Tamaño de la boca

        # Dibuja la boca
        img = cv.circle(img, (cx_boca, cy_boca), radio_boca, (60, 0, 60), -1)  # Color morado oscuro

        
        # Boca abierta o cerrada
        # Extrae la región inferior del rostro donde debería estar la boca
        roi_gray = gris[y + int(h * 0.6):y + h, x:x + w]
        boca = bocaCascade.detectMultiScale(roi_gray, 1.7, 11)  # Detección de sonrisa

        if len(boca) == 0:
            # Si NO detecta boca, osea si esta cerrada se dibuja una lengua animada
            lengua_top = cy_boca
            lengua_bottom = cy_boca + modificadorLengua
            lengua_izq = cx_boca - int(w * 0.04)
            lengua_der = cx_boca + int(w * 0.04)

            # Dibuja lengua animada (rosa claro con contorno blanco)
            img = cv.rectangle(img, (lengua_izq, lengua_top), (lengua_der, lengua_bottom), (255, 130, 200), -1)
            img = cv.rectangle(img, (lengua_izq, lengua_top), (lengua_der, lengua_bottom), (255, 255, 255), 1)

            # Anima la lengua (sube y baja)
            modificadorLengua += vueltaLengua
            if modificadorLengua > 20 or modificadorLengua < 0:
                vueltaLengua *= -1
        else:
            modificadorLengua = 0  # Si detecta boca abierta, no muestra lengua

  
    # Mostrar imagen resultante
    cv.imshow('ProyectoU2', img)

    # Presionar 'q' para salir
    if cv.waitKey(1) == ord('q'):
        break


# Liberar recursos
cap.release()
cv.destroyAllWindows()

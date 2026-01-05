import cv2
import numpy as np
import keyboard as key
import mediapipe as mp
import math

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Variables globales
color = (0,255,0) # Color inicial (verde)
opcion = 0 # 1: paint, 2: rectangulo, 3: circulo

# Inicializar la captura de video desde la cámara web
cap = cv2.VideoCapture(0)
cv2.waitKey(2000) # Esperar 2 segundos para que la cámara se estabilice

pizarra = None   # lienzo donde pintaremos
figuras = []     # lista para rectángulos y círculos
mano=False
mano_actual=None
mx1,my1,mx2,my2=0,0,0,0
mx_1,my_1,mx_2,my_2=0,0,0,0

def dibujar_rectangulo(x1,y1,x2,y2,guardar):
    
    cx = (x2+x1)/2
    cy = (y2+y1)/2
    angulo = math.atan2(y2 - y1, x2 - x1)
    distancia = math.hypot(x2 - x1, y2 - y1)
    
    x1,y1 = transformar(-distancia*2,-distancia*2.5,angulo,cx,cy)
    x2,y2 = transformar(distancia*2,distancia*2.5,angulo,cx,cy)
    x3,y3 = transformar(-distancia*2,distancia*2.5,angulo,cx,cy)
    x4,y4 = transformar(distancia*2,-distancia*2.5,angulo,cx,cy)

    if guardar:
        figuras.append((2, (x1,y1,x2,y2,x3,y3,x4,y4), color))
        
    return x1,y1,x2,y2,x3,y3,x4,y4

def dibujar_circulo(x1,y1,x2,y2,guardar):
    
    cx = int((x2+x1)/2)
    cy = int((y2+y1)/2)
    distancia = int(math.hypot(x2 - x1, y2 - y1))

    if guardar:
        figuras.append((3, (cx,cy,int(distancia*1.1)), color))
        
        
    return cx,cy, distancia
       
def dibujar_triangulo(x1,y1,x2,y2,guardar):

    cx = (x2 + x1) / 2
    cy = (y2 + y1) / 2
    angulo = math.atan2(y2 - y1, x2 - x1)
    distancia = math.hypot(x2 - x1, y2 - y1)

    x1, y1 = transformar(0, distancia * 2.5, angulo, cx, cy)        
    x2, y2 = transformar(-distancia * 2, -distancia * 2.5, angulo, cx, cy) 
    x3, y3 = transformar(distancia * 2, -distancia * 2.5, angulo, cx, cy)  

    if guardar:
        figuras.append((4, (x1, y1, x2, y2, x3, y3), color))
        
    return x1,y1,x2,y2,x3,y3

def dibujar_linea(x1,y1,x2,y2,guardar):
    cx = (x2 + x1) / 2
    cy = (y2 + y1) / 2
    angulo = math.atan2(y2 - y1, x2 - x1)
    distancia = math.hypot(x2 - x1, y2 - y1)

    x1, y1 = transformar(-distancia * 1.5, 0, angulo, cx, cy) 
    x2, y2 = transformar(distancia * 1.5,0, angulo, cx, cy) 

    if guardar:
        figuras.append((5, (x1, y1, x2, y2), color))
        
    return x1,y1,x2,y2
        
def transformar(dx, dy, angulo, cx, cy):
    px = int(cx + dx * math.cos(angulo) - dy * math.sin(angulo))
    py = int(cy + dx * math.sin(angulo) + dy * math.cos(angulo))
    return px, py

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
    
    alto, ancho = frame.shape[:2]
    
    # Opciones de figuras
    opx1=ancho-100
    opx2=ancho-30
    
    cv2.circle(frame2,(((opx1+opx2)//2),((80+130)//2)),15,color,-1)
    cv2.rectangle(frame2, (opx2,140), (opx1,190), (255,0,140), 3)   
    cv2.circle(frame2,(((opx1+opx2)//2),((200+250)//2)),20,(255,0,140),3)
    
    cv2.line(frame2,(opx1,310),(opx2,310),(255,0,140), 3)
    cv2.line(frame2,(opx1,310),((opx1+opx2)//2,260),(255,0,140), 3)
    cv2.line(frame2,(opx2,310),((opx1+opx2)//2,260),(255,0,140), 3)
    
    cv2.line(frame2,(opx1,320),(opx2,370),(255,0,140), 3)
    
    #Borrar
    cv2.circle(frame2,(((30+100)//2),((160+230)//2)),15,(250,250,250),-1)
    cv2.rectangle(frame2, (30,240), (100,310), (250,250,250), -1)   
    cv2.circle(frame2,(((30+100)//2),((320+390)//2)),15,(250,250,250),3)
    
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 80, 40])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)


    # Dibujar figuras con la mano
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            guardar=False
            label = handedness.classification[0].label
            if(not mano):
                mano_actual=label
                mano=True
                
            mp_drawing.draw_landmarks(frame2, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            pulgar = hand_landmarks.landmark[4]
            indice = hand_landmarks.landmark[8]
            indice_base = hand_landmarks.landmark[5]
            
            if(label==mano_actual):
                mx1, my1 = int(pulgar.x * w), int(pulgar.y * h)
                mx2, my2 = int(indice.x * w), int(indice.y * h)
                
            if(label!=mano_actual):
                mx_1, my_1 = int(pulgar.x * w), int(pulgar.y * h)
                mx_2, my_2 = int(indice.x * w), int(indice.y * h)
                if(my_2>my_1): guardar=True
            
            
            label = handedness.classification[0].label
            
            if(not mano):
                mano_actual=label
            
            if 30<my2<100: # paleta de colores
                if 30<mx2<100: color=(0,255,0)
                elif 110<mx2<180: color=(0,0,255)
                elif 190<mx2<260: color=(255,0,140)
                elif 270<mx2<340: color=(0,136,255)
                elif 350<mx2<420: color=(0,255,255)
                elif 430<mx2<500: color=(255,0,0)
                
            if opx1<mx2<opx2: # opciones de figura
                if 80<my2<140: opcion=1
                elif 140<my2<200: opcion=2
                elif 200<my2<260: opcion=3
                elif 260<my2<320: opcion=4
                elif 320<my2<380: opcion=5
                
            if  30<mx2<100: 
                #borrar
                if 160<my2<230: opcion=7
                elif 240<my2<310: opcion=6
                elif 320<my2<390: opcion=8
                
            if opcion==2:
                x1,y1,x2,y2,x3,y3,x4,y4=dibujar_rectangulo(mx1,my1,mx2,my2,guardar)
                cv2.line(frame2, (x1, y1), (x3, y3), color, 3)
                cv2.line(frame2, (x2, y2), (x4, y4), color, 3)
                cv2.line(frame2, (x1, y1), (x4, y4), color, 3)
                cv2.line(frame2, (x2, y2), (x3, y3), color, 3)
            if opcion==3:
                cx,cy,distancia=dibujar_circulo(mx1,my1,mx2,my2,guardar)
                cv2.circle(frame2,(cx,cy),int(distancia*1.1),color,3)
            if opcion==4:
                x1,y1,x2,y2,x3,y3=dibujar_triangulo(mx1,my1,mx2,my2,guardar)
                cv2.line(frame2, (x1, y1), (x3, y3), color, 3)
                cv2.line(frame2, (x2, y2), (x1, y1), color, 3)
                cv2.line(frame2, (x2, y2), (x3, y3), color, 3)
            if opcion==5:
                x1,y1,x2,y2 = dibujar_linea(mx1,my1,mx2,my2, guardar)
                cv2.line(frame2, (x2, y2), (x1, y1), color, 3)
            if opcion==6:
                figuras.clear()
            if opcion==7:
                pizarra[:] = 0 
    else: mano=False     
   
                
    # Pintar con el objeto azul detectado
    if opcion in [0,1]:
        coords = np.column_stack(np.where(mask==255))
        for y,x in coords:
            if opcion==1:
                pizarra[y,x] = color
            
    

    # Superponer lienzo y figuras
    combined = cv2.addWeighted(frame2, 0.7, pizarra, 0.3, 0)
    for figura in figuras:
        if figura[0]==2:
            puntos = figura[1]; col = figura[2]
            cv2.line(combined,(puntos[0],puntos[1]),(puntos[4],puntos[5]),col,3)
            cv2.line(combined,(puntos[2],puntos[3]),(puntos[6],puntos[7]),col,3)
            cv2.line(combined,(puntos[0],puntos[1]),(puntos[6],puntos[7]),col,3)
            cv2.line(combined,(puntos[2],puntos[3]),(puntos[4],puntos[5]),col,3)
        elif figura[0]==3:
            cx,cy,r = figura[1]; col = figura[2]
            cv2.circle(combined,(cx,cy),r,col,3)
        elif figura[0]==4:
            puntos = figura[1]; col = figura[2]
            cv2.line(combined,(puntos[0],puntos[1]),(puntos[4],puntos[5]),col,3)
            cv2.line(combined,(puntos[2],puntos[3]),(puntos[0],puntos[1]),col,3)
            cv2.line(combined,(puntos[2],puntos[3]),(puntos[4],puntos[5]),col,3)
        elif figura[0]==5:
            puntos = figura[1]; col = figura[2]
            cv2.line(combined,(puntos[0],puntos[1]),(puntos[2],puntos[3]),col,3)
            
                  

    cv2.imshow("Seguimiento", combined)
    cv2.imshow("mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty("Seguimiento", cv2.WND_PROP_VISIBLE) < 1:
        break


#. Liberar los recursos
cap.release()
cv2.destroyAllWindows()


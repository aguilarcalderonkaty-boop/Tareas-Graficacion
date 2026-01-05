# Proyecto Final - Ciudad 3D que se explora con landmarks
""" Instrucciones:
Un entorno 3D es una representación digital tridimensional (con altura, anchura y profundidad) de objetos y espacios, creada por computadora para simular mundos virtuales interactivos, utilizada en diseño (AutoCAD), videojuegos (Fortnite), formación (Realidad Virtual), o efectos visuales, permitiendo explorar escenarios complejos o recrear la realidad con gran detalle mediante texturas, iluminación y modelado, ofreciendo inmersión y funcionalidad.

Con la información anterior y utilizando el apartado MediaPipe, casas, snowman conformados en estos apuntes realizar los siguientes puntos.

implementar una ciudad, entorno, mundo 3, donde por lo menos tengas 20 objetos móviles
implementar el movimiento mediante los landmark de las manos afectando el desplazamiento de la cámara gluLookAt para poder divisar todo el entorno
los objetos deben de tener alguna animación de transformación geométrica

Proyecto realizado por:
- Chavez Mandujano Abril Michelle
- Aguilar Calderon Katia
- Paz Alfaro Mariana

"""

# Librerías
import glfw 
import cv2 
import mediapipe as mp 
import numpy as np 
from OpenGL.GL import * 
from OpenGL.GLU import * 
import math 
import keyboard as key  
import random 

# Configuración 
# Inicializar MediaPipe Hands 

mp_hands = mp.solutions.hands 
mp_drawing = mp.solutions.drawing_utils 
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) 

# Configuración de la ventana GLFW
WINDOW_WIDTH = 640 
WINDOW_HEIGHT = 480 
WINDOW_TITLE = "Ciudad 3D que se explora con landmarks" 

 

#Variables para movimientos ---------------------------------------------------------------------------------------------
moverx, movery, moverz,dx,dz,girar=0, 0, 0,0,0,0 #Variables para mover la cámara
angulo_carros,angulo_vivos,angulo_insectos=0,0,0 #Variables para los objetos móviles
ang_mov_persona,ang_mov_perro, ang_mov_peli_mari,ang_mov_pollo_pez=60,60,80,60 #Variables para los que vuelan o caminan
dir_persona, dir_perro,dir_peli_mari,dir_pol_pez=0,0,0,0 #Dirección de los que vuelan o caminan

#Día 
angulo_dia,r,g,b,vuelta_dia=0,0,0,0,1 

 
#Ola del mar
ola_tamano,dir_ola=0,0 

 

#cococrilo 
angulo_coco1,dir_coco1,angulo_coco2,dir_coco2=0,-10,0,-10 


#Pelicanos 
angulo_peli1, angulo_peli2,angulo_peli3, dir_peli1, dir_peli2,dir_peli3= 0,0,0,0.07,0.11,0.03 

d_peli1, d_peli2,d_peli3=0,0,0 

 
#Pollos 

#Pelicanos 
angulo_pol1, angulo_pol2,angulo_pol3, dir_pol1, dir_pol2,dir_pol3= 0,0,0,0.09,0.11,0.05 
d_pol1, d_pol2,d_pol3=0,0,0 

 
#Peces 
angulo_pez1, angulo_pez2,angulo_pez3, dir_pez1, dir_pez2,dir_pez3= 0,0,0,0.01,0.05,0.03 
d_pez1, d_pez2,d_pez3=0,0,0 



#Barquito 
angulo_bar,d_bar, dir_bar= 0,0,0.3 

 
#Nubes 
d_nubes1,d_nubes2=65,0 

 

#Humo que funciona como las nubes xd 
d_humo1,d_humo2=65,0 

 

#abeja, mariposa 
mov_abeja,dir_abeja=0,0.25 

 

#Tipos pateando una pelota 
ang_patear1,pat1,ang_patear2,pat2,mov_pelota,dir_pelota=0,10,0,0,0,0 

 

#Antena 
angulo_antena=0 

 

#Fuente 
d_gotas,dir_gotas=0,0.1 

#-----------------------------------------------------------------------------------------------------------------

def init_glfw(): # Inicializa GLFW y crea una ventana OpenGL  

    if not glfw.init(): 

        raise Exception("No se pudo inicializar GLFW") 


    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, None, None) # Crear ventana GLFW


    if not window: # Si no se pudo crear la ventana, terminar GLFW y lanzar excepción

        glfw.terminate() 

        raise Exception("No se pudo crear la ventana GLFW") 

     

    glfw.make_context_current(window) # Hacer el contexto OpenGL actual
    glfw.swap_interval(1)  # Habilitar VSync


    return window 


# Configuracion inicial de OpenGL -------------------------------------------------------------------------------------

def setup_opengl(): 

    glClearColor(0.0, 0.0, 0.0, 1.0) # color de fondo
    glEnable(GL_DEPTH_TEST) # activar el z-buffer para el manejo de profundidad
    glDepthFunc(GL_LESS) # función de prueba de profundidad, GL_LESS significa que un fragmento se dibuja si está más cerca de la cámara
    glEnable(GL_BLEND) # habilitar blending para transparencia
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # función de blending estándar para transparencia
    glEnable(GL_LINE_SMOOTH) # suavizado de líneas (menos pixeleado)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST) # mejor calidad de suavizado de líneas

 

def create_video_texture(): # Crea una textura para el video de la cámara

    video_tex = glGenTextures(1) # Generar una textura
    glBindTexture(GL_TEXTURE_2D, video_tex) # Vincular la textura 
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) # Establecer parámetros de la textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) 
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE) 
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE) 

    return video_tex 

 

def setup_lights(): # Configura la iluminación en la escena

    glEnable(GL_LIGHTING) 
    glEnable(GL_LIGHT0) 
    glEnable(GL_LIGHT1)  # Luz adicional 
    glEnable(GL_COLOR_MATERIAL) 
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE) # Configurar material para que use el color de los vértices 

     

    # Luz principal frontal 

    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 2, 1)) 
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1)) 
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1)) 
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1)) 


    # Luz de relleno lateral 

    glLightfv(GL_LIGHT1, GL_POSITION, (1, 1, 1, 0)) 
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.5, 0.5, 0.5, 1)) 



# Funciones de dibujo -------------------------------------------------------------------------------------


def normal_tri(v1, v2, v3, normal_falla=(0.0, 1.0, 0.0)): 

    """ 

    Calcula la normal unitaria de un triángulo definido por v1, v2, v3. 

    v1, v2, v3: tuplas (x, y, z) 

    fallback: normal por defecto si el triángulo es degenerado 

    """ 

 

    ux = v2[0] - v1[0] 
    uy = v2[1] - v1[1] 
    uz = v2[2] - v1[2] 

    vx = v3[0] - v1[0] 
    vy = v3[1] - v1[1] 
    vz = v3[2] - v1[2] 

    nx = uy * vz - uz * vy 
    ny = uz * vx - ux * vz 
    nz = ux * vy - uy * vx 


    longitud = math.sqrt(nx*nx + ny*ny + nz*nz) # Calcular la longitud de la normal

    if longitud < 1e-8: # Triángulo degenerado, usar normal por defecto 

        return normal_falla # Retornar la normal por defecto


    return (nx/longitud, ny/longitud, nz/longitud) # Retornar la normal unitaria

 

 

def draw_rectangulo(lado1,lado2, color=(1,1,1)):  # Dibuja un plano para representar el suelo o calle

    glBegin(GL_QUADS) 
    glColor3f(*color)  # Gris oscuro para la calle 
    glNormal3f(0, 1, 0)  

     

    # Coordenadas del plano 

    glVertex3f(-lado1, 0, lado2) 
    glVertex3f(lado1, 0, lado2) 
    glVertex3f(lado1, 0, -lado2) 
    glVertex3f(-lado1, 0, -lado2) 

    glEnd() 

     

def draw_elipse(a1,b1,a2,b2,angulo,capa,color=(1,1,1)): # Dibuja una elipse en el plano XZ

    glPushMatrix() # Guardar la matriz actual
    glTranslatef(0, capa, 0) # Elevar la elipse a la altura 'capa'
    glBegin(GL_QUAD_STRIP) 
    glColor3f(*color) 
    glNormal3f(0, 1, 0) 

 

    i = 0 

    while i <= angulo:  # Dibujar la elipse

        ang = math.radians(i) # Convertir grados a radianes
        x1 = a1 * math.cos(ang) 
        z1 = b1 * math.sin(ang) 

        x2 = a2 * math.cos(ang) 
        z2 = b2 * math.sin(ang) 

        glVertex3f(x1, 0, z1) 
        glVertex3f(x2, 0, z2) 

        i += 1 

 

    # cerrar el strip 
    glVertex3f(a1, 0, 0) 
    glVertex3f(a2, 0, 0) 

    glEnd() 
    glPopMatrix() 

     

def draw_cube(alto,ancho,largo,color1,color2,color3): # Dibuja un cubo con colores diferentes para la base de la casa. paredes, techo

    glBegin(GL_QUADS) 

    glColor3f(*color1)  # Marrón para todas las caras 

    ancho=ancho/2 

    largo=largo/2 

    # Frente 

    glNormal3f(1,0,0) 
    glVertex3f(-ancho, 0, largo) 
    glVertex3f(ancho, 0, largo) 
    glVertex3f(ancho, alto, largo) 
    glVertex3f(-ancho, alto, largo) 

     

    # Atras 
    glNormal3f(1,0,0) 
    glVertex3f(-ancho, 0, -largo) 
    glVertex3f(ancho, 0, -largo) 
    glVertex3f(ancho, alto, -largo) 
    glVertex3f(-ancho, alto, -largo) 

 

    # Izquierda 
    glNormal3f(0,0,1) 
    glVertex3f(-ancho, 0, -largo) 
    glVertex3f(-ancho, 0, largo) 
    glVertex3f(-ancho, alto, largo) 
    glVertex3f(-ancho, alto, -largo) 

     

    # Derecha 
    glNormal3f(0,0,1) 
    glVertex3f(ancho, 0, -largo) 
    glVertex3f(ancho, 0, largo) 
    glVertex3f(ancho, alto, largo) 
    glVertex3f(ancho, alto, -largo) 

     

    # Arriba 
    glNormal3f(0,1,0) 
    glColor3f(*color2)  # Color diferente para el techo 
    glVertex3f(-ancho, alto, -largo) 
    glVertex3f(ancho, alto, -largo) 
    glVertex3f(ancho, alto, largo) 
    glVertex3f(-ancho, alto, largo) 

     

    # Abajo 
    glNormal3f(0,1,0) 
    glColor3f(*color3)  # Color diferente para el suelo 
    glVertex3f(-ancho, 0, -largo) 
    glVertex3f(ancho, 0, -largo) 
    glVertex3f(ancho, 0, largo) 
    glVertex3f(-ancho, 0, largo) 


    glEnd() 

 

def draw_piramide(alto, ancho, largo, altura, color):  # Dibuja una pirámide con base rectangular

    glBegin(GL_TRIANGLES) 
    glColor3f(*color) 

    ancho /= 2 
    largo /= 2 
    alto = alto + altura 

    cima = (0, alto, 0) # Cima de la pirámide

    v1 = (-ancho, altura,  largo) 
    v2 = ( ancho, altura,  largo) 

    n = normal_tri(v1, v2, cima) 

    glNormal3f(*n) 
    glVertex3f(*v1) 
    glVertex3f(*v2) 
    glVertex3f(*cima) 


    v1 = ( ancho, altura, -largo) 
    v2 = (-ancho, altura, -largo) 

    n = normal_tri(v1, v2, cima) 

    glNormal3f(*n) 
    glVertex3f(*v1) 
    glVertex3f(*v2) 
    glVertex3f(*cima) 

    v1 = (-ancho, altura, -largo) 
    v2 = (-ancho, altura,  largo) 

    n = normal_tri(v1, v2, cima) 

    glNormal3f(*n) 
    glVertex3f(*v1) 
    glVertex3f(*v2) 
    glVertex3f(*cima) 


    v1 = ( ancho, altura,  largo) 
    v2 = ( ancho, altura, -largo) 

    n = normal_tri(v1, v2, cima) 

    glNormal3f(*n) 
    glVertex3f(*v1) 
    glVertex3f(*v2) 
    glVertex3f(*cima) 

    glEnd() 
 

def draw_sphere( radius, color=(1, 1, 1)): # Dibuja una esfera usando GLU

    glColor3f(*color) 
    quad = gluNewQuadric() 
    gluQuadricNormals(quad, GLU_SMOOTH) # Normales suaves para iluminación
    gluSphere(quad, radius, 16, 16) # Dibujar la esfera
    gluDeleteQuadric(quad) 

 

def draw_line(p1, p2, color=(1, 1, 1), width=2.0): # Dibuja una línea entre dos puntos 3D


    glDisable(GL_LIGHTING) # Desactivar la iluminación para líneas sólidas
    glLineWidth(width) 
    glColor3f(*color) 
    glBegin(GL_LINES) 
    glVertex3f(*p1) 
    glVertex3f(*p2) 

    glEnd() 

    glEnable(GL_LIGHTING) 



def draw_cilindro(ang_in,ang_fin,radius,largo,color=(1,1,1)): # Dibuja un cilindro sin tapas

    glBegin(GL_TRIANGLE_STRIP) 

    for i in range(ang_in,ang_fin+1): 

        x1=math.cos(math.radians(i)) 
        y1=math.sin(math.radians(i)) 
        z1=largo  

        glColor3f(*color) 
        glNormal3f(x1, y1, 0) 
        glVertex3f(x1 * radius, y1 * radius, 0 ) 


        glColor3f(*color) 
        glNormal3f(x1, y1, 0) 
        glVertex3f((x1 * radius), (y1 * radius), (z1)) 


    glEnd() 

 

def draw_cilindro_tapado(ang_in, ang_fin, radius, largo, color=(1,1,1)): # Dibuja un cilindro con tapas

    glBegin(GL_TRIANGLE_STRIP) 

    for i in range(ang_in, ang_fin+1): 

        x1 = math.cos(math.radians(i)) 
        y1 = math.sin(math.radians(i)) 
        z1 = largo 

        glColor3f(*color) 
        glNormal3f(x1, y1, 0) 
        glVertex3f(x1 * radius, y1 * radius, 0) 

        glColor3f(*color) 
        glNormal3f(x1, y1, 0) 
        glVertex3f(x1 * radius, y1 * radius, z1) 

    glEnd() 

 

    glBegin(GL_TRIANGLE_FAN) 
    glColor3f(*color) 
    glNormal3f(0,0,-1) 
    glVertex3f(0,0,0) 

    for i in range(ang_in, ang_fin+1): # Dibujar la tapa inferior

        x1 = math.cos(math.radians(i)) * radius 
        y1 = math.sin(math.radians(i)) * radius 

        glVertex3f(x1, y1, 0) 

    x1 = math.cos(math.radians(ang_in)) * radius 
    y1 = math.sin(math.radians(ang_in)) * radius 

    glVertex3f(x1, y1, 0) 

    glEnd() 

 

    glBegin(GL_TRIANGLE_FAN) 
    glColor3f(*color) 
    glNormal3f(0,0,1) 
    glVertex3f(0,0,largo) 

    for i in range(ang_fin, ang_in-1, -1): # Dibujar la tapa superior

        x1 = math.cos(math.radians(i)) * radius 
        y1 = math.sin(math.radians(i)) * radius 

        glVertex3f(x1, y1, largo) 

    x1 = math.cos(math.radians(ang_fin)) * radius 
    y1 = math.sin(math.radians(ang_fin)) * radius 

    glVertex3f(x1, y1, largo) 

    glEnd() 

 


# Acomodo y algunas animaciones 

#Hermosa función para mover algo en circulo ------------------------------------------------------------------------

 

def mover_en_circulo(draw_funcion, radio, angulo_cambio, angulo, voltear, altura=0.0): # Mueve un objeto en un círculo

    theta = angulo_cambio + angulo # Ángulo actual en radianes

    x = radio * math.cos(theta) 
    z = radio * math.sin(theta) 

 

    glPushMatrix() 
    glTranslatef(x, altura, z) # Mover al punto en el círculo
    glRotatef(math.degrees(-theta) + voltear, 0, 1, 0) # Rotar para que mire hacia el centro del círculo

    draw_funcion() 

    glPopMatrix() # Restaurar la matriz anterior




#Función para moverse en línea, dar la vuelta y así ---------------------------------------------------------------------------------



def mover_en_linea_girando(draw_funcion, x,y,z,distancia, distancia_m, 

                            dir_mov,ang_vuelta,mov_es_x,mov_es_y,mov_es_z,rotar): # Mueve un objeto en línea y lo hace girar al llegar al final

     

    y_giro,xz_giro=0,0 

    distancia_x,distancia_y,distancia_z=0,0,0 

    if(mov_es_x): #Mover en X

        if((x+distancia_m)<=x+distancia and (x+distancia_m)>=x): #Dentro de los límites

            distancia_m+=dir_mov 

        else: 

            if(dir_mov>0): # Mover en dirección positiva

                if(ang_vuelta<180 and rotar): # Si no ha dado la vuelta completa

                    ang_vuelta+=20 # Girar

                else: 

                    dir_mov=-dir_mov # Cambiar dirección
                    distancia_m+=dir_mov # Seguir moviéndose

                     

            else: 

                if(ang_vuelta>0 and rotar): # Si no ha vuelto a la posición inicial

                    ang_vuelta-=20 # Girar de vuelta

                else: 

                    dir_mov=-dir_mov # Cambiar dirección
                    distancia_m+=dir_mov # Seguir moviéndose

       

        xz_giro=1 

        distancia_x=distancia_m 

    if(mov_es_y): # Mover en Y

         

        if((y+distancia_m)<=y+distancia and (y+distancia_m)>=y): # Dentro de los límites

            distancia_m+=dir_mov 

        else: 

            if(dir_mov>0): # Mover en dirección positiva

                if(ang_vuelta<180 and rotar): # Si no ha dado la vuelta completa

                    ang_vuelta+=20 # girar

                else: 

                    dir_mov=-dir_mov # Cambiar dirección
                    distancia_m+=dir_mov # Seguir moviéndose

                     

            else: 

                if(ang_vuelta>0 and rotar): # Si no ha vuelto a la posición inicial

                    ang_vuelta-=20 # Girar de vuelta

                else: 

                    dir_mov=-dir_mov # Cambiar dirección
                    distancia_m+=dir_mov # Seguir moviéndose

         

        y_giro=1 
        distancia_y=distancia_m 

         

    if(mov_es_z): # Mover en Z (mismas lógicas que en X y Y)

         

        if((z+distancia_m)<=z+distancia and (z+distancia_m)>=z): 

            distancia_m+=dir_mov 

        else: 

            if(dir_mov>0): 

                if(ang_vuelta<180 and rotar): 

                    ang_vuelta+=20 

                else: 

                    dir_mov=-dir_mov 
                    distancia_m+=dir_mov 

                     

            else: 

                if(ang_vuelta>0 and rotar): 

                    ang_vuelta-=20 

                else: 

                    dir_mov=-dir_mov 
                    distancia_m+=dir_mov 

         

        xz_giro=1 
        distancia_z=distancia_m 

         

    glPushMatrix() 
    glTranslatef(x+distancia_x, y+distancia_y, z+distancia_z)  # Mover al punto en la línea
    glRotatef(ang_vuelta, y_giro, xz_giro, 0) # Rotar para dar la vuelta
    draw_funcion() 
    glPopMatrix() 
     
    return distancia_m,dir_mov,ang_vuelta 




#Casas en circulo -----------------------------------------------------------------------------------------------------



def draw_houses_circulo(num_casas, radio): # Dibuja varias casas en un círculo

    for i in range(num_casas): # Iterar sobre el número de casas

        angulo = 2 * math.pi * i / num_casas 
        x = radio * math.cos(angulo) 
        z = radio * math.sin(angulo) 

        glPushMatrix() 
        glTranslatef(x, 0, z) 
        glRotatef(math.degrees(-angulo) + 270, 0, 1, 0) # Rotar para que mire hacia el centro del círculo
        draw_house((0.75,0.6,0),(0.6, 0.2, 0.2),(0.53, 0.81, 1),(0.6, 0.2, 0.2),0.0015) #Dibuja una casa
        glPopMatrix() 

         

def draw_arbustos_circulo(num_arbustos, radio): # Dibuja varios arbustos en un círculo con logica similar a las casas

    for i in range(num_arbustos): 

        angulo = 2 * math.pi * i / num_arbustos 
        x = radio * math.cos(angulo) 
        z = radio * math.sin(angulo) 

        glPushMatrix() 
        glTranslatef(x, 0, z) 
        glRotatef(math.degrees(-angulo) + 90, 0, 1, 0) 
        draw_arbusto_flores() 
        glPopMatrix() 

         

         

def draw_sol_luna(): # Dibuja el sol y la luna moviéndose en el cielo

    global angulo_dia,r,g,b,vuelta_dia 


    if (0 < angulo_dia < math.radians(70)): # Amanecer

        g = g+1/70 

        b = b+1/70 

    if(angulo_dia<=math.radians(70) and angulo_dia>=math.radians(110)): # Mediodía

        g=1 

        b=1 

    if(math.radians(110) < angulo_dia < math.radians(180)): # Atardecer

        g = g-1/70 

        b = b-1/70 

    if(math.radians(180) < angulo_dia < math.radians(360)): # Noche

        g = 0 

        b = 0 

     

    glPushMatrix() 

    glTranslate(-15,0,0) # Alejar del centro para que no choque con la cámara
    glRotate(90,1,0,0) # Rotar para que esté en el plano XZ

    mover_en_circulo(lambda: draw_sphere(4, (0.75, 0.75, 0.75)),39,angulo_dia,0,0,0) # Dibuja la luna
    mover_en_circulo(lambda: draw_sphere(10,(0.83, 0.69, 0.22)),39,angulo_dia,math.radians(180),0,0) # Dibuja el sol

    glPopMatrix() 

    angulo_dia+=0.02 # Velocidad del día

    if(angulo_dia>= math.radians(360)): # Reiniciar el ciclo del día

        angulo_dia=0 

         

     

# Animación nubes, van desde el punto más negativo 

def draw_nubes_moviendose(x,y,z,distancia_1,distancia_2): # Dibuja nubes moviéndose en el cielo

    global d_nubes1,d_nubes2 

    d_nubes1+=0.5 # Velocidad de las nubes
    d_nubes2+=0.5 

    x_1=x-distancia_1+d_nubes1 # Posición inicial de la nube 1
    x_2=x-distancia_1+d_nubes2 

    if(d_nubes1>=distancia_1*2): # Reiniciar la posición de la nube 1

        d_nubes1=0 

    if(d_nubes2>=distancia_1*2): 

        d_nubes2=0 



    i=0 

    while i < distancia_1: # Iterar sobre la distancia para dibujar nubes

        count_nube=0 

        if( distancia_1 <=d_nubes1+i<=distancia_1*2): # Condición para dibujar la nube 1

            for mov_z in range(0, int(distancia_2), 10): # Mover en Z para dar profundidad a las nubes

                count_nube+=1 
                incremento=0 #Incremento random porque ya funciona y no le quiero mover así que solo le voy a mover aquí, ahora que sé que solo hace 3 nubes 

                if(count_nube==2): # Para que no se vean tan alineadas

                    incremento=10 

                glPushMatrix() 
                glTranslate(x_1 +i+incremento, y, z + mov_z) 
                draw_nube((0.7,0.7,0.7)) 
                glPopMatrix() 

                 
        count_nube=0 

        if(distancia_1 <= d_nubes2+i<=distancia_1*2): # Condición para dibujar la nube 2

            for mov_z in range(0, int(distancia_2), 10): 

                count_nube+=1 
                incremento=0 #Incremento random porque ya funciona y no le quiero mover así que solo le voy a mover aquí, ahora que sé que solo hace 3 nubes 

                if(count_nube==2): 

                    incremento=10 

                glPushMatrix() 
                glTranslate(x_2+incremento + i, y, z + mov_z) 
                draw_nube((0.7,0.7,0.7)) 
                glPopMatrix() 

         

        i+=20 

         

#La misma función para mover nubes pero esa no la podemos usar  para el humo porque se ve raro

def draw_humo_moviendose(x,y,z,distancia_1,distancia_2): 

    global d_humo1,d_humo2 

    d_humo1+=0.5 
    d_humo2+=0.5 

    x_1=x-distancia_1+d_humo1 
    x_2=x-distancia_1+d_humo2 

    if(d_humo1>=distancia_1*2): 

        d_humo1=0 

    if(d_humo2>=distancia_1*2): 

        d_humo2=0 

       

    i=0 

    while i < distancia_1: 

        count_nube=0 

        if( distancia_1 <=d_humo1+i<=distancia_1*2): 

            for mov_z in range(0, int(distancia_2), 10): 

                count_nube+=1 

                incremento=0 #Incremento random porque ya funciona y no le quiero mover así que solo le voy a mover aquí, ahora que sé que solo hace 3 nubes 

                if(count_nube==2): 

                    incremento=10 

                glPushMatrix() 

                glTranslate(x_1 +i+incremento, y, z + mov_z) 


                draw_nube( (0.25, 0.25, 0.25)) 

                glPopMatrix() 
 

        count_nube=0 

        if(distancia_1 <= d_humo2+i<=distancia_1*2): 

            for mov_z in range(0, int(distancia_2), 10): 

                count_nube+=1 

                incremento=0 #Incremento random porque ya funciona y no le quiero mover así que solo le voy a mover aquí, ahora que sé que solo hace 3 nubes 

                if(count_nube==2): 

                    incremento=10 

                glPushMatrix() 

                glTranslate(x_2+incremento + i, y, z + mov_z) 

                draw_nube( (0.25, 0.25, 0.25)) 

                glPopMatrix() 

         

        i+=20 

         

 

def draw_tipos_jugando(colorp1,colorp2,color_pelota): # Dibuja dos personas pateando una pelota

    global ang_patear1,pat1,ang_patear2,pat2,mov_pelota,dir_pelota 

    #0.4,2.96 

    ang_patear1+=pat1 
    ang_patear2+=pat2 

    # Lógica para patear la pelota

    if(mov_pelota<0.6 and dir_pelota<=0): 

        pat1=40 

    if(ang_patear1>=80): 

        pat1=-40 

    if(ang_patear1<=0 and pat1<0): 

        pat1=0 
      

    if(mov_pelota>1.3 and dir_pelota>0): 

        pat2=40 

    if(ang_patear2>=80): 

        pat2=-40 

    if(ang_patear2<=0 and pat2<0): 

        pat2=0 


    mov_pelota+=dir_pelota 

     

    if(ang_patear1>=80): 

        dir_pelota=0.15  

         

    if(ang_patear2>=80): 

        dir_pelota=-0.15   

     
    glPushMatrix() 
    glRotate(180,0,1,0) 
    draw_persona((colorp1),0,0,0,ang_patear1) 
    glPopMatrix()     
 

    glPushMatrix() 
    glTranslate(0,0.1,0.4+mov_pelota) 
    draw_sphere(0.2,color_pelota) 
    glPopMatrix() 


    glPushMatrix() 
    glTranslate(0,0,3) 
    draw_persona((colorp2),0,0,0,ang_patear2) 
    glPopMatrix() 

     

# Funciones de figuras -------------------------------------------------------------------------------------

#Calles -----------------------------------------------------------------------------------------------------
def draw_calles(): 

    #Vereda/Base_mundo 

    draw_rectangulo(15,15,(0.4,0.4,0.4)) 

    #Primer anillo (fuente) #Va al último porque en el medio pruebo lo que voy haciendo 

    draw_elipse(2,2,0,0,360,0.001,(1,1,1)) 

    #Segundo anillo (arbustos y flores) para poner a las abejas 

    draw_elipse(4,4,2,2,360,0.001,(0,1,0.5)) 

    #Tercer anillo (Personas/Animales)   

    draw_elipse(6,6,4,4,360,0.001,(0.4,0.4,0.4)) 

    #Cuarto anillo (autos y así) 

    draw_elipse(8,8,6,6,360,0.001,(0,0,0)) 

    #Quinto anillo (Personas y así) 

    draw_elipse(10,10,8,8,360,0.001,(0.4,0.4,0.4)) 

    #Sexto anillo (Casas y edificios, en frente de la fuente hay un edificio con un reloj) 

    draw_elipse(15,15,10,10,360,0.001,(0,1,0.5)) 

     

    #Playa 

    glPushMatrix() 
    glTranslatef(-20,-5,0) 
    # dibujar el rectángulo de la playa
    draw_cube(5,10,30,(0.52, 0.48, 0.35),(0.52, 0.48, 0.35),(0.52, 0.48, 0.35)) 
    glPopMatrix() 

     

    #Mar 

    glPushMatrix() 
    glTranslatef(-32.501,-5,0) 
    draw_cube(5,15,30,(0.0, 0.4, 0.7),(0.0, 0.4, 0.7),(0.0, 0.4, 0.7)) 
    glPopMatrix() 

     

#Arbusto Flores -----------------------------------------------------------------------------------------------------  

def draw_arbusto_flores(): 

    #Arbusto 
    glPushMatrix() 
    glTranslate(0,0.2,0) 
    draw_sphere(0.5,((0.1, 0.4, 0.1))) 
    glPopMatrix() 

    #Flor1 
    glPushMatrix() 
    glTranslate(0,0.7,0) 
    draw_sphere(0.05,((0.35, 0.1, 0.45))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,-0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix()  

    glPushMatrix() 
    glTranslate(0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 

    glPopMatrix() 

    #Flor2 
    glPushMatrix() 
    glTranslate(0,0.2,0) 
    glRotate(90,1,0,0) 
    glTranslate(0,-0.2,0) 

    glPushMatrix() 
    glTranslate(0,0.7,0) 
    draw_sphere(0.05,((0.35, 0.1, 0.45))) 
    glPopMatrix()   

    glPushMatrix() 
    glTranslate(0,0.7,0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,-0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix()    

    glPushMatrix() 
    glTranslate(0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPopMatrix() 
   
        #Flor3 

    glPushMatrix() 
    glTranslate(0,0.2,0) 
    glRotate(45,1,0,1) 
    glTranslate(0,-0.2,0) 

    glPushMatrix() 
    glTranslate(0,0.7,0) 
    draw_sphere(0.05,((0.35, 0.1, 0.45))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,-0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPopMatrix() 
   

    #Flor4 
    glPushMatrix() 
    glTranslate(0,0.2,0) 
    glRotate(-45,1,0,1) 
    glTranslate(0,-0.2,0) 

    glPushMatrix() 
    glTranslate(0,0.7,0) 
    draw_sphere(0.05,((0.35, 0.1, 0.45))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,-0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPopMatrix() 

        #Flor5 

    glPushMatrix() 
    glTranslate(0,0.2,0) 
    glRotate(90,1,0,1) 
    glTranslate(0,-0.2,0) 

    glPushMatrix() 
    glTranslate(0,0.7,0) 
    draw_sphere(0.05,((0.35, 0.1, 0.45))) 
    glPopMatrix()   

    glPushMatrix() 
    glTranslate(0,0.7,0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,-0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPopMatrix() 

    glPushMatrix() 
    glRotate(90,0,1,0) 

    #Flor2 

    glPushMatrix() 
    glTranslate(0,0.2,0) 
    glRotate(90,1,0,0) 
    glTranslate(0,-0.2,0)   

    glPushMatrix() 
    glTranslate(0,0.7,0) 
    draw_sphere(0.05,((0.35, 0.1, 0.45))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,-0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix()  

    glPushMatrix() 
    glTranslate(0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPopMatrix() 


        #Flor3 

    glPushMatrix() 
    glTranslate(0,0.2,0) 
    glRotate(45,1,0,1) 
    glTranslate(0,-0.2,0)  

    glPushMatrix() 
    glTranslate(0,0.7,0) 
    draw_sphere(0.05,((0.35, 0.1, 0.45))) 
    glPopMatrix()  

    glPushMatrix() 
    glTranslate(0,0.7,0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,-0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix()    

    glPushMatrix() 
    glTranslate(-0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPopMatrix() 

    #Flor4 
    glPushMatrix() 
    glTranslate(0,0.2,0) 
    glRotate(-45,1,0,1) 
    glTranslate(0,-0.2,0) 

    glPushMatrix() 
    glTranslate(0,0.7,0) 
    draw_sphere(0.05,((0.35, 0.1, 0.45))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,-0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 
     
    glPushMatrix() 
    glTranslate(0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPopMatrix() 

        #Flor5 
    glPushMatrix() 
    glTranslate(0,0.2,0) 
    glRotate(90,1,0,1) 
    glTranslate(0,-0.2,0) 

    glPushMatrix() 
    glTranslate(0,0.7,0) 
    draw_sphere(0.05,((0.35, 0.1, 0.45))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,-0.05) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.05,0.7,0) 
    draw_sphere(0.05,((1,1,1))) 
    glPopMatrix() 

    glPopMatrix() 
    glPopMatrix() 


#Casa -----------------------------------------------------------------------------------------------------

def draw_house(color1,color2,color3,color4,capa): # Dibujar casa (base + techo)

    glPushMatrix() 
    glTranslate(0,capa,0) 
    draw_cube(2,2,2,color1,color2,color3)  # Base de la casa 
    draw_piramide(2,2,2,2,color4)  # Techo 
  
    #Ventanas abiertas 
    glPushMatrix() 
    glTranslate(-0.5,1.5,1.001) # Posición de la ventana
    glRotate(90,1,0,0) 
    draw_rectangulo(0.25,0.25,(0,0,0)) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.5,1.5,1.001) 
    glRotate(90,1,0,0) 
    draw_rectangulo(0.25,0.25,(0,0,0)) 
    glPopMatrix() 

    #Ventanas cerradas 
    glPushMatrix() 
    glTranslate(-0.5,1.5,1.002) 
    glRotate(90,1,0,0) 
    draw_rectangulo(0.25,0.25,(0,0.75,0.75)) # simula el vidrio
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.5,1.5,1.002) 
    glRotate(90,1,0,0) 
    draw_rectangulo(0.25,0.25,(0,0.75,0.75)) 
    glPopMatrix() # restaurar 

    #Puerta abierta 
    glPushMatrix() 
    glTranslate(0,0.5,1.001) 
    glRotate(90,1,0,0) 
    draw_rectangulo(0.25,0.5,(0,0, 0)) 
    glPopMatrix() 

    #Puerta cerrada 
    glPushMatrix() 
    glTranslate(0,0.5,1.002) 
    glRotate(90,1,0,0) 
    draw_rectangulo(0.25,0.5,(0.6, 0.2, 0.2)) 
    glPopMatrix() 

    glPopMatrix() 

     

def draw_edificio_principal(): 

    pass 

     
# Autos -----------------------------------------------------------------------------------------------------
def draw_auto(color): 

    glPushMatrix() 
    glTranslate(0,0.001,0) 

    #Carcaza 
    glPushMatrix() 
    glTranslate(0,0.4,0) 
    draw_cube(0.3,1.2,0.6,color,color,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.7,0) 
    draw_cube(0.2,0.8,0.4,color,color,color) 
    glPopMatrix() 

    #Llantas 
    glPushMatrix() 
    glTranslate(0.3,0.2,-0.2) 
    draw_cilindro_tapado(0,360,0.2,0.1,(0.15,0.15,0.15)) # Llanta delantera derecha
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.3,0.2,0.2) 
    draw_cilindro_tapado(0,360,0.2,0.1,(0.15,0.15,0.15)) # Llanta trasera derecha
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.3,0.2,-0.2) 
    draw_cilindro_tapado(0,360,0.2,0.1,(0.15,0.15,0.15)) # Llanta delantera izquierda
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.3,0.2,0.2) 
    draw_cilindro_tapado(0,360,0.2,0.1,(0.15,0.15,0.15)) # Llanta trasera izquierda
    glPopMatrix() 

    #Luces 
    glPushMatrix() 
    glTranslate(-0.6,0.6,-0.2)  # Posición de la luz
    draw_sphere(0.05,(1,1,0)) # Dibuja la luz
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.6,0.6,0.2) 
    draw_sphere(0.05,(1,1,0)) 
    glPopMatrix() 
     
    glPopMatrix() 

     

# Funcion de dibujar camion -----------------------------------------------------------------------------------------------------     

def draw_camion(color): 

    glPushMatrix() 
    glTranslate(0,0.001,0) 

    #Carcaza
    glPushMatrix() 
    glTranslate(0,0.5,0) 
    draw_cube(0.7,2,0.7,color,color,color) 
    glPopMatrix() 

    #Llantas 
    glPushMatrix() 
    glTranslate(0.8,0.25,-0.4) 
    draw_cilindro_tapado(0,360,0.25,0.1,(0.15,0.15,0.15)) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.8,0.25,0.2) 
    draw_cilindro_tapado(0,360,0.25,0.1,(0.15,0.15,0.15)) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.8,0.25,-0.4) 
    draw_cilindro_tapado(0,360,0.25,0.1,(0.15,0.15,0.15)) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.8,0.25,0.2) 
    draw_cilindro_tapado(0,360,0.25,0.1,(0.15,0.15,0.15)) 
    glPopMatrix() 

    #Luces 
    glPushMatrix() 
    glTranslate(-1,0.7,-0.2) 
    draw_sphere(0.05,(1,1,0)) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-1,0.7,0.2) 
    draw_sphere(0.05,(1,1,0)) 
    glPopMatrix() 

    glPopMatrix() 


# Funcion de dibujar moto -----------------------------------------------------------------------------------------------------     

def draw_moto(color): 

    glPushMatrix() 
    glTranslate(0,0.001,0) 

    #Carcaza 
    glPushMatrix() 
    glTranslate(0,0.3,0) 
    draw_cube(0.2,1,0.3,color,color,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.4,0.5,0) 
    draw_cube(0.35,0.4,0.3,color,color,color) 
    glPopMatrix() 

    #Llantas 
    glPushMatrix() 
    glTranslate(0.3,0.2,-0.1) 
    draw_cilindro_tapado(0,360,0.15,0.1,(0.15,0.15,0.15)) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.3,0.2,0.1) 
    draw_cilindro_tapado(0,360,0.15,0.1,(0.15,0.15,0.15)) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.3,0.2,-0.1) 
    draw_cilindro_tapado(0,360,0.15,0.1,(0.15,0.15,0.15)) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.3,0.2,0.1) 
    draw_cilindro_tapado(0,360,0.15,0.1,(0.15,0.15,0.15)) 
    glPopMatrix() 

    #Luz 
    glPushMatrix() 
    glTranslate(-0.6,0.65,0) 
    draw_sphere(0.1,(0.0, 1.0, 1.0)) 
    glPopMatrix() 

    glPopMatrix() 

 
# Persona -----------------------------------------------------------------------------------------------------

def draw_persona(color,ang_b_iz, ang_b_d, ang_p_iz, ang_p_d): 

    #Cabeza 
    glPushMatrix() 
    glTranslate(0,0.7,0) 
    draw_sphere(0.15,color) 
    glPopMatrix() 

    #Torso 
    glPushMatrix() 
    glTranslate(0,0.3,0) 
    glRotatef(270,1,0,0) 
    draw_cilindro_tapado(0,360,0.06,0.4,color) 
    glPopMatrix() 

    #Pierna derecha, Brazo izquierdo 
    glPushMatrix() 
    glTranslate(0.06,0.3,0) 
    glRotatef(90,1,0,0) 
    glRotatef(ang_p_d,1,0,0) 
    draw_cilindro_tapado(0,360,0.06,0.3,color) # Pierna derecha
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.12,0.6,0) 
    glRotatef(90,1,0,0) 
    glRotatef(ang_b_iz,1,0,0) 
    draw_cilindro_tapado(0,360,0.06,0.3,color) # Brazo izquierdo
    glPopMatrix() 

    #Pierna izquierda, Brazo derecho 
    glPushMatrix() 
    glTranslate(-0.06,0.3,0) 
    glRotatef(90,1,0,0) 
    glRotatef(ang_p_iz,1,0,0) 
    draw_cilindro_tapado(0,360,0.06,0.3,color) # Pierna izquierda
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.12,0.6,0) 
    glRotatef(90,1,0,0) 
    glRotatef(ang_b_d,1,0,0) 
    draw_cilindro_tapado(0,360,0.06,0.3,color) # Brazo derecho
    glPopMatrix() 

 
# Funcion de dibujar persona caminando -----------------------------------------------------------------------------------------------------

def draw_persona_caminando(color): 

    global ang_mov_persona, dir_persona 

    ang_mov_persona += dir_persona # Incrementa el ángulo de movimiento de la persona

    if ang_mov_persona >= 50: # Si el ángulo alcanza 50 grados, cambia la dirección

        dir_persona = -10 


    if ang_mov_persona <= -50: # Si el ángulo alcanza -50 grados, cambia la dirección

        dir_persona = 10 

         
    #Cabeza 
    glPushMatrix() 
    glTranslate(0,0.7,0) 
    draw_sphere(0.15,color) 
    glPopMatrix() 

    #Torso 
    glPushMatrix() 
    glTranslate(0,0.3,0) 
    glRotatef(270,1,0,0) 
    draw_cilindro_tapado(0,360,0.06,0.4,color) 
    glPopMatrix() 

    #Pierna derecha, Brazo izquierdo 
    glPushMatrix() 
    glTranslate(0.06,0.3,0) 
    glRotatef(90,1,0,0) 
    glRotatef(-ang_mov_persona,1,0,0) 
    draw_cilindro_tapado(0,360,0.06,0.3,color) 
    glPopMatrix() 
     
    glPushMatrix() 
    glTranslate(-0.12,0.6,0) 
    glRotatef(90,1,0,0) 
    glRotatef(-ang_mov_persona,1,0,0) 
    draw_cilindro_tapado(0,360,0.06,0.3,color) 
    glPopMatrix() 

    #Pierna izquierda, Brazo derecho 
    glPushMatrix() 
    glTranslate(-0.06,0.3,0) 
    glRotatef(90,1,0,0) 
    glRotatef(ang_mov_persona,1,0,0) 
    draw_cilindro_tapado(0,360,0.06,0.3,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.12,0.6,0) 
    glRotatef(90,1,0,0) 
    glRotatef(ang_mov_persona,1,0,0) 
    draw_cilindro_tapado(0,360,0.06,0.3,color) 
    glPopMatrix() 

     

# Funcion de dibujar perro caminando -------------------------------------------------------------------------------------------

def draw_perro_caminando(color): 

    global ang_mov_perro, dir_perro 

    ang_mov_perro += dir_perro # Incrementa el ángulo de movimiento del perro

    if ang_mov_perro >= 60: # Si el ángulo alcanza 60 grados, cambia la dirección

        dir_perro = -12 

    if ang_mov_perro <= -60: # Si el ángulo alcanza -60 grados, cambia la dirección

        dir_perro = 12    

    #Cabeza 
    glPushMatrix() 
    glTranslate(0,0.21,0.3) 
    draw_sphere(0.08,color) 
    glPopMatrix() 

    #Orejas 
    glPushMatrix() 
    glTranslate(-0.02,0.27,0.3) 
    draw_piramide(0.021,0.2,0.05,0,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.02,0.27,0.3) 
    draw_piramide(0.021,0.2,0.05,0,color) 
    glPopMatrix() 

    #Torso 
    glPushMatrix() 
    glTranslate(0,0.15,0) 
    draw_cilindro_tapado(0,360,0.06,0.3,color) 
    glPopMatrix() 

    #Patita derecha adelante, patita izquierda detrás 
    glPushMatrix() 
    glTranslate(0.06,0.15,0) 
    glRotatef(90,1,0,0) 
    glRotatef(-ang_mov_perro,1,0,0) 
    draw_cilindro_tapado(0,360,0.03,0.15,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-0.06,0.15,0.3) 
    glRotatef(90,1,0,0) 
    glRotatef(-ang_mov_perro,1,0,0) 
    draw_cilindro_tapado(0,360,0.03,0.15,color) 
    glPopMatrix() 

    #Patita izquierda adelante, patita derecha detrás 
    glPushMatrix() 
    glTranslate(- 0.06,0.15,0) 
    glRotatef(90,1,0,0) 
    glRotatef(ang_mov_perro,1,0,0) 
    draw_cilindro_tapado(0,360,0.03,0.15,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0.06,0.15,0.3) 
    glRotatef(90,1,0,0) 
    glRotatef(ang_mov_perro,1,0,0) 
    draw_cilindro_tapado(0,360,0.03,0.15,color) 
    glPopMatrix() 



# Funcion de dibujar pelicano -----------------------------------------------------------------------------------------------------

def draw_pelicano(color): 

    global ang_mov_peli_mari,dir_peli_mari 

    ang_mov_peli_mari += dir_peli_mari 

    if ang_mov_peli_mari >= 30: # Si el ángulo alcanza 30 grados, cambia la dirección

        dir_peli_mari = -10 


    if ang_mov_peli_mari <= -30: # Si el ángulo alcanza -30 grados, cambia la dirección

        dir_peli_mari = 10 

         

    ang=ang_mov_peli_mari # Ángulo de movimiento del pelícano

    glPushMatrix() 
    glRotate(90,0,1,0) # Rotar para orientar el pelícano correctamente

    #Cabeza 
    glPushMatrix() 
    glTranslate(0,0.43,0) 
    draw_sphere(0.06,color) 
    glPopMatrix() 

    #Pico 
    glPushMatrix() 
    glTranslate(0,0.43,0.05) 
    glRotatef(110,1,0,0) 
    draw_piramide(0.15,0.05,0.05,0,(1.0, 0.5, 0.0)) 
    glPopMatrix() 

    #Cuello 
    glPushMatrix() 
    glTranslate(0,0.43,0) 
    glRotatef(140,1,0,0) 
    draw_cilindro_tapado(0,360,0.04,0.25,color) 
    glPopMatrix() 

    #Cuerpo 
    glPushMatrix() 
    glTranslate(0,0.17,-0.25) 
    draw_sphere(0.12,color) 
    glPopMatrix() 

    #Alas 
    glPushMatrix() 
    glTranslate(0,0.15,-0.25) 
    glRotatef(ang,0,0,1) # Rotar ala derecha
    glTranslate(0.17,0,0) 
    draw_cube(0.05,0.3,0.2,color,color,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.17,-0.25) 
    glRotatef(180-ang,0,0,1) 
    glRotatef(180,0,1,0) # Rotar ala izquierda
    glTranslate(-0.15,0,0) 
    draw_cube(0.05,0.3,0.2,color,color,color) 
    glPopMatrix() 

    glPopMatrix() 

     
# Funcion de dibujar pollo -----------------------------------------------------------------------------------------------------

def draw_pollo(color): 

    global ang_mov_pollo_pez,dir_pol_pez 

    ang_mov_pollo_pez += dir_pol_pez 

    if ang_mov_pollo_pez >= 30: # Si el ángulo alcanza 30 grados, cambia la dirección

        dir_pol_pez = -10 


    if ang_mov_pollo_pez <= -30: # Si el ángulo alcanza -30 grados, cambia la dirección

        dir_pol_pez = 10 

         

    ang=ang_mov_pollo_pez # Ángulo de movimiento del pollo 


    glPushMatrix() 
    glRotate(90,0,1,0) 
    glScaled(0.75,0.75,0.75) 

    #Cuerpo 
    glPushMatrix() 
    glTranslate(0,0.17,-0.25) 
    draw_sphere(0.12,color) 
    glPopMatrix() 

    #Alas 
    glPushMatrix() 
    glTranslate(0,0.15,-0.25) 
    glRotatef(ang,0,0,1) 
    glTranslate(0.17,0,0) 
    draw_cube(0.05,0.2,0.2,color,color,color) 
    glPopMatrix() 

    # Alas izquierda
    glPushMatrix() 
    glTranslate(0,0.17,-0.25) 
    glRotatef(180-ang,0,0,1) 
    glRotatef(180,0,1,0) 
    glTranslate(-0.15,0,0) 
    draw_cube(0.05,0.2,0.2,color,color,color) 
    glPopMatrix() 

    #pico  
    glPushMatrix() 
    glTranslate(0,0.15,0) 
    glRotatef(0,0,0,1) 
    glTranslate(0,0,-0.16) 
    draw_cube(0.05,0.2,0.1, (1.0, 0.5, 0.0), (1.0, 0.5, 0.0), (1.0, 0.5, 0.0)) 
    glPopMatrix() 

    glPopMatrix() 

 
# Funcion de dibujar caracol -----------------------------------------------------------------------------------------------------

def draw_caracol(color1,color2): 

    #cuerpo 
    glPushMatrix() 
    glTranslatef(0,0.07,0) 
    draw_cilindro_tapado(0,360,0.07,0.2,color2) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslatef(0,0.07,0.13) 
    glRotatef(-45,1,0,0) 
    draw_cilindro_tapado(0,360,0.07,0.2,color2) 
    glPopMatrix() 

    #Ojos 
    glPushMatrix() 
    glTranslatef(-0.03,0.15,0.24) 
    glRotatef(270,1,0,0) 
    draw_cilindro_tapado(0,360,0.02,0.2,color2) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslatef(0.03,0.15,0.24) 
    glRotatef(270,1,0,0) 
    draw_cilindro_tapado(0,360,0.02,0.2,color2) 
    glPopMatrix() 

    #Caparazón 
    glPushMatrix() 
    glTranslatef(0,0.11,0.05) 
    draw_sphere(0.1,color1) 
    glPopMatrix() 

     
# Funcion de dibujar abeja -----------------------------------------------------------------------------------------------------
     

def draw_bee(): 

    global mov_abeja,dir_abeja 

    mov_abeja+=dir_abeja 

    if(mov_abeja<=0): # Si el movimiento alcanza 0, cambia la dirección

        dir_abeja=0.05 


    if(mov_abeja>=2): # Si el movimiento alcanza 2, cambia la dirección

        dir_abeja=-0.05 

         

    glPushMatrix() 
    glTranslatef(0,mov_abeja,0) 
    glRotate(270,0,1,0) 
    glPushMatrix() 
    glScaled(0.1,0.1,0.1) 
    glTranslatef(0,10,0) 

    #Cuerpo amarillo 
    glPushMatrix() 
    glTranslatef(0.56, 0, 0) 
    draw_sphere(1,(1,1,0)) 
    glPopMatrix() 

    #Ojo negro 
    glPushMatrix() 
    glTranslatef(1.3, 0.4, -0.5) 
    draw_sphere(0.2, (0,0,0)) 
    glPopMatrix() 

    #Ojo negro 
    glPushMatrix() 
    glTranslatef(1.3, 0.4, 0.5) 
    draw_sphere(0.2, (0,0,0)) 
    glPopMatrix() 

    #Línea negra 
    glPushMatrix() 
    glRotate(180,1,0,1) 
    glTranslatef(0, 0, 0) 
    draw_cilindro(0,360,1.001,1,(0,0,0)) 
    glPopMatrix() 

    #sonrisa 
    glColor3f(0, 0, 0)  # negro 
    glPushMatrix() 
    glRotate(180,1,0,1) 
    glTranslatef(0, 0, 0.7) 
    draw_cilindro(0,180,0.8,0.5,(0,0,0)) 
    glColor3f(0.2, 0.2, 0.9)  # Blanco 
    glPopMatrix() 

    #alita 
    glColor3f(1, 1, 1)  # blanco 
    glPushMatrix() 
    glTranslatef(0.3, 0, 0.5) 
    glRotate(45,1,1,1) 
    glTranslatef(0.3, 0.6, -0.5) 
    draw_cilindro(0,360,0.7,0.7,(1,1,1)) 
    glColor3f(0.2, 0.2, 0.9)  # Blanco 
    glPopMatrix() 

    #alita 
    glColor3f(1, 1, 1)  # blanco 
    glPushMatrix() 
    glRotate(45,0,0,1) 
    glRotate(165,1,1,0) 
    #glRotate(45,0,1,1) 
    glTranslatef(0.3, 0.6, -0.3) 
    draw_cilindro(0,360,0.7,0.7,(1,1,1)) 
    glColor3f(0.2, 0.2, 0.9)  # Blanco 
    glPopMatrix() 

    glPopMatrix() 
    glPopMatrix() 

 

 
# Funcion de dibujar pez -----------------------------------------------------------------------------------------------------
     

def draw_pez(color): 

    glPushMatrix() 
    glRotate(180,0,1,0) 
    glPushMatrix() 
    glTranslate(0,0.1,0) 
    draw_sphere(0.1,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0.12,0) 
    glRotate(ang_mov_peli_mari,0,1,0) 
    glTranslate(0,0,0.2) 
    glRotate(-90,1,0,0) 
    draw_piramide(0.1,0.05,0.2,0,color) 
    glPopMatrix() 
    glPopMatrix() 

 
# Funcion de dibujar barquito -----------------------------------------------------------------------------------------------------


def draw_barquito(color,color2): 

    glPushMatrix() 
    glRotate(90,0,1,0) 
    glPushMatrix() 
    glTranslate(0,0.5,0) 
    draw_cilindro_tapado(180,360,0.5,0.5,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,0,0.2) 
    glRotate(90,0,1,0) 
    draw_persona(color2,0,0,0,0) 
    glPopMatrix() 

    glPopMatrix() 

     

# Funcion de dibujar nube -----------------------------------------------------------------------------------------------------

def draw_nube(color): 

    #4 , 2.5,  4 es el tamaño aproximado de la nube
    #Parte de en medio 

    glPushMatrix() 
    glTranslate(0,1,-0.5) 
    draw_sphere(1,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,1,0.5) 
    draw_sphere(1,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(0,2,0) 
    draw_sphere(1,color) 
    glPopMatrix() 

    #Parte derecha 
    glPushMatrix() 
    glTranslate(-1,1,-0.5) 
    draw_sphere(1,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-1,1,0.5) 
    draw_sphere(1,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-1,2,0) 
    draw_sphere(1,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-2,1,0) 
    draw_sphere(1,color) 
    glPopMatrix() 

    #Parte izquierda 
    glPushMatrix() 
    glTranslate(1,1,-0.5) 
    draw_sphere(1,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(1,1,0.5) 
    draw_sphere(1,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(1,2,0) 
    draw_sphere(1,color) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(2,1,0) 
    draw_sphere(1,color) 
    glPopMatrix() 

 


#Edificio y reloj -------------------------------------------------------------------------------------------------------------

def draw_reloj_animado(): 


   t = glfw.get_time() # Tiempo para animar las manecillas 

   # Disco del reloj 

   glColor3f(0.9, 0.9, 0.9) 

   quad = gluNewQuadric() 

   gluDisk(quad, 0, 0.8, 32, 1) 

   # Manecilla Horas 

   glPushMatrix() 

   glRotatef(-t * 20, 0, 0, 1) 

   glLineWidth(4) 

   glBegin(GL_LINES) 

   glColor3f(0, 0, 0) 

   glVertex3f(0, 0, 0.01); glVertex3f(0, 0.4, 0.01) 

   glEnd() 

   glPopMatrix() 

   # Manecilla Minutos mas rapida 

   glPushMatrix() 

   glRotatef(-t * 150, 0, 0, 1) 

   glLineWidth(2) 

   glBegin(GL_LINES) 

   glColor3f(0.2, 0.2, 0.2) 

   glVertex3f(0, 0, 0.02); glVertex3f(0, 0.6, 0.02) 

   glEnd() 

   glPopMatrix() 

    

def draw_edificio_reloj(): 

   # Cuerpo principal del edificio 

   draw_cube(10, 4, 4, (0.4, 0.4, 0.45),(0.4, 0.4, 0.45),(0.4, 0.4, 0.45)) # Gris azulado 

   # Ventanas 

   glColor3f(0.7, 0.9, 1.0) 

   for fila in range(1, 4): 

       for col in [-1, 1]: 

           glPushMatrix() 

           glTranslatef(col * 0.8, fila * 2, 2.01) # Frente

           draw_cube(1, 0.8, 0.01, (0.7, 0.9, 1.0),(0.4, 0.4, 0.45),(0.4, 0.4, 0.45)) 

           glPopMatrix() 

   # Sección superior para el reloj 

   glPushMatrix() 

   glTranslatef(0, 10, 0) 

   draw_cube(2.5, 3, 3, (0.3, 0.3, 0.35),(0.4, 0.4, 0.45),(0.4, 0.4, 0.45)) 

   # Colocar reloj en la cara frontal del edificio 

   glTranslatef(0, 1.25, 1.51) 

   draw_reloj_animado() 

   glPopMatrix() 

    

# Bandera ondeando -----------------------------------------------------------------------------------------------------

def draw_bandera(): 

   t = glfw.get_time() # Tiempo para animar la bandera 

   # Palito o hasta? 

   glPushMatrix() 

   glRotatef(-90, 1, 0, 0) 

   glColor3f(0.6, 0.6, 0.6) 

   quad = gluNewQuadric() 

   gluCylinder(quad, 0.1, 0.1, 8, 16, 1) 

   glPopMatrix() 

   # Tela de la bandera con ondas 

   glPushMatrix() 

   glTranslatef(0, 7.5, 0) 

   num_seg = 15 

   ancho_seg = 2.5 / num_seg # Ancho de cada segmento

   glBegin(GL_QUAD_STRIP) 

   for i in range(num_seg + 1): 

       x = i * ancho_seg 

       z_onda = math.sin(t * 5 + x * 3) * 0.2 # Crea el efecto de onda 

       # Color: azul con franja blanca porque es un pais ficticio sjjsjs 

       if i < 7: glColor3f(0.0, 0.2, 0.6) 

       else: glColor3f(0.1, 0.4, 0.9) 

       glVertex3f(x, 0, z_onda) 

       glVertex3f(x, -1.5, z_onda) 

   glEnd() 

   glPopMatrix() 

 

 # Funcion de dibujar antena -----------------------------------------------------------------------------------------------------

def draw_antena(color,angulo_antena): 

    if(angulo_antena==360): # Reiniciar el ángulo después de una rotación completa

        angulo_antena=0 

     

    angulo_antena+=10 

     # Dibujar antena

    glPushMatrix() 

    glTranslatef(0,0.8,0) 

    glRotate(angulo_antena,0,1,0) 

    glRotate(45,0,0,1) 

     #Cuerpo de la antena

    glPushMatrix() 

    glTranslate(0,0.7,0) 

    glRotate(180,0,0,1) 

    draw_piramide(0.7,0.6,0.6,0,color) 

    glPopMatrix() 

     #Parte superior de la antena

    glPushMatrix() 

    glRotate(270,1,0,0) 

    draw_cilindro_tapado(0,360,0.07,0.8,color) 

    glPopMatrix() 

     #Esfera superior de la antena

    glPopMatrix() 

    glPushMatrix() 

    glRotate(270,1,0,0) 

    draw_cilindro_tapado(0,360,0.09,0.8,color) 

    glPopMatrix() 

     

    return angulo_antena 

 
# Funcion de dibujar ola animada -----------------------------------------------------------------------------------------------------
 
def draw_ola(): 

    global ola_tamano,dir_ola 

    ola_tamano+=dir_ola 

    if(ola_tamano<=0): # Si el tamaño alcanza 0, cambia la dirección

        dir_ola=0.05 

    if(ola_tamano>=1.6): # Si el tamaño alcanza 1.6, cambia la dirección

        dir_ola=-0.05 

     
    #Ola azul
    glPushMatrix() 

    glTranslatef(-25.0002,0.0002,0) # Posición del ola 

    draw_rectangulo(ola_tamano,15,(0.0, 0.4, 0.7)) # Azul

    glPopMatrix() 

 

    if ola_tamano >= 1: 

        glPushMatrix() 

        glTranslatef(-24.5001,0.0001,0) 

        draw_rectangulo(ola_tamano,15,(0.7, 0.7, 0.7)) # Gris para simular espuma

        glPopMatrix() 

         
# Funcion de dibujar fogata -----------------------------------------------------------------------------------------------------

def draw_fogata(color,color_tronco): 

    glPushMatrix() 
    glTranslatef(0,0.5,0) 

    #Llamas
    glPushMatrix() 
    draw_piramide(0.5,0.2,0.2,0,color) 
    glPopMatrix() 

    #Rotaciones para dar forma de llama
    glPushMatrix() 
    glRotate(40,0,0,1) 
    draw_piramide(0.5,0.2,0.2,0,color) 
    glPopMatrix() 

    glPushMatrix() 
    glRotate(-40,0,0,1) 
    draw_piramide(0.5,0.2,0.2,0,color) 
    glPopMatrix() 

    glPushMatrix() 
    glRotate(40,1,0,0) 
    draw_piramide(0.5,0.2,0.2,0,color) 
    glPopMatrix() 

    glPushMatrix() 
    glRotate(-40,1,0,0) 
    draw_piramide(0.5,0.2,0.2,0,color) 
    glPopMatrix() 

    glPushMatrix() 
    glRotate(40,1,0,1) 
    draw_piramide(0.5,0.2,0.2,0,color) 
    glPopMatrix() 

    glPushMatrix() 
    glRotate(-40,1,0,1) 
    draw_piramide(0.5,0.2,0.2,0,color) 
    glPopMatrix() 

    glPushMatrix() 
    glRotate(90-40,1,0,1) 
    draw_piramide(0.5,0.2,0.2,0,color) 
    glPopMatrix() 

    glPushMatrix() 
    glRotate(90+40,1,0,1) 
    draw_piramide(0.5,0.2,0.2,0,color) 
    glPopMatrix() 

    glPopMatrix()

    #Troncos
    glPushMatrix() 
    glTranslatef(0,0.25,0) 
    glRotate(45,0,1,0) 
    draw_cilindro_tapado(0,360,0.125,0.5,color_tronco) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslatef(0,0.25,0) 
    glRotate(135,0,1,0) 
    draw_cilindro_tapado(0,360,0.125,0.5,color_tronco) 
    glPopMatrix() 

    glPushMatrix() 
    glRotate(180,0,1,0) 
    glPushMatrix() 
    glTranslatef(0,0.25,0) 
    glRotate(45,0,1,0) 
    draw_cilindro_tapado(0,360,0.125,0.5,color_tronco) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslatef(0,0.25,0) 
    glRotate(135,0,1,0) 
    draw_cilindro_tapado(0,360,0.125,0.5,color_tronco) 
    glPopMatrix() 

    glPopMatrix() 

    #Humo
    glPushMatrix() 
    glRotate(90,0,0,1) 
    glScale(0.3,0.3,0.3) 
    draw_humo_moviendose(7,0,0,15,3) 
    glPopMatrix() 

    glPushMatrix() 
    glRotate(90,0,1,0) 
    glRotate(90,0,0,1) 
    glScale(0.3,0.3,0.3) 
    draw_humo_moviendose(7,0,0,15,3) 
    glPopMatrix() 

    

# Funcion de dibujar cocodrilo -----------------------------------------------------------------------------------------------------

def draw_cocodrilo(color,angulo_coco,dir_coco): 

    angulo_coco+=dir_coco 
     

    if(angulo_coco>=20): # Si el ángulo alcanza 20 grados, cambia la dirección

        dir_coco=-10 

    if(angulo_coco<=0): # Si el ángulo alcanza 0 grados, cambia la dirección

        dir_coco=10 


    #Cabeza 

    glPushMatrix() 

    glTranslatef(0,0.4,0) 

    draw_sphere(0.2,color) 

    glPopMatrix() 

         
    #Mandibulas
    glPushMatrix() 

    glTranslatef(0,0.4,0) 

    glRotate(angulo_coco,0,0,1) 

    glRotate(90,0,1,0) 

    draw_cilindro_tapado(0,180,0.2,0.6,color) 

    glPopMatrix() 

     
    
    glPushMatrix() 

    glTranslatef(0,0.4,0) 

    glRotate(-angulo_coco,0,0,1) 

    glRotate(90,0,1,0) 

    draw_cilindro_tapado(180,360,0.2,0.6,color) 

    glPopMatrix() 

     

    #Cuerpo 

    glPushMatrix() 

    glTranslatef(0,0.2,0) 

    glRotate(270,0,1,0) 

    draw_cilindro_tapado(0,360,0.22,0.9,color) 

    glPopMatrix() 

     

    #Cola 

    glPushMatrix() 

    glTranslatef(-0.9,0.2,0) 

    glRotate(90,0,0,1) 

    draw_piramide(0.8,0.25,0.25,0,color) 

    glPopMatrix() 

     

    #Patas 

    glPushMatrix() 

    glTranslatef(-0.1,0.1,0.2) 

    glRotate(90,0,1,0) 

    draw_cilindro_tapado(0,360,0.1,0.3,color) 

    glPopMatrix() 

     
    #Patas
    glPushMatrix() 

    glTranslatef(-0.9,0.1,0.2) 

    glRotate(90,0,1,0) 

    draw_cilindro_tapado(0,360,0.1,0.3,color) 

    glPopMatrix() 

     
    
    glPushMatrix() 

    glTranslatef(-0.1,0.1,-0.2) 

    glRotate(90,0,1,0) 

    draw_cilindro_tapado(0,360,0.1,0.3,color) 

    glPopMatrix() 

     

    glPushMatrix() 

    glTranslatef(-0.9,0.1,-0.2) 

    glRotate(90,0,1,0) 

    draw_cilindro_tapado(0,360,0.1,0.3,color) 

    glPopMatrix() 

     

    return angulo_coco,dir_coco 

 

 # Funcion de dibujar gotas de la fuente -----------------------------------------------------------------------------------------------------


def draw_gotas(cantidad, pendiente, gravedad, altura_min): 

    global d_gotas 

    d_gotas += 0.1 

    for i in range(cantidad):  # Iterar sobre el número de gotas

        t = d_gotas - i * 0.6   

        x = pendiente * t + i * 0.5 

        y = -gravedad * (t ** 2) 

         

        if y < altura_min: # Si la gota ha caído por debajo de la altura mínima,

            continue # saltar a la siguiente gota

         
        # Dibujar gota a la derecha y a la izquierda del centro
        glPushMatrix() 

        glTranslatef(x, y, 0) 

        draw_sphere(0.3, (0, 0, 1)) 

        glPopMatrix() 

         

        glPushMatrix() 

        glTranslatef(-x, y, 0) 

        draw_sphere(0.3, (0, 0, 1)) 

        glPopMatrix() 

     

    if d_gotas > 100: # Reiniciar la posición de las gotas después de un tiempo

        d_gotas = 0 

 

# Funcion de dibujar fuente en el centro del mundo -----------------------------------------------------------------------------------------------------
 

def fuente_centro_mundo(color): 

    pass 

     
# Funcion de dibujar todo el mundo -----------------------------------------------------------------------------------------------------


def draw_mundo(): 

    #Variables para los que se mueven en circulo 

    global angulo_carros, angulo_vivos,angulo_insectos 

    #Variables para los que se mueven y giran 

    #Pelicanos 

    global angulo_peli1, angulo_peli2,angulo_peli3,angulo_peli1, dir_peli1, dir_peli2,dir_peli3 
    global d_peli1, d_peli2,d_peli3 

    #Pollos 

    global angulo_pol1, angulo_pol2,angulo_pol3,angulo_pol1, dir_pol1, dir_pol2,dir_pol3 
    global d_pol1, d_pol2,d_pol3 

    #Peces 

    global angulo_pez1, angulo_pez2,angulo_pez3, dir_pez1, dir_pez2,dir_pez3 
    global d_pez1, d_pez2,d_pez3 

    #Barquito 

    global d_bar,dir_bar,angulo_bar 

    #Cocodrilos 

    global angulo_coco2,dir_coco2,angulo_coco1,dir_coco1 

    #Antena 

    global angulo_antena   

    #Gotas de la fuente 

    global d_gotas 


    draw_gotas(15,3,2,10) 

    # Edificio en un lado 

    glPushMatrix() 
    glTranslatef(0, 0, -13) 
    glScaled(0.6,0.6,0.6) 
    draw_edificio_reloj() 
    glPopMatrix() 

    #Antena del edificio 
    glPushMatrix() 
    glTranslatef(0,7.5,-13) 
    angulo_antena=draw_antena((0.2,0.2,0.2),angulo_antena) 
    glPopMatrix() 

    # Bandera en el centro 
    glPushMatrix() 
    glTranslatef(2.5, 0, -11) 
    glScaled(0.6,0.6,0.6) 
    draw_bandera() 
    glPopMatrix() 

    glPushMatrix() 
    glTranslatef(-2.5, 0, -11) 
    glScaled(0.6,0.6,0.6) 
    glRotatef(180,0,1,0) 
    draw_bandera() 
    glPopMatrix() 


    #Calles --------------------------------------------

    draw_calles() 

    #Casas --------------------------------------------

    draw_houses_circulo(10,13) 

    #Arbustos con flores -----------------------------

    draw_arbustos_circulo(15,3)  

    #Sol y Luna --------------------------------------------

    draw_sol_luna() 





    #Objetos con animaciones -----------------------------------------------------------------------------------------------
    
    # Nubes

    draw_nubes_moviendose(-50,8,-15,65,30) 

    # Autos

    mover_en_circulo(lambda: draw_auto((1,0,0)),7,angulo_carros,0,90,0) 
    mover_en_circulo(lambda: draw_auto((0,0.75,1)),7,angulo_carros,2,90,0) 
    mover_en_circulo(lambda: draw_auto((1,0,1)),7,angulo_carros,3,90,0) 
    mover_en_circulo(lambda: draw_auto((1.0, 0.5, 0.0)),7,angulo_carros,4,90,0) 

    #Camiones

    mover_en_circulo(lambda: draw_camion((0.0, 1.0, 0.0)),7,angulo_carros,1,90,0) 
    mover_en_circulo(lambda: draw_camion((0.0, 1.0, 0.0)),7,angulo_carros,5,90,0) 

    #Motos

    mover_en_circulo(lambda: draw_moto((0.5, 0.0, 0.5)),7,angulo_carros,1.5,90,0) 
    mover_en_circulo(lambda: draw_moto((1.0, 1.0, 0.0)),7,angulo_carros,5.5,90,0) 

    angulo_carros+=0.05 

    # Personas caminando

    mover_en_circulo(lambda: draw_persona_caminando((0.75, 0.55, 0.38)),9,angulo_vivos,0,0,0) 
    mover_en_circulo(lambda: draw_persona_caminando((0.55, 0.40, 0.28)),9,angulo_vivos,1,0,0) 
    mover_en_circulo(lambda: draw_persona_caminando((0.75, 0.55, 0.38)),9,angulo_vivos,4,0,0) 
    mover_en_circulo(lambda: draw_persona_caminando((0.55, 0.40, 0.28)),5,angulo_vivos,6,0,0) 
    mover_en_circulo(lambda: draw_persona_caminando((0.75, 0.55, 0.38)),5,angulo_vivos,2,0,0) 

   # Perros caminando
     
    mover_en_circulo(lambda: draw_perro_caminando((0.83, 0.69, 0.22)),9.1,angulo_vivos,0.15,180,0) 
    mover_en_circulo(lambda:  draw_perro_caminando((0.6, 0.4, 0.2)),5.1,angulo_vivos,5.90,180,0) 
    mover_en_circulo(lambda:  draw_perro_caminando( (0.8, 0.8, 0.8)),5.1,angulo_vivos,1.85,180,0) 

    angulo_vivos-=0.01 

    # Abejas

    mover_en_circulo(lambda: draw_bee(),3.2,angulo_insectos,0.2,0,0) 
    mover_en_circulo(lambda: draw_bee(),3.2,angulo_insectos,2,0,0) 
    mover_en_circulo(lambda: draw_bee(),3.2,angulo_insectos,4,0,0) 

    angulo_insectos+=0.03 

    # Caracoles

    mover_en_circulo(lambda: draw_caracol((0.55, 0.47, 0.35),(0.33, 0.42, 0.18)),3.8,angulo_insectos,1.2,0,0) 
    mover_en_circulo(lambda: draw_caracol( (0.35, 0.1, 0.45),(0.5, 0.5, 0.2)),3.8,angulo_insectos,3,0,0) 
    mover_en_circulo(lambda: draw_caracol((0.0, 0.3, 0.35),(0.33, 0.42, 0.18)),3.8,angulo_insectos,5,0,0) 

    angulo_insectos+=0.03   

       #Pelicanos que viendolos bien son más que nada gaviotas jsjs

    d_peli1,dir_peli1, angulo_peli1=mover_en_linea_girando(lambda: draw_pelicano((0.5,0.5,0.5)), 

                                                                        -35.5,7,18,50,d_peli1,dir_peli1,angulo_peli1,True,False,False,True) 

    d_peli1,dir_peli1, angulo_peli1=mover_en_linea_girando(lambda: draw_pelicano((0.8, 0.8, 0.8)), 

                                                                        -35.5,7,10,50,d_peli1,dir_peli1,angulo_peli1,True,False,False,True) 

     
    d_peli2,dir_peli2, angulo_peli2=mover_en_linea_girando(lambda: draw_pelicano((0.5,0.5,0.5)), 

                                                                        -35.5,7,0,50,d_peli2,dir_peli2,angulo_peli2,True,False,False,True) 


    d_peli2,dir_peli2, angulo_peli2=mover_en_linea_girando(lambda: draw_pelicano((0.5,0.5,0.5)), 

                                                                        -35.5,7,-4,50,d_peli2,dir_peli2,angulo_peli2,True,False,False,True) 


    d_peli2,dir_peli2, angulo_peli2=mover_en_linea_girando(lambda: draw_pelicano((0.5,0.5,0.5)), 

                                                                        -35.5,7,14,50,d_peli2,dir_peli2,angulo_peli2,True,False,False,True) 


    d_peli3,dir_peli3, angulo_peli3=mover_en_linea_girando(lambda: draw_pelicano((0.8, 0.8, 0.8)), 

                                                                        -35.5,7,7,50,d_peli3,dir_peli3,angulo_peli3,True,False,False,True) 


    d_peli3,dir_peli3, angulo_peli3=mover_en_linea_girando(lambda: draw_pelicano((0.5,0.5,0.5)), 

                                                                        -35.5,7,14,50,d_peli3,dir_peli3,angulo_peli3,True,False,False,True) 


    #Pollitos 

    d_pol1,dir_pol1, angulo_pol1=mover_en_linea_girando(lambda: draw_pollo( (0.05, 0.1, 0.3)), 

                                                                        -15,4,4,30,d_pol1,dir_pol1,angulo_pol1,True,False,False,True) 

    d_pol2,dir_pol2, angulo_pol2=mover_en_linea_girando(lambda: draw_pollo( (0.05, 0.1, 0.3)), 

                                                                        -15,4,13,30,d_pol2,dir_pol2,angulo_pol2,True,False,False,True) 

    d_pol3,dir_pol3, angulo_pol3=mover_en_linea_girando(lambda: draw_pollo( (0.05, 0.1, 0.3)), 

                                                                        -15,4,1,30,d_pol3,dir_pol3,angulo_pol3,True,False,False,True) 

     

    #PLAYA ANIMACIONES ----------------------------------------------------------------------------------------------

    #Ola animada

    draw_ola() 

    #Tipos jugando en la orilla

    glPushMatrix() 
    glTranslatef(-23,0.001,10) 
    draw_tipos_jugando((0.55, 0.40, 0.28),(0.75, 0.55, 0.38),(1,0,1)) 
    glPopMatrix() 

    #Peces 

    d_pez1,dir_pez1,angulo_pez1=mover_en_linea_girando(lambda: draw_pez( (0.5, 0.0, 0.1)), 

                                                                        -34,-2,-5,18,d_pez1,dir_pez1,angulo_pez1,False,False,True,True) 

    d_pez2,dir_pez2,angulo_pez2=mover_en_linea_girando(lambda: draw_pez((1.0, 1.0, 0.0)), 

                                                                        -32,-4,-5,18,d_pez2,dir_pez2,angulo_pez2,False,False,True,True) 

    d_pez3,dir_pez3,angulo_pez3=mover_en_linea_girando(lambda: draw_pez( (1.0, 1.0, 1.0)), 

                                                                        -30,-2,-5,18, d_pez3,dir_pez3,angulo_pez3,False,False,True,True) 

    #Barquito 

    d_bar,dir_bar,angulo_bar=mover_en_linea_girando(lambda: draw_barquito( (0.55, 0.27, 0.07), (0.70, 0.50, 0.35)), 

                                                    -33,0.005,-5,18,d_bar,dir_bar,angulo_bar,False,False,True,True) 

    #Fogata 

    glPushMatrix() 
    glTranslate(-20,0.002,-10) 
    draw_fogata((1,0,0),(0.35, 0.2, 0.1)) 
    glPopMatrix() 

    #Cocodrilo 
    glPushMatrix() 
    glTranslate(-23,0.002,0) 
    glRotate(45,0,1,0) 
    angulo_coco1,dir_coco1=draw_cocodrilo((0.1, 0.4, 0.1),angulo_coco1,dir_coco1) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslate(-23.5,0.002,-2) 
    glRotate(-50,0,1,0) 
    angulo_coco2,dir_coco2=draw_cocodrilo((0.1, 0.4, 0.1),angulo_coco2,dir_coco2) 
    glPopMatrix() 




# Funcion principal -----------------------------------------------------------------------------------------------------

def main(): 

    global moverx,movery,moverz,dx,dz,girar 

    try: 

        window = init_glfw() # Inicializar GLFW

    except Exception as e: 

        print(f" Error al inicializar GLFW: {e}") 

        return 


    setup_opengl() # Configurar OpenGL
    setup_lights() # Configurar luces

    frame_count = 0 
    fps_timer = glfw.get_time() # Temporizador para FPS

     

    try: 

        # Inicializar la captura de video desde la cámara web 

        cap = cv2.VideoCapture(0) 

        cv2.waitKey(2000) #Esperar 2 segundos para que la cámara se estabilice 


        while not glfw.window_should_close(window): 

             # Ventana de OpenCV para el seguimiento de manos

            ret, frame = cap.read() #Lectura del frame actual 
            frame2 = frame.copy() #Hacer una copia del frame actual 

            if not ret: 

                break 

            #Landmarks 

            h, w, _ = frame.shape # Obtener dimensiones del frame 

            # Convertir a RGB 

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

            # Procesar la imagen con MediaPipe 

            results = hands.process(frame_rgb) 

            #puntos para diferenciar indices de 2 manos 

            xil,yil,xir,yir=0,0,0,0 
            xbl,ybl,xbr,ybr=0,0,0,0 
            xml,yml,xmr,ymr=0,0,0,0 
            xgl,ygl,xgr,ygr=0,0,0,0 

             

            if results.multi_hand_landmarks and results.multi_handedness: # Si se detectan manos

                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness): # Iterar sobre cada mano detectada

                        # Dibujar los landmarks en la imagen

                    mp_drawing.draw_landmarks(frame2, hand_landmarks, mp_hands.HAND_CONNECTIONS) 

                        # Obtener la etiqueta de la mano (izquierda o derecha)

                    label = handedness.classification[0].label 

                    #Distancia de referencia 

                    #Obtener coordenadas del pulgar e índice con hand_landmarks 

                    indice = hand_landmarks.landmark[8] 
                    indice_base=hand_landmarks.landmark[5] 
                    muneca=hand_landmarks.landmark[0]  
                    dedo_grosero=hand_landmarks.landmark[9] 

                   # Coordenadas en píxeles
                    if(label=="Left"):
                        xil, yil = int(indice_base.x * w), int(indice_base.y * h) #esto convierte a pixeles
                        xbl, ybl = int(indice.x * w), int(indice.y * h)
                        xml, yml = int(muneca.x * w), int(muneca.y * h)
                        xgl, ygl = int(dedo_grosero.x * w), int(dedo_grosero.y * h)
                        
                    if(label=="Right"):
                        xir, yir = int(indice_base.x * w), int(indice_base.y * h) #esto convierte a pixeles
                        xbr, ybr = int(indice.x * w), int(indice.y * h)
                        xmr, ymr = int(muneca.x * w), int(muneca.y * h)
                        xgr, ygr = int(dedo_grosero.x * w), int(dedo_grosero.y * h)
                    
                    distancial=math.hypot(abs(xml-xgl),abs(yml-ygl))
                    distanciar=math.hypot(abs(xmr-xgr),abs(ymr-ygr))
                    
                    mov_x=(xir-xbr)
                    mov_y=(yir-ybr)
                    mov_z=(yil-ybl)
                    giro=(xil-xbl)
                    
                    if(mov_x<=-distanciar/2):
                        moverx -= dz * 0.5
                        moverz -= -dx * 0.5
                    if(mov_x>=distanciar/2):
                        moverx += dz * 0.5
                        moverz += -dx * 0.5
                        
                        
                    if(mov_y<=-distanciar/2):
                        movery=movery-0.5
                    if(mov_y>=distanciar/2):
                        movery=movery+0.5
                        
                    if(mov_z<=-distancial/2):
                        moverx -= dx * 0.5
                        moverz -= dz * 0.5
                        
                    if(mov_z>=distancial/2):
                        moverx += dx * 0.5
                        moverz += dz * 0.5
                        
                #/////////////////////////////////
                    if(giro<=-distancial/2):
                        girar=girar+0.25
                    if(giro>=distancial/2):
                        girar=girar-0.25
                     

            cv2.imshow("Manos", frame2) #Mostrar el video con el seguimiento 

            if cv2.waitKey(1) & 0xFF == ord('q'): # q para salir

                break 

             # Movimiento con teclado como segundo control----------------------------------------------------------

            if key.is_pressed('up'): 

                moverx += dx  
                moverz += dz  

 

            if key.is_pressed('down'): 

                moverx -= dx 
                moverz -= dz  

                 

            if key.is_pressed('left'): 

                moverx += dz 
                moverz += -dx  

 

            if key.is_pressed('right'): 

                moverx -= dz 
                moverz -= -dx  


            if(key.is_pressed('w')): 

                movery=movery+1 

                 

            if(key.is_pressed('s')): 

                movery=movery-1 

                 

            if (key.is_pressed('a')): 

                girar =girar- 0.2 

 

            if (key.is_pressed('d')): 

                girar =girar+0.2 

            dx = math.sin(girar) 
            dz = -math.cos(girar)     

            glfw.poll_events() 


            if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS: 

                break 

             # Configuración de la ventana y cámara

            glClearColor(r, g, b,0) 
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
            glMatrixMode(GL_PROJECTION) 
            glLoadIdentity() 
            gluPerspective(60, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100.0)  

            glMatrixMode(GL_MODELVIEW) 
            glLoadIdentity() 
            gluLookAt( 

                moverx, movery, moverz,   # cámara 
                moverx+dx, movery, moverz+dz,    # mira al centro 
                0, 1, 0    # arriba 

            ) 

            #Funcion de dibujo 
            glDisable(GL_CULL_FACE) 

            # dibujar el mundo
            draw_mundo() 
            # Intercambiar buffers
            glfw.swap_buffers(window) 

            frame_count += 1 
            current_time = glfw.get_time() 

            if current_time - fps_timer >= 1.0: 

                fps = frame_count / (current_time - fps_timer) # Calcular FPS
                glfw.set_window_title(window, f"{WINDOW_TITLE} - FPS: {fps:.1f}") # Actualizar título de la ventana
                frame_count = 0 
                fps_timer = current_time # Reiniciar temporizador


    except Exception as e: # bloque para capturar errores en el loop principal

        print(f" Error en el loop principal: {e}") 
        import traceback # Importar módulo traceback
        traceback.print_exc() # Imprimir la traza del error


    finally: 

        print("\nCerrando aplicación...") 

        #. Liberar los recursos 

        cap.release() 
        cv2.destroyAllWindows() 

        glfw.terminate() 

       

if __name__ == "__main__": 

    main() 

 

 



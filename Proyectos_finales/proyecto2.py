import glfw
import cv2
import mediapipe as mp
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# ============================================================
# Configuración
# ============================================================
#WINDOW_WIDTH
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_TITLE = "Mascara 3D Extendida + Mediapipe"

#Angulo de la estrellita, movimiento en x
animar_estrellitar, estrella_angr, estrella_xr=False,0,0
animar_estrellital, estrella_angl, estrella_xl=False,0,0

# Conexiones para dibujar el contorno facial
contorno_cara  = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
             397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
             172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]

# Cejas
LEFT_EYEBROW = [70, 63, 105, 66, 107]
RIGHT_EYEBROW = [336, 296, 334, 293, 300]


def init_glfw():
    if not glfw.init():
        raise Exception("No se pudo inicializar GLFW")
    
    # No especificar version de OpenGL - usar la mejor disponible compatible
    # con fixed-function pipeline (glBegin/glEnd, GL_LIGHTING, etc.)
    
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, None, None)
    
    if not window:
        glfw.terminate()
        raise Exception("No se pudo crear la ventana GLFW")
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    
    return window

# ============================================================
# Configuracion inicial de OpenGL
# ============================================================
def setup_opengl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

def create_video_texture():
    video_tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, video_tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    return video_tex

def setup_lights():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)  # Luz adicional
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Luz principal frontal
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 2, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1))
    
    # Luz de relleno lateral
    glLightfv(GL_LIGHT1, GL_POSITION, (1, 1, 1, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))

# ============================================================
# Funciones de dibujo
# ============================================================
def draw_sphere(x, y, z, radius, color=(1, 1, 1)):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 16, 16)
    gluDeleteQuadric(quad)
    glPopMatrix()

def draw_line(p1, p2, color=(1, 1, 1), width=2.0):
    """Dibuja una línea entre dos puntos 3D"""
    glDisable(GL_LIGHTING)
    glLineWidth(width)
    glColor3f(*color)
    glBegin(GL_LINES)
    glVertex3f(*p1)
    glVertex3f(*p2)
    glEnd()
    glEnable(GL_LIGHTING)


def dibujar_cilindro(a,b,c,ang_in,ang_fin,ar,br,cr,radius,largo,angulo,color=(1,1,1)):
    glPushMatrix()
    glTranslatef(a, b, c)
    
    glRotatef(angulo, ar, br, cr)
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
    glPopMatrix()
        
def dibujar_trianguloR(x1,y1,z1,x2,y2,z2,ang,ar,br,cr,angulo,color=(1,1,1)):
    lado1= abs(y2-y1)
    lado2=lado1*2
    glPushMatrix()
    glTranslate(x2,y2,z2)
    glRotatef(ang, 0, 0, 1)
    glRotatef(angulo, ar, br, cr)
    glColor3f(*color)
    
    
    glBegin(GL_TRIANGLE_STRIP)
    glNormal3f(0, lado1, 0)
    glVertex3f(0, lado1, 0)
    glNormal3f(0, 0, 0)
    glVertex3f(0, 0, 0)
    glNormal3f(lado2, 0, 0)
    glVertex3f(lado2, 0, 0)
    
    glEnd()
    glPopMatrix()
    
def dibujar_estrellita(x,y,z,lado,angulo,color=(1,1,1)):
    
    R = lado
    r = lado * 0.4
    glPushMatrix()
    glTranslate(x,y,z)
    glRotatef(angulo, 0, 0, 1)
    glColor3f(*color) 
    

    glBegin(GL_TRIANGLE_FAN)

    # Centro exacto
    glNormal3f(0, 0, 1)
    glVertex3f(0.0, 0.0, 0.0)

    # Vértices de la estrella
    for i in range(11):  # 10 puntos + cierre
        ang = i * math.pi / 5   # 36°
        radio = R if i % 2 == 0 else r

        x1 = math.cos(ang) * radio
        y1 = math.sin(ang) * radio

        glNormal3f(0, 0, 1)
        glVertex3f(x1, y1, 0.0)
    
    glEnd()
    glPopMatrix()
    
def dibujar_elipse(x,y,z,a,b,ang,inicio,fin,color=(1,1,1)):
    glPushMatrix()
    glTranslatef(x,y,z)
    glRotatef(ang,0,0,1)
    glColor3f(*color) 
    
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0,0,0) 
    for i in range(inicio,fin):
        ang=math.radians(i)
        x1=a*math.cos(ang)
        y1=b*math.sin(ang)
        glNormal3f(0, 0, 1)
        glVertex3f(x1, y1, 0.0)
        
    glEnd()
    glPopMatrix()
    
def norm_landmark(p):
    return ((p.x - 0.5)*2, -2*(p.y - 0.5), (p.z)*2)

# ============================================================
# Renderizado
# ============================================================
def render_video_background(frame_rgb, video_tex):
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1, 0, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glBindTexture(GL_TEXTURE_2D, video_tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 
                 frame_rgb.shape[1], frame_rgb.shape[0],
                 0, GL_RGB, GL_UNSIGNED_BYTE, frame_rgb)
    
    glColor3f(1.0, 1.0, 1.0)
    
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(0, 0)
    glTexCoord2f(1, 1); glVertex2f(1, 0)
    glTexCoord2f(1, 0); glVertex2f(1, 1)
    glTexCoord2f(0, 0); glVertex2f(0, 1)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_face_contour(landmarks, indices, color=(0.3, 0.8, 0.4)):
    glDisable(GL_LIGHTING)
    glLineWidth(1.5)
    glColor3f(*color)
    
    glBegin(GL_LINE_STRIP)
    for idx in indices:
        p = norm_landmark(landmarks[idx])
        glVertex3f(*p)
    # Cerrar el contorno
    p = norm_landmark(landmarks[indices[0]])
    glVertex3f(*p)
    glEnd()
    
    glEnable(GL_LIGHTING)

def render_3d_mask_extended(face_landmarks):
    """Renderiza la máscara 3D extendida"""
    glEnable(GL_DEPTH_TEST)
    glClear(GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 100)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(0, 0, 2, 0, 0, 0, 0, 1, 0)
    
    setup_lights()
    
    lm = face_landmarks.landmark
    
 
    
    # ============================================================
    # 2. OJOS
    # ============================================================
    
    # left_eye = lm[386]
    # right_eye = lm[159]
    
    lx1,ly1,lz1= norm_landmark(lm[133]) #Ojo lagrimal
    lx2,ly2,lz2= norm_landmark(lm[33]) #Ojo lagrimal
    
    rx1,ry1,rz1= norm_landmark(lm[362])
    rx2,ry2,rz2= norm_landmark(lm[263])
    
    
    lx, ly, lz = ((lx1+lx2)/2),((ly1+ly2)/2),((lz1+lz2)/2) #Centro ojo
    rx, ry, rz = ((rx1+rx2)/2), ((ry1+ry2)/2), ((rz1+rz2)/2) #Centro ojo
    
    ladol=abs(lx2-lx1)/2
    lador=abs(rx2-rx1)/2
    
    
        
    # ============================================================
    # 2. Parpados
    # ============================================================
    left_eye_p1 = lm[386]
    left_eye_p2 = lm[374]
    
    right_eye_p1 = lm[159]
    right_eye_p2 = lm[145]
    
    lx1, ly1, lz1 = norm_landmark(left_eye_p1)
    lx2, ly2, lz2 = norm_landmark(left_eye_p2)
    
    rx1, ry1, rz1 = norm_landmark(right_eye_p1)
    rx2, ry2, rz2 = norm_landmark(right_eye_p2)
    

    
    # ============================================================
    # 2. Estrellita
    # ============================================================

    global animar_estrellitar, estrella_angr, estrella_xr, animar_estrellital, estrella_angl, estrella_xl
    
    #Guiño izquierdo
    if(abs(ly1-ly2)<(ladol*0.4) and abs(ry1-ry2)>(lador*0.6)):
        animar_estrellital=True
        
    if(animar_estrellital):
        dibujar_estrellita(rx+estrella_xl,ry,rz,lador*1.5,estrella_angr,(0.5,0.5,0))
        estrella_angl=estrella_angl+10
        estrella_xl=estrella_xl+(ladol/3)
    
    if(lx+estrella_xl>=1.5):
        estrella_xl=0
        estrella_angl=0
        animar_estrellital=False
    
    #Guiño derecho
    if(abs(ry1-ry2)<(lador*0.4) and abs(ly1-ly2)>(ladol*0.6)):
        animar_estrellitar=True
        
    if(animar_estrellitar):
        dibujar_estrellita(lx+estrella_xr,ly,lz,ladol*1.5,estrella_angl,(0.5,0.5,0))
        estrella_angr=estrella_angr+10
        estrella_xr=estrella_xr-(lador/3)
    
    if(rx+estrella_xr<=-1.5):
        estrella_xr=0
        estrella_angr=0
        animar_estrellitar=False

    
    # ============================================================
    # 5. BOCA
    # ============================================================
    mouth_left = lm[61]
    mouth_right = lm[291]
    mouth_top = lm[0]
    mouth_top2 = lm[13]
    mouth_bottom = lm[14] 
    
    mlx, mly, mlz = norm_landmark(mouth_left) #Comisura derecha
    mrx, mry, mrz = norm_landmark(mouth_right)#Comisura izquierda
    mtx, mty, mtz = norm_landmark(mouth_top) #Labio superior
    mbx, mby, mbz = norm_landmark(mouth_bottom) #Labio inferior
    
    #sonrisa
    a=abs(mlx-mrx)/2
    b=abs(mty-mby)
    ang=math.atan2(mry - mly, mrx - mlx)
    ang=math.degrees(ang)
    
    dibujar_elipse(mtx,mty,mtz,a,b,ang,180,361)

    
    # ============================================================
    # 5. Bigote
    # ============================================================
    #Arriba de la boca
    mtx, mty, mtz = norm_landmark(mouth_top2) #Labio superior
    #Fosas de la nariz
    nose_left = lm[98] 
    nose_right = lm[327]
    

    nlx, nly, nlz = norm_landmark(nose_left)
    nrx, nry, nrz = norm_landmark(nose_right)
    
    distancial=nly-mty 
    distanciar=nry-mty
    
    dibujar_trianguloR(nrx,nry+(distanciar*0.1),nrz,nrx,mty+(distanciar*0.5),mtz,ang,0,0,0,0,(0,0,0))
    dibujar_trianguloR(nlx,nly+(distancial*0.1),nlz,nlx,mty+(distancial*0.5),mtz,ang,0,1,0,180,(0,0,0))
    

    
    # ============================================================
    # 7. FRENTE Y BARBA
    # ============================================================
    forehead = lm[10]
    chin = lm[152]
    
    fx, fy, fz = norm_landmark(forehead)
    cx, cy, cz = norm_landmark(chin)
    

    
    # Restaurar matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    # ============================================================
    # 5. Sombrero
    # ============================================================
    largo=9*abs(fy-cy)/16
    radio=7*abs(fy-cy)/18
    incremento=abs(fy-cy)/2
    
    glPushMatrix()
    glRotatef(ang, 0, 0, 1)
    dibujar_cilindro(fx,fy+incremento,fz+(incremento*0.2),0,360,1,0,0,radio,largo,70,(0.25, 0.25, 0.25))
    dibujar_cilindro(fx,fy+(incremento*0.5),fz,150,390,1,0,0,radio*1.1,largo*0.3,70,(1, 0, 0))
    dibujar_cilindro(fx,fy+(incremento*0.3),fz,0,360,1,0,0,radio*1.3,largo*0.4,70,(0.25, 0.25, 0.25))
    glPopMatrix()
# ============================================================
# Función principal
# ============================================================
def main():
    
    try:
        window = init_glfw()
    except Exception as e:
        print(f" Error al inicializar GLFW: {e}")
        return
    
    setup_opengl()
    video_tex = create_video_texture()
    
    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(" No se pudo abrir la camara")
        glfw.terminate()
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)
    print("Camara inicializada")
    
    
    frame_count = 0
    fps_timer = glfw.get_time()
    
    try:
        while not glfw.window_should_close(window):
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            results = face_mesh.process(frame_rgb)
            
            glfw.poll_events()
            
            if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
                break
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            render_video_background(frame_rgb, video_tex)
            
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    render_3d_mask_extended(face_landmarks)
            
            glfw.swap_buffers(window)
            
            frame_count += 1
            current_time = glfw.get_time()
            if current_time - fps_timer >= 1.0:
                fps = frame_count / (current_time - fps_timer)
                glfw.set_window_title(window, f"{WINDOW_TITLE} - FPS: {fps:.1f}")
                frame_count = 0
                fps_timer = current_time
    
    except Exception as e:
        print(f" Error en el loop principal: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\nCerrando aplicación...")
        cap.release()
        face_mesh.close()
        glfw.terminate()
      
if __name__ == "__main__":
    main()

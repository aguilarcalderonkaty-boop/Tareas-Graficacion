from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

#Dimensiones iniciales de la ventana
win_w, win_h = 900, 900

def setup():
    #Activar prueba de profundidad para que se vean bien las figuras 3D
    glEnable(GL_DEPTH_TEST)
    #Activar iluminación 
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    #Posición de la luz
    glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
    #Permitir que el color afecte el material
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    #Color de fondo (gris oscuro)
    glClearColor(0.15, 0.15, 0.15, 1)

#Función para dibujar figura según índice
def render_object(idx):
    if idx == 0: glutWireSphere(0.6, 20, 20)      #Esfera de alambre
    elif idx == 1: glutSolidSphere(0.6, 20, 20)   #Esfera sólida
    elif idx == 2: glutWireCube(1.0)              #Cubo de alambre
    elif idx == 3: glutSolidCube(1.0)             #Cubo sólido
    elif idx == 4: glutWireCone(0.6, 1.0, 20, 4)  #Cono de alambre
    elif idx == 5: glutSolidCone(0.6, 1.0, 20, 4) #Cono sólido
    elif idx == 6: glutWireDodecahedron()         #Dodecaedro de alambre
    elif idx == 7: glutSolidDodecahedron()        #Dodecaedro sólido
    elif idx == 8: glutWireOctahedron()           #Octaedro de alambre
    elif idx == 9: glutSolidOctahedron()          #Octaedro sólido
    elif idx == 10: glutWireTetrahedron()         #Tetraedro de alambre
    elif idx == 11: glutSolidTetrahedron()        #Tetraedro sólido
    elif idx == 12: glutWireIcosahedron()         #Icosaedro de alambre
    elif idx == 13: glutSolidIcosahedron()        #Icosaedro sólido
    elif idx == 14: glutWireTeapot(0.5)           #Tetera de alambre
    elif idx == 15: glutSolidTeapot(0.5)          #Tetera sólida

#Función principal de dibujo
def draw_scene():
    #Limpiar buffers de color y profundidad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    filas, columnas = 4, 4  #Dividir en cuadrícula 
    cell_w = win_w // columnas
    cell_h = win_h // filas
    
    #Recorrer cada celda de la cuadrícula
    for fila in range(filas):
        for col in range(columnas):
            idx = fila * columnas + col  #Índice de figura
            #Definir viewport para cada celda
            glViewport(col * cell_w, (filas - 1 - fila) * cell_h, cell_w, cell_h)
            
            #Configurar proyección en perspectiva
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(50, cell_w / cell_h, 1, 20)
            
            #Configurar vista de cámara
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            gluLookAt(0, 0, 3, 0, 0, 0, 0, 1, 0)
            
            #Rotación fija para ver mejor las figuras
            glRotatef(25, 1, 1, 0)
            
            #Colores alternados para cada figura
            if idx % 2 == 0:
                glColor3f(0.3, 0.9, 0.7)  #Verde
            else:
                glColor3f(0.9, 0.4, 0.2)  #Naranja
            
            #Dibujar la figura correspondiente
            render_object(idx)
    
    #Intercambiar buffers 
    glutSwapBuffers()

#Función para redimensionar ventana
def resize(w, h):
    global win_w, win_h
    win_w, win_h = w, h

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(win_w, win_h)
    glutCreateWindow(b"Figuras GLUT estaticas - OpenGL Python")

    setup()
    glutDisplayFunc(draw_scene)
    glutReshapeFunc(resize)
    glutMainLoop()

if __name__ == "__main__":
    main()

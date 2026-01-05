import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Triángulo invertido con cuadrado
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)   # Fondo negro
    glMatrixMode(GL_PROJECTION)        # Usar la matriz de proyección
    glLoadIdentity()                   # Reiniciar la matriz
    gluPerspective(45, 1.0, 0.1, 50.0) # Perspectiva con ángulo de visión
    glMatrixMode(GL_MODELVIEW)         # Cambiar a la matriz de modelo-vista

# Función principal de dibujo
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar pantalla y profundidad
    glLoadIdentity()                                    # Reiniciar transformaciones
    glTranslatef(0.0, 0.0, -3)                          # Alejar la cámara

    # Triángulo invertido
    glBegin(GL_TRIANGLES)
    glColor3f(0.9, 0.2, 0.2)   # Rojo suave
    glVertex3f(-1.0, 1.0, 0.0)
    glColor3f(0.2, 0.9, 0.4)   # Verde claro
    glVertex3f(1.0, 1.0, 0.0)
    glColor3f(0.2, 0.4, 0.9)   # Azul más brillante
    glVertex3f(0.0, -1.0, 0.0)
    glEnd()
    
    # Cuadrado con degradado distinto
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.8, 0.2)   # Amarillo apagado
    glVertex3f(-0.5, -0.5, 0.0)
    glColor3f(0.2, 0.9, 0.9)   # Turquesa
    glVertex3f(0.5, -0.5, 0.0)
    glColor3f(0.9, 0.2, 0.9)   # Magenta más suave
    glVertex3f(0.5, 0.5, 0.0)
    glColor3f(1.0, 0.4, 0.1)   # Naranja más cálido
    glVertex3f(-0.5, 0.5, 0.0)
    glEnd()

    glutSwapBuffers()  # Cambiar buffers para mostrar el resultado

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) # Ventana 
    glutInitWindowSize(800, 600)                            # Dimensiones de la ventana
    glutCreateWindow("Triángulo invertido y cuadrado".encode('utf-8'))
    
    init()
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()

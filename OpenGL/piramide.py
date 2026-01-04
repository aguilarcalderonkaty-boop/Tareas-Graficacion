import glfw
from OpenGL.GL import glClearColor, glEnable, glClear, glLoadIdentity, glTranslatef, glRotatef, glMatrixMode
from OpenGL.GL import glBegin, glColor3f, glVertex3f, glEnd, glFlush, glViewport
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_QUADS, GL_PROJECTION, GL_MODELVIEW,GL_TRIANGLES
from OpenGL.GLU import gluPerspective
import sys

# Variables globales
window = None
angle = 0  # Declaramos angle en el nivel superior

def init():
    # Configuración inicial de OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Color de fondo
    glEnable(GL_DEPTH_TEST)  # Activar prueba de profundidad para 3D

    # Configuración de proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 50.0)

    # Cambiar a la matriz de modelo para los objetos
    glMatrixMode(GL_MODELVIEW)


def draw_piramide():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar pantalla y buffer de profundidad

    # Configuración de la vista
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -6)   # Alejar la pirámide
    glRotatef(angle, 1, 1, 0)    # Rotación en los ejes X e Y

    glBegin(GL_TRIANGLES)

    # Cara frontal
    glColor3f(0.2, 0.8, 0.9)   # Turquesa
    glVertex3f(0.0, 1.5, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    # Cara derecha
    glColor3f(0.9, 0.3, 0.7)   # Rosa fuerte
    glVertex3f(0.0, 1.5, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)

    # Cara trasera
    glColor3f(0.3, 0.9, 0.4)   # Verde claro
    glVertex3f(0.0, 1.5, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)

    # Cara izquierda
    glColor3f(0.9, 0.6, 0.1)   # Naranja
    glVertex3f(0.0, 1.5, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)

    glEnd()

    # Base cuadrada
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.2, 0.7)   # Morado
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glEnd()

    glFlush()
    glfw.swap_buffers(window)
    angle += 0.05  # Incrementar ángulo para rotación


def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    # Crear ventana de GLFW
    width, height = 500, 500
    window = glfw.create_window(width, height, "Piramide 3D Rotando con GLFW", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    # Configurar el contexto de OpenGL en la ventana
    glfw.make_context_current(window)

    # Configuración de viewport y OpenGL
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_piramide()
        glfw.poll_events()

    glfw.terminate()  # Cerrar GLFW al salir

if __name__ == "__main__":
    main()

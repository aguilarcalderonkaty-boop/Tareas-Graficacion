import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

rotation = 0.0

def draw_sphere(radius, slices=30, stacks=30):
    """Dibuja una esfera usando primitivas OpenGL (sin GLUT)"""
    for i in range(stacks):
        lat1 = math.pi * (-0.5 + i / stacks)
        lat2 = math.pi * (-0.5 + (i + 1) / stacks)
        
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * j / slices
            x1 = math.cos(lat1) * math.cos(lng)
            y1 = math.sin(lat1)
            z1 = math.cos(lat1) * math.sin(lng)
            x2 = math.cos(lat2) * math.cos(lng)
            y2 = math.sin(lat2)
            z2 = math.cos(lat2) * math.sin(lng)
            
            glNormal3f(x1, y1, z1)
            glVertex3f(x1 * radius, y1 * radius, z1 * radius)
            
            glNormal3f(x2, y2, z2)
            glVertex3f(x2 * radius, y2 * radius, z2 * radius)
        glEnd()

#Dibujar cilindro con GLUT
def dibujar_cilindro(radius, height=2.0):
    """Dibuja un cilindro usando gluCylinder de GLU"""
    quadric = gluNewQuadric()
    gluCylinder(quadric, radius, radius, height, 30, 30)

def draw_bone():
    """Dibuja un hueso con 4 esferas (2 en cada extremo) y un cilindro"""
    glPushMatrix()
    
    glColor3f(0.95, 0.95, 0.85)  # color hueso
    
    # Extremo izquierdo
    glPushMatrix()
    glTranslatef(-1.0, 0.2, 0)   # primera esfera izquierda
    draw_sphere(0.35, 30, 30)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-1.0, -0.2, 0)  # segunda esfera izquierda 
    draw_sphere(0.35, 30, 30)
    glPopMatrix()
    
    # Extremo derecho
    glPushMatrix()
    glTranslatef(1.0, 0.2, 0)    # primera esfera derecha
    draw_sphere(0.35, 30, 30)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(1.0, -0.2, 0)   # segunda esfera derecha 
    draw_sphere(0.35, 30, 30)
    glPopMatrix()
    
    # Cilindro central
    glPushMatrix()
    glTranslatef(-1.0, 0, 0)    
    glRotatef(90, 0, 1, 0)      
    dibujar_cilindro(0.2, 2.0)
    glPopMatrix()
    
    glPopMatrix()



def setup_lighting():
    """Configura iluminación básica para la escena"""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    
    light_position = [1.0, 1.0, 1.0, 0.2]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)


def main():
    global rotation
    
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Hueso con esferas y cilindro", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glClearColor(0.7, 0.8, 0.9, 1.0)
    setup_lighting()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -6)
        
        # Rotación de la escena
        rotation += 0.5
        glRotatef(rotation, 0, 1, 0) 
        
        draw_bone()
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()

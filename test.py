from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Cube vertices
vertices = [
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, -1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

# Cube edges
edges = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 4],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7]
]

def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 0, -10, 0, 0, 0, 0, 1, 0)  # Set the camera position
    glColor3f(1.0, 0.0, 0.0)  # Set color to red
    glRotatef(30, 1, 1, 1)  # Rotate the cube
    draw_cube()
    glFlush()

def main():
    glutInit()
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"OpenGL Cube")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()

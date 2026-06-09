from OpenGL.GL import *
from PySide6.QtOpenGLWidgets import QOpenGLWidget


class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(640, 480)
        self.pos_x = 100.0
        self.pos_y = 100.0

    def set_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.update()

    def initializeGL(self):
        glClearColor(0.2, 0.3, 0.3, 1.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # простая отрисовка квадрата
        glLoadIdentity()
        glOrtho(0, self.width(), self.height(), 0, -1, 1)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(self.pos_x, self.pos_y)
        glVertex2f(self.pos_x + 50, self.pos_y)
        glVertex2f(self.pos_x + 50, self.pos_y + 50)
        glVertex2f(self.pos_x, self.pos_y + 50)
        glEnd()

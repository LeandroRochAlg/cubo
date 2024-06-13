import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Define o caminho da imagem
imagem = 'img\Image.jpeg'

# Define os vértices do cubo
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

# Define as arestas do cubo
edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

# Define as faces do cubo
surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

# Coordenadas da textura
texture_coords = (
    (0, 0),
    (1, 0),
    (1, 1),
    (0, 1)
)

# Carrega a textura
def load_texture():
    texture_surface = pygame.image.load(imagem)
    texture_data = pygame.image.tostring(texture_surface, 'RGB', 1)
    width = texture_surface.get_width()
    height = texture_surface.get_height()
    
    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id

# Desenha o cubo com a textura
def Cube(texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for surface in surfaces:
        for i, vertex in enumerate(surface):
            glTexCoord2fv(texture_coords[i])
            glVertex3fv(vertices[vertex])
    glEnd()

# Função principal
def main():
    pygame.init()
    display = (600, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    scaling_factor = [1.0, 1.0, 1.0]
    rotation_angle_x = 0
    rotation_angle_y = 0
    mouse1_down = False
    mouse2_down = False
    last_pos = None

    texture_id = load_texture()

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    scaling_factor[0] *= 1.1
                    scaling_factor[1] *= 1.1
                    scaling_factor[2] *= 1.1
                elif event.button == 5:  # Scroll down
                    scaling_factor[0] *= 0.9
                    scaling_factor[1] *= 0.9
                    scaling_factor[2] *= 0.9
                elif event.button == 1:  # Left mouse button down
                    mouse1_down = True
                    last_pos = pygame.mouse.get_pos()
                elif event.button == 3:  # Right mouse button down
                    mouse2_down = True
                    last_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button up
                    mouse1_down = False
                elif event.button == 3:  # Right mouse button up
                    mouse2_down = False
            elif event.type == pygame.MOUSEMOTION:
                if mouse1_down:
                    x, y = pygame.mouse.get_pos()
                    dx = x - last_pos[0]
                    dy = y - last_pos[1]
                    rotation_angle_x += dy * 0.2
                    rotation_angle_y += dx * 0.2
                    last_pos = (x, y)
                elif mouse2_down:
                    x, y = pygame.mouse.get_pos()
                    dx = x - last_pos[0]
                    dy = y - last_pos[1]
                    glTranslatef(dx * 0.01, -dy * 0.01, 0)
                    last_pos = (x, y)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()  # Save the current matrix
        glScalef(scaling_factor[0], scaling_factor[1], scaling_factor[2])
        glRotatef(rotation_angle_x, 1, 0, 0)
        glRotatef(rotation_angle_y, 0, 1, 0)
        
        Cube(texture_id)
        
        glPopMatrix()  # Restore the previous matrix
        
        pygame.display.flip()
        pygame.time.wait(10)

main()

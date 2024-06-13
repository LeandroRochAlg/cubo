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
    superficieTextura = pygame.image.load(imagem)
    infoTextura = pygame.image.tostring(superficieTextura, 'RGB', 1)
    largura = superficieTextura.get_width()
    altura = superficieTextura.get_height()
    
    # Cria a textura
    glEnable(GL_TEXTURE_2D)
    idTextura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, idTextura)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, largura, altura, 0, GL_RGB, GL_UNSIGNED_BYTE, infoTextura)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return idTextura

# Desenha o cubo com a textura
def Cube(idTextura):
    glBindTexture(GL_TEXTURE_2D, idTextura)
    glBegin(GL_QUADS)
    for surface in surfaces:
        for i, vertex in enumerate(surface):
            glTexCoord2fv(texture_coords[i])
            glVertex3fv(vertices[vertex])
    glEnd()

# Função principal
if __name__ == '__main__':
    pygame.init()
    display = (600, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL) # DOUBLEBUF para evitar flickering e OPENGL para usar OpenGL
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    fatorEscala = [1.0, 1.0, 1.0]
    anguloRotacaoX = 0
    anguloRotacaoY = 0
    clickMouse1 = False
    clickMouse2 = False
    ultimaPos = None

    idTextura = load_texture()

    # Habilita o uso de texturas e o teste de profundidade
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    fatorEscala[0] *= 1.1
                    fatorEscala[1] *= 1.1
                    fatorEscala[2] *= 1.1
                elif event.button == 5:  # Scroll down
                    fatorEscala[0] *= 0.9
                    fatorEscala[1] *= 0.9
                    fatorEscala[2] *= 0.9
                elif event.button == 1:  # Left mouse button down
                    clickMouse1 = True
                    ultimaPos = pygame.mouse.get_pos()
                elif event.button == 3:  # Right mouse button down
                    clickMouse2 = True
                    ultimaPos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button up
                    clickMouse1 = False
                elif event.button == 3:  # Right mouse button up
                    clickMouse2 = False
            elif event.type == pygame.MOUSEMOTION:
                if clickMouse1:
                    x, y = pygame.mouse.get_pos()
                    dx = x - ultimaPos[0]
                    dy = y - ultimaPos[1]
                    anguloRotacaoX += dy * 0.2
                    anguloRotacaoY += dx * 0.2
                    ultimaPos = (x, y)
                elif clickMouse2:
                    x, y = pygame.mouse.get_pos()
                    dx = x - ultimaPos[0]
                    dy = y - ultimaPos[1]
                    glTranslatef(dx * 0.01, -dy * 0.01, 0)
                    ultimaPos = (x, y)
        
        # Limpa o buffer de cor e o buffer de profundidade
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Desenha o cubo na tela
        glPushMatrix()  # Salva a matriz atual
        glScalef(fatorEscala[0], fatorEscala[1], fatorEscala[2])
        glRotatef(anguloRotacaoX, 1, 0, 0)
        glRotatef(anguloRotacaoY, 0, 1, 0)
        
        Cube(idTextura)
        
        glPopMatrix()  # Restaura a matriz salva
        
        pygame.display.flip()
        pygame.time.wait(10)
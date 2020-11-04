import pygame as pg
from math import atan2,pi

pg.init()
FPS = 60
WIDTH , HEIGHT = 600,600
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()

#funcao
def rotate(surface,angle,rect):
    rotated_surface = pg.transform.rotozoom(surface,angle,1).convert_alpha()
    rotated_surface.set_colorkey((0,0,0))
    rotated_rect = rotated_surface.get_rect(center=(300,300))
    rotated_rect.center = rect.center
    return rotated_surface,rotated_rect

#Triangulo
space = pg.image.load("space.jpg").convert()
sprite = pg.image.load("ship1.png").convert_alpha()
sprite = pg.transform.rotate(sprite,-90).convert_alpha()
sprite = pg.transform.scale(sprite,(100,100))
rect = sprite.get_rect()
angle = 0.0

i = 0
loop = True
while loop:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT: loop = False
    #teclado
    keyboard = pg.key.get_pressed()    
    if  keyboard[pg.K_a]: rect.x -= 5
    if  keyboard[pg.K_d]: rect.x += 5
    if  keyboard[pg.K_s]: rect.y += 5
    if  keyboard[pg.K_w]: rect.y -= 5
    #mouse
    mouse_x, mouse_y = pg.mouse.get_pos()
    rel_x, rel_y = mouse_x - rect.centerx, mouse_y - rect.centery
    angle = (180 / pi) * -atan2(rel_y, rel_x)
    # print(angle)
    #girar
    rotacionado,rotacionado_rect = rotate(sprite,angle,rect)
    #printarsd
    screen.blit(space,pg.Rect(0,0,WIDTH,HEIGHT))
    screen.blit(rotacionado,rotacionado_rect)
    pg.display.flip()

pg.quit()
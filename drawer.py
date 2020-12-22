import pygame as py
from pygame import Color, display,draw,Rect,time

#Constantes
WIDTH,HEIGHT = 600,600
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
AMARELO = (255,255,0)
MAGENTA = (255,0,255)
ANIL = (0,255,255)

color_dict = {py.K_1:BLACK, py.K_2:RED, py.K_3:GREEN, py.K_4:BLUE, 
                py.K_5: AMARELO,py.K_6:MAGENTA,py.K_7:ANIL, py.K_8: WHITE}

#variaveis
radius = 10
color = BLACK

#tudo
screen = display.set_mode((WIDTH,HEIGHT))
screen.fill(WHITE)
clock = time.Clock()

loop = True
while loop:
    for event in py.event.get():
        if event.type == py.QUIT: loop = False
        elif event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE: loop = False
            if event.key == py.K_0: screen.fill(WHITE)
            else: color = color_dict.setdefault(event.key, color)
        elif event.type == py.MOUSEBUTTONDOWN:
            if event.button == 4 and radius < 50: radius+=1
            elif event.button == 5 and radius > 1: radius-=1
    clock.tick_busy_loop(60)
    display.set_caption(f'PAINT (FPS:{clock.get_fps()})')
                
    #comandos
    mouse_pos = py.mouse.get_pos()
    mouse_btn = py.mouse.get_pressed(3)

    if mouse_btn[0]:    py.draw.circle(screen,color,mouse_pos,radius)
    if mouse_btn[2]:  py.draw.circle(screen,WHITE,mouse_pos,radius)
    draw.rect(screen,WHITE,Rect(0,0,50,50))
    if not color == WHITE: draw.rect(screen,color,Rect(0,0,radius,radius))
    else: draw.lines(screen,BLACK,False,[(0,radius),(radius,radius),(radius,0)])
    draw.lines(screen,BLACK,False,[(0,50),(50,50),(50,0)])

    #desenhar
    display.flip()
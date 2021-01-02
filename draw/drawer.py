import pygame as py
from pygame import Color,display,draw,Rect,time,mouse,font
from os import path

py.init()

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
CWD = path.dirname(__file__)

color_dict = {py.K_1:BLACK, py.K_2:RED, py.K_3:GREEN, py.K_4:BLUE, 
                py.K_5: AMARELO,py.K_6:MAGENTA,py.K_7:ANIL, py.K_8: WHITE}

#variaveis
radius = 10
color = BLACK

#tudo
screen = display.set_mode((WIDTH,HEIGHT))
screen.fill(WHITE)
clock = time.Clock()
last_mouse_pos = (0,0)
green_flag,red_flag,blue_flag = False,False,False   
fonte = py.font.Font(path.join(CWD,"times-roman.ttf"),50)

loop = True
while loop:
    for event in py.event.get():
        if event.type == py.QUIT: loop = False
        elif event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE: loop = False
            elif event.key == py.K_0: screen.fill(WHITE)
            color = color_dict.get(event.key, color)
            if event.key == py.K_z and event.mod & py.KMOD_CTRL: screen.fill(WHITE)
            #Checar as flags
            elif event.key == py.K_q: red_flag = True
            elif event.key == py.K_w: green_flag = True
            elif event.key == py.K_e: blue_flag = True
        elif event.type == py.KEYUP:
            if event.key == py.K_q: red_flag = False
            elif event.key == py.K_w: green_flag = False
            elif event.key == py.K_e: blue_flag = False 
        elif event.type == py.MOUSEBUTTONDOWN:
            #mudar cores
            if red_flag or blue_flag or green_flag:
                if red_flag:
                    if event.button == 4 and color[0] < 255: color = (color[0]+15,*color[1:])
                    elif event.button == 5 and color[0] > 0: color = (color[0]-15,*color[1:])
                if green_flag:
                    if event.button == 4 and color[1] < 255: color = (color[0],color[1]+15,color[2])
                    elif event.button == 5 and color[1] > 0: color = (color[0],color[1]-15,color[2])
                if blue_flag:
                    if event.button == 4 and color[2] < 255: color = (*color[0:2],color[2]+15)
                    elif event.button == 5 and color[2] > 0: color = (*color[0:2],color[2]-15)
            #outros
            elif event.button == 4 and radius < 50: radius+=1
            elif event.button == 5 and radius > 1: radius-=1
        elif event.type == py.MOUSEBUTTONUP:
            pass
    clock.tick_busy_loop(1200)
    display.set_caption(f'PAINT (FPS:{clock.get_fps():04.2f})')
    draw.rect(screen,WHITE,Rect(0,0,WIDTH,50))

    #comandos
    mouse_pos = mouse.get_pos()
    mouse_btn = mouse.get_pressed(3)
    rectangle = Rect(0,0,radius,radius)
    rectangle.center = (25,25)

    if mouse_btn[0]: 
        draw.circle(screen,color,last_mouse_pos,radius)
        draw.line(screen,color,last_mouse_pos, mouse_pos,2*radius)
        draw.circle(screen,color,mouse_pos,radius)
    if mouse_btn[2]: 
        draw.circle(screen,WHITE,last_mouse_pos,radius)
        draw.line(screen,WHITE,last_mouse_pos, mouse_pos,2*radius)
        draw.circle(screen,WHITE,mouse_pos,radius)
    draw.rect(screen,WHITE,Rect(0,0,50,50))
    if not color == WHITE: draw.rect(screen,color,rectangle)
    else: draw.rect(screen,BLACK,rectangle,1)
    draw.lines(screen,BLACK,False,[(0,50),(50,50),(50,0)])

    #desenhar
    rectangle = Rect(0,0,51,51)
    rectangle.x = 50
    number = 1
    for colors in color_dict.values():
        rectangle.move_ip(50,0)
        if not colors == BLACK and not colors == WHITE:
            draw.rect(screen,colors,rectangle)
            screen.blit(fonte.render(f"{number}",True,BLACK),rectangle.midtop)
        elif colors == BLACK:
            draw.rect(screen,BLACK,rectangle)
            screen.blit(fonte.render(f"{number}",True,WHITE),rectangle.midtop)
        else:
            draw.rect(screen,BLACK,rectangle,1)
            screen.blit(fonte.render(f"{number}",True,BLACK),rectangle.midtop)
        number+=1
    screen.blit(fonte.render(f'{0}',True,BLACK),Rect(WIDTH-38,0,50,50))
    draw.line(screen,RED,(WIDTH,0),(WIDTH-50,50),5)
    draw.line(screen,RED,(WIDTH-50,0),(WIDTH,50),5)

    display.flip()
    last_mouse_pos = mouse.get_pos()

py.quit()
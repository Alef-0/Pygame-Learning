import pygame as py
from pygame import Color,display,draw,Rect,time,mouse,font,event,sprite,surface
from os import path

py.init()

#Constantes
WIDTH,HEIGHT = 600,600
WHITE = Color(255,255,255)
RED = Color(255,0,0)
GREEN = Color(0,255,0)
BLUE = Color(0,0,255)
BLACK = Color(0,0,0)
YELLOW = Color(255,255,0)
MAGENTA = Color(255,0,255)
ANIL = Color(0,255,255)
CWD = path.dirname(__file__)

class Base(sprite.Sprite):
    image : surface.Surface
    rect : Rect
    def __init__(self,groups):
        sprite.Sprite.__init__(self,groups)

color_dict = {py.K_1:BLACK, py.K_2:RED, py.K_3:GREEN, py.K_4:BLUE, 
                py.K_5: YELLOW,py.K_6:MAGENTA,py.K_7:ANIL, py.K_8: WHITE}

#variaveis
radius = 10
color = Color(0,0,0)
screen = display.set_mode((WIDTH,HEIGHT))
clock = time.Clock()
last_mouse_pos = (0,0)
green_flag,red_flag,blue_flag = False,False,False   
button_1_flag, button_2_flag = False,False
fonte = font.SysFont("Times New Roman",15)
numeros = font.SysFont("Times New Roman",50)
fonte.bold = True
loop = True

#canvas

group = sprite.LayeredUpdates()
class Canvas(Base):
    def __init__(self,*groups):
        Base.__init__(self,groups)
        self.image = surface.Surface((600,600))
        self.rect = self.image.get_rect(topleft=(0,0))
        self.image.fill(WHITE)
canvas = Canvas(group)
class Cursor(Base):
    def __init__(self,*groups):
        _layer = 2
        Base.__init__(self,groups)
        self.image = surface.Surface((50,50))
        self.image.fill(WHITE)
        draw.circle(self.image,BLACK,(25,25),radius,1)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center = mouse.get_pos())

    def update(self):
        self.rect.center = mouse.get_pos()
        self.image.fill(WHITE)
        draw.circle(self.image,BLACK,(25,25),radius,1)
cursor = Cursor(group)
class Menu(Base):
    def __init__(self,*groups):
        _layer = 3
        Base.__init__(self,groups)
        self.image = surface.Surface((600,50))
        self.rect = self.image.get_rect(topleft=(0,0))
        self.image.fill(WHITE)
        #desenhar quadrados
        start = 145
        for cores in color_dict.values():
            if cores != BLACK and cores != WHITE: 
                draw.rect(self.image, cores, Rect((start,0),(50,50)))
                self.image.blit(numeros.render(f'{int((start-95)/50)}',True,BLACK),(start+25,0))
            elif cores == WHITE: 
                self.image.blit(numeros.render(f'{int((start-95)/50)}',True,BLACK),(start+25,0))
            else: 
                draw.rect(self.image, BLACK, Rect(start,0,50,50))
                self.image.blit(numeros.render(f'{int((start-95)/50)}',True,WHITE),(start+25,0))
            draw.rect(self.image, BLACK, Rect(start,0,50,50), 1)
            start+=50
        draw.line(self.image,RED,(550,0),(600,50),5)
        draw.line(self.image,RED,(600,0),(550,50),5)
        draw.rect(self.image, BLACK, Rect(550,0,50,50), 1)
        self.image.blit(numeros.render(f'{0}',True,BLACK),(563,0))
    def update(self):
        draw.rect(self.image,WHITE,Rect((0,0),(150,50)))
        draw.circle(self.image,color,(26,25),radius) #Um pixel a esquerda para ficar mais bonito
        draw.circle(self.image,BLACK,(26,25),radius,1)
        #Valores
        self.image.blit(fonte.render(f'(Q) R = {color.r :3}',True,RED),Rect((55,0),(50,50)))
        self.image.blit(fonte.render(f'(W) G = {color.g :3}',True,GREEN),Rect((55,15),(50,50)))
        self.image.blit(fonte.render(f'(E) B = {color.b :3}',True,BLUE),Rect((55,30),(50,50)))
menu = Menu(group)
#Tudo

while loop:
    #eventos
    for evento in event.get():
        if evento.type == py.QUIT: loop = False
        elif evento.type == py.MOUSEBUTTONDOWN:
            if evento.button == 1: button_1_flag = True; last_mouse_pos = mouse.get_pos()
            elif evento.button == 3: button_2_flag = True; last_mouse_pos = mouse.get_pos()
            elif red_flag or blue_flag or green_flag:
                if evento.button == 4: add = 15
                elif evento.button == 5: add = -15
                else: add = 0
                #calcular
                if red_flag and color.r + add <= 255 and  color.r + add >= 0: color.r += add
                if green_flag and color.g + add <= 255 and  color.g + add >= 0: color.g += add
                if blue_flag and color.b + add <= 255 and  color.b + add >= 0: color.b += add         
            elif evento.button == 4: 
                if radius < 25: radius+=1
            elif evento.button == 5: 
                if radius > 1: radius-=1
        elif evento.type == py.MOUSEBUTTONUP:
            if evento.button == 1: button_1_flag = False
            elif evento.button == 3: button_2_flag = False
        elif evento.type == py.KEYDOWN:
            if evento.key == py.K_0: canvas.image.fill(WHITE)
            elif evento.key == py.K_q: red_flag = True
            elif evento.key == py.K_w: green_flag = True
            elif evento.key == py.K_e: blue_flag = True
            else: color = Color(color_dict.get(evento.key,color))
        elif evento.type == py.KEYUP:
            if evento.key == py.K_q: red_flag = False
            elif evento.key == py.K_w: green_flag = False
            elif evento.key == py.K_e: blue_flag = False
    #update
    clock.tick()
    group.update()
    display.set_caption(f'Draw game')
    #Draw:
    mouse_pos = mouse.get_pos()
    if button_1_flag:
        if last_mouse_pos == mouse_pos: draw.circle(canvas.image,color,last_mouse_pos,radius-2) # O -2 suaviza as linhas
        else: draw.line(canvas.image,color,last_mouse_pos,mouse_pos,radius*2)
    elif button_2_flag:
        if last_mouse_pos == mouse_pos: draw.circle(canvas.image,WHITE,last_mouse_pos,radius-2) # O -2 suaviza as linhas
        else: draw.line(canvas.image,WHITE,last_mouse_pos,mouse_pos,radius*2)
    last_mouse_pos = mouse_pos
    group.draw(screen)
    display.flip()

py.quit()
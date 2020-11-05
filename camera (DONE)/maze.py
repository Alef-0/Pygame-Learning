import pygame as pg
from os import path
from math import pi,atan2

from pygame.transform import rotate
import create
pg.init()

#constantes
WIDTH_SCREEN,HEIGHT_SCREEN = 600,600
width, height = 15,15
CWD = path.dirname(__file__)
FRICTION = -0.1
TILE = 40
FPS = 60
screen = pg.display.set_mode((WIDTH_SCREEN,HEIGHT_SCREEN))

#grupos
all_sprites = pg.sprite.LayeredUpdates()
paredes = pg.sprite.Group()
goals = pg.sprite.Group()

#sprites
floor = pg.transform.scale(pg.image.load(path.join(CWD,"floor.jpg")),(100,100)).convert()
cheese = pg.transform.scale(pg.image.load(path.join(CWD,"cheese.png")),(TILE,TILE)).convert_alpha()
cheese.set_colorkey((255,255,255))
mouse = pg.transform.scale(pg.image.load(path.join(CWD,"mouse.png")),(25,25)).convert_alpha()
bricks = pg.transform.scale(pg.image.load(path.join(CWD,"bricks.png")),(TILE,TILE)).convert_alpha()

#funcoes

#Sprites
class Player(pg.sprite.Sprite):
    def __init__(self,pos,*grupos):
        self._layer = 2
        super().__init__(grupos)
        self.original = mouse
        self.image = mouse
        self.rect = self.image.get_rect(topleft=pos)
        self.vx = self.vy = 0
        self.angle = 0
    
    def update(self):
        self.accx = self.accy = 0
        keyboard = pg.key.get_pressed()
        if keyboard[pg.K_w]: self.accy -= 0.5
        if keyboard[pg.K_a]: self.accx -= 0.5
        if keyboard[pg.K_s]: self.accy += 0.5
        if keyboard[pg.K_d]: self.accx += 0.5

        #imagem
        rel_x,rel_y = goal.rect.x - self.rect.x,goal.rect.y - self.rect.y
        self.angle = 180/pi * -atan2(rel_y,rel_x)
        self.image = pg.transform.rotozoom((self.original),self.angle+90,1)

        #colisao de paredes
        self.vx += self.accx + self.vx * FRICTION
        if abs(self.vx) < 0.5: self.vx = 0
        self.rect.x += self.vx
        for x in pg.sprite.spritecollide(self,paredes,False):
            if self.vx > 0: self.rect.right = x.rect.left
            if self.vx < 0: self.rect.left = x.rect.right

        self.vy += self.accy + self.vy * FRICTION
        if abs(self.vy) < 0.5: self.vy = 0
        self.rect.y += self.vy
        for x in pg.sprite.spritecollide(self,paredes,False):
            if self.vy < 0: self.rect.top = x.rect.bottom
            if self.vy > 0: self.rect.bottom = x.rect.top
        #goals
        for x in pg.sprite.spritecollide(self,goals,False):
            if self.rect.collidepoint(x.rect.center): global loop; loop = False 
class Parede(pg.sprite.Sprite):
    def __init__(self,pos,*grupos):
        self._layer=2
        super().__init__(grupos)
        self.image = bricks
        self.rect = self.image.get_rect(topleft = pos)
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH_SCREEN / 2)
        y = -target.rect.y + int(HEIGHT_SCREEN / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH_SCREEN), x)  # right
        y = max(-(self.height - HEIGHT_SCREEN), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
class Goal(pg.sprite.Sprite):
    def __init__(self,pos,*grupos):
        self._layer=1
        super().__init__(grupos)
        self.image = cheese
        self.rect = self.image.get_rect(topleft=pos)

#pegar mapa
create.make_map(width,height) 
with open(path.join(CWD,"maze.txt"),"r") as file:
    x,y = 0,0
    first = False
    last_avaiable = (x,y)
    while True:
        linha = file.readline()
        if not linha: break
        for i in linha:
            if i=="|" or i=="-" or i=="+": Parede((x*TILE,y*TILE),all_sprites,paredes)
            elif i==" " and first == False: global player; player = Player((x*TILE,y*TILE),all_sprites); first=True
            elif i==" ": last_avaiable=(x,y)
            x += 1
            if x>width: width = x-1
        y += 1; x = 0
    global goal; goal = Goal((last_avaiable[0]*TILE,last_avaiable[1]*TILE),all_sprites,goals)
    height = y - 1

#Principais
clock = pg.time.Clock()

if TILE*width >= WIDTH_SCREEN or TILE*height >= HEIGHT_SCREEN: camera = Camera(TILE*width,TILE*height)
else: camera = Camera(WIDTH_SCREEN,HEIGHT_SCREEN)

loop = True
while loop:
    clock.tick_busy_loop(FPS)
    pg.display.set_caption(f'Maze (FPS: {clock.get_fps()})')
    for ev in pg.event.get():
        if ev.type == pg.QUIT: loop = False

    #print
    screen.fill((125,125,125))
    for x in range(0,WIDTH_SCREEN,TILE): pg.draw.line(screen,(0,0,0),(x,0),(x,HEIGHT_SCREEN))
    for y in range(0,HEIGHT_SCREEN,TILE): pg.draw.line(screen,(0,0,0),(0,y),(WIDTH_SCREEN,y))

    all_sprites.update()
    camera.update(player)
    for x in range(0,width*TILE,100):
        for y in range(0,height*TILE,100):
            screen.blit(floor, camera.camera.move(pg.Rect(x,y,100,100).topleft))
    for x in all_sprites: screen.blit(x.image,camera.apply(x))
    pg.display.flip()

pg.quit()
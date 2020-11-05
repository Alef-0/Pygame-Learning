import pygame as pg
from pygame.math import Vector2 as v2

WIDTH,HEIGHT = 600,600
FPS = 60
pg.init()
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()

#bola
class Box(pg.sprite.Sprite):
    image = pg.Surface((0,0))
    rect = pg.Rect(0,0,0,0)

    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50,50))
        self.image.set_colorkey((0,0,0))
        pg.draw.circle(self.image,radius=25,center=(25,25),color=(255,0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (10,10)
        self.mask = pg.mask.from_surface(self.image)
box = Box()

#quadrado
class Player(pg.sprite.Sprite):
    image = pg.Surface((0,0))
    rect = pg.Rect(0,0,0,0)

    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50,50))
        self.image.set_colorkey((0,0,0))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (350,300)
        self.mask = pg.mask.from_surface(self.image)
player = Player()

loop = True
acceleration = v2(0,1)
velocity = v2(0,0)
vx,vy = 5,5
while loop:
    keyboard = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT: loop = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and player.rect.bottom==HEIGHT: velocity.y = -20
    clock.tick_busy_loop(FPS)
    pg.display.set_caption(f"{clock.get_fps()}")

    acceleration = v2(0,0.9)
    if keyboard[pg.K_a]:   acceleration.x -= 10
    if keyboard[pg.K_d]:   acceleration.x += 10

    velocity.x += acceleration.x + -1*velocity.x
    velocity.y += acceleration.y
    player.rect.move_ip(velocity)
    if player.rect.left < 0: player.rect.left = 0
    if player.rect.right > WIDTH: player.rect.right = WIDTH
    if player.rect.bottom > HEIGHT: player.rect.bottom = HEIGHT
    if player.rect.top < 0 : player.rect.top = 0
    
    if pg.sprite.collide_mask(player,box):
        if abs(player.rect.bottom - box.rect.top) <= 10 or velocity.y > 0:  player.rect.bottom = box.rect.top; velocity.y = -20
        if abs(player.rect.top - box.rect.bottom) <= 10:  box.rect.bottom = player.rect.top
        if abs(player.rect.right - box.rect.left) <= 10:  box.rect.left = player.rect.right
        if abs(player.rect.left - box.rect.right) <= 10:  box.rect.right = player.rect.left

    #colisao
    box.rect.x += vx
    box.rect.y += vy

    #colisao com box
    if pg.sprite.collide_mask(player,box):
        if abs(player.rect.top - box.rect.bottom) <= 10: vy*=-1; box.rect.bottom = player.rect.top
        if abs(player.rect.bottom - box.rect.top) <= 10: vy*=-1; box.rect.top = player.rect.bottom
        if abs(player.rect.right - box.rect.left) <= 10: vx*=-1; box.rect.left = player.rect.right
        if abs(player.rect.left - box.rect.right) <= 10: vx*=-1; box.rect.right = player.rect.left

    if box.rect.left <= 0: vx*=-1; box.rect.left = 0
    if box.rect.right >= WIDTH: vx*=-1; box.rect.right = WIDTH
    if box.rect.top <= 0: vy*=-1; box.rect.top = 0
    if box.rect.bottom >= HEIGHT: vy*=-1; box.rect.bottom = HEIGHT

    
    
    screen.fill((255,255,255))
    screen.blit(box.image,box.rect)
    screen.blit(player.image,player.rect)

    pg.display.flip()

pg.quit()

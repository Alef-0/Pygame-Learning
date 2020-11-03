import pygame as pg

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

vx,vy = 5,-5
loop = True
while loop:
    keyboard = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT: loop = False
    clock.tick(FPS)

    if keyboard[pg.K_a]:   player.rect.x -= 5
    if keyboard[pg.K_d]:   player.rect.x += 5
    if keyboard[pg.K_s]:   player.rect.y += 5
    if keyboard[pg.K_w]:   player.rect.y -= 5
    
    #colisao
    box.rect.x += vx
    box.rect.y += vy

    if box.rect.right >= WIDTH or box.rect.left <= 0: vx*=-1
    if box.rect.top <= 0 or box.rect.bottom >= HEIGHT: vy*=-1
    #colisao com box
    if pg.sprite.collide_mask(player,box):
        if abs(player.rect.top - box.rect.bottom) <= 10: vy*=-1; box.rect.bottom = player.rect.top
        if abs(player.rect.bottom - box.rect.top) <= 10: vy*=-1; box.rect.top = player.rect.bottom
        if abs(player.rect.right - box.rect.left) <= 10: vx*=-1; box.rect.left = player.rect.right
        if abs(player.rect.left - box.rect.right) <= 10: vx*=-1; box.rect.right = player.rect.left
    
    
    screen.fill((255,255,255))
    screen.blit(box.image,box.rect)
    screen.blit(player.image,player.rect)

    pg.display.flip()

pg.quit()

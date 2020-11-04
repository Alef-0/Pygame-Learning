import pygame as pg
from math import atan2,pi
from pygame.math import Vector2
from os import path
from random import randint

pg.init()
FPS = 60
BASE_SPEED = Vector2((5,0))
BULLET_SPEED = Vector2((10,0))
STOP_SPEED = Vector2((0,0))
ASTEROID_SPEED = Vector2((0,3))
CWD = path.dirname(path.realpath(__file__))
WIDTH , HEIGHT = 600,600
OBSTACLES_QUANTITY = 8
LAYER_PROJECTILE,LAYER_TEXT,LAYER_PLAYER = 2,1,3
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
asteroids_killed = 0

#Pegar Sprites
space = pg.image.load(path.join(CWD,"space.jpg"))
player_sprite = pg.image.load(path.join(CWD,"ship1.png"))
player_sprite = pg.transform.rotate(player_sprite,-90).convert_alpha() #Gira a imagem
player_sprite = pg.transform.scale(player_sprite,(80,80))
asteroid_sprite = pg.transform.scale(pg.image.load(path.join(CWD,"asteroid.png")),(50,50)).convert_alpha()
fonte = pg.font.Font(path.join(CWD,"SPACE.ttf"),16)


#funcao
def rotate(surface,angle,rect):
    rotated_surface = pg.transform.rotozoom(surface,angle,1).convert_alpha()
    rotated_rect = rotated_surface.get_rect(center=rect.center)
    return rotated_surface,rotated_rect

def calculate_angle(rect):
    mouse_x, mouse_y = pg.mouse.get_pos()
    rel_x, rel_y = mouse_x - rect.centerx, mouse_y - rect.centery
    return (180 / pi) * -atan2(rel_y, rel_x)

class Bullet(pg.sprite.Sprite):
    image = pg.Surface((0,0))
    rect = pg.Rect(0,0,0,0)
    def __init__(self,angle,speed,rect,*grupos):
        self._layer = LAYER_PROJECTILE
        super().__init__(grupos)
        global CWD
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(path.join(CWD,"triangulo.png")),(15,15)),angle).convert_alpha()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center = rect.move(Vector2(rect.height//2,0).rotate(-angle)).center)
        self.speed = speed.rotate(-angle)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.rect.topleft += self.speed
        for _ in pg.sprite.groupcollide(bullets,obstacles,True,True,pg.sprite.collide_mask):
            Obstacle(all_sprites,obstacles)
            global asteroids_killed; asteroids_killed += 1
        if not screen.get_rect().collidepoint(self.rect.center): self.kill()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, *grupos):
        self._layer = LAYER_PROJECTILE
        super().__init__(grupos)
        self.original = self.image = asteroid_sprite
        self.rect = self.image.get_rect()
        self.rect.center = (randint(25,WIDTH-25),randint(-1000,-50))
        self.mask = pg.mask.from_surface(self.image)
        self.base = self.rotation = randint(1,10)

    def update(self):
        self.rotation = (self.rotation + self.base)%360
        self.image,self.rect = rotate(self.original,self.rotation,self.rect)
        self.mask = pg.mask.from_surface(self.image)
        if pg.sprite.collide_mask(self,player): player.kill()
        if self.rect.top>HEIGHT: 
            self.kill()
            Obstacle(obstacles,all_sprites)
        self.rect.move_ip(ASTEROID_SPEED)
    
class Player(pg.sprite.Sprite):
    speed = Vector2(0,0)

    def __init__(self,pos,*grupos):
        self._layer = LAYER_PLAYER
        super().__init__(grupos)
        self.original = player_sprite.convert_alpha()
        self.image = self.original
        self.rect = self.image.get_rect(center=pos)
        self.mask = pg.mask.from_surface(self.image)
        self.speed = Vector2(0,0)
    
    def update(self):
        angle = calculate_angle(self.rect)
        if not self.rect.move(self.speed).collidepoint(pg.mouse.get_pos()): self.rect = self.rect.move(self.speed)
        self.image, self.rect = rotate(self.original,angle,self.rect)
        self.mask = pg.mask.from_surface(self.image)

class Texto(pg.sprite.Sprite):
    def __init__(self,fonte):
        self._layer = LAYER_TEXT
        super().__init__()
        self.fonte = fonte
    
    def update(self):
        self.image = self.fonte.render(f"Pontos: {asteroids_killed}",True,(255,255,255))
        self.rect = self.image.get_rect()


bullets = pg.sprite.Group()
obstacles = pg.sprite.Group()
all_sprites = pg.sprite.LayeredUpdates()

player = Player((WIDTH//2,HEIGHT//2),all_sprites)
all_sprites.add(Texto(fonte))
for i in range(OBSTACLES_QUANTITY): Obstacle(obstacles,all_sprites)


#event tester
SOUNDEND = pg.event.custom_type()
som = pg.mixer.Sound(path.join(CWD,"Shoot_02.wav"))
pg.mixer.music.load(path.join(CWD,"Hardmoon_-_Deep_space.ogg"))
som.set_volume(0.09)
pg.mixer.music.play()
#Walking

i = 0
loop = True
pg.key.set_repeat(1)

while loop:
    clock.tick_busy_loop(FPS)
    pg.display.set_caption(f'ASTEROIDS (FPS:{clock.get_fps()})')
    angle = calculate_angle(player.rect)

    for event in pg.event.get():
        if event.type == pg.QUIT: loop = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: 
            som.play()
            Bullet(angle,BULLET_SPEED,player.rect,bullets,all_sprites)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_w: player.speed = BASE_SPEED.rotate(-angle)
            elif event.key == pg.K_a: player.speed = BASE_SPEED.rotate(-angle).rotate(-90)
            elif event.key == pg.K_d: player.speed = BASE_SPEED.rotate(-angle).rotate(90)
            elif event.key == pg.K_s: player.speed = -1 * BASE_SPEED.rotate(-angle)
        elif event.type == pg.KEYUP:
            if event.key == pg.K_w: player.speed = STOP_SPEED
            elif event.key == pg.K_s: player.speed = STOP_SPEED
            elif event.key == pg.K_a: player.speed = STOP_SPEED
            elif event.key == pg.K_d: player.speed = STOP_SPEED

    #printar
    screen.blit(space,pg.Rect(0,0,WIDTH,HEIGHT))

    all_sprites.update()
    all_sprites.draw(screen)

    pg.display.flip()
    if not player.alive(): loop = False

pg.quit()
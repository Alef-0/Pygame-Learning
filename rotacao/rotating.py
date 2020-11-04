import pygame as pg
from math import atan2,pi
from pygame.math import Vector2
from os import path

pg.init()
FPS = 60
cwd = path.dirname(path.realpath(__file__))
WIDTH , HEIGHT = 600,600
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()

#funcao
def rotate(surface,angle,rect):
    rotated_surface = pg.transform.rotozoom(surface,angle,1).convert_alpha()
    rotated_surface.set_colorkey((0,0,0))
    rotated_rect = rotated_surface.get_rect(center=rect.center)
    return rotated_surface,rotated_rect
def calculate_angle():
    mouse_x, mouse_y = pg.mouse.get_pos()
    rel_x, rel_y = mouse_x - rect.centerx, mouse_y - rect.centery
    return (180 / pi) * -atan2(rel_y, rel_x)
class Bullet(pg.sprite.Sprite):
    image = pg.Surface((0,0))
    rect = pg.Rect(0,0,0,0)
    def __init__(self,angle,speed,rect):
        super().__init__()
        global cwd
        self.image = pg.transform.rotozoom(pg.transform.scale(pg.image.load(path.join(cwd,"triangulo.png")),(20,20)),angle,1).convert_alpha()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center=rect.center+Vector2(rect.height//2,0).rotate(-angle))
        self.speed = speed.rotate(-angle)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.rect.topleft += self.speed
        if self.rect.right<0: self.kill()
        if self.rect.left>WIDTH: self.kill()
        if self.rect.top>HEIGHT: self.kill()
        if self.rect.bottom<0: self.kill()

bullets = pg.sprite.Group()

#sprites
space = pg.image.load(path.join(cwd,"space.jpg"))
sprite = pg.image.load(path.join(cwd,"ship1.png"))
sprite = pg.transform.rotate(sprite,-90).convert_alpha() #Gira a imagem
sprite = pg.transform.scale(sprite,(100,100))
rect = sprite.get_rect(center=(300,300))
angle = 0.0


#event tester
SOUNDEND = pg.event.custom_type()
som = pg.mixer.Sound(path.join(cwd,"Shoot_02.wav"))
music = path.join(cwd,"Shoot_02.wav")

#Walking
base_speed = Vector2((5,0))
bullet_speed = Vector2((10,0))
stop_speed = Vector2((0,0))
speed = Vector2((0,0))

i = 0
loop = True
pg.key.set_repeat(1)

while loop:
    clock.tick_busy_loop(FPS)
    angle = calculate_angle()

    for event in pg.event.get():
        if event.type == pg.QUIT: loop = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: 
            som.play()
            bullets.add(Bullet(angle,bullet_speed,rect))
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w: speed = base_speed.rotate(-angle)
            if event.key == pg.K_s: speed = -1/2 * base_speed.rotate(-angle)
        if event.type == pg.KEYUP:
            if event.key == pg.K_w: speed = stop_speed
            if event.key == pg.K_s: speed = stop_speed

    #movimento
    mouse=pg.mouse.get_pos()

    if not rect.collidepoint(mouse):
        rect.centerx += int(speed[0])
        rect.centery += int(speed[1])
        if rect.collidepoint(mouse):
            rect.centerx -= int(speed[0])
            rect.centery -= int(speed[1])


    #girar
    rotacionado,rotacionado_rect = rotate(sprite,angle,rect)
    #printar
    screen.blit(space,pg.Rect(0,0,WIDTH,HEIGHT))
    screen.blit(rotacionado,rotacionado_rect)

    bullets.update()
    bullets.draw(screen)
    pg.display.flip()

pg.quit()
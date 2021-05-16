import pygame
from random import randint
from typing import List
from os import path

pygame.init()

WIDTH,HEIGHT = 600, 600
FONTSIZE = 20
FRUITQUANTITY = 3
FPS = 15
WAITTIME = 10
SPEED = 10

#quantidade, max quantity
total_fruits = 0
max_fruits = (HEIGHT-FONTSIZE)*WIDTH

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
cwd = path.dirname(path.realpath(__file__))
chomp = pygame.mixer.Sound(path.join(cwd, "pacman_eatfruit.wav"))

class Body(pygame.sprite.Sprite):
    def __init__(self,w,h,color,x,y, *grupos):
        super().__init__(grupos)
        self.image = pygame.Surface((w,h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

class Snake():
    segmentos : List[Body] = []
    tail = pygame.sprite.Group()
    come = 0

    def __init__(self, *grupos):
        self.grupos = grupos
        super().__init__()
        self.head = Body(10,10,(0,255,0),40,10+FONTSIZE,self.grupos)
        self.segmentos.append(self.head)
        self.segmentos.append(Body(10,10,(255,255,255),30,10+FONTSIZE,self.grupos,self.tail))
        self.segmentos.append(Body(10,10,(255,255,255),20,10+FONTSIZE,self.grupos,self.tail))
        #colisoes
        self.vx,self.vy = 10,0

    def update(self,fruits):
        global max_fruits,total_fruits, loop, pontos
        #Checa se possui uma fruta
        if pygame.sprite.spritecollide(self.head,fruits,True):
            chomp.play()
            self.segmentos.append(Body(10,10,(255,255,255),0,0,self.grupos,self.tail))
            if (total_fruits < max_fruits): Fruit(player_sprites,fruits,all_sprites); total_fruits += 1
            pontos += 1
        if pontos >= max_fruits: loop = False
        #Move os segmentos
        for i in range(len(self.segmentos)-1,0,-1): self.segmentos[i].rect.topleft = self.segmentos[i-1].rect.topleft
        #Move a cabeça
        self.head.rect.x += self.vx
        self.head.rect.y += self.vy
        #Faz ela dar um loop
        if self.head.rect.x < 0 : self.head.rect.x = WIDTH-10
        if self.head.rect.y < FONTSIZE : self.head.rect.y = HEIGHT-10
        if self.head.rect.x >= WIDTH : self.head.rect.x = 0
        if self.head.rect.y >= HEIGHT: self.head.rect.y = FONTSIZE
        #Checa se colide com a cauda
        if pygame.sprite.spritecollide(self.head,self.tail,True): loop = False

class Fruit(pygame.sprite.Sprite):
    def __init__(self,player,fruits,*grupos):
        super().__init__()
        self.image = pygame.Surface((10,10))
        self.image.fill((255,0,0))
        self.rect = pygame.Rect((0,0),(10,10))
        while True:
            self.rect.topleft = randint(0,(WIDTH-10)//10)*10, randint(FONTSIZE//10,(HEIGHT-10)//10)*10
            if not(pygame.sprite.spritecollide(self,player,False) or pygame.sprite.spritecollide(self,fruits,False)): break
        self.add(fruits, grupos)
        self.start = pygame.time.get_ticks()
        self.wait = randint(0,WAITTIME) + 5
    
    def update(self):
        self.elapsed = pygame.time.get_ticks() - self.start
        if self.elapsed > self.wait * 1000: 
            Fruit(player_sprites,all_sprites,fruits)
            self.kill()

all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
fruits = pygame.sprite.Group()

player = Snake(player_sprites, all_sprites)
for _ in range(min(FRUITQUANTITY,max_fruits)): Fruit(player_sprites,fruits,all_sprites);
total_fruits += FRUITQUANTITY
texto = pygame.font.SysFont("Arial",FONTSIZE,True,True)

pontos = 0
loop = True
button_pressed = False #Evita morte por pressionar dois butoes
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT : pygame.quit(); quit()
        elif (event.type == pygame.KEYDOWN and not button_pressed):
            if (event.key == pygame.K_ESCAPE): loop = False
            if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and player.come != 0: player.vx,player.vy = -SPEED,0; player.come = 2
            if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and player.come != 1: player.vx,player.vy = 0,SPEED; player.come = 3
            if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and player.come != 2: player.vx,player.vy = SPEED,0; player.come = 0
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and player.come != 3: player.vx,player.vy = 0,-SPEED; player.come = 1
            button_pressed = True
    button_pressed = False

    clock.tick_busy_loop(FPS)
    pygame.display.set_caption(f'SNAKE (FPS:{clock.get_fps() :.2f})')

    screen.fill((0,0,0))
    player.update(fruits)
    fruits.update()
    screen.blit(texto.render(f"Pontuacao: {pontos}",True,(255,255,255)),(0,0))
    all_sprites.draw(screen)
    #bordas
    pygame.draw.lines(screen,(255,255,255),True,[(0,FONTSIZE),(WIDTH-1,FONTSIZE),(WIDTH-1, HEIGHT-1),(0, HEIGHT-1)])

    pygame.display.flip()

#mensagem de pontuacao
screen.fill((0,0,0))
texto = pygame.font.SysFont("Arial",27,True,True)
if max_fruits == pontos: 
    frase = f"PONTUACAO MAXIMA! {pontos}"
    screen.blit(texto.render(frase,True,(255,255,255)),(WIDTH//2 - 16*(len(frase)//2),HEIGHT//2-27//2))
else: 
    frase = f"Pontuacao Final: {pontos}"
    screen.blit(texto.render(frase,True,(255,255,255)),(WIDTH//2 - 15*(len(frase)//2),HEIGHT//2-27//2))
pygame.display.flip()

loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: loop = False
        elif event.type == pygame.QUIT: loop = False

pygame.quit()

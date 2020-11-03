import pygame
from random import randint
from math import floor

pygame.init()

WIDTH,HEIGHT = 600, 600
FONTSIZE = 20
FRUITQUANTITY = 3
FPS = 20
WAITTIME = 10

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(f'SNAKE')
clock = pygame.time.Clock()
cwd = path.dirname(path.realpath(__file__))
chomp = pygame.mixer.Sound(path.join(cwd, "pacman_eatfruit.wav"))


class Square(pygame.sprite.Sprite):
    def __init__(self,w,h,color,x,y, *grupos):
        super().__init__(grupos)
        self.image = pygame.Surface((w,h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
class Snake(pygame.sprite.Sprite):
    segmentos = []
    tail = pygame.sprite.Group()
    come = 0

    def __init__(self, *grupos):
        self.grupos = grupos
        super().__init__()
        self.head = Square(10,10,(0,255,0),40,10+FONTSIZE,self.grupos)
        self.segmentos.append(self.head)
        self.segmentos.append(Square(10,10,(255,255,255),30,10+FONTSIZE,self.grupos,self.tail))
        self.segmentos.append(Square(10,10,(255,255,255),20,10+FONTSIZE,self.grupos,self.tail))
        #colisoes
        self.vx,self.vy = 10,0
    def update(self):
        keyboard = pygame.key.get_pressed()
        #muda a velocidade
        if (keyboard[pygame.K_a] or keyboard[pygame.K_LEFT]) and self.come != 0: self.vx,self.vy = -10,0; self.come = 2
        elif (keyboard[pygame.K_s] or keyboard[pygame.K_DOWN]) and self.come != 1: self.vx,self.vy = 0,10; self.come = 3
        elif (keyboard[pygame.K_d] or keyboard[pygame.K_RIGHT]) and self.come != 2: self.vx,self.vy = 10,0; self.come = 0
        elif (keyboard[pygame.K_w] or keyboard[pygame.K_UP]) and self.come != 3: self.vx,self.vy = 0,-10; self.come = 1
        #Checa se possui uma fruta
        if pygame.sprite.spritecollide(self.head,fruits,True):
            chomp.play()
            self.segmentos.append(Square(10,10,(255,255,255),0,0,self.grupos,self.tail))
            fruit = Fruit(player_sprites,fruits,all_sprites)
            fruits.add(fruit)
            global pontos; pontos+=1
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
        #Checa se colide
        if pygame.sprite.spritecollide(self.head,self.tail,False): global loop; loop = False
class Fruit(pygame.sprite.Sprite):
    def __init__(self,player,*grupos):
        super().__init__()
        while True:
            self.fruit = Square(10,10,(255,0,0),randint(0,(WIDTH-10)//10)*10,randint(FONTSIZE//10,(HEIGHT-10)//10)*10)
            if pygame.sprite.spritecollide(self.fruit,player,False) or pygame.sprite.spritecollide(self.fruit,fruits,False): self.fruit.kill()
            else: break
        self.fruit.add(grupos)
        self.start = pygame.time.get_ticks()
        self.image = self.fruit.image
        self.rect = self.fruit.rect
        self.wait = randint(0,WAITTIME) + 5
    
    def update(self):
        self.elapsed = pygame.time.get_ticks() - self.start
        if self.elapsed > self.wait * 1000: 
            fruit = Fruit(player_sprites,all_sprites,fruits)
            fruits.add(fruit)
            self.fruit.kill()
            self.kill()

all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
fruits = pygame.sprite.Group()

player = Snake(all_sprites, player_sprites)
for _ in range(FRUITQUANTITY): fruit = Fruit(player_sprites,fruits,all_sprites); fruits.add(fruit)
texto = pygame.font.SysFont("Arial",FONTSIZE,True,True)
pontos = 0

loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT : pygame.quit(); quit()
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): loop = False

    clock.tick_busy_loop(20)

    screen.fill((0,0,0))
    player.update()
    fruits.update()

    screen.blit(texto.render(f"Pontuacao: {pontos}",True,(255,255,255)),(0,0))
    all_sprites.draw(screen)

    pygame.display.flip()

#mensagem de pontuacao
screen.fill((0,0,0))
texto = pygame.font.SysFont("Arial",27,True,True)
screen.blit(texto.render(f"Pontuacao Final: {pontos}",True,(255,255,255)),(WIDTH//2 - 4*29,HEIGHT//2-27//2))
pygame.display.flip()

loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: loop = False
        elif event.type == pygame.QUIT: loop = False

pygame.quit()

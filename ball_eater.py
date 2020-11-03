import pygame
from random import randint

WIDTH,HEIGHT = 600,600
pygame.init()

class Player(pygame.sprite.Sprite):
    image = pygame.Surface((0,0))
    def __init__(self, *grupos):
        self._layer = 3
        super().__init__(grupos)
        self.image = pygame.Surface((50,50))
        pygame.draw.circle(self.image,color=(255,0,0),radius=25,center=(25,25))
        self.image.set_colorkey((0,0,0))
        self.rect = pygame.Rect((100,100),(50,50))
        self.radius = 25
        self.mask = pygame.mask.from_surface(self.image)
        self.mouse=False
    def update(self):
        mouse = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed(3)
        keyboard = pygame.key.get_pressed()

        if buttons[0] and (self.rect.collidepoint(mouse) or self.mouse): 
            self.rect.center = mouse
            self.mouse = True
        elif not buttons[0]: self.mouse = False

        if keyboard[pygame.K_a]: self.rect.left -= 5
        if keyboard[pygame.K_s]: self.rect.top += 5
        if keyboard[pygame.K_d]: self.rect.left += 5
        if keyboard[pygame.K_w]: self.rect.top -= 5
        #mover
        self.rect.left = max(0,self.rect.left)
        self.rect.top = max(0,self.rect.top)
        self.rect.right = min(WIDTH,self.rect.right)
        self.rect.bottom = min(HEIGHT,self.rect.bottom)
        #colisao
        for x in pygame.sprite.spritecollide(player,fruits,True,pygame.sprite.collide_mask):
            fruit = Fruit(all_sprites,fruits)
            all_sprites.change_layer(fruit,1)
            texto.pontos += 1       
class Fruit(pygame.sprite.Sprite):
    image = pygame.Surface((0,0))
    def __init__(self, *grupos):
        self._layer = 1
        super().__init__(grupos)
        self.image = pygame.Surface((50,50))
        pygame.draw.circle(self.image,color=(0,0,255),radius=25,center=(25,25))
        self.image.set_colorkey((0,0,0))
        self.rect = pygame.Rect((randint(0,WIDTH-50),randint(0,HEIGHT-50)),(50,50))
        self.radius = 25
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        mouse = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed(3)
        keyboard = pygame.key.get_pressed()
        if buttons[2] and keyboard[pygame.K_LSHIFT]: self.rect.center = mouse
class Texto(pygame.sprite.Sprite):
    image = pygame.Surface((0,0))
    def __init__(self, *grupos):
        self._layer = 2
        super().__init__(grupos)
        self.fonte = pygame.font.SysFont("Times New Roman",47,True,True)
        self.pontos = 0
    def update(self):
        self.image = self.fonte.render(f'Pontos {self.pontos}',True,(255,255,255))
        self.rect = self.image.get_rect()
class Camera:
    image = pygame.Surface((0,0))
    def __init__(self,width,height):
        self.width = width 
        self.height = height
        self.rect = pygame.Rect(0,0,width,height)
    def apply(self,target): return target.rect.move(self.rect.topleft)
    def update(self,target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
screen = pygame.display.set_mode((WIDTH,HEIGHT))
loop = True
camera = Camera(WIDTH,HEIGHT)
clock = pygame.time.Clock()

#grupos e sprites
all_sprites = pygame.sprite.LayeredUpdates()
playable = pygame.sprite.Group()
fruits = pygame.sprite.Group()

player = Player(all_sprites,playable)
for _ in range(10): Fruit(all_sprites,fruits)
texto = Texto(all_sprites)

while loop:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: loop = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: loop = False

    clock.tick_busy_loop(60)
    pygame.display.set_caption(f'{clock.get_fps() :.2f}')
    #draw
    all_sprites.update()
    camera.update(player)
    screen.fill((0,0,0))
    for x in all_sprites: screen.blit(x.image,camera.apply(x))

    #flip
    pygame.display.flip()

pygame.quit()
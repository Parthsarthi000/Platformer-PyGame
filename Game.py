import pygame,sys

from random import choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
        self.stand=self.image
        self.walk1=pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        self.walk2=pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.jump=pygame.image.load("graphics/Player/jump.png").convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.bottomleft=(100,300)
        self.animationList=[self.walk1,self.walk2]
        self.animationCounter=0
        self.gravity=0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.jump
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and self.rect.bottom >= 300:
                self.animationCounter += 0.1
                if self.animationCounter >= len(self.animationList): self.animationCounter = 0
                self.image = self.animationList[int(self.animationCounter)]
            else: self.image=self.stand

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Enemy(pygame.sprite.Sprite):

    def __init__(self,type):
        super().__init__()
        if type == "snail":
            self.snail1=pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            self.snail2=pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.animationlist=[self.snail1,self.snail2]
            self.animationCounter=0
            self.image = self.animationlist[self.animationCounter]
            self.rect = self.image.get_rect()
            self.rect.bottomleft=(800, 300)

        elif type == "fly":
            self.fly1=pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            self.fly2=pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.animationlist = [self.fly1, self.fly2]
            self.animationCounter = 0
            self.image = self.animationlist[self.animationCounter]
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (800, 200)

    def update(self):
        self.animate()
        self.rect.x -= 5
        self.destroy()
    def animate(self):
        self.animationCounter+=0.1
        if self.animationCounter >= len(self.animationlist): self.animationCounter = 0
        self.image = self.animationlist[int(self.animationCounter)]
    def destroy(self):
        if self.rect.x<=-100:
            self.kill()
pygame.init()
screen = pygame.display.set_mode((800,468))
clock = pygame.time.Clock()
sky = pygame.image.load("graphics/Sky.png").convert()
ground = pygame.image.load("graphics/ground.png").convert()

player = pygame.sprite.GroupSingle()
player.add(Player())

enemy=pygame.sprite.Group()

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

gamestate=False
def checkcollision():
    global gamestate
    if pygame.sprite.spritecollide(player.sprite,enemy,False):
        enemy.empty()
        gamestate=False

startscreen=pygame.image.load("graphics/img.png")
startscreen_rect=startscreen.get_rect()
startscreen_rect.center=(480,234)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if gamestate == False and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            gamestate=True
        if event.type == obstacle_timer and gamestate == True:
            enemy.add(Enemy(choice(['fly', 'snail', 'fly', 'snail'])))
    if gamestate==True:
        screen.blit(sky,(0,0))
        screen.blit(ground,(0,300))
        player.draw(screen)
        player.update()
        enemy.draw(screen)
        enemy.update()
        checkcollision()
    else:
        screen.fill("Light Blue")
        screen.blit(startscreen,startscreen_rect)
    pygame.display.flip()
    clock.tick(60)
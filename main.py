import pygame
from pygame.locals import *
import random

pygame.init()

klocka = pygame.time.Clock()
fps = 60

screen_width = 500
screen_height = 550

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy bird')


#variablar
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frekvens = 1500 #milisekund
sista_pipe = pygame.time.get_ticks() - pipe_frekvens


#Bilder
bg = pygame.image.load('img/bg.png')
floor_img = pygame.image.load('img/floor.png')


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            #Gravitation
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            print(self.vel)
            if self.rect.bottom < 1080:
                self.rect.y += int(self.vel)

        if game_over == False:
            #Hopp funktion
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False


            #hanterar animationen
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe4.png')
        self.rect = self.image.get_rect()
        hitbox_inflate_x = 0
        hitbox_inflate_y = 1
        #self.pseudo_rect = self.rect.inflate(-, )
        #position 1 är toppen, -1 är under
        self.hitbox = self.rect.inflate(hitbox_inflate_x, hitbox_inflate_y)

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
           self.rect.topleft = [x, y + int(pipe_gap / 2)]


    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()




bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(10, int(screen_height / 2))

bird_group.add(flappy)
bird_group.update()




run = True
while run:

    klocka.tick(fps)

    #bakgreundsbilderna
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    pipe_group.update()

    #marken
    screen.blit(floor_img, (ground_scroll, 500))
    #kollar för krockar
    if pygame.sprite.groupcollide(pipe_group, bird_group, False, False):
        print("Hit!")
        game_over = True


    #kollar när fågeln har nuddat marken
    if flappy.rect.bottom >= 1080:
        game_over = True
        print("Hit!")
        flying = False

    if game_over == False and flying == True:
        #skapar nya pipes
        time_now = pygame.time.get_ticks()
        if time_now - sista_pipe > pipe_frekvens:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(screen_width+500, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width+500, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            sista_pipe = time_now


        #bakgrundsbilderna och skrollning
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 55:
            ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()

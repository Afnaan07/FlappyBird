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

#definerar texten
font = pygame.font.SysFont('Bauhaus 93', 60)

#definerar färger
white = (255, 255, 255)

#variablar
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frekvens = 1500 #milisekund
sista_pipe = pygame.time.get_ticks() - pipe_frekvens
score = 0
pass_pipe = False


#Bilder
bg = pygame.image.load('img/bg.png')
floor_img = pygame.image.load('img/floor.png')
knapp_img = pygame.image.load('img/restartknapp.png')
gameover_img = pygame.image.load('img/gameover.png')

#definerar text, textfärg och textstil
def rita_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#startar om spelet och börjar allt om från början
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird1.0.png')
            self.images.append(img) # addar bilder tiåll list
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


        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
           self.rect.topleft = [x, y + int(pipe_gap / 2)]


    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


    def draw(self):

        action = False

        #Får muspositionen på restartknappen
        pos = pygame.mouse.get_pos()

        #kollar om musen är över knappen
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True


        # ritar kanppen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
class Over():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    #ritar game over
    def draw(self):
        action = False
        screen.blit(self.image, (self.rect.x, self.rect.y))

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(20, int(screen_height / 2))

bird_group.add(flappy)
bird_group.update()

#skapar restartknappen
knapp = Button(screen_width // 2 - 50, screen_height // 2 -100, knapp_img)
over = Over(screen_width // 2 - 270, screen_height // 2 - 200, gameover_img)

run = True
while run:

    klocka.tick(fps)

    #bakgreundsbilderna
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)


    #marken
    screen.blit(floor_img, (ground_scroll, 500))

    #kollar din score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    rita_text(str(score), font, white, int(screen_width/2), 20)


    #kollar för krockar för pipen
    if pygame.sprite.groupcollide(pipe_group, bird_group, False, False) or flappy.rect.top < 0:
        game_over = True


    #kollar när fågeln har nuddat marken
    if flappy.rect.bottom >= 500:
        game_over = True
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
        pipe_group.update()

    #kollar när spelet är över och startar om
    if game_over == True:
        if knapp.draw() == True:
            game_over = False
            score = reset_game()

        if over.draw() == True:
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()

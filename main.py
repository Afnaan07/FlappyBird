import pygame
from pygame.locals import *
import random
from pygame import mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
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
middle_screen_w = screen_width // 2
middle_screen_h = screen_height // 2

#Bilder
bg = pygame.image.load('img/bg.png')
floor_img = pygame.image.load('img/floor.png')
knapp_img = pygame.image.load('img/restartknapp.png')
gameover_img = pygame.image.load('img/gameover.png')
coin_img = pygame.image.load('img/coin.png')

#ljud
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('img/game_over.mp3')
game_over_fx.set_volume(0.5)
coin_fx = pygame.mixer.Sound('img/coin.wav')
coin_fx.set_volume(0.8)
bg_music_fx = pygame.mixer.Sound('img/bg_music.mp3')
bg_music_fx.set_volume(0.3)
#definerar text, textfärg och textstil
def rita_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#startar om spelet och börjar allt om från början
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(middle_screen_h)
    score = 0
    coin_group.empty()
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bluebird-midflap.png')
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


            #Hopp funktion
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                jump_fx.play()
                self.clicked = True
                self.vel = -8
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

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = coin_img
        self.rect = self.image.get_rect()

        self.rect.center = [x, y]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

coin_group = pygame.sprite.Group() #skapar en grupp som skapar mynt
def spawn_coins():
    if random.randint(1, 150) == 1: #Hur mycket och vart myntet ska spawna
        coin = Coin(screen_width, random.randint(90, screen_height - 90))
        coin_group.add(coin)


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
knapp = Button(middle_screen_w - 50, middle_screen_h -100, knapp_img)
over = Over(middle_screen_w - 270, middle_screen_h - 200, gameover_img)

run = True
while run:

    bg_music_fx.play()
    klocka.tick(fps)

    #bakgreundsbilderna
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    #skapar mynten
    spawn_coins()
    #Ritar mynt
    coin_group.draw(screen)

    if pygame.sprite.spritecollide(flappy, coin_group, True): #kollar om fågeln nuddar mynten
        score += 1
        coin_fx.play()


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
    rita_text(str(score), font, white, int(middle_screen_w), 20)


    #kollar för krockar för pipen
    if pygame.sprite.groupcollide(pipe_group, bird_group, False, False) or flappy.rect.top < 0:
        game_over = True
        flying = False
        game_over_fx.play()


    #kollar när fågeln har nuddat marken
    if flappy.rect.bottom >= 500:
        game_over = True
        flying = False
        game_over_fx.play()

    if game_over == False and flying == True:
        #skapar nya pipes
        time_now = pygame.time.get_ticks()
        if time_now - sista_pipe > pipe_frekvens:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(screen_width+500, int(middle_screen_h) + pipe_height, -1)
            top_pipe = Pipe(screen_width+500, int(middle_screen_h) + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            sista_pipe = time_now


        #bakgrundsbilderna och skrollning
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 55:
            ground_scroll = 0

        pipe_group.update()

        #updaterar mynt
        coin_group.update()

    #kollar när spelet är över och startar om
    if game_over == True:
        bg_music_fx.stop()
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

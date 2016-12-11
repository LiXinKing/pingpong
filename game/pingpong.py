import pygame
from random import *
from pygame.locals import *
from pygame.font import *


class MyPlayer(pygame.sprite.Sprite):
    def __init__(self, image_file, location, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.status = True

    def move(self):
        global score, score_font, score_surf
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0:
            self.speed[1] = -self.speed[1]
            score = score + 1
            # score_surf = score_font.render(str(score), 1, (0, 0, 0))
        if self.rect.bottom > height:
            # Game over
            self.status = False


class Reflector(pygame.sprite.Sprite):
    def __init__(self, image_file, location, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed

    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = -self.speed[1]


def animate(players):
    screen.fill([255, 255, 255])
    for player in players:
        player.move()
    for player in players:
        players.remove(player)
        if pygame.sprite.spritecollide(player, players, False):
            # player.speed[0] = -player.speed[0]
            player.speed[1] = -player.speed[1]

        players.add(player)
        player.move()
        screen.blit(player.image, player.rect)
    pygame.display.flip()
    pygame.time.delay(10)


def end():
    # 1
    final_text = "Game Over!"
    ft_font = pygame.font.Font(None, 100)
    ft_surf = ft_font.render(final_text, 1, (0, 0, 0))
    screen.blit(ft_surf, [screen.get_width() / 2 - ft_surf.get_width() / 2, 100])
    # 2
    tip_text = "Type any key to continue"
    tip_font = pygame.font.Font(None, 50)
    tip_surf = tip_font.render(tip_text, 1, (0, 0, 0))
    screen.blit(tip_surf, [screen.get_width() / 2 - tip_surf.get_width() / 2, 200])
    # 3
    sc_text = "Your score is " + str(score)
    sc_font = pygame.font.Font(None, 50)
    sc_surf = sc_font.render(sc_text, 1, (0, 0, 0))
    screen.blit(sc_surf, [screen.get_width() / 2 - sc_surf.get_width() / 2, 300])
    pygame.display.flip()


pygame.init()
size = width, height = 600, 500
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_caption("MiaoWa Game")
score = 0
score_pos = [10, 10]
score_font = pygame.font.Font(None, 50)
score_surf = score_font.render(str(score), 1, (0, 0, 0))
img_player = "player.png"
playerSpeed = [choice([-2, 1]), choice([-2, 1])]
player = MyPlayer(img_player, [10, 10], playerSpeed)
players = pygame.sprite.Group()
players.add(player)
img_ref_path = "reflector.png"
ref_pos = [0, 450]
ref_speed = [0, 0]
reflector = Reflector(img_ref_path, ref_pos, ref_speed)
players.add(reflector)
running = True
while running:
    key_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if player.status is True:
            if event.type == pygame.QUIT:
                game.quit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    ref_speed[0] = -2
                elif event.key == K_RIGHT:
                    ref_speed[0] = +2
        if player.status is False:
            #if event.type == pygame.QUIT:
                #pygame.quit()
            #if event.type == KEYDOWN:
            player.rect.topleft = [10, 10]
            player.status = True
            reflector.rect.topleft = [0, 450]
            ref_speed[0] = 0
            score = 0
            # score_surf = score_font.render(str(score), 1, (0, 0, 0))
    if player.status is True:
        animate(players)
        # screen.blit(score_surf, score_pos)
        pygame.display.flip()
    else:
        player.rect.topleft = [10, 10]
        player.status = True
        reflector.rect.topleft = [0, 450]
        ref_speed[0] = 0
        score = 0

    #if player.status is False:
        #end()

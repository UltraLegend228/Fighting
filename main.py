import pygame
import os
import sys
import random

pygame.init()
current_path=os.path.dirname(__file__)
os.chdir(current_path)
WIDTH=1200
HEIGHT=600
FPS=60
#pygame.mixer.music.load('sound/mario.mp3')
#pygame.mixer.music.play(-1)
sc=pygame.display.set_mode((WIDTH, HEIGHT))
clock=pygame.time.Clock()


from load import *


def game_lvl():
    sc.fill("grey")
    fon.update()
    player1_group.update()
    player1_group.draw(sc)
    player2_group.update()
    player2_group.draw(sc)
    pygame.display.update()


class Player1(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.rect.x = 50
        self.rect.bottom = HEIGHT - 40
        self.jump = False
        self.jump_step = -22
        self.frame = 0
        self.timer_anime = 0
        self.anime_idle = True
        self.anime_run = False
        self.anime_atk = False
        self.dir = "right"
        self.hp = 100
        self.flag_damage = False
        self.hp_bar = "blue"
        self.mask_list = []


    def update(self):
        global FPS, player2
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.jump = True
        if key[pygame.K_e] and not self.anime_atk:
            self.frame = 0
            self.anime_idle = False
            self.anime_run = False
            self.anime_atk = True
            self.flag_damage = True
        elif key[pygame.K_d]:
            self.rect.x += 5
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        elif key[pygame.K_a]:
            self.rect.x -= 5
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        else:
            if not self.anime_atk:
                self.anime_idle = True
            self.anime_run = False


        if self.anime_idle:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player1_idle_image) - 1:
                    self.frame = 0
                    if self.anime_atk:
                        self.anime_atk = False
                        self.anime_idle = True
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player1_idle_image[self.frame]
            except:
                self.frame = 0


        if self.anime_run:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player1_run_image) - 1:
                    self.frame = 0
                    if self.anime_atk:
                        self.anime_atk = False
                        self.anime_run = True
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player1_run_image[self.frame]
            except:
                self.frame = 0

        if self.anime_atk:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player1_atk_image) - 1:
                    self.frame = 0
                    self.anime_idle = True
                    self.anime_atk = False
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player1_atk_image[self.frame]
            except:
                self.frame = 0


        if self.jump:
            if self.jump_step <= 22:
                self.rect.y += self.jump_step
                self.jump_step += 1
            else:
                self.jump = False
                self.jump_step = -22


        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))
        if len(set(self.mask_list) & set(player2.mask_list)) > 0:
            if self.anime_atk and self.flag_damage:
                player2.hp -= 10
                self.flag_damage = False
        #for point in self.mask_list:
        #    x = point[0]
        #    y = point[1]
        #    pygame.draw.circle(sc, "blue", (x, y), 3)


        pygame.draw.rect(sc, self.hp_bar, (0, 0, 600 * self.hp / 100, 50))



class Player2(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.rect.x = 1000
        self.rect.bottom = HEIGHT - 40
        self.jump = False
        self.jump_step = -22
        self.frame = 0
        self.timer_anime = 0
        self.anime_idle = True
        self.anime_run = False
        self.anime_atk = False
        self.dir = "left"
        self.hp = 100
        self.flag_damage = False
        self.hp_bar = "red"
        self.mask_list = []


    def update(self):
        global FPS

        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.jump = True
        if key[pygame.K_m] and not self.anime_atk:
            self.frame = 0
            self.anime_idle = False
            self.anime_run = False
            self.anime_atk = True
            self.flag_damage = True
        elif key[pygame.K_RIGHT]:
            self.rect.x += 5
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        elif key[pygame.K_LEFT]:
            self.rect.x -= 5
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        else:
            if not self.anime_atk:
                self.anime_idle = True
            self.anime_run = False


        if self.anime_idle:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player2_idle_image) - 1:
                    self.frame = 0
                    if self.anime_atk:
                        self.anime_atk = False
                        self.anime_idle = True
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player2_idle_image[self.frame]
            except:
                self.frame = 0



        if self.anime_run:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player2_run_image) - 1:
                    self.frame = 0
                    if self.anime_atk:
                        self.anime_atk = False
                        self.anime_run = True
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player2_run_image[self.frame]
            except:
                self.frame = 0

        if self.anime_atk:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player2_atk_image) - 1:
                    self.frame = 0
                    self.anime_idle = True
                    self.anime_atk = False
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player2_atk_image[self.frame]
            except:
                self.frame = 0


        if self.jump:
            if self.jump_step <= 22:
                self.rect.y += self.jump_step
                self.jump_step += 1
            else:
                self.jump = False
                self.jump_step = -22


        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))
        if len(set(self.mask_list) & set(player1.mask_list)) > 0:
            if self.anime_atk and self.flag_damage:
                player1.hp -= 10
                self.flag_damage = False
        #for point in self.mask_list:
        #    x = point[0]
        #    y = point[1]
        #    pygame.draw.circle(sc, "red", (x, y), 3)


        pygame.draw.rect(sc, self.hp_bar, (600 + (600 - self.hp * 6), 0, 600, 50))


class FON:
    def __init__(self):
        self.timer = 0
        self.frame = 0
        self.image = bg_image

    def update(self):
        self.timer += 2
        sc.blit(self.image[self.frame], (0, 0))
        if self.timer / FPS > 0.1:
            if self.frame == len(self.image) - 1:
                self.frame = 0
            else:
                self.frame += 1
            self.timer = 0


def restart():
    global fon, player1, player1_group, player2, player2_group
    fon = FON()
    player1_group = pygame.sprite.Group()
    player1 = Player1(player1_idle_image, (0, 0))
    player1_group.add(player1)
    player2_group = pygame.sprite.Group()
    player2 = Player2(player2_idle_image, (0, 0))
    player2_group.add(player2)

restart()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    game_lvl()
    clock.tick(FPS)
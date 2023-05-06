import pygame
import os
import sys
import random

pygame.init()
current_path=os.path.dirname(__file__)
os.chdir(current_path)
WIDTH= 1200
HEIGHT= 600
FPS=60
p1 = "aizen"
p2 = "byakuya"
sc=pygame.display.set_mode((WIDTH, HEIGHT))
clock=pygame.time.Clock()
lvl = "menu"
#pygame.mixer.music.load('aizen-bankai.mp3')
#pygame.mixer.music.play(0)
aizen_music = pygame.mixer.Sound('music/aizen-bankai.wav')
byakuya_music = pygame.mixer.Sound('music/byakuya-bankai.wav')
gin_music = pygame.mixer.Sound('music/ichimaru-gin-bankay_fKauaS9d.mp3')
pygame.display.set_mode((1200, 600))



from load import *



def startMenu():
    global lvl
    sc.blit(menu_image, (0, 0))
    sc.blit(start_image, (100, 100))
    sc.blit(aizen_menu2_image, (670, 200))
    sc.blit(bleach_image, (500, -100))
    sc.blit(help_image, (100, 400))
    #sc.blit(records_image, (100, 300))
    #sc.blit(exit_image, (100, 400))
    pos_mouse=pygame.mouse.get_pos()
    if 100 < pos_mouse[0] < 400:
        if 100 < pos_mouse[1] < 175:
            sc.blit(start2_image, (100, 100))
    pos_mouse = pygame.mouse.get_pos()
    if 100 < pos_mouse[0] < 400:
        if 400 < pos_mouse[1] < 475:
            sc.blit(help2_image, (100, 400))
    if pygame.mouse.get_pressed()[0]:
        if 100<pos_mouse[0]<400:
            if 100<pos_mouse[1]<175:
                restart()
                lvl="Select"
    if pygame.mouse.get_pressed()[0]:
        if 100 < pos_mouse[0] < 400:
            if 400 < pos_mouse[1] < 475:
                restart()
                lvl = "Help"

            #elif 300<pos_mouse[1]<375:
            #    lvl="score"
            #    with open("score.txt", "r", encoding="utf-8") as file:
            #        records_list = []
            #        for i in range(5):
            #            records_list.append(file.readline().replace("\n", ""))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()



def game_lvl():
    #sc.fill("grey")
    sc.blit(fon, (0, 0))
    player1_group.update()
    player1_group.draw(sc)
    player2_group.update()
    player2_group.draw(sc)
    sakura_group.update()
    sakura_group.draw(sc)
    korobka_group.update()
    korobka_group.draw(sc)
    bankaiGIN_group.update()
    bankaiGIN_group.draw(sc)
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
        self.anime_atk2 = False
        self.anime_ult = False
        self.anime_form = False
        self.dir = "right"
        self.hp = 100
        self.flag_damage = False
        self.hp_bar = "blue"
        self.mask_list = []
        self.ulta = 75
        self.form = False


    def update(self):
        global FPS, player1, player2, p1, p2, Korobka
        key = pygame.key.get_pressed()
        if p1 == "aizen":
            self.control = [
                pygame.K_d,
                pygame.K_a,
                pygame.K_e,
                pygame.K_w,
                pygame.K_s,
                pygame.K_q]
        elif p2 == "aizen":
            self.control = [
                pygame.K_RIGHT,
                pygame.K_LEFT,
                pygame.K_m,
                pygame.K_UP,
                pygame.K_DOWN,
                pygame.K_n]
        if key[self.control[3]]:
            self.jump = True
        if key[self.control[2]] and not self.anime_atk and not self.anime_atk2 and not self.form:
            self.frame = 0
            self.anime_idle = False
            self.anime_run = False
            self.anime_atk = True
            self.flag_damage = True
        if key[self.control[5]] and not self.anime_atk and not self.anime_atk2 and not self.form:
            self.frame = 0
            self.anime_idle = False
            self.anime_run = False
            self.anime_atk2 = True
            self.flag_damage = True
        if key[self.control[4]] and self.ulta >= 75 and not self.anime_ult and not self.form:
            self.frame = 0
            self.anime_idle = False
            self.anime_run = False
            self.anime_atk = False
            self.anime_ult = True
            self.flag_damage = True
            aizen_music.play()
        if key[self.control[0]] and not self.anime_ult and not self.anime_atk and not self.anime_atk2:
            if self.form:
                self.anime_run = False
            else:
                self.rect.x += 4
                self.anime_idle = False
                if not self.anime_atk and not self.anime_ult and not self.form:
                    self.anime_run = True
        elif key[self.control[1]] and not self.anime_ult and not self.anime_atk and not self.anime_atk2:
            if self.form:
                self.anime_run = False
            else:
                self.rect.x -= 4
                self.anime_idle = False
                if not self.anime_atk and not self.anime_ult and not self.form:
                    self.anime_run = True
        else:
            if not self.anime_atk and not self.anime_atk2 and not self.anime_ult and not self.form:
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

        if self.anime_atk2:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.16:
                if self.frame == len(player1_atk2_image) - 1:
                    self.frame = 0
                    self.anime_idle = True
                    self.anime_atk2 = False
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player1_atk2_image[self.frame]
            except:
                self.frame = 0

        if self.anime_ult:
            self.timer_anime += 1
            sc.blit(aizen_menu_image, (300, 200))
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player1_ult_image) - 1:
                    self.frame = 0
                    self.anime_ult = False
                    self.form = True
                    player1.ulta = 0
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player1_ult_image[self.frame]
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
                player2.hp -= 5
                self.ulta += 5
                self.flag_damage = False
            if self.anime_atk2 and self.flag_damage:
                player2.hp -= 7
                self.ulta += 5
                self.flag_damage = False
        #for point in self.mask_list:
        #    x = point[0]
        #    y = point[1]
        #    pygame.draw.circle(sc, "blue", (x, y), 3)


        pygame.draw.rect(sc, self.hp_bar, (0, 0, 600 * self.hp / 100, 50))

        if self.ulta < 75:
            pygame.draw.rect(sc, (0, 191, 255), (0, 50, 2 * self.ulta, 30))
        elif self.ulta >= 75:
            pygame.draw.rect(sc, (0, 191, 255), (0, 50, 150, 30))
            sc.blit(BANKAI_image, (65, 55))
            #bankai_aizen = pygame.mixer.Sound('aizen-bankai.wav')
            #bankai_aizen.play(0)

        if self.hp <= 0:
            self.kill()

        if self.rect.center[0] - player2.rect.center[0] < 0:
            self.dir = "right"
        else:
            self.dir = "left"

        try:
            if self.dir == "right":
                self.image = self.image
            else:
                self.image = pygame.transform.flip(self.image, True, False)
        except:
            self.frame = 0

        if self.ulta < 75:
            self.anime_ult = False

        if self.form:
            self.anime_idle = False
            self.anime_run = False
            self.anime_atk = False
            self.anime_ult = False
            self.anime_form = True
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player1_form_image) - 1:
                    self.frame = 0

                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player1_form_image[self.frame]
            except:
                self.frame = 0

        if self.form:
            global Korobka
            korobka = Korobka(korobka_image, (600, 100))
            korobka_group.add(korobka)


class Player2(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.bottom = pos[1]
        self.jump = False
        self.jump_step = -22
        self.frame = 0
        self.timer_anime = 0
        self.anime_idle = True
        self.anime_run = False
        self.anime_atk = False
        self.anime_atk2 = False
        self.anime_ult = False
        self.anime_form = False
        self.dir = "left"
        self.hp = 100
        self.flag_damage = False
        self.hp_bar = "red"
        self.mask_list = []
        self.ulta = 75
        self.form = False


    def update(self):
        global FPS, p1, p2

        key = pygame.key.get_pressed()
        if p2 == "byakuya":
            self.control = [
                pygame.K_RIGHT,
                pygame.K_LEFT,
                pygame.K_m,
                pygame.K_UP,
                pygame.K_DOWN,
                pygame.K_n]
        elif p1 == "byakuya":
            self.control = [
                pygame.K_d,
                pygame.K_a,
                pygame.K_e,
                pygame.K_w,
                pygame.K_s,
                pygame.K_q]

        if key[self.control[3]]:
            self.jump = True
        if key[self.control[2]] and not self.anime_atk and not self.anime_atk2:
            self.frame = 0
            self.anime_idle = False
            self.anime_run = False
            self.anime_atk = True
            self.flag_damage = True
        if key[self.control[5]] and not self.anime_atk and not self.anime_atk2:
            self.frame = 0
            self.anime_idle = False
            self.anime_run = False
            self.anime_atk2 = True
            self.flag_damage = True
        if key[self.control[4]] and self.ulta >= 75 and not self.anime_ult and not self.form:
            self.frame = 0
            self.anime_idle = False
            self.anime_run = False
            self.anime_atk = False
            self.anime_ult = True
            self.flag_damage = True
            byakuya_music.play()
        if key[self.control[0]] and not self.anime_ult and not self.anime_atk and not self.anime_atk2:
            self.rect.x += 6
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        elif key[self.control[1]] and not self.anime_ult and not self.anime_atk and not self.anime_atk2:
            self.rect.x -= 6
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        else:
            if not self.anime_atk and not self.anime_ult and not self.anime_atk2:
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

        if self.anime_atk2:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.16:
                if self.frame == len(player2_atk2_image) - 1:
                    self.frame = 0
                    self.anime_idle = True
                    self.anime_atk2 = False
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player2_atk2_image[self.frame]
            except:
                self.frame = 0

        if self.anime_ult:
            self.timer_anime += 1
            sc.blit(byakuya_menu_image, (600, 200))
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player2_ult_image) - 1:
                    self.frame = 0
                    self.anime_ult = False
                    self.ulta = 0
                    sakura = Sakura(sakura_image, (1200, 300))
                    sakura_group.add(sakura)
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player2_ult_image[self.frame]
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
                player1.hp -= 2
                self.ulta += 5
                self.flag_damage = False
            if self.anime_atk2 and self.flag_damage:
                player1.hp -= 5
                self.ulta += 5
                self.flag_damage = False
        #for point in self.mask_list:
        #    x = point[0]
        #    y = point[1]
        #    pygame.draw.circle(sc, "red", (x, y), 3)


        pygame.draw.rect(sc, self.hp_bar, (600 + (600 - self.hp * 6), 0, 600, 50))
        if self.ulta < 75:
            pygame.draw.rect(sc, (205, 92, 92), (200 + (1000 - 2 * self.ulta), 50, 600, 30))
        elif self.ulta >= 75:
            pygame.draw.rect(sc, (205, 92, 92), (1050, 50, 600, 30))
            sc.blit(BANKAI_image, (1135, 55))

        if self.hp <= 0:
            self.kill()

        if self.rect.center[0] - player1.rect.center[0] < 0:
            self.dir = "right"
        else:
            self.dir = "left"

        try:
            if self.dir == "right":
                self.image = self.image
            else:
                self.image = pygame.transform.flip(self.image, True, False)
        except:
            self.frame = 0

        if self.ulta < 75:
            self.anime_ult = False


class Player3(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.bottom = pos[1]
        self.jump = False
        self.jump_step = -22
        self.frame = 0
        self.timer_anime = 0
        self.anime_death = False
        self.anime_idle = True
        self.anime_run = False
        self.anime_atk = False
        self.anime_atk2 = False
        self.anime_ult = False
        self.anime_form = False
        self.dir = "left"
        self.hp = 1
        self.flag_damage = False
        self.hp_bar = "green"
        self.mask_list = []
        self.ulta = 75
        self.form = False
        self.death = False


    def update(self):
        global FPS, p1, p2, player2

        key = pygame.key.get_pressed()
        if p2 == "gin":
            self.control = [
                pygame.K_RIGHT,
                pygame.K_LEFT,
                pygame.K_m,
                pygame.K_UP,
                pygame.K_DOWN,
                pygame.K_n]
        elif p1 == "gin":
            self.control = [
                pygame.K_d,
                pygame.K_a,
                pygame.K_e,
                pygame.K_w,
                pygame.K_s,
                pygame.K_q]

        if key[self.control[3]] and not self.death == True:
            self.jump = True
        if key[self.control[2]] and not self.anime_atk and not self.anime_atk2 and not self.death == True:
            self.frame = 0
            self.anime_idle = False
            self.anime_run = False
            self.anime_atk = True
            self.flag_damage = True
        if key[self.control[5]] and not self.anime_atk and not self.anime_atk2 and not self.death == True:
            self.frame = 0
            self.anime_idle = False
            self.anime_run = False
            self.anime_atk2 = True
            self.flag_damage = True
        if key[self.control[4]] and self.ulta >= 75 and not self.anime_ult and not self.form and not self.death == True:
            self.frame = 0
            self.anime_idle = False
            self.anime_run = False
            self.anime_atk = False
            self.anime_ult = True
            self.flag_damage = True
            gin_music.play()
        if key[self.control[0]] and not self.anime_ult and not self.anime_ult and not self.form and not self.death == True:
            self.rect.x += 6
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        elif key[self.control[1]] and not self.anime_ult and not self.anime_atk and not self.anime_atk2 and not self.death == True:
            self.rect.x -= 6
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        else:
            if not self.anime_atk and not self.anime_ult and not self.anime_atk2:
                self.anime_idle = True
            self.anime_run = False
        if self.hp <= 0 and not self.anime_ult and not self.anime_atk and not self.anime_atk2 and not self.anime_run and not self.jump:
            self.anime_death = True
            self.anime_atk = False
            self.anime_atk2 = False
            self.anime_idle = False
            self.anime_run = False
            self.anime_ult = False
            self.jump = False

        if self.anime_idle:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player3_idle_image) - 1:
                    self.frame = 0
                    if self.anime_atk:
                        self.anime_atk = False
                        self.anime_idle = True
                else:
                    self.frame += 1
                self.timer_anime = 0

            try:
                self.image = player3_idle_image[self.frame]
            except:
                self.frame = 0


        if self.anime_run:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.2:
                if self.frame == len(player3_run_image) - 1:
                    self.frame = 0
                    if self.anime_atk:
                        self.anime_atk = False
                        self.anime_run = True
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player3_run_image[self.frame]
            except:
                self.frame = 0



        if self.anime_atk:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player3_atk_image) - 1:
                    self.frame = 0
                    self.anime_idle = True
                    self.anime_atk = False
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player3_atk_image[self.frame]
            except:
                self.frame = 0

        if self.anime_death and self.death == False:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player3_death_image) - 1:

                    self.death = True
                    self.anime_death = False
                    self.anime_atk = False
                    self.anime_atk2 = False
                    self.anime_idle = False
                    self.anime_run = False
                    self.anime_ult = False
                    self.jump = False

                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player3_death_image[self.frame]
            except:
                self.frame = 0


        if self.anime_atk2:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.14:
                if self.frame == len(player3_atk2_image) - 1:
                    self.frame = 0
                    self.anime_idle = True
                    self.anime_atk2 = False
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player3_atk2_image[self.frame]
            except:
                self.frame = 0
#
        if self.anime_ult:
            self.timer_anime += 1
            sc.blit(gin_menu_image, (300, 200))
            if self.timer_anime / FPS > 0.13:
                if self.frame == len(player3_ult_image) - 1:
                    self.image = player3_ult_image[6]
                    self.frame = 0
                    self.anime_ult = False
                    self.ulta = 0
                    bankaiGIN = BankaiGIN(bankaiGIN_image, (self.rect.x, self.rect.y))
                    bankaiGIN_group.add(bankaiGIN)
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = player3_ult_image[self.frame]
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
                player2.hp -= 4
                self.ulta += 5
                self.flag_damage = False
            if self.anime_atk2 and self.flag_damage:
                player2.hp -= 7
                self.ulta += 5
                self.flag_damage = False

        pygame.draw.rect(sc, self.hp_bar, (0, 0, 600 * self.hp / 100, 50))

        if self.ulta < 75:
            pygame.draw.rect(sc, (0, 191, 255), (0, 50, 2 * self.ulta, 30))
        elif self.ulta >= 75:
            pygame.draw.rect(sc, (0, 191, 255), (0, 50, 150, 30))
            sc.blit(BANKAI_image, (65, 55))



        if self.rect.center[0] - player2.rect.center[0] < 0:
            self.dir = "right"
        else:
            self.dir = "left"

        try:
            if self.dir == "right":
                self.image = self.image
            else:
                self.image = pygame.transform.flip(self.image, True, False)
        except:
            self.frame = 0

        if self.ulta < 75:
            self.anime_ult = False


class Sakura(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    def update(self):
            self.rect.x -= 20
            self.mask = pygame.mask.from_surface(self.image)
            self.mask_outline = self.mask.outline()
            self.mask_list = []
            for i in self.mask_outline:
                self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))
            if len(set(self.mask_list) & set(player1.mask_list)) > 0:
                player1.hp -= 0.8
                self.flag_damage = False


class BankaiGIN(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = ""
    def update(self):
        #if player1.dir == "right":
        self.rect.x += 10
        #    self.dir = player1.dir
        #elif player1.dir == "left":
        #    self.rect.x -= 10
        #    self.dir = player1.dir
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))
        if len(set(self.mask_list) & set(player2.mask_list)) > 0:
            player2.hp -= 0.8
            self.flag_damage = False
        #try:
        #    if self.dir == "right":
        #        self.image = self.image[0]
        #    else:
        #        self.image = self.image[1]
        #except:
        #    self.frame = 0


class Korobka(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.frame = 0
        self.timer_anime = 0
        self.mask_list = []

    def update(self):
        global player1
        if player1.form:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(korobka_image) - 1:
                    self.frame = 0
                    player1.form = False
                else:
                    self.frame += 1
                self.timer_anime = 0
            try:
                self.image = korobka_image[self.frame]
            except:
                self.frame = 0

        if player1.form == False:
            self.kill()

        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))
        if len(set(self.mask_list) & set(player2.mask_list)) > 0:
            player2.hp -= 0.05


#class FON:
    #def __init__(self):
    #    self.timer = 0
    #    self.frame = 0
    #    self.image = bg_image
#
    #def update(self):
    #    self.timer += 2
    #    sc.blit(self.image[self.frame], (0, 0))
    #    if self.timer / FPS > 0.1:
    #        if self.frame == len(self.image) - 1:
    #            self.frame = 0
    #        else:
    #            self.frame += 1
    #        self.timer = 0

def help():
    global lvl
    sc.fill("grey")
    f1 = pygame.font.SysFont('arial', 46)
    sc.blit(control_wasd_image, (50, 50))
    sc.blit(control_arrows_image, (300, 50))
    sc.blit(control_e_image, (50, 300))
    sc.blit(control_m_image, (200, 300))
    sc.blit(control_q_image, (50, 450))
    sc.blit(control_n_image, (200, 450))
    sc.blit(control_back_image, (1100, 50))
    control = f1.render(' ------ CONTROL', True, (0, 0, 0))
    sc.blit(control, (530, 130))
    weakATK = f1.render(' ------ WEAK ATTACK', True, (0, 0, 0))
    sc.blit(weakATK, (350, 320))
    strongATK = f1.render(' ------ STRONG ATTACK', True, (0, 0, 0))
    sc.blit(strongATK, (350, 470))
    if pygame.mouse.get_pressed()[0]:
        pos_mouse = pygame.mouse.get_pos()
        if 1100 < pos_mouse[0] < 1150:
            if 50 < pos_mouse[1] < 100:
                lvl = "menu"
        pygame.display.update()

def select():
    global lvl, p1, p2
    f1 = pygame.font.SysFont('arial', 46)
    f2 = pygame.font.SysFont('arial', 30)
    sc.blit(shop_image, (0, 0))
    sc.blit(aizen_select_image, (350, 100))
    sc.blit(aizen_select_image, (800, 100))
    sc.blit(byakuya_select_image, (800, 250))
    sc.blit(byakuya_select_image, (350, 250))
    sc.blit(gin_select_image, (800, 400))
    sc.blit(gin_select_image, (350, 400))
    P1 = f1.render('P1', True, (0, 0, 0))
    sc.blit(P1, (180, 50))
    P2 = f1.render('P2', True, (0, 0, 0))
    sc.blit(P2, (1010, 50))
    aizen = f2.render('AIZEN', True, (0, 0, 0))
    sc.blit(aizen, (360, 200))
    sc.blit(aizen, (800, 200))
    byakuya = f2.render('BYAKUYA', True, (0, 0, 0))
    sc.blit(byakuya, (800, 350))
    sc.blit(byakuya, (350, 350))
    gin = f2.render('GIN', True, (0, 0, 0))
    sc.blit(gin, (825, 500))
    sc.blit(gin, (375, 500))
    sc.blit(continue_image, (495, 500))
    pos_mouse = pygame.mouse.get_pos()
    if 495 < pos_mouse[0] < 677:
        if 500 < pos_mouse[1] < 582:
            sc.blit(continue2_image, (495, 500))
            if pygame.mouse.get_pressed()[0]:
                restart()
                lvl = "Game"

    if pygame.mouse.get_pressed()[0]:
        if 350 < pos_mouse[0] < 450:
            if 100 < pos_mouse[1] < 200:
                p1 = "aizen"
        if 350 < pos_mouse[0] < 450:
            if 250 < pos_mouse[1] < 350:
                p1 = "byakuya"
        if 350 < pos_mouse[0] < 450:
            if 400 < pos_mouse[1] < 500:
                p1 = "gin"

    if pygame.mouse.get_pressed()[0]:
        if 800 < pos_mouse[0] < 900:
            if 100 < pos_mouse[1] < 200:
                p2 = "aizen"
        if 800 < pos_mouse[0] < 900:
            if 250 < pos_mouse[1] < 350:
                p2 = "byakuya"
        if 800 < pos_mouse[0] < 900:
            if 400 < pos_mouse[1] < 500:
                p2 = "gin"

    if p1 == "aizen":
        sc.blit(player1_idle_image[0], (100, 200))
    elif p1 == "byakuya":
        sc.blit(player2_idle_image[0], (100, 200))
    elif p1 == "gin":
        sc.blit(player3_idle_image[0], (100, 200))

    if p2 == "aizen":
        sc.blit(player1_idle_image[0], (950, 220))
    elif p2 == "byakuya":
        sc.blit(player2_idle_image[0], (950, 220))
    elif p2 == "gin":
        sc.blit(player3_idle_image[0], (950, 220))
    pygame.display.update()

def restart():
    print("uhfjkes")
    global player1, player1_group, player2, player2_group
    global korobka_group, sakura_group, bankaiGIN_group
    player1_group = pygame.sprite.Group()
    player2_group = pygame.sprite.Group()
    #fon = FON()
    #player1_group = pygame.sprite.Group()
    #player1 = Player1(player1_idle_image, (0, 0))
    #player1_group.add(player1)
    #player2_group = pygame.sprite.Group()
    #player2 = Player2(player2_idle_image, (0, 0))
    #player2_group.add(player2)
    #player3_group = pygame.sprite.Group()
    #player3 = Player3(player3_idle_image, (0, 0))
    #player3_group.add(player2)
    korobka_group = pygame.sprite.Group()
    sakura_group = pygame.sprite.Group()
    bankaiGIN_group = pygame.sprite.Group()

    if p1 == "aizen":
        player1_group = pygame.sprite.Group()
        player1 = Player1(player1_idle_image, (50, HEIGHT - 40))
        player1_group.add(player1)
    elif p1 == "byakuya":
        player1_group = pygame.sprite.Group()
        player1 = Player2(player2_idle_image, (50, HEIGHT - 40))
        player1_group.add(player1)
    elif p1 == "gin":
        player1_group = pygame.sprite.Group()
        player1 = Player3(player3_idle_image, (50, HEIGHT - 40))
        player1_group.add(player1)

    if p2 == "aizen":
        player2_group = pygame.sprite.Group()
        player2 = Player1(player1_idle_image, (1000, HEIGHT - 40))
        player2_group.add(player2)
    elif p2 == "byakuya":
        player2_group = pygame.sprite.Group()
        player2 = Player2(player2_idle_image, (1000, HEIGHT - 40))
        player2_group.add(player2)
    elif p2 == "gin":
        player2_group = pygame.sprite.Group()
        player2 = Player3(player3_idle_image, (1000, HEIGHT - 40))
        player2_group.add(player2)


restart()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    if lvl == "Game":
        game_lvl()

    elif lvl == "menu":
        startMenu()
    elif lvl == "Help":
        help()
    elif lvl == "Select":
        select()
    clock.tick(FPS)
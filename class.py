# Ishan Sharma and Aryan Kukreja
# For Mr. Cope
# April 23, 2016

# Main.py
# An RTS game

# Input: Mouse clicks
# Output: Gameplay

import pygame
from pygame.locals import *
import math
from random import randint

pygame.init()
screen = pygame.display.set_mode((1015, 768))

# Loading images and initializing list to store them in
back = pygame.image.load("Game initial sketch.png").convert_alpha()  # the background pic needs to be 1015x595 px.
tank_image = pygame.image.load("Tank.gif").convert_alpha()
missile_image = pygame.image.load("missile.png").convert_alpha()
mine_image = pygame.image.load("Army mine.png").convert_alpha()
bullet_image = pygame.image.load("projectile.png").convert_alpha()
ship1_image = pygame.image.load("Army Ship Level 1.gif").convert_alpha()
ship2_image = pygame.image.load("Army Ship Level 2.gif").convert_alpha()
ship3_image = pygame.image.load("Army Ship Level 3.gif").convert_alpha()
rocket_image = pygame.image.load("rocket.gif").convert_alpha()
splash = pygame.image.load("Splash screen.jpg").convert_alpha()
settings = pygame.image.load("Settings Screen.jpg").convert_alpha()
highscore_image = pygame.image.load("highscore_image.png").convert_alpha()

dark_gray = (75, 75, 75)
white = (255, 255, 255)
pressed = (0, 100, 0)
green = (0, 200, 0)
dark_green = (0, 255, 0)
dark_brown = (255, 0, 0)
gray = (200, 200, 200)
light_gray = (242, 242, 242)
black = (0, 0, 0)
poor = (100, 0, 0)
red = (200, 0, 0)
blue = (162, 196, 201)
dark_blue = (100, 100, 200)


# setting up surfaces for the menu, along with the menu backdrop
bottom_bounds = 155
border = pygame.Surface((122, bottom_bounds + 2)).convert()
border.fill(dark_gray)
main_border = pygame.Surface((327, bottom_bounds + 2)).convert()
main_border.fill(dark_gray)
display = pygame.Surface((325, bottom_bounds)).convert()
display.fill(gray)
white_surface = pygame.Surface((1015, 173)).convert()
white_surface.fill((255, 255, 255))

tank_surface = pygame.Surface((120, bottom_bounds)).convert()
missile_surface = pygame.Surface((120, bottom_bounds)).convert()
seamine_surface = pygame.Surface((120, bottom_bounds)).convert()
pause_surface = pygame.Surface((120, bottom_bounds)).convert()

blue_surface = pygame.Surface(screen.get_size()).convert()
blue_surface.fill(blue)
border_play = pygame.Surface((302, 102)).convert()
border_play.fill(dark_gray)
play_surface = pygame.Surface((300, 100)).convert()
play_surface.fill(light_gray)
game_over_border = pygame.Surface((952, 702)).convert()
game_over_border.fill(dark_gray)
game_over_surface = pygame.Surface((950, 700)).convert()
game_over_surface.fill(light_gray)

yes_music_surface = pygame.Surface((50, 50)).convert()
yes_music_surface.fill(green)
no_music_surface = pygame.Surface((50, 50)).convert()
no_music_surface.fill(light_gray)
return_home_surface = pygame.Surface((1015, 100))
return_home_surface.fill(red)

back_button_surface = pygame.Surface((120, bottom_bounds)).convert()
back_button_surface.fill(dark_blue)
back_button_border_surface = pygame.Surface((122, bottom_bounds + 2)).convert()
back_button_border_surface.fill(black)

tank_price = 1000
mine_price = 50000
missile_price = 10000

# fonts and text on the top of the game
font = pygame.font.SysFont("arial", 14)
splash_font = pygame.font.SysFont("helvetica", 80)
title_font = pygame.font.SysFont("helvetica", 117)

tank_text = font.render("Tank".center(18), True, black)
tank_cost = font.render(("$"+str(tank_price)).center(18), True, black)
missile_text = font.render("Missile Launcher".center(18), True, black)
missile_cost = font.render(("$"+str(missile_price)).center(18), True, black)
mine_text = font.render("Sea Mine".center(18), True, black)
mine_cost = font.render(("$"+str(mine_price)).center(18), True, black)
paused = font.render("", True, black)

play_text = splash_font.render("Play".center(11), True, black)
settings_text = splash_font.render("Settings".center(11), True, black)

title_text = title_font.render("WORLD WAR SEA", True, black)
music_title = splash_font.render("Music Settings: ", True, black)
yes_music = font.render("Turn Music on", True, black)
no_music = font.render("Turn Music off", True, black)
return_home = font.render("Back", True, black)
go_back_home = font.render("Quit".center(18), True, black)

# setting up variables that will be displayed on top
money = 50000
chances = 0
pause = True
ships_destroyed = 0
ships_remaining = 0
tank_pressed = True
missile_pressed = False
seamine_pressed = False
wave_interval = 800


ship_spawns = 0

# variables relating to tank
sprite_type = ""
angle = 0

splash_screen = True
settings_screen = False
game_over = False
score_achieved_index = 11
level = 1


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, angle_missile):
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle_missile
        self.image = pygame.transform.rotate(rocket_image, self.angle)
        self.rect = self.image.get_rect()
        self.x = x_pos
        self.y = y_pos
        self.dir_x = -16*math.sin(self.angle)
        self.dir_y = -16*math.cos(self.angle)
        self.rect.move_ip(self.x, self.y)
        self.active = True
        self.money = 15

    def update(self):
        self.image = pygame.transform.rotate(rocket_image, math.degrees(self.angle))
        self.rect.move_ip(self.dir_x, self.dir_y)
        self.x = self.rect.left
        self.y = self.rect.top
        for enemy in ship_group:
            if self.rect.colliderect(enemy.rect):
                self.active = False
                enemy.health -= 4
        if 0 > self.x or self.x > screen.get_size()[0] or 0 > self.y or self.y > screen.get_size()[1]:
            self.active = False


class Mine(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = mine_image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.x = x_pos
        self.y = y_pos
        self.rect.move_ip(self.x, self.y)
        self.active = True
        self.type = "S"
        self.size = self.image.get_size()

    def update(self):
        self.x = self.rect.left
        self.y = self.rect.top
        for enemy in ship_group:
            if self.rect.colliderect(enemy.rect):
                self.active = False
                enemy.health = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, angle_tank):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.x = x_pos
        self.y = y_pos
        self.angle = angle_tank
        self.dir_x = -8*math.sin(self.angle)
        self.dir_y = -8*math.cos(self.angle)
        self.rect.move_ip(self.x, self.y)
        self.active = True
        self.money = 2

    def update(self):
        self.rect.move_ip(self.dir_x, self.dir_y)
        self.x = self.rect.left
        self.y = self.rect.top
        for enemy in ship_group:
            if self.rect.colliderect(enemy.rect):
                self.active = False
                enemy.health -= 1/3
        if 0 > self.x or self.x > screen.get_size()[0] or 0 > self.y or self.y > screen.get_size()[1]:
            self.active = False


class Tank(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = tank_image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.x = x_pos
        self.y = y_pos
        self.timer = 0
        self.active = True
        self.type = "T"
        self.size = self.image.get_size()

    def update(self):
        for enemy in ship_group:
            if 500 > self.x-enemy.x > -500 and 250 > self.y-enemy.y > -250:
                lower = abs(self.y-enemy.y+(enemy.image.get_size()[1]/2))
                if lower == 0:
                    lower = 10**100
                self.angle = math.atan((self.x-abs(enemy.x+(enemy.image.get_size()[0]/2)))/lower)
                self.angle_adjust = self.angle * 35/math.pi
                if self.y < enemy.y:
                    self.angle = 135-self.angle
                self.timer += 1
                if self.timer == 5:
                    bullet_group.add(Bullet(self.x + (tank_image.get_size()[0]/2), self.y + (tank_image.get_size()[1]/2), self.angle))
                    self.timer = 0
                self.image = pygame.transform.rotate(tank_image, math.degrees(self.angle))
                break


class MissileLauncher(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.x = x
        self.y = y
        self.timer = 0
        self.active = True
        self.type = "M"
        self.size = self.image.get_size()

    def update(self):
        for enemy in ship_group:
            if 500 > self.x-enemy.x > -500 and 500 > self.y-enemy.y > -500:
                lower = abs(self.y - enemy.y + (enemy.image.get_size()[1]/2))
                if lower == 0:
                    lower = 10**100
                self.angle = math.atan((self.x-abs(enemy.x + (enemy.image.get_size()[0]/2)))/lower)
                if self.y < enemy.y:
                    self.angle = 135-self.angle
                self.timer += 1
                if self.timer == 30:
                    bullet_group.add(Rocket(self.x+(1.25*missile_image.get_size()[0]/7), self.y, self.angle))
                    bullet_group.add(Rocket(self.x+(1.1*missile_image.get_size()[0]/3), self.y, self.angle))
                    bullet_group.add(Rocket(self.x+(1.625*missile_image.get_size()[0]/3), self.y, self.angle))
                    bullet_group.add(Rocket(self.x+0.73*missile_image.get_size()[0], self.y, self.angle))
                    self.timer = 0
                break


class Ship(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        ship_choice = randint(1, 6)
        print(ship_choice)
        if ship_choice == 1:
            self.image = ship3_image
            self.health = 2000
            self.late_money = 5000
        elif 2 <= ship_choice <= 3:
            self.image = ship2_image
            self.health = 1625
            self.late_money = 2500
        else:
            self.image = ship1_image
            self.health = 1250
            self.late_money = 500

        if level == 2:
            self.health += 500
            self.late_money += 750
        self.rect = self.image.get_rect()

        self.dir_x = 0
        self.dir_y = 0
        self.x = x_pos
        self.y = y_pos - self.image.get_size()[1]
        self.speed = 1
        self.rect.move_ip(self.x, self.y)
        self.active = True
        self.money = 0
        self.victor = False

    def update(self):
        self.x = self.rect.left
        self.y = self.rect.top
        if self.y < 170:
            self.dir_y = 1
            self.dir_x = 0
        elif self.y == 175:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir_y = 110
        elif 300 > self.y > 175 and self.x < 850:
            self.dir_y = 0
            self.dir_x = 1
        elif self.x == 850 and self.y < 330:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir_x = 110
        elif self.x > 850 and self.y < 390:
            self.dir_y = 1
            self.dir_x = 0
        elif self.y == 392:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir_y = 120
        elif 395 < self.y < 600 and self.x > 100:
            self.dir_x = -1
            self.dir_y = 0
        elif self.x == 100 and 600 > self.y > 395:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir_x = -50
        elif self.x < 100 and 395 <= self.y < 600:
            self.dir_x = 0
            self.dir_y = 1
        elif self.x < 100 and self.y == 600:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir_y = 65
        elif self.y > 600 and self.x < 700:
            self.dir_x = 1
            self.dir_y = 0
        elif self.y > 600 and self.x == 700:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir_y = -30
        elif self.y > 600 and self.x > 700:
            self.dir_x = 0
            self.dir_y = 1
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.x, self.y)

        self.rect.move_ip(self.speed * self.dir_x, self.speed * self.dir_y)
        if self.health <= 0:
            self.active = False
            self.money = self.late_money

        if self.y > screen.get_size()[1]:
            self.active = False
            self.victor = True


ship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(30)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            keep_going = False

        elif ev.type == MOUSEBUTTONDOWN:
            x_unadjusted = ev.pos[0]
            y_unadjusted = ev.pos[1]
            x = (x_unadjusted//35)*35  # getting the x of where the mouse clicked
            y = (y_unadjusted//35)*35  # getting the y of where the mouse clicked
            if splash_screen:
                if (380 < x_unadjusted < 640) and (480 < y_unadjusted < 570):
                    print("play")
                    splash_screen = False
                    pause = False
                elif (300 < x_unadjusted < 750) and (590 < y_unadjusted < 680):
                    settings_screen = True
                    splash_screen = False
                    print("settings")
            elif settings_screen:
                print(x_unadjusted, y_unadjusted)
                if (160 < x_unadjusted < 300) and (320 < y_unadjusted < 435):
                    music = True
                elif (160 < x_unadjusted < 300) and (470 < y_unadjusted < 535):
                    music = False
                elif y_unadjusted < 100:
                    splash_screen = True
                    pause = True
                    settings_screen = False
            elif game_over:
                pass
            else:
                y_clicked = 142 > y_unadjusted > 9

                if 131 > x_unadjusted > 9 and y_clicked:  # if the tank part of the menu is pressed
                    tank_pressed = True
                    missile_pressed = False
                    seamine_pressed = False

                elif 261 > x_unadjusted > 139 and y_clicked:  # if the missile part of the menu is pressed
                    tank_pressed = False
                    missile_pressed = True
                    seamine_pressed = False

                elif 391 > x_unadjusted > 269 and y_clicked:  # if the sea mine part of the menu is pressed
                    tank_pressed = False
                    missile_pressed = False
                    seamine_pressed = True

                elif y_clicked and 400 < x_unadjusted < 520:  # if any other part of the menu is pressed
                    if pause:  # if the game is already paused
                        pause = False
                    elif not pause:  # if the game is not already paused
                        pause = True

                elif y_clicked and 529 < x_unadjusted < 649:
                    splash_screen = True
                    pause = True
                    player_group.empty()
                    ship_group.empty()
                    bullet_group.empty()

                elif (not pause) and y > 150:  # if the main gameplay part is pressed
                    item = 0
                    pathway_pressed = (y < 243 and x > 140) or (383 < y < 453 and x < 840) or (595 >= y > 525 and x > 140) or (y > 595 and x > 840)
                    overlap = False

                    for player in player_group.sprites():
                        if player.x-1 <= x <= (player.x + player.size[0]-1) and player.y-1 <= y <= (player.y + player.size[1]-1):
                            overlap = True

                    if not overlap:
                        if tank_pressed and pathway_pressed and (money - tank_price) >= 0:
                            player_group.add(Tank(x, y))
                            money -= tank_price

                        elif missile_pressed and pathway_pressed and money - missile_price >= 0:
                            player_group.add(MissileLauncher())
                            money -= missile_price

                        elif seamine_pressed and money - mine_price >= 0 and not pathway_pressed:
                            player_group.add(Mine(x, y))
                            money -= mine_price

                        else:
                            break

    if not pause:
        ship_spawns += 1
        if ship_spawns == wave_interval or len(ship_group) == 0:
            ship_group.add(Ship(100, 173))
            ship_spawns = 0
            wave_interval *= 0.925
            if wave_interval < 20:
                back = pygame.image.load("Game initial sketch 2.png").convert_alpha()
                tank_price += 500
                missile_price += 1000
                mine_price += 75000
                if level == 2:
                    game_over = True
                else:
                    level = 2
                    money += 2000
                    wave_interval = 700
                    player_group.empty()
                    ship_group.empty()
                    bullet_group.empty()
                    tank_cost = font.render(("$"+str(tank_price)).center(18), True, black)
                    missile_cost = font.render(("$"+str(missile_price)).center(18), True, black)
                    mine_cost = font.render(("$"+str(mine_price)).center(18), True, black)
                    pause = True
            wave_interval = int(wave_interval)
            print(wave_interval)
    if not tank_pressed:
        tank_surface.fill(gray)
    elif (tank_price - money) > 0:
        tank_surface.fill(poor)
    else:
        tank_surface.fill(pressed)
    if not missile_pressed:
        missile_surface.fill(gray)
    elif (missile_price - money) > 0:
        missile_surface.fill(poor)
    else:
        missile_surface.fill(pressed)
    if not seamine_pressed:
        seamine_surface.fill(gray)
    elif (mine_price - money) > 0:
        seamine_surface.fill(poor)
    else:
        seamine_surface.fill(pressed)

    if pause:
        pause_surface.fill(red)
        paused = "Paused".center(18)
    else:
        pause_surface.fill(green)
        paused = "Resumed".center(18)

    if not pause:
        ship_group.update()
        player_group.update()
        bullet_group.update()

    money_text = font.render("Money: $"+str(money), True, black)
    numweapons_text = font.render("Weapons: "+str(0), True, black)
    islandsdestroyed_text = font.render("Islands Destroyed: "+str(3-chances), True, black)
    chance_text = font.render("Chances: "+str(chances), True, black)
    shipsdestroyed_text = font.render("Ships Destroyed: "+str(ships_destroyed), True, black)
    shipsremaining_text = font.render("Ships Remaining: "+str(len(ship_group)), True, black)
    paused_text = font.render(paused, True, black)
    level_text = font.render("Level "+str(level), True, black)

    # Blitting
    screen.blit(back, (0, 173))
    for player in player_group.sprites():
        if player.active:
            screen.blit(player.image, (player.x, player.y-2))
        else:
            player_group.remove(player)
    for projectile in bullet_group:
        if projectile.active:
            screen.blit(projectile.image, (projectile.x, projectile.y))
        else:
            bullet_group.remove(projectile)
            money += projectile.money
    for ship in ship_group.sprites():
        if ship.active:
            screen.blit(ship.image, (ship.x, ship.y))
        elif ship.victor:
            ship_group.remove(ship)
            chances -= 1
        else:
            ship_group.remove(ship)
            money += ship.money
            ships_destroyed += 1

    if chances == 0:
        pause = True
        player_group.empty()
        ship_group.empty()
        bullet_group.empty()
        game_over = True
        high_scores = []
        with open("highscores.txt", "r") as file:
            for line in file:
                try:
                    int(line)
                except:
                    continue
                else:
                    high_scores.append(int(line))
        done = False
        if len(high_scores) == 0:
            high_scores.append(ships_destroyed)
        else:
            for score_index in range(0, len(high_scores)):
                if high_scores[score_index] <= ships_destroyed:
                    high_scores.insert(score_index, ships_destroyed)
                    done = True
                    score_achieved_index = score_index
                    break
            if not done:
                high_scores.append(ships_destroyed)
        with open("highscores.txt", "w") as file:
            for score in high_scores[0:10]:
                file.write(str(score)+chr(10))
                chances = 3
        print(high_scores[0:10])
        game_over = True
        print(len(high_scores))

    # blitting the top part of the screen
    top_bounds = 10
    screen.blit(white_surface, (0, 0))
    screen.blit(border, (9, top_bounds - 1))
    screen.blit(tank_surface, (10, top_bounds))
    screen.blit(border, (139, top_bounds - 1))
    screen.blit(missile_surface, (140, top_bounds))
    screen.blit(border, (269, top_bounds - 1))
    screen.blit(seamine_surface, (270, top_bounds))
    screen.blit(main_border, (679, top_bounds - 1))
    screen.blit(display, (680, top_bounds))
    screen.blit(border, (399, top_bounds - 1))
    screen.blit(pause_surface, (400, top_bounds))

    scale = 125
    top_bounds = 100
    screen.blit(paused_text, (408, 70))
    screen.blit(islandsdestroyed_text, (400 + scale + 200, top_bounds + 15))
    screen.blit(shipsdestroyed_text, (400 + scale + 200, top_bounds - 25))
    screen.blit(money_text, (400 + scale + 200, top_bounds - 65))
    screen.blit(shipsremaining_text, (650 + scale + 100, top_bounds - 25))
    screen.blit(numweapons_text, (650 + scale + 100, top_bounds - 65))
    screen.blit(chance_text, (650 + scale + 100, top_bounds + 15))
    screen.blit(level_text, (600 + scale + 90, top_bounds - 90))

    scale = 50
    screen.blit(tank_text, (10, top_bounds))
    screen.blit(missile_text, (143, top_bounds))
    screen.blit(mine_text, (270, top_bounds))
    screen.blit(tank_cost, (10, top_bounds + 15))
    screen.blit(missile_cost, (140, top_bounds + 15))
    screen.blit(mine_cost, (270, top_bounds + 15))

    screen.blit(back_button_border_surface, (529, top_bounds - 91))
    screen.blit(back_button_surface, (530, top_bounds - 90))
    screen.blit(go_back_home, (535, 70))

    screen.blit(tank_image, (scale + 3, 50))
    screen.blit(missile_image, (scale + 98, 50))
    screen.blit(mine_image, (scale + 260, 50))

    if splash_screen:
        screen.blit(splash, (0, 0))

    if settings_screen:
        screen.blit(settings, (0, 0))

    if game_over:
        screen.blit(highscore_image, (0, 0))
        rank_text = font.render("Rank".ljust(20) + "Score", True, black)
        screen.blit(rank_text, (400, 195))
        for score_index in range(0, len(high_scores[0:10])):
            if score_index == score_achieved_index:
                rank_text = font.render((str(score_index + 1)).ljust(20) + str(high_scores[score_index]), True, red)
            else:
                rank_text = font.render((str(score_index + 1)).ljust(20) + str(high_scores[score_index]), True, black)
            screen.blit(rank_text, (400, 230 + 35*score_index))
        if score_achieved_index > 10:
            rank_text = font.render(str(11).ljust(20) + str(ships_destroyed), True, red)
            screen.blit(rank_text, (400, 230 + 35*11))

    pygame.display.flip()
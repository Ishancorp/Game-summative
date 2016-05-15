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

# Setting up some colours
dark_gray = (75, 75, 75)
pressed = (0, 100, 0)
green = (0, 200, 0)
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
main_border = pygame.Surface((307, bottom_bounds + 2)).convert()
main_border.fill(dark_gray)
display = pygame.Surface((305, bottom_bounds)).convert()
display.fill(gray)
white_surface = pygame.Surface((1015, 173)).convert()
white_surface.fill((255, 255, 255))

tank_surface = pygame.Surface((120, bottom_bounds)).convert()
missile_surface = pygame.Surface((120, bottom_bounds)).convert()
seamine_surface = pygame.Surface((120, bottom_bounds)).convert()
pause_surface = pygame.Surface((120, bottom_bounds)).convert()

blue_surface = pygame.Surface((1015, 768)).convert()
blue_surface.fill(blue)
play_surface = pygame.Surface((300, 100)).convert()
play_surface.fill(light_gray)
settings_surface = pygame.Surface((300, 100)).convert()
settings_surface.fill(light_gray)

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

# fonts and text on the top of the game
font = pygame.font.SysFont("arial", 14)
splash_font = pygame.font.SysFont("helvetica", 80)
title_font = pygame.font.SysFont("helvetica", 125)

tank_text = font.render("Tank", True, black)
tank_cost = font.render("$1 000", True, black)
missile_text = font.render("Missile Launcher", True, black)
missile_cost = font.render("$10 000", True, black)
mine_text = font.render("Sea Mine", True, black)
mine_cost = font.render("$50 000", True, black)
paused = font.render("", True, black)

play_text = splash_font.render("Play".center(11), True, black)
settings_text = splash_font.render("Settings".center(11), True, black)

title_text = title_font.render("WORLD WAR SEA", True, black)
music_title = splash_font.render("Music Settings: ", True, black)
yes_music = font.render("Turn Music on", True, black)
no_music = font.render("Turn Music off", True, black)
return_home = font.render("Back", True, black)

go_back_home = font.render("Back", True, black)

# setting up variables that will be displayed on top
money = 100000
chances = 3
pause = True
ships_destroyed = 0
ships_remaining = 0
tank_pressed = True
missile_pressed = False
seamine_pressed = False


tank_price = 1000
mine_price = 50000
missile_price = 10000
ship_spawns = 0

# variables relating to tank
sprite_type = ""
angle = 0

splash_screen = True
settings_screen = False


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

    def update(self):
        self.image = pygame.transform.rotate(rocket_image, math.radians(self.angle))
        self.rect.move_ip(self.dir_x, self.dir_y)
        self.x = self.rect.left
        self.y = self.rect.top
        for enemy in ship_group:
            if enemy.x < self.x < (enemy.x+(enemy.image.get_size()[0])) and enemy.y < self.y < (enemy.y+(enemy.image.get_size()[1])):
                self.active = False
                enemy.health -= 5
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

    def update(self):
        self.x = self.rect.left
        self.y = self.rect.top
        for enemy in ship_group:
            if (enemy.x+enemy.image.get_size()[0] >= self.x >= enemy.x or enemy.x+enemy.image.get_size()[0] >= self.x + mine_image.get_size()[1] >= enemy.x) and (enemy.y+enemy.image.get_size()[1] >= self.y >= enemy.y or enemy.y+enemy.image.get_size()[1] >= self.y + mine_image.get_size()[1] >= enemy.y):
                self.active = False
                enemy.health -= 50


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, angle_tank):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.x = x_pos + (tank_image.get_size()[0]/2)
        self.y = y_pos + (tank_image.get_size()[1]/2)
        self.angle = angle_tank
        self.dir_x = -8*math.sin(self.angle)
        self.dir_y = -8*math.cos(self.angle)
        self.rect.move_ip(self.x + (bullet_image.get_size()[0]/2), self.y + (bullet_image.get_size()[1]/2))
        self.active = True

    def update(self):
        self.rect.move_ip(self.dir_x, self.dir_y)
        self.x = self.rect.left
        self.y = self.rect.top
        for enemy in ship_group:
            if enemy.x < self.x < (enemy.x+(enemy.image.get_size()[0])) and enemy.y < self.y < (enemy.y+(enemy.image.get_size()[1])):
                self.active = False
                enemy.health -= 1
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
        self.angle_adjust = 0

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
                    bullet_group.add(Bullet(self.x, self.y, self.angle))
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

    def update(self):
        for enemy in ship_group:
            if 500 > self.x-enemy.x > -500 and 500 > self.y-enemy.y > -500:
                lower = abs(self.y-enemy.y+(enemy.image.get_size()[1]/2))
                if lower == 0:
                    lower = 10**100
                self.angle = math.atan((self.x-abs(enemy.x))/lower)
                if self.y < enemy.y:
                    self.angle = 135-self.angle
                self.timer += 1
                if self.timer == 10:
                    bullet_group.add(Rocket(self.x+(1.25*missile_image.get_size()[0]/7), self.y, self.angle))
                    bullet_group.add(Rocket(self.x+(1.1*missile_image.get_size()[0]/3), self.y, self.angle))
                    bullet_group.add(Rocket(self.x+(1.625*missile_image.get_size()[0]/3), self.y, self.angle))
                    bullet_group.add(Rocket(self.x+0.73*missile_image.get_size()[0], self.y, self.angle))
                    self.timer = 0
                break


class Ship(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        ship_choice = randint(0, 6)
        if ship_choice == 0:
            self.image = ship3_image
            self.health = 8000
        elif 2 <= ship_choice <= 3:
            self.image = ship2_image
            self.health = 5000
        else:
            self.image = ship1_image
            self.health = 2000
        self.rect = self.image.get_rect()

        self.dir_x = 0
        self.dir_y = 0
        self.x = x_pos
        self.y = y_pos
        self.speed = 1
        self.rect.move_ip(self.x, self.y)
        self.active = True
        self.money = 0

    def update(self):
        self.x = self.rect.left
        self.y = self.rect.top
        if self.y < 170:
            self.dir_y = 1
            self.dir_x = 0
        elif self.y == 175:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir_y = 100
        elif self.y > 175 and self.x < 850:
            self.dir_y = 0
            self.dir_x = 1
        elif self.x == 851:
            self.image = pygame.transform.rotate(self.image, -90)
            self.dir_y = -100
        elif 850 < self.rect.left:
            self.dir_y = 1
            self.dir_x = 0
        elif (385 < self.rect.top < 500) and 990 < self.rect.left:
            self.dir_y = 0
            self.dir_x = -1
        elif 100 > self.rect.left and 300 < self.rect.top < 500:
            self.dir_y = 1
            self.dir_x = 0
        elif self.rect.top > 550 and 990 > self.rect.left:
            self.dir_y = 0
            self.dir_x = 1
        elif self.rect.top > 550 and 800 < self.rect.left:
            self.dir_y = 0
            self.dir_x = 0
        self.rect.move_ip(self.speed * self.dir_x, self.speed * self.dir_y)
        if self.health <= 0:
            self.active = False
            self.money = 10000


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
            x = ((ev.pos[0])//35)*35  # getting the x of where the mouse clicked
            y = ((ev.pos[1])//35)*35  # getting the y of where the mouse clicked
            if splash_screen:
                if (blue_surface.get_size()[0] / 3 < x < blue_surface.get_size()[0] / 3 + 300) and (blue_surface.get_size()[1] / 2 - 100 < y < blue_surface.get_size()[1] / 2):
                    print("play")
                    splash_screen = False
                    pause = False
                    ship_spawns = 199
                elif (blue_surface.get_size()[0] / 3 < x < blue_surface.get_size()[0] / 3 + 300) and (blue_surface.get_size()[1] / 2 + 100 < y < blue_surface.get_size()[1] / 2 + 200):
                    settings_screen = True
                    splash_screen = False
                    print("settings")
            elif settings_screen:
                print(x, y)
                if (160 < x < 300) and (320 < y < 435):
                    music = True
                elif (160 < x < 300) and (470 < y < 535):
                    music = False
                elif y < 100:
                    splash_screen = True
                    pause = True
                    settings_screen = False
            else:
                y_clicked = 142 > y > 9

                if 131 > x > 9 and y_clicked:  # if the tank part of the menu is pressed
                    tank_pressed = True
                    missile_pressed = False
                    seamine_pressed = False

                elif 261 > x > 139 and y_clicked:  # if the missile part of the menu is pressed
                    tank_pressed = False
                    missile_pressed = True
                    seamine_pressed = False

                elif 391 > x > 269 and y_clicked:  # if the sea mine part of the menu is pressed
                    tank_pressed = False
                    missile_pressed = False
                    seamine_pressed = True

                elif y_clicked and 400 < x < 520:  # if any other part of the menu is pressed
                    if pause:  # if the game is already paused
                        pause = False
                    elif not pause:  # if the game is not already paused
                        pause = True

                elif y_clicked and 529 < x < 649:
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
                        if (x == player.x and y == player.y) or (missile_pressed and player.type == "M" and (player.x-70 <= x <= player.x+70 and y == player.y)):
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

    ship_spawns += 1
    if ship_spawns == 200:
        ship_group.add(Ship(100 + randint(-20, 20), 0))
        ship_spawns = 0
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
        paused = "Paused".center(7)
    else:
        pause_surface.fill(green)
        paused = "Resumed".center(7)

    screen.blit(back, (0, 173))
    if not pause:
        ship_group.update()
        player_group.update()
        bullet_group.update()

    money_text = font.render("Money: $"+str(money), True, black)
    numweapons_text = font.render("Weapons: "+str(0), True, black)
    islandsdestroyed_text = font.render("Islands Destroyed: "+str(3-chances), True, black)
    chance_text = font.render("Chances: "+str(chances), True, black)
    shipsdestroyed_text = font.render("Ships Destroyed: "+str(ships_destroyed), True, black)
    shipsremaining_text = font.render("Ships Remaining: "+str(ships_remaining), True, black)
    paused_text = font.render(paused, True, black)

    # Blitting
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
    for ship in ship_group.sprites():
        if ship.active:
            screen.blit(ship.image, (ship.x, ship.y))
        else:
            ship_group.remove(ship)
            money += ship.money

    # blitting the top part of the screen
    top_bounds = 10
    screen.blit(white_surface, (0, 0))
    screen.blit(border, (9, top_bounds - 1))
    screen.blit(tank_surface, (10, top_bounds))
    screen.blit(border, (139, top_bounds - 1))
    screen.blit(missile_surface, (140, top_bounds))
    screen.blit(border, (269, top_bounds - 1))
    screen.blit(seamine_surface, (270, top_bounds))
    screen.blit(main_border, (704, top_bounds - 1))
    screen.blit(display, (705, top_bounds))
    screen.blit(border, (399, top_bounds - 1))
    screen.blit(pause_surface, (400, top_bounds))

    scale = 150
    top_bounds = 100
    screen.blit(paused_text, (408, 50))
    screen.blit(islandsdestroyed_text, (400 + scale + 200, top_bounds + 15))
    screen.blit(shipsdestroyed_text, (400 + scale + 200, top_bounds - 25))
    screen.blit(money_text, (400 + scale + 200, top_bounds - 65))
    screen.blit(shipsremaining_text, (650 + scale + 100, top_bounds - 25))
    screen.blit(numweapons_text, (650 + scale + 100, top_bounds - 65))
    screen.blit(chance_text, (650 + scale + 100, top_bounds + 15))

    scale = 50
    screen.blit(tank_text, (scale, top_bounds))
    screen.blit(missile_text, (110 + scale, top_bounds))
    screen.blit(mine_text, (250 + scale, top_bounds))
    screen.blit(tank_cost, (scale, top_bounds + 15))
    screen.blit(missile_cost, (scale + 110, top_bounds + 15))
    screen.blit(mine_cost, (250 + scale, top_bounds + 15))

    screen.blit(back_button_border_surface, (529, top_bounds - 91))
    screen.blit(back_button_surface, (530, top_bounds - 90))
    screen.blit(go_back_home, (535, top_bounds - 45))

    screen.blit(tank_image, (scale + 3, 50))
    screen.blit(missile_image, (scale + 98, 50))
    screen.blit(mine_image, (scale + 260, 50))

    if splash_screen:
        screen.blit(blue_surface, (0, 0))
        screen.blit(play_surface, (blue_surface.get_size()[0] / 3, blue_surface.get_size()[1] / 2 - 100))
        screen.blit(settings_surface, (blue_surface.get_size()[0] / 3, blue_surface.get_size()[1] / 2 + 100))
        screen.blit(title_text, (blue_surface.get_size()[0] / 15, blue_surface.get_size()[1] / 2 - 300))
        screen.blit(play_text, (blue_surface.get_size()[0] / 3, blue_surface.get_size()[1] / 2 - 100))
        screen.blit(settings_text, (blue_surface.get_size()[0] / 3, blue_surface.get_size()[1] / 2 + 100))

    if settings_screen:
        screen.blit(blue_surface, (0, 0))
        screen.blit(music_title, (blue_surface.get_size()[0] / 3, blue_surface.get_size()[1] / 2 - 200))
        screen.blit(yes_music, (235, 400))
        screen.blit(no_music, (235, 500))
        screen.blit(yes_music_surface, (180, 383))
        screen.blit(no_music_surface, (180, 483))
        screen.blit(return_home_surface, (0, 0))
        screen.blit(return_home, (100, 50))
    pygame.display.flip()

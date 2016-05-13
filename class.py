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

pygame.init()
screen = pygame.display.set_mode((1015, 768))

# Loading images and initializing list to store them in
back = pygame.image.load("Game initial sketch.png").convert_alpha()  # the background pic needs to be 1015x595 px.
ball = pygame.image.load("Tank.gif").convert_alpha()  # must be 35x35, or (some multiple of 35)x(some multiple of 35)
missile = pygame.image.load("missile.png").convert_alpha()
mine = pygame.image.load("Army mine.png").convert()
bullet = pygame.image.load("projectile.png").convert_alpha()

# Setting up some colours
dark_gray = (75, 75, 75)
pressed = (0, 100, 0)
green = (0, 200, 0)
gray = (200, 200, 200)
light_gray = (242, 242, 242)
black = (0, 0, 0)
poor = (100, 0, 0)
red = (200, 0, 0)

# setting up surfaces for the menu, along with the menu backdrop
bottom_bounds = 155
border = pygame.Surface((122, bottom_bounds+2)).convert()
border.fill(dark_gray)
main_border = pygame.Surface((477, bottom_bounds+2)).convert()
main_border.fill(dark_gray)
display = pygame.Surface((475, bottom_bounds)).convert()
display.fill(gray)
white_surface = pygame.Surface((1015, 173)).convert()
white_surface.fill((255, 255, 255))

tank_surface = pygame.Surface((120, bottom_bounds)).convert()
missile_surface = pygame.Surface((120, bottom_bounds)).convert()
seamine_surface = pygame.Surface((120, bottom_bounds)).convert()
pause_surface = pygame.Surface((120, bottom_bounds)).convert()

# fonts and text on the top of the game
font = pygame.font.SysFont("arial", 14)
tank_text = font.render("Tank", True, black)
tank_cost = font.render("$1 000", True, black)
missile_text = font.render("Missile Launcher", True, black)
missile_cost = font.render("$10 000", True, black)
mine_text = font.render("Sea Mine", True, black)
mine_cost = font.render("$50 000", True, black)
paused = font.render("", True, black)

# setting up coordinate variables
x = 0
y = 0
y_enemy = 15
x_enemy = 100
enemy_health = 1000

# setting up variables that will be displayed on top
money = 10000000
chances = 3
pause = False
ships_destroyed = 0
ships_remaining = 0
tank_pressed = True
missile_pressed = False
seamine_pressed = False

tank_price = 1000
mine_price = 50000
missile_price = 10000

# variables relating to tank
sprite_type = ""
angle = 0


# render text with new values for every variable
money_text = font.render("Money: $"+str(money), True, black)
numweapons_text = font.render("Weapons: "+str(0), True, black)
islandsdestroyed_text = font.render("Islands Destroyed: "+str(3-chances), True, black)
chance_text = font.render("Chances: "+str(chances), True, black)
shipsdestroyed_text = font.render("Ships Destroyed: "+str(ships_destroyed), True, black)
shipsremaining_text = font.render("Ships Remaining: "+str(ships_remaining), True, black)


class Mine(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Army mine.png").convert_alpha()
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.x = x_pos
        self.y = y_pos
        self.rect.move_ip(self.x, self.y)
        self.active = True


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, angle_tank):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.x = x_pos
        self.y = y_pos
        self.angle = angle_tank
        self.dir_x = -4*math.sin(self.angle)
        self.dir_y = -4*math.cos(self.angle)
        self.rect.move_ip(self.x + (ball.get_size()[0]/2), self.y + (ball.get_size()[1]/2))
        self.active = True

    def update(self):
        self.rect.move_ip(self.dir_x, self.dir_y)
        self.x = self.rect.left
        self.y = self.rect.top
        for enemy in ship_group:
            if enemy.x < self.x < (enemy.x+(enemy.image.get_size()[0]/2)) and enemy.y < self.y < (enemy.y+(enemy.image.get_size()[1]/2)):
                self.active = False
                enemy.health -= 1
        if 0 > self.x or self.x > screen.get_size()[0] or 0 > self.y or self.y > screen.get_size()[1]:
            self.active = False


class Tank(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Tank.gif").convert_alpha()
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.x = x_pos
        self.y = y_pos
        self.timer = 0

    def update(self):
        for enemy in ship_group:
            lower = (self.y-enemy.y+(enemy.image.get_size()[1]/2))
            if lower == 0:
                lower = 10**100
            self.angle = math.atan((self.x-(enemy.x+(enemy.image.get_size()[0]/2)))/lower)
            if self.y < enemy.y:
                self.angle -= 180
            self.timer += 1
            if self.timer == 10 and 500 > self.x-enemy.x > -500 and 250 > self.y-enemy.y > -250:
                bullet_group.add(Bullet(self.x, self.y, self.angle))
                self.timer = 0
            self.image = pygame.transform.rotate(self.orig_image, math.degrees(self.angle))


class MissileLauncher(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("missile.png").convert_alpha()
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.x = x
        self.y = y

    def update(self):
        pass


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Army Ship Level 1 (1).gif").convert_alpha()
        self.rect = self.image.get_rect()

        self.dir_x = 0
        self.dir_y = 0
        self.x = 100
        self.y = 15
        self.speed = 1
        self.rect.move_ip(self.x, self.y)
        self.health = 100
        self.active = True

    def update(self):
        self.x = self.rect.left
        self.y = self.rect.top
        if self.y < 170:
            self.dir_y = 1
            self.dir_x = 0
        elif self.y == 170:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir_y = 100
        elif self.y > 170 and self.x < 950:
            self.dir_y = 0
            self.dir_x = 1
        elif 950 < self.rect.left:
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
        if self.health == 0:
            self.active = False


ship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
for counter in range(0, 1):
    warship = Ship()
    ship_group.add(warship)
player_group = pygame.sprite.Group()

background = pygame.Surface(screen.get_size()).convert()
background.fill((255, 255, 255))
screen.blit(background, (0, 0))

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
            y_clicked = 131 > y > 9

            if 131 > x > 9 and y_clicked:  # if the tank part of the menu is pressed
                tank_pressed = True
                missile_pressed = False
                seamine_pressed = False

            elif 245 > x > 139 and y_clicked:  # if the missile part of the menu is pressed
                tank_pressed = False
                missile_pressed = True
                seamine_pressed = False

            elif 391 > x > 245 and y_clicked:  # if the sea mine part of the menu is pressed
                tank_pressed = False
                missile_pressed = False
                seamine_pressed = True

            elif y_clicked and 400 < x < 520:  # if any other part of the menu is pressed
                if pause:  # if the game is already paused
                    pause = False
                elif not pause:  # if the game is not already paused
                    pause = True

            elif (not pause) and y > 150:  # if the main gameplay part is pressed
                item = 0
                pathway_pressed = (y < 243 and x > 140) or (383 < y < 453 and x < 840) or (595 >= y > 525 and x > 140) or (y > 595 and x > 840)

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
        paused = "Paused"
    else:
        pause_surface.fill(green)
        paused = "Resumed"

    for warship in ship_group.sprites():
        pass

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
        screen.blit(player.image, (player.x, player.y))
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


    top_bounds = 10
    screen.blit(white_surface, (0, 0))
    screen.blit(border, (9, top_bounds-1))
    screen.blit(tank_surface, (10, top_bounds))
    screen.blit(border, (139, top_bounds-1))
    screen.blit(missile_surface, (140, top_bounds))
    screen.blit(border, (269, top_bounds-1))
    screen.blit(seamine_surface, (270, top_bounds))
    screen.blit(border, (399, top_bounds-1))
    screen.blit(pause_surface, (400, top_bounds))
    screen.blit(main_border, (529, top_bounds-1))
    screen.blit(display, (530, top_bounds))
    scale = 150
    top_bounds = 100
    screen.blit(islandsdestroyed_text, (400+scale, top_bounds+15))
    screen.blit(chance_text, (650+scale, top_bounds+15))
    screen.blit(shipsdestroyed_text, (400+scale, top_bounds-25))
    screen.blit(shipsremaining_text, (650+scale, top_bounds-25))
    screen.blit(money_text, (400+scale, top_bounds-65))
    screen.blit(numweapons_text, (650+scale, top_bounds-65))
    scale = 50
    screen.blit(tank_text, (scale, top_bounds))
    screen.blit(missile_text, (100+scale, top_bounds))
    screen.blit(mine_text, (250+scale, top_bounds))
    screen.blit(tank_cost, (scale, top_bounds+15))
    screen.blit(missile_cost, (scale+100, top_bounds+15))
    screen.blit(mine_cost, (250+scale, top_bounds+15))
    screen.blit(paused_text, (375+scale, top_bounds-15))

    screen.blit(ball, (scale+3, 50))
    screen.blit(missile, (scale+98, 50))
    screen.blit(mine, (scale+260, 50))
    pygame.display.flip()

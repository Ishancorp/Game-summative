# World War Sea | A Pygame and Python Project
# Designed by Aryan Kukreja and Ishan Sharma
# Submitted to Mr. Cope for ICS3U1-01 as a summative project
# Submitted on Monday, May 23, 2016

# world_war_sea.py
# A Real-Time Surveillance Game
# Involves the militarization of an island in defence of an incoming attack
# For specific data on the game, open "ReadMe - Understanding the Game.txt"

# Files used in the game:
#   - Python files
#   - .gif image files
#   - .png image files
#   - .jpg image files
#   - .wav music files
#   - .mp3 music files
#   - .txt text files
# For a detailed description of every file, visit the ReadMe - List of Files

# Input: Selections made in game through mouse clicks
# Output: Playing the game

import pygame
from pygame.locals import *
import math
import random
from random import randint
import webbrowser

pygame.init()
screen = pygame.display.set_mode((1015, 768))

# Loading images and initializing list to store them in
back = pygame.image.load("Game Initial Sketch.png").convert_alpha()  # the background pic needs to be 1015x595 px.
tank_image = pygame.transform.rotate((pygame.image.load("Tank.gif").convert_alpha()), 180)
missile_image = pygame.image.load("Missile Launcher.png").convert_alpha()
mine_image = pygame.image.load("Sea mine.png").convert_alpha()

# Loading ammunition images
bullet_image = pygame.image.load("projectile.gif").convert_alpha()
rocket_image = pygame.image.load("Army Rocket.gif").convert_alpha()

# Loading enemy ship images
ship1_image = pygame.image.load("Army Ship Level 1.gif").convert_alpha()
ship2_image = pygame.image.load("Army Ship Level 2.gif").convert_alpha()
ship3_image = pygame.image.load("Army Ship Level 3.gif").convert_alpha()

# Loading splash screen images
splash = pygame.image.load("Splash_Screen.jpg").convert_alpha()

# Loading the high score background image
highscore_image = pygame.image.load("highscores_background.png").convert_alpha()

# Loading the settings screen image and the select image
settings = pygame.image.load("Settings_Screen.png").convert_alpha()
select = pygame.image.load("select.png")

# Loading the unselected image for the weapons in the gameplay
tank_grey = pygame.image.load("grey_surface.png").convert_alpha()
missile_grey = pygame.image.load("grey_surface.png").convert_alpha()
seamine_grey = pygame.image.load("grey_surface.png").convert_alpha()

# Loading the control buttons on the menu: Pause and retrn home
pause_red = pygame.image.load("pause_red.png").convert_alpha()
pause_green = pygame.image.load("pause_green.png").convert_alpha()
back_button_surface = pygame.image.load("back_button_surface.png").convert_alpha()

# Loading the weapons surface if user selects weapon and cannot afford it
tank_red = pygame.image.load("red_surface.png").convert_alpha()
missile_red = pygame.image.load("red_surface.png").convert_alpha()
seamine_red = pygame.image.load("red_surface.png").convert_alpha()

# Loading the weapons surface for the weapons if it is selected and user can afford it
tank_green = pygame.image.load("surface.png").convert_alpha()
missile_green = pygame.image.load("surface.png").convert_alpha()
seamine_green = pygame.image.load("surface.png").convert_alpha()

# Loading the background surface for the the menu
white_surface = pygame.image.load("back_surface.png").convert_alpha()

# Loading the menu information points for the gameplay:
#   Money Surface
#   Ships Surface
#   Weapons Surface
#   Loading the chances surface
money_surface = pygame.image.load("money_surface.png").convert_alpha()
ships_destroyed_surface = pygame.image.load("ships_destroyed_surface.png").convert_alpha()
weapons_surface = pygame.image.load("weapons_surface.png").convert_alpha()
chances_surface = pygame.image.load("chances_surface.png").convert_alpha()

# Loading the swirl designs for the levels
swirl_1 = pygame.image.load("swirl_image.png").convert_alpha()
swirl_2 = pygame.image.load("swirl_image.png").convert_alpha()

# Loading the image for the social media
social = pygame.image.load("socialmediabar.png").convert_alpha()

# Load sound effects here:
gunshot = pygame.mixer.Sound("gunshot.wav")
bomb = pygame.mixer.Sound("bomb.wav")
explosion = pygame.mixer.Sound("explosion.wav")

# Load the background music here
pygame.mixer.music.load("start_music.mp3")

# Loading all the colors used in the game
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

back_button_border = pygame.Surface((122, 77)).convert()
back_button_border.fill(black)

# Setting up the prices for the weapons
tank_price = 1000
mine_price = 50000
missile_price = 10000

# Setting up the fonts and text on the top of the game
font = pygame.font.SysFont("arial", 14)
splash_font = pygame.font.SysFont("helvetica", 80)
title_font = pygame.font.SysFont("helvetica", 117)

# Setting up the text of the game
tank_text = font.render("Tank".center(18), True, black)
tank_cost = font.render(("$" + str(tank_price)).center(18), True, black)
missile_text = font.render("Missile Launcher".center(18), True, black)
missile_cost = font.render(("$" + str(missile_price)).center(18), True, black)
mine_text = font.render("Sea Mine".center(18), True, black)
mine_cost = font.render(("$" + str(mine_price)).center(18), True, black)
paused = font.render("", True, black)
go_back_home = font.render("Quit".center(18), True, black)

# setting up variables that will be displayed on top
money = 55000
chances = 0
pause = True
ships_destroyed = 9
ships_remaining = 0
tank_pressed = True
missile_pressed = False
seamine_pressed = False
wave_interval = 800

# Setting up the highscores variable
high_scores = []

# Turning on music
music = True

# Number of ships spawned
ship_spawns = 0

# variables relating to user weapons - angle, sprite type, and number of weapons of the user
sprite_type = ""
angle = 0
weapons = 0

# Variables relating to screens other than the gameplay
splash_screen = True
settings_screen = False
game_over = False
score_achieved_index = 11
level = 1

# Defining the Class for the rocket launched from the missile launcher
# Rocket is initialized with the angle, x position y-position, and angle it is facing.
# Initializing whether it is active or not
# Initializing the money earnied from it's hit in the ship
# Size of the Rocket is defined
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, angle_missile):
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle_missile
        self.image = pygame.transform.rotate(rocket_image, self.angle)
        self.rect = self.image.get_rect()
        self.x = x_pos
        self.y = y_pos
        self.dir_x = -16 * math.sin(self.angle)
        self.dir_y = -16 * math.cos(self.angle)
        self.rect.move_ip(self.x, self.y)
        self.active = True
        self.money = 15

    # Defining the image of the rocket
    # Moving the rocket in the direction of x or y
    #    For every enemy ship active in the gameplay
    #   If the rocket collides with any of the enemy ships:
    #          Deactivate it
    #          Take 5 off the enemy ship's health (only for the one it hit)
    #          Add money to the user's money supply
    #          The sound of the explosion is played
    def update(self):
        self.image = pygame.transform.rotate(rocket_image, math.degrees(self.angle))
        self.rect.move_ip(self.dir_x, self.dir_y)
        self.x = self.rect.left
        self.y = self.rect.top
        for enemy in ship_group:
            if self.rect.colliderect(enemy.rect):
                self.active = False
                enemy.health -= 5
                if music:
                    bomb.play()
        if 0 > self.x or self.x > screen.get_size()[0] or 0 > self.y or self.y > screen.get_size()[1]:
            self.active = False

# Defining the Class for the Army mine
# Army Mine is initialized with the angle, x position y-position, and angle it is facing.
# Initializing whether it is active or not
# Initializing the money earnied from it's hit in the ship
# Size of rocket is defined
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

    # The position of the mine is defined through self.x and self.y
    # For every enemy ship active in the game:
    #       If the enemy ship collides with the mine:
    #           It blows up and disappears
    #           The user gets money for it
    #           Enemy Health of the hit ship is set to zero
    #           The sound of an explosion is played
    #           The mine is un-blitted

    def update(self):
        self.x = self.rect.left
        self.y = self.rect.top
        for enemy in ship_group:
            if self.rect.colliderect(enemy.rect):
                self.active = False
                enemy.health = 0
                if music:
                    explosion.play()

# Defining the Class for the Tank Projectile
# Tank Projectile is initialized with the angle, x position y-position, and angle it is facing.
# Initializing whether it is active or not
# Initializing the money earned from it's hit in the ship
# Size of bullet is defined
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, angle_tank):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.x = x_pos
        self.y = y_pos
        self.angle = angle_tank
        self.dir_x = -8 * math.sin(self.angle)
        self.dir_y = -8 * math.cos(self.angle)
        self.rect.move_ip(self.x, self.y)
        self.active = True
        self.money = 2

    # The position of the projectile is defined through self.x and self.y
    # For every enemy ship active in the game:
    #       If the enemy ship collides with the projectile:
    #           It loses 5 enemy health
    #           The user gets money for it
    #           If the enemy health hits zero, the ship is un-blitted
    #           The sound of an explosion is played
    #           The mine is un-blitted
    def update(self):
        self.rect.move_ip(self.dir_x, self.dir_y)
        self.x = self.rect.left
        self.y = self.rect.top
        for enemy in ship_group:
            if self.rect.colliderect(enemy.rect):
                self.active = False
                enemy.health -= 5
                if music:
                    gunshot.play()
        if 0 > self.x or self.x > screen.get_size()[0] or 0 > self.y or self.y > screen.get_size()[1]:
            self.active = False

# Defining the Class for the Tank
# Tank is initialized with the angle, x position y-position, and angle it is facing.
# Initializing whether it is active or not
# Initializing the money earned from it's hit in the ship
# Size of Tank is defined as self.size
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

    # The position of the Tank is defined through self.x and self.y
    # For every enemy ship active in the game:
    #       If the enemy ship is within a certain range of the tank
    #           The tank fires a projectile at it
    #           The timer has one added to it; if it is 5, it is reset to 1
    #           The tank fires every one fifth of a second in a 30 frame game clock
    #           The tank is rotated to face the enemy ship
    def update(self):
        for enemy in ship_group:
            if 500 > self.x - enemy.x > -500 and 250 > self.y - enemy.y > -250:
                lower = abs(self.y - enemy.y + (enemy.image.get_size()[1] / 2))
                if lower == 0:
                    lower = 10**100
                self.angle = math.atan((self.x - abs(enemy.x + (enemy.image.get_size()[0] / 2))) / lower)
                self.angle_adjust = self.angle * 35 / math.pi
                if self.y < enemy.y:
                    self.angle = 135 - self.angle
                self.timer += 1
                if self.timer == 5:
                    bullet_group.add(Bullet(self.x + (tank_image.get_size()[0] / 2), self.y + (tank_image.get_size()[1] / 2), self.angle))
                    self.timer = 0
                self.image = pygame.transform.rotate(tank_image, math.degrees(self.angle))
                break

# Defining the Class for the Missile Launcher
# Missile Launcher is initialized with the angle, x position y-position, and angle it is facing.
# Initializing whether it is active or not
# Initializing the money earned from it's hit in the ship
# Size of Missile Launcher is defined
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

    # The position of the Tank is defined through self.x and self.y
    # For every enemy ship active in the game:
    #       If the enemy ship is within a certain range of the missile launcher (a much larger range than the tank)
    #           The missile launcher fires four projectile at it
    #           The timer has one added to it; if it is 30, it is reset to 1
    #           The tank fires every second in a 30 frame game clock
    #           The missile launcher is NOT is rotated to face the enemy ship
    def update(self):
        for enemy in ship_group:
            if 500 > self.x - enemy.x > -500 and 500 > self.y - enemy.y > -500:
                lower = abs(self.y - enemy.y + (enemy.image.get_size()[1] / 2))
                if lower == 0:
                    lower = 10**100
                self.angle = math.atan((self.x - abs(enemy.x + (enemy.image.get_size()[0] / 2))) / lower)
                if self.y < enemy.y:
                    self.angle = 135 - self.angle
                self.timer += 1
                if self.timer == 30:
                    bullet_group.add(Rocket(self.x + (1.25 * missile_image.get_size()[0] / 7), self.y, self.angle))
                    bullet_group.add(Rocket(self.x + (1.1 * missile_image.get_size()[0] / 3), self.y, self.angle))
                    bullet_group.add(Rocket(self.x + (1.625 * missile_image.get_size()[0] / 3), self.y, self.angle))
                    bullet_group.add(Rocket(self.x + 0.73 * missile_image.get_size()[0], self.y, self.angle))
                    self.timer = 0
                break

# Defining the Class for the Ships
# The ships are selected to become active on a random basis
# Ship is initialized with the angle, x position y-position, and angle it is facing.
# Initializing whether it is active or not
# Initializing whether it has crossed the island or not
# Initializing the money earned from it's hit in the ship
# Size of ship is defined
# Health of ship is defined based in the type of ship selected from the random
# Loot from ship is also defined based on type of whip coming from random selection
class Ship(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        ship_choice = randint(1, 6)
        if 6 >= ship_choice >= 1:
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

    # The motion of the ship is specified here
    # This includes directions from start to stop
    # If the ship's health has run out, un-blit it
    def update(self):
        self.x = self.rect.left
        self.y = self.rect.top
        if self.y < 150:
            self.dir_y = 1
            self.dir_x = 0
        elif self.y == 155:
            self.image = pygame.transform.rotate(self.image, 90)
            self.y = random.randrange(250, 345)
        elif 345 > self.y > 250 and self.x < 800:
            self.dir_y = 0
            self.dir_x = 1
        elif self.x == 800 and 345 > self.y > 250:
            self.image = pygame.transform.rotate(self.image, 90)
            self.x = random.randrange(850, 980)
        elif 981 > self.x > 850 and self.y < 345:
            self.dir_y = 1
            self.dir_x = 0
        elif self.y == 345:
            self.image = pygame.transform.rotate(self.image, 90)
            self.y = random.randrange(461, 531)
            self.x = 800
        elif 460 < self.y < 532 and self.x > 100:
            self.dir_x = -1
            self.dir_y = 0
        elif self.x == 100 and 532 > self.y > 460:
            self.image = pygame.transform.rotate(self.image, 90)
            self.x = random.randrange(99, 100)
        elif self.x < 100 and 392 <= self.y < 600:
            self.dir_x = 0
            self.dir_y = 1
        elif self.x < 100 and self.y == 600:
            self.image = pygame.transform.rotate(self.image, 90)
            self.y = random.randrange(630, 760)
        elif self.y > 630 and self.x < 650:
            self.dir_x = 1
            self.dir_y = 0
        elif self.y > 630 and self.x == 650:
            self.dir_x = 0
            self.dir_y = 0
            self.active = False
            self.victor = True
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.x, self.y)

        self.rect.move_ip(self.speed * self.dir_x, self.speed * self.dir_y)
        if self.health <= 0:
            self.active = False
            self.money = self.late_money

# Initializing the different groups of sprites in the game
ship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# Initializing the clock and keeping the game on
clock = pygame.time.Clock()
keep_going = True
while keep_going:
    # Clock is set to 30 frames per second
    # If the user wants to quit the game, keep_going = False
    clock.tick(30)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            keep_going = False

        # If the user clicks the mouse button
        # Obtain x and y position of the mouse click
        # If splash screen is on, user can either click play or settings
        # Or if the setting screen is live then the user can either turn the music on or off, or return to the home page
        # Or if the game over screen is live, then user can only select the return home menu
        elif ev.type == MOUSEBUTTONDOWN:
            x_unadjusted = ev.pos[0]
            y_unadjusted = ev.pos[1]
            x = (x_unadjusted // 35) * 35  # getting the x of where the mouse clicked
            y = (y_unadjusted // 35) * 35  # getting the y of where the mouse clicked
            if game_over:  # if the game is over, if the lower part of the screen is pressed, game is quitted
                if y_unadjusted > 600:
                    keep_going = False
            elif splash_screen:
                y_selected = 20 < y < 50
                if (380 < x_unadjusted < 640) and (480 < y_unadjusted < 570):
                    splash_screen = False
                    pause = False
                elif (300 < x_unadjusted < 750) and (590 < y_unadjusted < 680):
                    settings_screen = True
                    splash_screen = False
                elif y_selected and x < 840 + 25:
                    webbrowser.get().open('http://www.twitter.com')
                elif y_selected and 840 + 25 < x < 890:
                    webbrowser.get().open('http://www.facebook.com')
                elif y_selected and 890 < x < 915:
                    webbrowser.get().open('http://www.linkedin.com')
                elif y_selected and 865 + 75 < x < 965:
                    webbrowser.get().open('http://plus.google.com')
                elif y_selected and 965 < x < 990:
                    webbrowser.get().open('http://www.instagram.com')
            elif settings_screen:
                if (0 < x_unadjusted < 1015) and (320 - 30 < y_unadjusted < 435 + 30):
                    music = True
                elif (0 < x_unadjusted < 1015) and (470 - 30 < y_unadjusted < 535 + 10):
                    music = False
                elif y_unadjusted > 650:
                    splash_screen = True
                    pause = True
                    settings_screen = False

            # If the user is in the main gameplay:
            # He can select between the tank, missile launcher, or sea mine
            # Alternatively he can click on the pause/unpause button
            # He can also return home
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

                elif 90 > y_unadjusted > 9 and 400 < x_unadjusted < 520:  # if any other part of the menu is pressed
                    if pause:  # if the game is already paused
                        pause = False
                    elif not pause:  # if the game is not already paused
                        pause = True

                elif 142 > y_unadjusted > 91 and 400 < x_unadjusted < 520:
                    splash_screen = True
                    pause = True
                    player_group.empty()
                    ship_group.empty()
                    bullet_group.empty()

                # If the action part of the game play is pressed:
                # Check of the user's weapon is touching going on the wrong geographical location
                # Check if the user's weapons are overlapping each other
                # If they are not overlapping:
                # Add the user weapon to the desired location and charge the user money
                elif (not pause) and y > 150:
                    item = 0
                    pathway_pressed = (y < 243 and x > 140) or (383 < y < 453 and x < 840) or (595 >= y > 525 and x > 140) or (y > 595 and x > 840)  # boolean for whether or not the path is pressed
                    overlap = False
                    for player in player_group.sprites():
                        if (x == player.x and y == player.y) or (missile_pressed and player.x - 70 <= x <= player.x and y == player.y) or (player.type == "M" and player.x <= x <= player.x + 70 and y == player.y):  # if an item overlaps with any other item
                            overlap = True

                    if not overlap:
                        if tank_pressed and pathway_pressed and (money - tank_price) >= 0:
                            weapons += 1
                            player_group.add(Tank(x, y))
                            money -= tank_price

                        elif missile_pressed and pathway_pressed and money - missile_price >= 0:
                            player_group.add(MissileLauncher())
                            weapons += 1
                            money -= missile_price

                        elif seamine_pressed and money - mine_price >= 0 and not pathway_pressed:
                            player_group.add(Mine(x, y))
                            weapons += 1
                            money -= mine_price

                        else:
                            break

    # If the game is not paused:
    # Spawn ships continuously
    # Increase the rate of spawning by 0.925 every frame
    # If the level becomes 2:
    # Increment the prices of the tank, missile launcher and mine
    # Increase the health of the ships
    # Empty the bullet, ship and weapons sprites group
    # Re-blit the weapons prices
    if not pause:
        ship_spawns += 1
        if ship_spawns == wave_interval or len(ship_group) == 0:
            ship_group.add(Ship(100, 173))
            ship_spawns = 0
            wave_interval *= 0.925
            if wave_interval < 20:
                back = pygame.image.load("Game Initial Sketch.png").convert_alpha()
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
                    tank_cost = font.render(("$" + str(tank_price)).center(18), True, black)
                    missile_cost = font.render(("$" + str(missile_price)).center(18), True, black)
                    mine_cost = font.render(("$" + str(mine_price)).center(18), True, black)
                    pause = True
            wave_interval = int(wave_interval)

    # Get status of music
    # Activate music if not on gameplay screen
    # Deactivate music if on gameplay screen
    # Fade music out in 1 second
    music_active = pygame.mixer.music.get_busy()
    if not music_active:
        if music:
            pygame.mixer.music.play(-1)
    elif music_active:
        if not music:
            pygame.mixer.music.fadeout(1000)
        elif not splash_screen and not settings_screen and not game_over:
            pygame.mixer.music.fadeout(1000)

    # Update the status of the weapons surfaces on the menu
    # If the user has selected the weapon and can afford it, use the green surface
    # If the user can't afford it and has selected it, fill it with the red surface
    # If the user has not selected it, fill it with the grey surface
    if not tank_pressed:
        tank_surface = tank_grey
    elif (tank_price - money) > 0:
        tank_surface = tank_red
    else:
        tank_surface = tank_green

    if not missile_pressed:
        missile_surface = missile_grey
    elif (missile_price - money) > 0:
        missile_surface = missile_red
    else:
        missile_surface = missile_green

    if not seamine_pressed:
        seamine_surface = seamine_grey
    elif (mine_price - money) > 0:
        seamine_surface = seamine_red
    else:
        seamine_surface = seamine_green

    if pause:
        pause_surface = pause_green
    else:
        pause_surface = pause_red

    # If the game is not paused
    # Update the game's bullet, ship, and user weapons group
    if not pause:
        ship_group.update()
        player_group.update()
        bullet_group.update()

    # Render the on-screen menu text for the money, weapons, lives, and number of ships destroyed
    money_text = font.render("Money: $" + str(money), True, white)
    numweapons_text = font.render("Ammo Used: " + str(weapons), True, white)
    chance_text = font.render("Chances: " + str(chances), True, white)
    shipsdestroyed_text = font.render("Ships Dead: " + str(ships_destroyed), True, white)
    level_text = font.render("Level " + str(level), True, white)

    # Blit the background of the gameplay
    # If the user weapon in the game is active:
    # Blit it; if not, remove the weapon from the player group
    # Repeat the above lines for the projectile group and the ship group of sprites
    # For the ship group, if the ship reaches the end of the island, decrease the user's lives by 1
    # If the ship is destroyed, remove the ship and add money to the user
    screen.blit(back, (0, 173))
    for player in player_group.sprites():
        if player.active:
            screen.blit(player.image, (player.x, player.y - 2))
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

    # If the user loses the game (lives are 0):
    # pause the game, empty all 3 groups, open up the game_over screen with the highscores.
    # To show highscores:
    # For every highscore saved in the highscores.txt file, append it to the list high_scores.
    # Check the current high score and compare it to every line
    # If the current highscore is less than the highscore it is being compared to:
    # Move to the next line; if not, then insert the highscore just before the one it is larger than.
    # Write the entire highscore list to the file "highscores.txt and blit them out on the screen
    if chances == 0:
        pause = True
        game_over = True
        chances = 3
        player_group.empty()
        ship_group.empty()
        bullet_group.empty()
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
                file.write(str(score) + chr(10))
        game_over = True

    # Blit the weapons surface on the menu
    # This blitting does not include the price and name of the weapons; those are blitted later
    # Set a standard value for the y values of the blitting
    # Blit their borders
    top_bounds = 10
    screen.blit(white_surface, (0, 0))
    screen.blit(border, (9, top_bounds - 1))
    screen.blit(tank_surface, (10, top_bounds))
    screen.blit(border, (139, top_bounds - 1))
    screen.blit(missile_surface, (140, top_bounds))
    screen.blit(border, (269, top_bounds - 1))
    screen.blit(seamine_surface, (270, top_bounds))
    screen.blit(pause_surface, (400, top_bounds))

    # Set a standard value for the x-values of all the items being blitted
    # Then adjust them by adding or subtracting scale by a number
    # Blit the data and information section of the gameplay menu
    # Blit the level number with the fancy design beside it
    scale = 125
    top_bounds = 100
    screen.blit(money_surface, (530 + 65, 10))
    screen.blit(money_text, (543 + 65, 85))
    screen.blit(ships_destroyed_surface, (635 + 65, 10))
    screen.blit(shipsdestroyed_text, (640 + 65, 85))
    screen.blit(weapons_surface, (740 + 65, 10))
    screen.blit(numweapons_text, (750 + 65, 85))
    screen.blit(chances_surface, (845 + 65, 10))
    screen.blit(chance_text, (855 + 65, 85))

    screen.blit(swirl_1, (600, 150))
    screen.blit(level_text, (743, 150))
    screen.blit(swirl_2, (800, 150))

    # Here, the name of the weapon is blitted onto the screen
    # The price of the weapon is also blitted here
    scale = 50
    screen.blit(tank_text, (10, top_bounds))
    screen.blit(missile_text, (143, top_bounds))
    screen.blit(mine_text, (270, top_bounds))
    screen.blit(tank_cost, (10, top_bounds + 15))
    screen.blit(missile_cost, (140, top_bounds + 15))
    screen.blit(mine_cost, (270, top_bounds + 15))

    # The border for the back button is blitted here
    # The back button image is blitted in fromt of it
    screen.blit(back_button_border, (400, 90))
    screen.blit(back_button_surface, (400, 90))

    # The image of the tank, missile launcher and mine are blitted here fot the menu
    screen.blit(tank_image, (scale + 3, 50))
    screen.blit(missile_image, (scale + 98, 50))
    screen.blit(mine_image, (scale + 260, 50))

    # If the user is on the splash screen:
    # Blit the start screen image
    # Blit the social media icons
    if splash_screen:
        screen.blit(splash, (0, 0))
        screen.blit(social, (850, 20))

    # If the user is on the settings screen:
    # Blit the settings screen image on the screen
    # If music is true:
    #   Blit the select image on the music:on area
    # If music is false; the user does not want music:
    #   Blit the selsct image on the music:off area
    if settings_screen:
        screen.blit(settings, (0, 0))
        if music:
            screen.blit(select, (132, 382 + 15))
        elif not music:
            screen.blit(select, (132, 470 + 13))

    # If the game is over:
    # Blit the highscores image
    # Blit the heading of the highscores table
    # If the rank number is that of the user:
    # Set it to red to differentiate it from the other ranks
    # If it is not the user's score, and it is some past score:
    # Set the color to black
    # If the user is not in the top 10:
    #   Blit his score as 11th on the screen in red
    if game_over:
        screen.blit(highscore_image, (0, 0))
        rank_text = font.render("Rank".ljust(20) + "Score", True, black)
        screen.blit(rank_text, (400, 195 - 15))

        for score_index in range(0, len(high_scores[0:10])):
            if score_index == score_achieved_index:
                rank_text = font.render((str(score_index + 1)).ljust(20) + str(high_scores[score_index]), True, red)
            else:
                rank_text = font.render((str(score_index + 1)).ljust(20) + str(high_scores[score_index]), True, black)
            screen.blit(rank_text, (400, 230 + 30 * score_index - 15))

        if score_achieved_index > 10:
            rank_text = font.render(str(11).ljust(20) + str(ships_destroyed), True, red)
            screen.blit(rank_text, (400, 230 + 35 * 11))

    # Flip the display program so that the user can see the screen and the images
    pygame.display.flip()

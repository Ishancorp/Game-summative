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
back = pygame.image.load("Game Initial Sketch.png").convert()  # the background pic needs to be 1015x595 px.
ball = pygame.image.load("Tank.gif").convert()  # must be 35x35, or (some multiple of 35)x(some multiple of 35)
missile = pygame.image.load("Missile Launcher.gif").convert()
mine = pygame.image.load("Sea Mine.png")
norm_enemy_ship = pygame.image.load("Army Ship Level 1.gif").convert()
bullet = pygame.image.load("projectile.gif").convert()
rocket = pygame.image.load("Army Rocket.gif").convert()
img = []

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
border_surface = pygame.Surface((3, bottom_bounds)).convert()
border_surface.fill(black)
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
back_button_surface = pygame.Surface((120, bottom_bounds)).convert()
back_button_surface.fill(dark_blue)
back_button_border_surface = pygame.Surface((122, bottom_bounds + 2)).convert()
back_button_border_surface.fill(black)

# fonts and text on the top of the game
font = pygame.font.SysFont("helvetica", 14)
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
escape_settings = font.render("Click 'q' on the keyboard to go back to the home page", True, black)

go_back_home = font.render("Return Home", True, black)

# setting up coordinate variables
x = 0
y = 0
y_enemy = 15
x_enemy = 100

# setting up variables that will be displayed on top
money = 10000000
chances = 3
pause = True
ships_destroyed = 0
ships_remaining = 0
tank_pressed = True
missile_pressed = False
seamine_pressed = False
speed_enemy = 0.5

tank_price = 1000
mine_price = 50000
missile_price = 10000

keys = pygame.key.get_pressed()

# variables relating to bullet
sprite_type = ""
angle = 0
music = True

# whether or not the enemy ship has been rotated
rotate = False
splash_screen = True
settings_screen = False

# Game engine
clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(30)
    for ev in pygame.event.get():
        if ev.type == QUIT:  # if the game is quit
            keep_going = False
        elif ev.type == MOUSEBUTTONDOWN:  # if the mouse is pressed
            x = ((ev.pos[0]) // 35) * 35  # getting the x of where the mouse clicked
            y = ((ev.pos[1]) // 35) * 35  # getting the y of where the mouse clicked
            if splash_screen:
                if (blue_surface.get_size()[0] / 3 < x < blue_surface.get_size()[0] / 3 + 300) and (blue_surface.get_size()[1] / 2 - 100 < y < blue_surface.get_size()[1] / 2):
                    print("play")
                    splash_screen = False
                    pause = False
                elif (blue_surface.get_size()[0] / 3 < x < blue_surface.get_size()[0] / 3 + 300) and (blue_surface.get_size()[1] / 2 + 100 < y < blue_surface.get_size()[1] / 2 + 200):
                    settings_screen = True
                    splash_screen = False
                    print("settings")
            if settings_screen:
                if (100 < x < 1015) and (0 < y < 400):
                    music = True
                elif (100 < x < 1015) and (400 < y < 768):
                    music = False
                elif x < 100:
                    splash_screen = True
                    pause = True
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
                elif y_clicked and 529 < x < 670:
                    pause = True
                    splash_screen = True
                    img = []
                elif (not pause) and y > 150:  # if the main gameplay part is pressed
                    overlap = False
                    for image in img:
                        if (image[1] == x and image[2] == y) or (sprite_type == "M" and (image[1] == x or image[1] == x-35 or image[1] == x-70) and image[2] == y) or (missile_pressed and (image[1] == x or image[1] == x+35 or image[1] == x+70) and image[2] == y):
                            overlap = True
                            print("Overlap")
                    # overlap is true if the x and y of the sprite is already covered
                    if not overlap:
                        item = 0
                        pathway_pressed = (y < 243 and x > 140) or (383 < y < 453 and x < 840) or (595 >= y > 525 and x > 140) or (y > 595 and x > 840)
                        if tank_pressed and pathway_pressed and (money - tank_price) >= 0:
                            item = ball
                            sprite_type = "T"
                            money -= tank_price
                            img.append([item, x, y - 2.5, sprite_type, 0, [], 0])
                        elif missile_pressed and pathway_pressed and money - missile_price >= 0:
                            item = missile
                            sprite_type = "M"
                            money -= missile_price
                            img.append([item, x, y - 2.5, sprite_type, 0, [], 0])
                        elif seamine_pressed and money - mine_price >= 0 and not pathway_pressed:
                            item = mine
                            sprite_type = "S"
                            money -= mine_price
                            img.append([item, x, y, sprite_type, 0, [], 0])
                        else:
                            break

    # paint selection surfaces to their colours
    if music:
        yes_music_surface.fill(green)
        no_music_surface.fill(light_gray)
    elif not music:
        yes_music_surface.fill(light_gray)
        no_music_surface.fill(green)
    if pause:
        pause_surface.fill(red)
        paused = font.render("Play", True, black)
    else:
        pause_surface.fill(green)
        paused = font.render("Pause", True, black)
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

    # render text with new values for every variable
    money_text = font.render("Money: $" + str(money), True, black)
    numweapons_text = font.render("Weapons: " + str(len(img)), True, black)
    islandsdestroyed_text = font.render("Islands Destroyed: " + str(3 - chances), True, black)
    chance_text = font.render("Chances: " + str(chances), True, black)
    shipsdestroyed_text = font.render("Ships Destroyed: " + str(ships_destroyed), True, black)
    shipsremaining_text = font.render("Ships Remaining: " + str(ships_remaining), True, black)

    # code for enemy ships route
    if not pause:
        if y_enemy < 100 or (x_enemy >= (screen.get_size()[0]-200) and y_enemy < 350):
            y_enemy += speed_enemy
            if x_enemy == (screen.get_size()[0] - 200):
                norm_enemy_ship = pygame.transform.rotate(norm_enemy_ship, -90)
                rotate = False
                x_enemy += 10
                y_enemy += 10
        elif y_enemy == 100 or (y_enemy == 350 and x_enemy == (screen.get_size()[0]-190)):
            norm_enemy_ship = pygame.transform.rotate(norm_enemy_ship, 90)
            rotate = True
            x_enemy += speed_enemy
            y_enemy += 150
        elif y_enemy == 350:
            norm_enemy_ship = pygame.transform.rotate(norm_enemy_ship, 270)
            rotate = False
            x_enemy -= speed_enemy
        elif y_enemy > 350 and x_enemy > 125:
            x_enemy -= speed_enemy
        elif x_enemy == 125 and y_enemy > 350:
            norm_enemy_ship = pygame.transform.rotate(norm_enemy_ship, 90)
            rotate = True
            x_enemy -= 0.01
        elif x_enemy < 125 and y_enemy > 350:
            y_enemy += speed_enemy
        else:
            x_enemy += speed_enemy

    # Blitting
    screen.blit(back, (0, 173))
    for ship_pointer in range(0, len(img)):  # looping through player stuff
        angle = 0
        if img[ship_pointer][3] == "T":  # if the item is a tank
            if not rotate:  # If the enemy ship has not been rotated
                lower = y_enemy-img[ship_pointer][2] - 20 + (norm_enemy_ship.get_size()[0] / 0.75)  # this code will be the divisor, may be equal to zero at times
                if lower == 0:  # if the divisor is zero, set it to a very large number
                    lower = 10**23
                angle = math.atan((x_enemy - img[ship_pointer][1] + (norm_enemy_ship.get_size()[1] / 100)) / lower) * 180 / 3.14  # finding the angle the tank needs to be pointed to
                angle -= 180
            else:  # If the ship has not been rotated
                lower = y_enemy - img[ship_pointer][2] - 20 + (norm_enemy_ship.get_size()[1] / 2)  # this code will be the divisor, may be equal to zero at times
                if lower == 0:  # if the divisor is zero, set it to a very large number
                    lower = 10**23
                angle = math.atan((x_enemy - img[ship_pointer][1] + (norm_enemy_ship.get_size()[0] / 2)) / lower) * 180 / 3.14  # finding the angle the tank needs to be pointed to
                angle -= 180
            if img[ship_pointer][2] <= y_enemy:  # if the tank is higher than the ship, invert it
                angle += 180
            img[ship_pointer][6] += 1  # add one to the ship's timer
            if img[ship_pointer][6] == 5:  # if ship timer is 5, reset it, and if the game is not paused, spawn bullet
                img[ship_pointer][6] = 0
                if not pause:
                    img[ship_pointer][5].append([bullet, img[ship_pointer][1]+(ball.get_size()[0] / 2), img[ship_pointer][2] + (ball.get_size()[1] / 2), math.sin(angle*3.14 / 180), math.cos(angle * 3.14 / 180)])
            for bullet_pointer in range(0, len(img[ship_pointer][5])):  # looping through bullets
                if not (img[ship_pointer][5][bullet_pointer] is None):  # if the bullet exists and has not been deleted
                    if not pause:
                        img[ship_pointer][5][bullet_pointer][1] += 5 * img[ship_pointer][5][bullet_pointer][3]  # moving the bullet's x
                        img[ship_pointer][5][bullet_pointer][2] += 5 * img[ship_pointer][5][bullet_pointer][4]  # moving the bullet's y
                    if 0 < img[ship_pointer][5][bullet_pointer][1] < 1015 and 0 < img[ship_pointer][5][bullet_pointer][2] < 768:  # only blit it if it is on the screen, otherwise delete it
                        screen.blit(img[ship_pointer][5][bullet_pointer][0], (img[ship_pointer][5][bullet_pointer][1], img[ship_pointer][5][bullet_pointer][2]))
                    else:
                        img[ship_pointer][5][bullet_pointer] = None
        elif img[ship_pointer][3] == "M":  # if the item is a tank
            if not rotate:  # If the enemy ship has not been rotated
                lower = y_enemy - img[ship_pointer][2] - 20 + (norm_enemy_ship.get_size ()[0] / 0.75)  # this code will be the divisor, may be equal to zero at times
                if lower == 0:  # if the divisor is zero, set it to a very large number
                    lower = 10 ** 23
                angle = math.atan ((x_enemy - img[ship_pointer][1] + (norm_enemy_ship.get_size ()[1] / 100)) / lower) * 180 / 3.14  # finding the angle the tank needs to be pointed to
            else:  # If the ship has been rotated
                lower = y_enemy - img[ship_pointer][2] - 20 + (norm_enemy_ship.get_size ()[1] / 2)  # this code will be the divisor, may be equal to zero at times
                if lower == 0:  # if the divisor is zero, set it to a very large number
                    lower = 10 ** 23
                angle = math.atan((x_enemy - img[ship_pointer][1] + (norm_enemy_ship.get_size ()[0] / 2)) / lower) * 180 / 3.14  # finding the angle the tank needs to be pointed to
            if img[ship_pointer][2] <= y_enemy:  # if the tank is higher than the ship, invert it
                img[ship_pointer][6] += 1  # add one to the ship's timer
            if img[ship_pointer][6] == 20:  # if the ship's timer is five, reset it, and if the game is not paused, spawn a bullet
                img[ship_pointer][6] = 0
                if not pause:
                    img[ship_pointer][5].append ([rocket, img[ship_pointer][1] + (ball.get_size ()[0] / 2) - 15, img[ship_pointer][2] + (ball.get_size ()[1] / 2), math.sin (angle * 3.14 / 180), math.cos (angle * 3.14 / 180)])
                    img[ship_pointer][5].append ([rocket, img[ship_pointer][1] + (ball.get_size ()[0] / 2) + 10, img[ship_pointer][2] + (ball.get_size ()[1] / 2), math.sin ((angle) * 3.14 / 180), math.cos ((angle) * 3.14 / 180)])
                    img[ship_pointer][5].append ([rocket, img[ship_pointer][1] + (ball.get_size ()[0] / 2) + 40, img[ship_pointer][2] + (ball.get_size ()[1] / 2), math.sin ((angle) * 3.14 / 180), math.cos ((angle ) * 3.14 / 180)])
                    img[ship_pointer][5].append ([rocket, img[ship_pointer][1] + (ball.get_size ()[0] / 2) + 67, img[ship_pointer][2] + (ball.get_size ()[1] / 2), math.sin ((angle) * 3.14 / 180), math.cos ((angle ) * 3.14 / 180)])
            for bullet_pointer in range (0, len (img[ship_pointer][5])):  # looping through bullets
                if not (img[ship_pointer][5][bullet_pointer] is None):  # if the bullet actually exists and has not been deleted
                    if not pause:
                        img[ship_pointer][5][bullet_pointer][1] += 6 * img[ship_pointer][5][bullet_pointer][3]  # moving the bullet's x
                        img[ship_pointer][5][bullet_pointer][2] += 6 * img[ship_pointer][5][bullet_pointer][4]  # moving the bullet's y
                    if 0 < img[ship_pointer][5][bullet_pointer][1] < 1015 and 0 < img[ship_pointer][5][bullet_pointer][2] < 768:  # only blit it if it is on the screen, otherwise delete it
                        screen.blit(img[ship_pointer][5][bullet_pointer][0],(img[ship_pointer][5][bullet_pointer][1], img[ship_pointer][5][bullet_pointer][2]))
                    else:
                        img[ship_pointer][5][bullet_pointer] = None
        img[ship_pointer][4] = angle  # add the variable "angle" to the image, before blitting the ship
        if img[ship_pointer][3] == "T":
            screen.blit(pygame.transform.rotate(img[ship_pointer][0], angle), (img[ship_pointer][1], img[ship_pointer][2]))
        elif img[ship_pointer][3] == "M":
            screen.blit(img[ship_pointer][0], (img[ship_pointer][1], img[ship_pointer][2]))
    screen.blit(norm_enemy_ship, (x_enemy, y_enemy))  # blitting the enemy

    # blitting the top part of the screen
    top_bounds = 10
    screen.blit(white_surface, (0, 0))
    screen.blit(border, (9, top_bounds-1))
    screen.blit(tank_surface, (10, top_bounds))
    screen.blit(border, (139, top_bounds-1))
    screen.blit(missile_surface, (140, top_bounds))
    screen.blit(border, (269, top_bounds-1))
    screen.blit(seamine_surface, (270, top_bounds))
    screen.blit(main_border, (704, top_bounds-1))
    screen.blit(display, (705, top_bounds))
    screen.blit(border, (399, top_bounds - 1))
    screen.blit(pause_surface, (400, top_bounds))

    scale = 150
    top_bounds = 100
    screen.blit(paused, (408, 50))
    screen.blit(islandsdestroyed_text, (400+scale + 200, top_bounds+15))
    screen.blit(shipsdestroyed_text, (400+scale +200, top_bounds-25))
    screen.blit(money_text, (400+scale + 200, top_bounds-65))
    screen.blit(shipsremaining_text, (650+scale + 100, top_bounds-25))
    screen.blit(numweapons_text, (650+scale + 100, top_bounds-65))
    screen.blit(chance_text, (650+scale + 100, top_bounds+15))

    scale = 50
    screen.blit(tank_text, (scale, top_bounds))
    screen.blit(missile_text, (110+scale, top_bounds))
    screen.blit(mine_text, (250+scale, top_bounds))
    screen.blit(tank_cost, (scale, top_bounds+15))
    screen.blit(missile_cost, (scale+110, top_bounds+15))
    screen.blit(mine_cost, (250+scale, top_bounds+15))

    screen.blit(back_button_border_surface, (529, top_bounds - 91))
    screen.blit(back_button_surface, (530, top_bounds-90))
    screen.blit(go_back_home, (535, top_bounds - 45))

    screen.blit(ball, (scale+3, 50))
    screen.blit(missile, (scale+98, 50))
    screen.blit(mine, (scale + 260, 50))

    if splash_screen:
        screen.blit(blue_surface, (0, 0))
        screen.blit(play_surface, (blue_surface.get_size()[0]/3, blue_surface.get_size()[1]/2-100))
        screen.blit(settings_surface, (blue_surface.get_size()[0]/3, blue_surface.get_size()[1]/2+100))
        screen.blit(title_text, (blue_surface.get_size()[0]/15, blue_surface.get_size()[1]/2-300))
        screen.blit(play_text, (blue_surface.get_size()[0]/3, blue_surface.get_size()[1]/2-100))
        screen.blit(settings_text, (blue_surface.get_size()[0]/3, blue_surface.get_size()[1]/2+100))
    if settings_screen:
        screen.blit(blue_surface, (0, 0))
        screen.blit(music_title, (blue_surface.get_size()[0]/3, blue_surface.get_size()[1]/2 - 200))
        screen.blit(yes_music, (235, 400))
        screen.blit(no_music, (235, 500))
        screen.blit(escape_settings, (235, 700))
        screen.blit(yes_music_surface, (180, 383))
        screen.blit(no_music_surface, (180, 483))
    pygame.display.flip()

pygame.display.quit()
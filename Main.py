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
back = pygame.image.load("Game initial sketch.png").convert()  # the background pic needs to be 1015x595 px.
ball = pygame.image.load("Tank.gif").convert()  # must be 35x35, or (some multiple of 35)x(some multiple of 35)
missile = pygame.image.load("missile.png").convert()
mine = pygame.image.load("Army mine.png")
norm_enemy_ship = pygame.image.load("enemy ship.gif").convert()
bullet = pygame.image.load("projectile.gif").convert()
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


# setting up variables that will be displayed on top
money = 10000000
chances = 3
pause = False
ships_destroyed = 0
ships_remaining = 0
tank_pressed = True
missile_pressed = False
seamine_pressed = False
speed_enemy = 0.5

tank_price = 1000
mine_price = 50000
missile_price = 10000

# variables relating to tank
sprite_type = ""
angle = 0

# whether or not the enemy ship has been rotated
rotate = False

tester=0

# Game engine
clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(30)
    for ev in pygame.event.get():
        if ev.type == QUIT:  # if the game is quitted
            keep_going = False
        elif ev.type == MOUSEBUTTONDOWN:  # if the mouse is pressed
            x = ((ev.pos[0])//35)*35  # getting the x of where the mouse clicked
            y = ((ev.pos[1])//35)*35  # getting the y of where the mouse clicked
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
                        img.append([item, x, y, sprite_type, 0, [], 0])
                    elif missile_pressed and pathway_pressed and money - missile_price >= 0:
                        item = missile
                        sprite_type = "M"
                        money -= missile_price
                        img.append([item, x, y, sprite_type, 0, [], 0])
                    elif seamine_pressed and money - mine_price >= 0 and not pathway_pressed:
                        item = mine
                        sprite_type = "S"
                        money -= mine_price
                        img.append([item, x, y, sprite_type, 0, [], 0])
                    else:
                        break
    # paint selection surfaces to their colours
    if pause:
        pause_surface.fill(red)
        paused = font.render("Resume", True, black)
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
    money_text = font.render("Money: $"+str(money), True, black)
    numweapons_text = font.render("Weapons: "+str(len(img)), True, black)
    islandsdestroyed_text = font.render("Islands Destroyed: "+str(3-chances), True, black)
    chance_text = font.render("Chances: "+str(chances), True, black)
    shipsdestroyed_text = font.render("Ships Destroyed: "+str(ships_destroyed), True, black)
    shipsremaining_text = font.render("Ships Remaining: "+str(ships_remaining), True, black)

    # code for enemy ships' route
    if not pause:
        if y_enemy < 100 or (x_enemy >= (screen.get_size()[0]-200) and y_enemy < 350):
            y_enemy += speed_enemy
            if x_enemy == (screen.get_size()[0]-200):
                norm_enemy_ship = None
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
    screen.blit(norm_enemy_ship, (x_enemy, y_enemy))  # blitting the enemy
    for ship_pointer in range(0, len(img)):  # looping through player stuff
        angle = 0
        if img[ship_pointer][3] == "T":  # if the item is a tank
            if not rotate:  # If the enemy ship has not been rotated
                lower = y_enemy-img[ship_pointer][2]-20+(norm_enemy_ship.get_size()[0]/0.75)  # this code will be the divisor, may be equal to zero at times
                if lower == 0:  # if the divisor is zero, set it to a very large number
                    lower = 10**23
                angle = math.atan((x_enemy-img[ship_pointer][1]+(norm_enemy_ship.get_size()[1]/100))/lower)*180/3.14  # finding the angle the tank needs to be pointed to
            else:
                lower = y_enemy-img[ship_pointer][2]-20+(norm_enemy_ship.get_size()[1]/2)  # this code will be the divisor, may be equal to zero at times
                if lower == 0:  # if the divisor is zero, set it to a very large number
                    lower = 10**23
                angle = math.atan((x_enemy-img[ship_pointer][1]+(norm_enemy_ship.get_size()[0]/2))/lower)*180/3.14  # finding the angle the tank needs to be pointed to
            if img[ship_pointer][2] >= y_enemy:  # if the tank is higher than the ship, invert it
                angle += 180
            img[ship_pointer][6] += 1  # add one to the ship's timer
            if img[ship_pointer][6] == 5:  # if the ship's timer is five, reset it, and if the game is not paused, spawn a bullet
                img[ship_pointer][6] = 0
                range_bullets = 250
                if (not pause) and -range_bullets < ((x_enemy-img[ship_pointer][1])**2+(y_enemy-img[ship_pointer][2])**2) ** 0.5 < range_bullets:  # Using Pythagorean Theorem to determine if tank within range
                    img[ship_pointer][5].append([bullet, img[ship_pointer][1]+(ball.get_size()[0]/2), img[ship_pointer][2]+(ball.get_size()[1]/2), math.sin(angle*3.14/180), math.cos(angle*3.14/180)])
            angle += 180
            for bullet_pointer in range(0, len(img[ship_pointer][5])):  # looping through bullets
                if type(img[ship_pointer][5][bullet_pointer]) == list:  # if the bullet actually exists and has not been deleted
                    if not pause:
                        img[ship_pointer][5][bullet_pointer][1] += 6*img[ship_pointer][5][bullet_pointer][3]  # moving the bullet's x
                        img[ship_pointer][5][bullet_pointer][2] += 6*img[ship_pointer][5][bullet_pointer][4]  # moving the bullet's y
                        
                    y_adj = norm_enemy_ship.get_size()[1]
                    x_adj = norm_enemy_ship.get_size()[0]
                    
                    collision = (0 <= (x_enemy-img[ship_pointer][5][bullet_pointer][1]) <= x_adj) or (0 <=(y_enemy-img[ship_pointer][5][bullet_pointer][2]) <= y_adj)
                    within_screen = 0 < img[ship_pointer][5][bullet_pointer][1] < 1015 and 0 < img[ship_pointer][5][bullet_pointer][2] < 768
                    if collision: #or not within_screen:
                        img[ship_pointer][5][bullet_pointer] = None
                        print("collision")

        img[ship_pointer][4] = angle  # add the variable "angle" to the image, before blitting the ship
        screen.blit(pygame.transform.rotate(img[ship_pointer][0], img[ship_pointer][4]), (img[ship_pointer][1], img[ship_pointer][2]))
        for bullet_pointer in range(0, len(img[ship_pointer][5])):
            if type(img[ship_pointer][5][bullet_pointer]) == list:
                if img[ship_pointer][5][bullet_pointer] != None:  # only blit it if it is on the screen, otherwise delete it
                    screen.blit(img[ship_pointer][5][bullet_pointer][0], (img[ship_pointer][5][bullet_pointer][1], img[ship_pointer][5][bullet_pointer][2]))

    # blitting the top part of the screen
    top_bounds = 10
    screen.blit(white_surface, (0, 0))
    screen.blit(border, (9, top_bounds-1))
    screen.blit(tank_surface, (10, top_bounds))
    screen.blit(border, (139, top_bounds-1))
    screen.blit(missile_surface, (140, top_bounds))
    screen.blit(border, (269, top_bounds-1))
    screen.blit(seamine_surface, (270, top_bounds))
    screen.blit(main_border, (534, top_bounds-1))
    screen.blit(display, (535, top_bounds))
    screen.blit(border, (399, top_bounds - 1))
    screen.blit(pause_surface, (400, top_bounds))

    scale = 150
    top_bounds = 100
    screen.blit(paused, (408, 50))
    screen.blit(islandsdestroyed_text, (400+scale, top_bounds+15))
    screen.blit(chance_text, (650+scale, top_bounds+15))
    screen.blit(shipsdestroyed_text, (400+scale, top_bounds-25))
    screen.blit(shipsremaining_text, (650+scale, top_bounds-25))
    screen.blit(money_text, (400+scale, top_bounds-65))
    screen.blit(numweapons_text, (650+scale, top_bounds-65))
    scale = 50
    screen.blit(tank_text, (scale, top_bounds))
    screen.blit(missile_text, (110+scale, top_bounds))
    screen.blit(mine_text, (250+scale, top_bounds))
    screen.blit(tank_cost, (scale, top_bounds+15))
    screen.blit(missile_cost, (scale+110, top_bounds+15))
    screen.blit(mine_cost, (250+scale, top_bounds+15))

    screen.blit(ball, (scale+3, 50))
    screen.blit(missile, (scale+98, 50))
    screen.blit(mine, (scale + 260, 50))
    pygame.display.flip()

pygame.display.quit()

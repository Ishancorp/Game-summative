#Ishan Sharma and Aryan Kukreja
#For Mr. Cope
#April 23, 2016

#Main.py
#An RTS game

#Input: Mouse clicks
#Output: Gameplay

import pygame
from pygame.locals import *
import math

pygame.init()
screen = pygame.display.set_mode((1015, 768))


#Loading images and initializing list to store them in
back = pygame.image.load("Game initial sketch.png").convert() #the background pic needs to be 1015x595 px. 
ball = pygame.image.load("tank.gif").convert() #must be 35x35, or (some multiple of 35)x(some multiple of 35)
missile=pygame.image.load("missile.png").convert()
norm_enemy_ship=pygame.image.load("EnemyShip1.png").convert()
img = []

#Setting up some colours
dark_gray=(75,75,75)
pressed=(75,125,230)
gray=(200,200,200)
light_gray=(242, 242, 242)
black=(0,0,0)

#setting up Surfaces for the menu, along with the menu backdrop

bottom_bounds=155
background = pygame.Surface(screen.get_size()).convert()
background.fill(light_gray)
border=pygame.Surface((122,bottom_bounds+2)).convert()
border.fill(dark_gray)
main_border=pygame.Surface((477,bottom_bounds+2)).convert()
main_border.fill(dark_gray)
display = pygame.Surface((475,bottom_bounds)).convert()
display.fill(gray)
white_surface = pygame.Surface((1015,173)).convert()
white_surface.fill((255,255,255))

#fonts
font = pygame.font.SysFont("helvetica", 14)
tank_text = font.render("Tank", True, black)
tank_cost = font.render("$1 000", True, black)
missile_text = font.render("Missile Launcher", True, black)
missile_cost = font.render("$10 000", True, black)
mine_text = font.render("Sea Mine", True, black)
mine_cost = font.render("$50 000", True, black)

tank_pressed=True
missile_pressed=False
seamine_pressed=False
#setting up coordinate variables
x=0
y=0
money=0
chances=3
pause=False
ships_destroyed=0
ships_remaining=0
sprite_type=""
y_enemy=-75
x_enemy=100
angle=0

#Game engine
clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(30)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            keep_going=False
        elif ev.type==MOUSEBUTTONDOWN: #if the mouse is pressed
            x=((ev.pos[0])//35)*35 #getting the x of where the mouse clicked
            y=((ev.pos[1])//35)*35 #getting the y of where the mouse clicked
            if 131>x>9 and 136>y>9: #if the tank part of the menu is pressed
                print("Tank")
                tank_pressed=True
                missile_pressed=False
                seamine_pressed=False
            elif 261>x>139 and 136>y>9: #if the missile part of the menu is pressed
                print("Missile")
                tank_pressed=False
                missile_pressed=True
                seamine_pressed=False
            elif 391>x>269 and 136>y>9: #if the sea mine part of the menu is pressed
                print("Sea Mine")
                tank_pressed=False
                missile_pressed=False
                seamine_pressed=True
            elif y<175: #if any other part of the menu is pressed
                if pause==True: #if the game is already paused
                    pause=False
                    print("Unpaused")
                elif pause==False: #if the game is not paused
                    pause=True
                    print("Paused")
            else: #if the main gameplay part is pressed
                overlap=False
                for image in img:
                    if ((image[1]==x and image[2]==y)) or ((sprite_type=="M" and (image[1]==x or image[1]==x-35 or image[1]==x-70) and image[2]==y)) or (missile_pressed and (image[1]==x or image[1]==x+35 or image[1]==x+70) and image[2]==y): #if the 
                        overlap=True
                        print("Overlap")
                #overlap is true if the x and y of the sprite is already covered
                if overlap==False:
                    item=0
                    if tank_pressed:
                        item=ball
                        sprite_type="T"
                    elif missile_pressed:
                        item=missile
                        sprite_type="M"
                    img.append([item,x,y,sprite_type])
    #print(x,y)
    
    tank_surface = pygame.Surface((120,bottom_bounds)).convert()
    missile_surface = pygame.Surface((120,bottom_bounds)).convert()
    seamine_surface = pygame.Surface((120,bottom_bounds)).convert()
    if tank_pressed==False:
        tank_surface.fill(gray)
    else:
        tank_surface.fill(pressed)
    if missile_pressed==False:
        missile_surface.fill(gray)
    else:
        missile_surface.fill(pressed)
    if seamine_pressed==False:
        seamine_surface.fill(gray)
    else:
        seamine_surface.fill(pressed)
    
    money_text = font.render("Money: $"+str(money), True, black)
    numweapons_text = font.render("Weapons: "+str(len(img)), True, black)
    islandsdestroyed_text = font.render("Islands Destroyed: "+str(3-chances), True, black)
    chance_text = font.render("Chances: "+str(chances), True, black)
    shipsdestroyed_text = font.render("Ships Destroyed: "+str(ships_destroyed), True, black)
    shipsremaining_text = font.render("Ships Remaining: "+str(ships_remaining), True, black)
    speed_enemy=1
    
    if pause==False:
        if y_enemy<100 or x_enemy>=(screen.get_size()[0]-200):
            y_enemy+=speed_enemy
            if x_enemy==(screen.get_size()[0]-200):
                norm_enemy_ship=pygame.transform.rotate(norm_enemy_ship,-90)
                x_enemy+=10
                y_enemy+=10
        elif y_enemy==100:
            norm_enemy_ship=pygame.transform.rotate(norm_enemy_ship,90)
            x_enemy+=speed_enemy
            y_enemy+=175
        else:
            x_enemy+=speed_enemy
    #Blitting
    screen.blit(background, (0,0))
    screen.blit(back, (0,173))
    for image in img:
        if y_enemy-image[2]==0:
            angle=math.atan((x_enemy-image[1])/(y_enemy-image[2]))
        else:
            angle=0
        screen.blit(pygame.transform.rotate(image[0],angle),(image[1],image[2]))
    screen.blit(norm_enemy_ship,(x_enemy,y_enemy))
    #print(img)
    top_bounds=10
    screen.blit(white_surface,(0,0))
    screen.blit(border, (9,top_bounds-1))
    screen.blit(tank_surface, (10,top_bounds))
    screen.blit(border, (139,top_bounds-1))
    screen.blit(missile_surface, (140,top_bounds))
    screen.blit(border, (269,top_bounds-1))
    screen.blit(seamine_surface, (270,top_bounds))
    screen.blit(main_border, (519,top_bounds-1))
    screen.blit(display, (520,top_bounds))

    scale=150
    scale2=50
    top_bounds=100
    screen.blit(tank_text, (scale2, top_bounds))
    screen.blit(missile_text, (110+scale2, top_bounds))
    screen.blit(mine_text, (250+scale2, top_bounds))
    screen.blit(tank_cost, (scale2, top_bounds+15))
    screen.blit(missile_cost, (scale2+110, top_bounds+15))
    screen.blit(mine_cost, (250+scale2, top_bounds+15))
    screen.blit(islandsdestroyed_text, (400+scale, top_bounds+15))
    screen.blit(chance_text, (650+scale, top_bounds+15))
    screen.blit(shipsdestroyed_text, (400+scale, top_bounds-25))
    screen.blit(shipsremaining_text, (650+scale, top_bounds-25))
    screen.blit(money_text, (400+scale, top_bounds-65))
    screen.blit(numweapons_text, (650+scale, top_bounds-65))

    screen.blit(ball, (scale2+3,50))
    screen.blit(missile, (scale2+98,50))
    pygame.display.flip()

pygame.display.quit()

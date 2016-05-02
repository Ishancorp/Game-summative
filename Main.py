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
missile=pygame.image.load("missile.gif").convert()
norm_enemy_ship=pygame.image.load("enemy ship.gif").convert()
bullet=pygame.image.load("projectile.png").convert()
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
bullet_speed_default=-5
bullet_speed=[bullet_speed_default]
bullet_pos_list=[]

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
            elif pause==False and ((y<243 and x>140) or (383<y<453 and x<840) or (595>=y>525 and x>140) or (y>595 and x>840)): #if the main gameplay part is pressed
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
                        bullet_speed.append(bullet_speed_default)
                        bullet_pos_list.append([])
                    elif missile_pressed:
                        item=missile
                        sprite_type="M"
                    img.append([item,x,y,sprite_type,0,[]])
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
        if y_enemy<100 or (x_enemy>=(screen.get_size()[0]-200) and y_enemy<350):
            y_enemy+=speed_enemy
            #print("h")
            if x_enemy==(screen.get_size()[0]-200):
                norm_enemy_ship=pygame.transform.rotate(norm_enemy_ship,-90)
                x_enemy+=10
                y_enemy+=10
        elif y_enemy==100 or (y_enemy==350 and x_enemy==(screen.get_size()[0]-190)):
            norm_enemy_ship=pygame.transform.rotate(norm_enemy_ship,90)
            x_enemy+=speed_enemy
            y_enemy+=150
            #print("o")
        elif y_enemy==350:
            norm_enemy_ship=pygame.transform.rotate(norm_enemy_ship,270)
            x_enemy-=speed_enemy
            #print("a")
        elif y_enemy>350 and x_enemy>125:
            x_enemy-=speed_enemy
            #print(x_enemy)
            #print("r")
        elif x_enemy==125 and y_enemy>350:
            norm_enemy_ship=pygame.transform.rotate(norm_enemy_ship,90)
            x_enemy-=0.01
            #print("e")
        elif x_enemy<125 and y_enemy>350:
            y_enemy+=speed_enemy
            #print("s")
        else:
            x_enemy+=speed_enemy
            #print("i")
    #print(y_enemy)
    #Blitting
    screen.blit(background, (0,0))
    screen.blit(back, (0,173))
    for ship_pointer in range(0,len(img)):
        if img[ship_pointer][3]=="T":
            try:
                math.atan((x_enemy-img[ship_pointer][1])/(y_enemy-img[ship_pointer][2]-20))
            except:
                angle=0
                img[ship_pointer][0]=pygame.transform.rotate(img[ship_pointer][0],180)
            else:
                angle=math.atan((x_enemy-img[ship_pointer][1])/(y_enemy-img[ship_pointer][2]-20))*180/3.14
        else:
            angle=0
        if img[ship_pointer][2]<=y_enemy:
            angle+=180
        bullet_pos_list[ship_pointer].append([math.sin(angle*3.14/180),math.cos(angle*3.14/180)])
        bullet_x=img[ship_pointer][1]+bullet_speed[ship_pointer]*bullet_pos_list[ship_pointer][0][0]
        bullet_y=img[ship_pointer][2]+bullet_speed[ship_pointer]*bullet_pos_list[ship_pointer][0][1]
        bullet_speed[ship_pointer]-=1
        screen.blit(bullet,(bullet_x,bullet_y))
        img[ship_pointer][4]=angle
        screen.blit(pygame.transform.rotate(img[ship_pointer][0],angle),(img[ship_pointer][1],img[ship_pointer][2]))
        img[ship_pointer][5].append([bullet,bullet_x,bullet_y])
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

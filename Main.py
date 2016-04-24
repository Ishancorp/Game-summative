#Ishan Sharma and Aryan Kukreja
#For Mr. Cope
#April 23, 2016

#Main.py
#An RTS game

#Input: Mouse clicks
#Output: Gameplay

import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1015, 770))


#Loading images and initializing list to store them in
back = pygame.image.load("Game initial sketch.png").convert() #the background pic needs to be 1015x595 px. 
ball = pygame.image.load("small_ball.png").convert()
img = []

#Setting up some colours
dark_gray=(75,75,75)
gray=(200,200,200)
light_gray=(242, 242, 242)
black=(0,0,0)

#setting up Surfaces for the menu, along with the menu backdrop

bottom_bounds=155
background = pygame.Surface(screen.get_size()).convert()
background.fill(light_gray)
border=pygame.Surface((102,bottom_bounds+2)).convert()
border.fill(dark_gray)
ship = pygame.Surface((100,bottom_bounds)).convert()
ship.fill(gray)
main_border=pygame.Surface((527,bottom_bounds+2)).convert()
main_border.fill(dark_gray)
display = pygame.Surface((525,bottom_bounds)).convert()
display.fill(gray)

#fonts
font = pygame.font.SysFont("helvetica", 14)
tank_text = font.render("Tank", True, black)
tank_cost = font.render("$1 000", True, black)
missile_text = font.render("Missile", True, black)
missile_cost = font.render("$10 000", True, black)
mine_text = font.render("Sea Mine", True, black)
mine_cost = font.render("$50 000", True, black)

#setting up coordinate variables
x=0
y=0

#Game engine
clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(30)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            keep_going=False
        elif ev.type==MOUSEBUTTONDOWN:
            x=((ev.pos[0])//35)*35 #getting the x of where the mouse clicked
            y=((ev.pos[1])//35)*35 #getting the y of where the mouse clicked
            if 111>x>9 and 136>y>9: #if the tank part of the menu is pressed
                print("Tank")
            elif 230>x>119 and 136>y>9: #if the missile part of the menu is pressed
                print("Missile")
            elif 340>x>229 and 136>y>9: #if the sea mine part of the menu is pressed
                print("Sea Mine")
            elif y<175: #if any other part of the menu is pressed
                print("Pause")
            else: #if the main gameplay part is pressed
                overlap=False
                for image in img:
                    if image[1]==x and image[2]==y:
                        overlap=True
                        print("Overlap")
                #overlap is true if the x and y of the sprite is already covered
                if overlap==False:
                    img.append([ball,x,y])
    #print(x,y)
    
    #Blitting
    screen.blit(background, (0,0))
    screen.blit(back, (0,175))
    for image in img:
        screen.blit(image[0], (image[1],image[2]))
    #print(img)
    top_bounds=10
    screen.blit(border, (9,top_bounds-1))
    screen.blit(ship, (10,top_bounds))
    screen.blit(border, (119,top_bounds-1))
    screen.blit(ship, (120,top_bounds))
    screen.blit(border, (229,top_bounds-1))
    screen.blit(ship, (230,top_bounds))
    screen.blit(main_border, (479,top_bounds-1))
    screen.blit(display, (480,top_bounds))
    
    screen.blit(tank_text, (27, 100))
    screen.blit(missile_text, (137, 100))
    screen.blit(mine_text, (247, 100))
    
    screen.blit(tank_cost, (27, 115))
    screen.blit(missile_cost, (137, 115))
    screen.blit(mine_cost, (247, 115))
    pygame.display.flip()

pygame.display.quit()

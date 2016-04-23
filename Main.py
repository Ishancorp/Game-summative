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

screen = pygame.display.set_mode((1024, 768))

background = pygame.Surface(screen.get_size()).convert()
background.fill((242, 242, 242))

back = pygame.image.load("Game initial sketch.png").convert()
ball = pygame.image.load("small_ball.png").convert()
img = []

font = pygame.font.SysFont("helvetica", 48) #system fonts, needs font name
field_value = "World War Sea"
field = font.render(field_value, True, (0,0,255))

x=1024
y=768

clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(30)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            quit()
        elif pygame.mouse.get_pressed()[0]:
            x=ev.pos[0]-(ball.get_width()/2)
            y=ev.pos[1]-(ball.get_height()/2)
            img.append([ball,x,y])
    #print(x,y)
    screen.blit(background, (0,0))
    screen.blit(back, (0,154))
    for image in img:
        screen.blit(image[0], (image[1],image[2]))
    #print(img)
    screen.blit(field, (60, 40))
    pygame.display.flip()

pygame.display.quit()
    

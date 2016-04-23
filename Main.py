""" 
A ball bouncing around the screen, off the walls, with dynamic speed.
Requires the file "Ball.bmp" to be in the program directory.
"""
import pygame
from pygame.locals import * 
pygame.init()

screen = pygame.display.set_mode((1024, 768))

background = pygame.Surface(screen.get_size()).convert()
background.fill((242, 242, 242))

back = pygame.image.load("Game initial sketch.png").convert()
img = pygame.image.load("small_ball.png").convert()

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
            keep_going = False
        elif pygame.mouse.get_pressed()[0]:
            x=ev.pos[0]
            y=ev.pos[1]
            x-=img.get_width()/2
            y-=img.get_height()/2
    print(x,y)
    screen.blit(background, (0,0))
    screen.blit(back, (0,154))
    screen.blit(img, (x,y))
    screen.blit(field, (60, 40))
    pygame.display.flip()

pygame.display.quit()
    

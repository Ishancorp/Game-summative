_author_ = "Aryan Kukreja"

import random
import pygame
from pygame.locals import * 
pygame.init()


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Army Ship Level 1.gif").convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.left = random.randrange(0, 100)
        self.rect.top = random.randrange(0, 1)
        self.dir_x = 0
        self.dir_y = -1
        self.speed = 5

    def update(self):
        if self.rect.top < 100:
            self.dir_y = 1
            self.dir_x = 0
        elif (100 <= self.rect.top < 200) and self.rect.left < 100:
            x = self.rect.left
            y = self.rect.top
            if self.rect.left < 100 and self.rect.top == 100:
                self.image = pygame.transform.rotate (self.image, 90)
                self.rect = self.image.get_rect()
                self.rect.top = y
                self.rect.left = x
            self.dir_y = 0
            self.dir_x = 1
        elif 990 < self.rect.left and 100 < self.rect.top < 200:
            if self.rect.left > 990 and self.rect.top == 100:
                self.image = pygame.transform.rotate (self.image, 90)
                self.rect = self.image.get_rect ()
            self.dir_y = 1
            self.dir_x = 0
        elif (385 < self.rect.top < 500) and 990 < self.rect.left:
            if self.rect.left > 990 and self.rect.top == 385:
                self.image = pygame.transform.rotate (self.image, 90)
                self.rect = self.image.get_rect ()
            self.dir_y = 0
            self.dir_x = -1
        elif 100 > self.rect.left and 300 < self.rect.top < 500:
            if self.rect.left < 100 and self.rect.top == 300:
                self.image = pygame.transform.rotate (self.image, 90)
                self.rect = self.image.get_rect ()
            self.dir_y = 1
            self.dir_x = 0
        elif self.rect.top > 550 and 990 > self.rect.left:
            if self.rect.left < 100 and self.rect.top == 550:
                self.image = pygame.transform.rotate (self.image, 90)
                self.rect = self.image.get_rect ()
            self.dir_y = 0
            self.dir_x = 1
        elif self.rect.top > 550 and 800 < self.rect.left:
            self.dir_y = 0
            self.dir_x = 0
        self.rect.move_ip(self.speed*self.dir_x, self.speed*self.dir_y)

screen = pygame.display.set_mode((1015, 768))
ship_group = pygame.sprite.Group()
for counter in range(0, 2):
    warship = Ship()
    ship_group.add(warship)

background = pygame.Surface(screen.get_size()).convert()
background.fill((255, 255, 255))
screen.blit(background, (0,0))

clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(30)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            keep_going = False

    for warship in ship_group.sprites():
        pass

    ship_group.clear(screen, background)
    ship_group.update()
    ship_group.draw(screen)
    pygame.display.flip()

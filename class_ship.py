# Ishan Sharma and Aryan Kukreja
# For Mr. Cope
# May 23, 2016

# Main.py
# An RTS game

# Input: Mouse clicks
# Output: Gameplay

import pygame
from pygame.locals import *
import math
from random import randint
import webbrowser

pygame.init()
screen = pygame.display.set_mode((1015, 768))

# Loading images and initializing list to store them in
back = pygame.image.load("Game Initial Sketch.png").convert_alpha()  # Loading background pic
tank_image = pygame.image.load("Tank.gif").convert_alpha()  # Loading image for the tank, has its angle readjusted constantly
missile_image = pygame.image.load("missile.png").convert_alpha()  # Loading image for the missile
mine_image = pygame.image.load("Sea mine.png").convert_alpha()  # Loading image for the mine

bullet_image = pygame.image.load("projectile.png").convert_alpha()  # Loading image for the bullet
rocket_image = pygame.image.load("Army Rocket.gif").convert_alpha()  # Loading image for the rocket, has its angle set when spawned

# Loading images for the army ships
ship1_image = pygame.image.load("Army Ship Level 1.gif").convert_alpha()
ship2_image = pygame.image.load("Army Ship Level 2.gif").convert_alpha()
ship3_image = pygame.image.load("Army Ship Level 3.gif").convert_alpha()

# Loading image for the splash screen, highscore screen, and setting screen
splash = pygame.image.load("Splash_Screen.jpg").convert_alpha()
highscore_image = pygame.image.load("highscores_background.png").convert_alpha()
settings = pygame.image.load("Settings_Screen.png").convert_alpha()
select = pygame.image.load("select.png")  # For music button
item_grey = pygame.image.load("grey_surface.png").convert_alpha()  # for buttons for selecting items, if selected
pause_red = pygame.image.load("pause_red.png").convert_alpha()  # pause button
pause_green = pygame.image.load("pause_green.png").convert_alpha()  # play button
back_button_surface = pygame.image.load("back_button_surface.png").convert_alpha()  # back button
item_red = pygame.image.load("red_surface.png").convert_alpha()  # if not enough money to purchase item
item_green = pygame.image.load("surface.png").convert_alpha()  # if enough money to purchase item
white_surface = pygame.image.load("back_surface.png").convert_alpha()  # surface just above gameplay area
swirl = pygame.image.load("swirl_image.png").convert_alpha()  # surface to display swirl designs
social = pygame.image.load("socialmediabar.png").convert_alpha()  # surface to display social bar options

# Surfaces to display money, number of ships destroyed, number of weapons placed, and number of chances remaining
money_surface = pygame.image.load("money_surface.png").convert_alpha()
ships_destroyed_surface = pygame.image.load("ships_destroyed_surface.png").convert_alpha()
weapons_surface = pygame.image.load("weapons_surface.png").convert_alpha()
chances_surface = pygame.image.load("chances_surface.png").convert_alpha()

# Load music and sound effects here:
gunshot = pygame.mixer.Sound("gunshot.wav")
gunshot.set_volume(0.5)
bomb = pygame.mixer.Sound("bomb.wav")
explosion = pygame.mixer.Sound("explosion.wav")
pygame.mixer.music.load("start_music.wav")

# Colours for text
white = (255, 255, 255)
black = (0, 0, 0)

# setting up prices for various items
tank_price = 1000
mine_price = 50000
missile_price = 10000

# font and text on the top of the game
font = pygame.font.SysFont("arial", 14)
tank_text = font.render("Tank".center(18), True, black)
tank_cost = font.render(("$"+str(tank_price)).center(18), True, black)
missile_text = font.render("Missile Launcher".center(18), True, black)
missile_cost = font.render(("$"+str(missile_price)).center(18), True, black)
mine_text = font.render("Sea Mine".center(18), True, black)
mine_cost = font.render(("$"+str(mine_price)).center(18), True, black)
paused = font.render("", True, black)
go_back_home = font.render("Quit".center(18), True, black)

# setting up variables that will be displayed on top
money = 55000
chances = 3
pause = True
ships_destroyed = 0
ships_remaining = 0
tank_pressed = True
missile_pressed = False
seamine_pressed = False
wave_interval = 800  # counter value for ship
high_scores = []
music = True  # whether or not background music is playing
ship_spawns = 0  # counter whether or not ships should be spawned

splash_screen = True
settings_screen = False
game_over = False
level = 1
score_achieved_index = 0


class Rocket(pygame.sprite.Sprite):  # sprite for the rocket
    def __init__(self, x_pos, y_pos, angle_missile):  # fed parameters telling it position, and angle to point
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle_missile
        self.image = pygame.transform.rotate(rocket_image, self.angle)  # setting image, and rotating it to angle
        self.rect = self.image.get_rect()  # creating a rect for collision detection
        self.x = x_pos
        self.y = y_pos
        self.dir_x = -16*math.sin(self.angle)  # setting up amount for rocket to move horizontally per frame
        self.dir_y = -16*math.cos(self.angle)  # setting up amount for rocket to move vertically per frame
        self.rect.move_ip(self.x, self.y)  # moving sprite to appropriate position
        self.active = True
        self.money = 10  # how much money the user should get for the rocket hitting the enemy

    def update(self):
        self.image = pygame.transform.rotate(rocket_image, math.degrees(self.angle))  # setting image, and rotating it to angle
        self.rect.move_ip(self.dir_x, self.dir_y)  # moving rectangle towards ship
        self.x = self.rect.left  # setting x- and y-coordinates to x- and y- coordinates of rect
        self.y = self.rect.top
        for enemy in ship_group:
            if self.rect.colliderect(enemy.rect):  # if any enemy has collided with the rocket
                self.active = False  # set it inactive
                enemy.health -= 3  # reduce the health of the enemy
                bomb.play()  # play an explosion sound
        if 0 > self.x or self.x > screen.get_size()[0] or 0 > self.y or self.y > screen.get_size()[1]: #if the rocket is outside the screen
            self.active = False  # set it inactive
            self.money = 0  # no money increase


class Mine(pygame.sprite.Sprite):  # Sprite for the sea mine
    def __init__(self, x_pos, y_pos):  # parameters telling mine its position
        pygame.sprite.Sprite.__init__(self)
        self.image = mine_image  # use mine image
        self.rect = self.image.get_rect()  # make rect for collision detecting with enemy ships
        self.x = x_pos
        self.y = y_pos
        self.rect.move_ip(self.x, self.y)  # move the rect to the same position as the mine displayed
        self.active = True
        self.type = "S"
        self.size = self.image.get_size()  # this variable is used to that the size of the mine can be known for

    def update(self):
        self.x = self.rect.left  # set x- and y--coordinates to x- and y-coordinates of rect
        self.y = self.rect.top
        for enemy in ship_group:
            if self.rect.colliderect(enemy.rect):  # if the mine collides with an enemy, delete the mine, and set the enemy ship's health to 0
                self.active = False
                enemy.health = 0
                explosion.play()  # play explosion sound


class Bullet(pygame.sprite.Sprite):  # sprite for the bullet
    def __init__(self, x_pos, y_pos, angle_tank):  # parameters for x, y and the angle of the tank
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image  # use bullet image
        self.rect = self.image.get_rect()  # make rect for collision detection with enemy ships
        self.x = x_pos
        self.y = y_pos
        self.angle = angle_tank
        self.dir_x = -8*math.sin(self.angle)  # intervals to move it per frame
        self.dir_y = -8*math.cos(self.angle)
        self.rect.move_ip(self.x, self.y)
        self.active = True
        self.money = 1

    def update(self):
        self.rect.move_ip(self.dir_x, self.dir_y)  # move it every frame at the pre-calculated x and y dirs
        self.x = self.rect.left
        self.y = self.rect.top
        for enemy in ship_group:
            if self.rect.colliderect(enemy.rect):  # if the enemy ship's collided with the bullet, set the bullet to false, reduce enemy health, and make a gunshot sound
                self.active = False
                enemy.health -= 1/5
                gunshot.play()
        if 0 > self.x or self.x > screen.get_size()[0] or 0 > self.y or self.y > screen.get_size()[1]:  # if it's outside visible window, delete bullet
            self.active = False
            self.money = 0


class Tank(pygame.sprite.Sprite):  # sprite for tank
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = tank_image  # set image, set rect
        self.rect = self.image.get_rect()
        self.angle = 0  # angle to be calculated later
        self.x = x_pos
        self.y = y_pos
        self.timer = 0
        self.active = True
        self.type = "T"
        self.size = self.image.get_size()

    def update(self):
        for enemy in ship_group:
            if 250 > self.x-enemy.x > -250 and 250 > self.y-enemy.y > -250:  # if it's within the range of 250
                lower = abs(self.y-enemy.y+(enemy.image.get_size()[1]/2))  # get the denominator to calc angle
                if lower == 0:  # if the denominator is zero, and thus calc is impossible, set lower to a very large number
                    lower = 10**100
                self.angle = math.atan((self.x-abs(enemy.x+(enemy.image.get_size()[0]/2)))/lower)  # calc angle with tan
                if self.y < enemy.y:  # if the tank is higher up than the enemy ship
                    self.angle = 135 - self.angle  # invert angle, plus a few other adjustions
                self.timer += 1
                if self.timer == 5:  # every fifth frame, initiate bullet
                    bullet_x = self.x + (tank_image.get_size()[0]/2)
                    bullet_y = self.y + (tank_image.get_size()[1]/2)
                    bullet_group.add(Bullet(bullet_x, bullet_y, self.angle))
                    self.timer = 0
                self.image = pygame.transform.rotate(tank_image, math.degrees(self.angle))  # rotate in accord to angle
                break  # if within range, break out of loop


class MissileLauncher(pygame.sprite.Sprite):  # sprite for missile launcher
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_image  # set image and rect
        self.rect = self.image.get_rect()
        self.angle = 0  # angle to be calc later
        self.x = x_pos
        self.y = y_pos
        self.timer = 0
        self.active = True
        self.type = "M"
        self.size = self.image.get_size()

    def update(self):
        for enemy in ship_group:
            if 500 > self.x-enemy.x > -500 and 500 > self.y-enemy.y > -500:  # if within range
                lower = abs(self.y - enemy.y + (enemy.image.get_size()[1]/2))  # calc denominator for angle
                if lower == 0:  # if the denominator is and angle calc is impossible, set to huge num
                    lower = 10**100
                self.angle = math.atan((self.x-abs(enemy.x + (enemy.image.get_size()[0]/2)))/lower)  # calc angle
                if self.y < enemy.y:  # if missile higher than enemy, adjust angle accordingly
                    self.angle = 135-self.angle
                self.timer += 1
                if self.timer == 30:  # every thirtieth frame, spawn four angles, one for every circle on missile launcher
                    bullet_group.add(Rocket(self.x+(1.25*missile_image.get_size()[0]/7), self.y, self.angle))
                    bullet_group.add(Rocket(self.x+(1.1*missile_image.get_size()[0]/3), self.y, self.angle))
                    bullet_group.add(Rocket(self.x+(1.625*missile_image.get_size()[0]/3), self.y, self.angle))
                    bullet_group.add(Rocket(self.x+0.73*missile_image.get_size()[0], self.y, self.angle))
                    self.timer = 0
                break  # if within range, break out of loop


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ship_choice = randint(1, 6)  # randomly choose ship
        if ship_choice == 1:  # one in six chance of hardest ship to beat
            self.image = ship3_image
            self.health = 2000
            self.late_money = 5000
        elif 2 <= ship_choice <= 3:  # one in three chance of moderate chance to beat
            self.image = ship2_image
            self.health = 1625
            self.late_money = 2500
        else:  # one in two chance of easiest ship to beat
            self.image = ship1_image
            self.health = 1250
            self.late_money = 500

        if level == 2:  # if the level is two, increase difficulty and reward for victory
            self.health += 500
            self.late_money += 750
        self.rect = self.image.get_rect()

        self.dir_x = 0
        self.dir_y = 0
        self.x = 100
        self.y = 173 - self.image.get_size()[1]  # so as to spawn the differently-sized ships just above play area, bottom edge of ship set to y value for play area
        self.rect.move_ip(self.x, self.y)
        self.active = True
        self.money = 0
        self.victor = False  # whether or not enemy ship has reached end

    def update(self):
        self.x = self.rect.left
        self.y = self.rect.top

        # path and rotations for enemy ship
        if self.y < 125:
            self.dir_y = 1
            self.dir_x = 0
        elif self.y == 125:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir_y = randint(140, 230)
        elif 386 > self.y > 246 and self.x < 850 - 45:
            self.dir_y = 0
            self.dir_x = 1
        elif self.x == 850 - 45 and self.y < 385:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir_x = randint(40, 130)
        elif self.x > 850 - 45 and self.y < 392 - 50:
            self.dir_y = 1
            self.dir_x = 0
        elif self.y == 392 - 40:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir_y = randint(110, 170)
            self.dir_x = -120
        elif 392 - 40 < self.y < 600 and self.x > 100:
            self.dir_x = -1
            self.dir_y = 0
        elif self.x == 100 and 600 > self.y > 392 - 40:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir_x = randint(-80, 0)
        elif self.x < 100 and 392 <= self.y < 600:
            self.dir_x = 0
            self.dir_y = 1
        elif self.x < 100 and self.y == 600:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir_y = randint(60, 100)
        elif self.y > 600 and self.x < 700:
            self.dir_x = 1
            self.dir_y = 0
        elif self.y > 600 and self.x == 700:
            self.dir_x = 0
            self.dir_y = 0
            self.active = False
            self.victor = True
        self.rect = self.image.get_rect()  # as the ship may have been rotated, re-create rect and move to existing x-positon
        self.rect.move_ip(self.x, self.y)
        self.rect.move_ip(self.dir_x, self.dir_y)
        if self.health <= 0:  # self-explanatory; if its health is zero, set itself to inactive, and new val for money
            self.active = False
            self.money = self.late_money

# initialize groups to store sprites in; player_group includes mines, tanks, and missile launcher, bullet_group includes bullets and rockets
ship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(30)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            keep_going = False

        elif ev.type == MOUSEBUTTONDOWN:
            x_unadjusted = ev.pos[0]  # getting the x of where the mouse clicked
            y_unadjusted = ev.pos[1]  # getting the u of where the mouse clicked
            x = (x_unadjusted//35)*35  # adjusting x to snap on to grid
            y = (y_unadjusted//35)*35  # adjusting y to snap on to grid
            if game_over:  # if the game is over, if the lower part of the screen is pressed, game is quitted
                if y_unadjusted > 700:
                    keep_going = False
            elif splash_screen:  # if the game is at splash screen
                y_selected = 20 < y < 50  # this boolean re-occurs
                if (380 < x_unadjusted < 640) and (480 < y_unadjusted < 570):  # if play is pressed, activate game
                    splash_screen = False
                    pause = False
                elif (300 < x_unadjusted < 750) and (590 < y_unadjusted < 680):  # if settings is pressed, go to setting sscreen
                    settings_screen = True
                    splash_screen = False
                elif y_selected and x < 840:  # the below are links to various pages, tongue-in-cheek
                    webbrowser.get().open('http://www.twitter.com')
                elif y_selected and 840 + 25 < x < 890:
                    webbrowser.get().open('http://www.facebook.com')
                elif y_selected and 890 < x < 915:
                    webbrowser.get().open('http://www.linkedin.com')
                elif y_selected and 865 + 75 < x < 965:
                    webbrowser.get().open('http://plus.google.com')
                elif y_selected and 965 < x < 990:
                    webbrowser.get().open('http://www.instagram.com')
            elif settings_screen:  # if the game is at settings screen
                music = True
                if (0 < x_unadjusted < 1015) and (320 - 50 < y_unadjusted < 435 + 30):  # if the music toggle is pressed on, turn music to true, vice versa
                    music = True
                elif (0 < x_unadjusted < 1015) and (470 - 30 < y_unadjusted < 535 + 10):
                    music = False
                elif y_unadjusted < 200:  # if go back is pressed, go back to splash screen
                    splash_screen = True
                    pause = True
                    settings_screen = False
            else:
                y_clicked = 142 > y_unadjusted > 9  # reoccuring boolean

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

                elif 142 > y_unadjusted > 91 and 400 < x_unadjusted < 520:  # if back button is pressed, reset game
                    splash_screen = True
                    pause = True
                    player_group.empty()
                    ship_group.empty()
                    bullet_group.empty()
                    ships_destroyed = 0
                    ships_remaining = 0
                    money = 55000

                elif (not pause) and y > 150:  # if the main gameplay part is pressed
                    item = 0
                    pathway_pressed = (y < 243 and x > 140) or (383 < y < 453 and x < 840) or (595 >= y > 525 and x > 140) or (y > 595 and x > 840)  # boolean for whether or not the path is pressed
                    overlap = False

                    for player in player_group.sprites():
                        if (x == player.x and y == player.y) or (missile_pressed and player.x - 70 <= x <= player.x and y == player.y) or (player.type == "M" and player.x <= x <= player.x + 70 and y == player.y): # if an item overlaps with any other item
                            overlap = True

                    if not overlap:  # if not overlapping, place item in accord to selection, if pathway and if enough money
                        if tank_pressed and pathway_pressed and (money - tank_price) >= 0:
                            player_group.add(Tank(x, y))
                            money -= tank_price

                        elif missile_pressed and pathway_pressed and money - missile_price >= 0:
                            player_group.add(MissileLauncher(x, y))
                            money -= missile_price

                        elif seamine_pressed and money - mine_price >= 0 and not pathway_pressed:
                            player_group.add(Mine(x, y))
                            money -= mine_price

    if not pause:
        ship_spawns += 1
        if ship_spawns == wave_interval or len(ship_group) == 0:  # if the frame corresponds to whatever wave_interval is, or if there are not any enemies existing
            if wave_interval >= 20:  # if the wave_inverval is not too low, add ship, reset counter, and re_adjust wave_interval accordingly
                ship_group.add(Ship())
                ship_spawns = 0
                wave_interval *= 0.925
                wave_interval = int(wave_interval)
            elif len(ship_group) == 0:  # all code below is for setting to second level, or else ending the game
                if level == 2:
                    game_over = True
                    chances = 0
                else:
                    back = pygame.image.load("Game Initial Sketch 2.png").convert_alpha()
                    tank_price += 500
                    missile_price += 1000
                    mine_price += 75000
                    level = 2
                    money += 2000
                    wave_interval = 700
                    player_group.empty()
                    ship_group.empty()
                    bullet_group.empty()
                    tank_cost = font.render(("$"+str(tank_price)).center(18), True, black)
                    missile_cost = font.render(("$"+str(missile_price)).center(18), True, black)
                    mine_cost = font.render(("$"+str(mine_price)).center(18), True, black)
                    pause = True

    if music:  # as long as music has been set by player as on, play music
        pygame.mixer.music.play(-1)

    # setting colours of item selections, if selected and if enough money to place
    if not tank_pressed:
        tank_surface = item_grey
    elif (tank_price - money) > 0:
        tank_surface = item_red
    else:
        tank_surface = item_green

    if not missile_pressed:
        missile_surface = item_grey
    elif (missile_price - money) > 0:
        missile_surface = item_red
    else:
        missile_surface = item_green

    if not seamine_pressed:
        seamine_surface = item_grey
    elif (mine_price - money) > 0:
        seamine_surface = item_red
    else:
        seamine_surface = item_green

    # setting colour of pause button, whether or not game is paused
    if pause:
        pause_surface = pause_green
    else:
        pause_surface = pause_red

    if not pause:  # do update functions of all three as long as game isn't paused
        ship_group.update()
        player_group.update()
        bullet_group.update()

    # set text to be displayed with new values for various variables
    money_text = font.render("Money: $"+str(money), True, white)
    numweapons_text = font.render("Ammo Used: " + str(len(player_group)), True, white)
    chance_text = font.render("Chances: "+str(chances), True, white)
    shipsdestroyed_text = font.render("Ships Dead: "+str(ships_destroyed), True, white)
    level_text = font.render("Level "+str(level), True, white)

    # Blitting
    screen.blit(back, (0, 173))  # blitting backdrop
    # blitting various sprites, and if they're inactive. delete them
    for player in player_group.sprites():
        if player.active:
            screen.blit(player.image, (player.x, player.y-2))
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

    if chances == 0 and len(high_scores) == 0:  # if the game is over, open high scores file and write to it if new high score surpasses others
        pause = True
        player_group.empty()
        ship_group.empty()
        bullet_group.empty()
        game_over = True
        high_scores = []
        with open("highscores.txt", "r") as file:
            for line in file:
                try:
                    int(line)
                except ValueError:
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
                score_achieved_index = 10
        with open("highscores.txt", "w") as file:
            for score in high_scores[0:10]:
                file.write(str(score)+chr(10))
                chances = 1
        print(high_scores)
        game_over = True

    # blitting the top part of the screen
    top_bounds = 10
    screen.blit(white_surface, (0, 0))
    screen.blit(tank_surface, (10, top_bounds))
    screen.blit(missile_surface, (140, top_bounds))
    screen.blit(seamine_surface, (270, top_bounds))
    screen.blit(pause_surface, (400, top_bounds))

    scale = 125
    top_bounds = 100
    screen.blit(money_surface, (530 + 65, 10))
    screen.blit(money_text, (543 + 55, 85))
    screen.blit(ships_destroyed_surface, (635 + 65, 10))
    screen.blit(shipsdestroyed_text, (640 + 65, 85))
    screen.blit(weapons_surface, (740 + 65, 10))
    screen.blit(numweapons_text, (750 + 65, 85))
    screen.blit(chances_surface, (845 + 65, 10))
    screen.blit(chance_text, (855 + 65, 85))

    screen.blit(swirl, (600, 150))
    screen.blit(level_text, (743, 150))
    screen.blit(swirl, (800, 150))

    screen.blit(tank_text, (10, top_bounds))
    screen.blit(missile_text, (143, top_bounds))
    screen.blit(mine_text, (270, top_bounds))
    screen.blit(tank_cost, (10, top_bounds + 15))
    screen.blit(missile_cost, (140, top_bounds + 15))
    screen.blit(mine_cost, (270, top_bounds + 15))

    screen.blit(back_button_surface, (400, 90))

    screen.blit(tank_image, (scale - 75, 50))
    screen.blit(missile_image, (scale + 22, 50))
    screen.blit(mine_image, (scale + 175, 50))

    if splash_screen:  # if the splash screen is active, blit splash image, and social bar
        screen.blit(splash, (0, 0))
        screen.blit(social, (850, 20))

    if settings_screen:  # if the setting screen is active, blit that
        screen.blit(settings, (0, 0))
        if music:
            screen.blit(select, (132, 382 + 15))
        elif not music:
            screen.blit(select, (132, 470 + 13))

    if game_over and len(high_scores) > 0:  # if the game is over, blit high score image and values
        screen.blit(highscore_image, (0, 0))
        rank_text = font.render("Rank".ljust(20) + "Score", True, black)
        screen.blit(rank_text, (450, 140 + 60))
        for score_index in range(0, len(high_scores)):
            if score_index == score_achieved_index:
                rank_text = font.render((str(score_index + 1)).ljust(20) + str(high_scores[score_index]), True, (255, 0, 0))
            else:
                rank_text = font.render((str(score_index + 1)).ljust(20) + str(high_scores[score_index]), True, black)
            screen.blit(rank_text, (450, 175 + 35*score_index + 60))

    pygame.display.flip()

"""
 * Copyright (C) Mathstronauts. All rights reserved.
 * This information is confidential and proprietary to Mathstronauts and may not be used, modified, copied or distributed.
"""
# Space Junk game part 2
import pygame
import random

# initialize pygame
pygame.init()

# SCREEN ------------------------------
WIDTH = 1000
HEIGHT = 600
FPS = 30  # frames per second

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Junk")

# CLOCK -------------------------------
clock = pygame.time.Clock()

# timer function
start_time = 0
elapse_time = 0
TIME_LIMIT = 10

def timer():
    global start_time, elapse_time
    current_time = pygame.time.get_ticks()
    elapse_time = current_time - start_time

# COUNTERS ----------------------------
score = 0
window = "gameplay"  # start, gameplay

# GRAPHICS ----------------------------
# define some colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# create file paths
background_file = "images/demo_background.png"
player_file = "images/player_ship.png"
junk_file = "images/space_junk.png"
satellite_file = "images/satellite_adv.png"
debris_file = "images/space_debris2.png"
laser_file = "images/laser_red.png"

start_button_file = "images/start_button.png"
replay_button_file = "images/play_again_button.png"

# load background images
background = pygame.image.load(background_file).convert()
backgroundRect = background.get_rect(topleft=(0,0))  # if no position specified, default is topleft(0,0)

# draw text function
def display_text(size, text, colour, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)  # specify the font and size
    textSurf = font.render(text, True, colour)  # create a surface for the text object
    textRect = textSurf.get_rect()  # get rect position of text on the screen
    textRect.topleft = (x, y)  # specify rect position of text on screen
    screen.blit(textSurf, textRect)  # show the text on the screen

# draw text on screen
def showTextBox():
    global elapse_time
    # player score
    show_score = "Score: " + str(score)
    display_text(25, show_score, YELLOW, 600, 15)
    # timer
    time_passed = TIME_LIMIT - round(elapse_time / 1000)  # pygame gets time in milliseconds
    show_time = "Time: " + str(time_passed)
    display_text(25, show_time, GREEN, 800, 15)

def showGameOver():
    display_text(100, "GAME OVER", WHITE, int(WIDTH/2), 250)
    show_final_score = "Final Score: " + str(score)
    display_text(30, show_final_score, WHITE, int(WIDTH/2), 350)
    pygame.display.flip()  # we need to update the display before waiting

# SPRITES -----------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # inherit Sprite class
        # self.image = pygame.Surface((50, 50)) # rectangle shape
        # self.image.fill(GREEN)
        self.image = pygame.image.load(player_file).convert()
        self.image.set_colorkey(BLACK)  # cancel out transparent background
        self.rect = self.image.get_rect()    # set rect dimentions
        # RECT POSITION
        self.rect.x = 30
        self.rect.y = int(HEIGHT/2)
        self.y_speed = 0  # start not moving
    
    def update(self):
        # check if key pressed
        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_UP]: 
            self.y_speed = -10  # move up 10 pixels
        elif keypressed[pygame.K_DOWN]:
            self.y_speed = 10  # move down 10 pixels
        else:
            self.y_speed = 0   # don't move

        # update position
        self.rect.y += self.y_speed

        # set boundaries for movement
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def fireLaser(self):
        laser_x = self.rect.left  # the laser's x position is the player's x position
        laser_y = self.rect.centery  # the laser's y poistion is the player's centery position
        laser = Laser(laser_x, laser_y)
        laser_sprites.add(laser)
        all_sprites.add(laser)

class Junk(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # inherit Sprite class
        # self.image = pygame.Surface((25, 25))
        # self.image.fill(YELLOW)
        self.image = pygame.image.load(junk_file).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(-500, -50)  # start off screen
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.x_speed = 3
        # self.x_speed = random.randint(8, 18)  # set a random speed

    def reset(self):  # create a method to reset the sprite to a random position
        self.rect.x = random.randint(-500, -50)  # start off screen
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        # self.x_speed = random.randint(8, 18)  # set a random speed

    def update(self):
        # update position
        self.rect.x += self.x_speed
        if self.rect.left > WIDTH:
            # self.rect.x = 0
            self.reset()

class Satellite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((100, 80))
        # self.image.fill(BLUE)
        self.image = pygame.image.load(satellite_file).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.right = random.randint(-1000, -500)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.x_speed = 3
    
    def reset(self):
        self.rect.right = random.randint(-1000, -50)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
    
    def update(self):
        # update position
        self.rect.x += self.x_speed
        if self.rect.left > WIDTH:
            self.reset()

class Debris(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((100, 80))
        # self.image.fill(RED)
        self.image = pygame.image.load(debris_file).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.right = random.randint(-1000, -500)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.x_speed = 3
    
    def reset(self):
        self.rect.right = random.randint(-1000, -50)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
    
    def update(self):
        # update position
        self.rect.x += self.x_speed
        if self.rect.left > WIDTH:
            self.reset()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):  # the laser class has parameters for the x and y rect position
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 10))
        # self.image.fill(WHITE)
        self.image = pygame.image.load(laser_file).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.centery = y
        self.x_speed = -15  # negative because laser moving towards the left
    
    def update(self):
        self.rect.x += self.x_speed
        if self.rect.right < 0:  # if laser goes off screen
            self.kill()  # remove sprite from all groups

# SPRITE GROUPS ---------------------------
all_sprites = pygame.sprite.Group()
junk_sprites = pygame.sprite.Group()
sat_sprites = pygame.sprite.Group()
deb_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

# INITIALIZE SPRITES ----------------------
def init_sprites():
    global player
    player = Player()  # create an instance of the Player class
    all_sprites.add(player)  # add the sprite to our group 

    # create multiple junk sprites
    for i in range(5):
        junk = Junk()
        junk_sprites.add(junk)
        all_sprites.add(junk)

    # create satellite sprites
    for i in range(1):
        satellite = Satellite()
        sat_sprites.add(satellite)
        all_sprites.add(satellite)

    # create debris sprites
    for i in range(1):
        debris = Debris()
        deb_sprites.add(debris)
        all_sprites.add(debris)

# remove sprites from all groups
def clear_sprites():
    global player
    player.kill()
    junk_sprites.empty()
    sat_sprites.empty()
    deb_sprites.empty()
    laser_sprites.empty()
    all_sprites.empty()

# DETECT COLLISIONS -------------------
# player collision functions
def playerCollide():
    global score
    # check for collisions between player and junk sprite
    collision_junk_list = pygame.sprite.spritecollide(player, junk_sprites, True)
    for collision in collision_junk_list:
        # print("collect junk!")
        score += 1
        junk = Junk()  # re-initialize junk
        junk_sprites.add(junk)
        all_sprites.add(junk)
    
    # check for collisions between player and satellite sprite
    collision_sat_list = pygame.sprite.spritecollide(player, sat_sprites, True)
    for collision in collision_sat_list:
        # print("satellite down!")
        score += -5
        satellite = Satellite()
        sat_sprites.add(satellite)
        all_sprites.add(satellite)
    
    # check for collisions between player and debris sprite
    collision_deb_list = pygame.sprite.spritecollide(player, deb_sprites, True)
    for collision in collision_deb_list:
        # print("debris collision!")
        score += 5
        debris = Debris()
        deb_sprites.add(debris)
        all_sprites.add(debris)

# laser collision functions
def laserCollide():
    global score
    # check for collisions between junk sprites and lasers
    hit_junk_list = pygame.sprite.groupcollide(junk_sprites, laser_sprites, True, True)  # junk and bullet collide
    for hit in hit_junk_list:
        score += 5
        junk = Junk()
        junk_sprites.add(junk)
        all_sprites.add(junk)

    # check for collisions between satellite sprites and lasers
    hit_sat_list = pygame.sprite.groupcollide(sat_sprites, laser_sprites, True, True)  # satellite and bullet
    for hit in hit_sat_list:
        score += -10
        satellite = Satellite()
        sat_sprites.add(satellite)
        all_sprites.add(satellite)

    # check for collisions between debris sprites and lasers
    hit_deb_list = pygame.sprite.groupcollide(deb_sprites, laser_sprites, True, True)  # debris and bullet collide
    for hit in hit_deb_list:
        score += 10
        debris = Debris()  # re-initialize debris sprite, since debris is global, we are "writing over" the previous object
        deb_sprites.add(debris)
        all_sprites.add(debris)

init_sprites()
start_time = pygame.time.get_ticks()  # get start time

# GAME LOOP ---------------------------
running = True
while running:
    # regulate the speed
    clock.tick(FPS)

    # process user input
    events = pygame.event.get()
    for event in events:
        mouse = pygame.mouse.get_pos() # get position of mouse cursor
        if event.type == pygame.QUIT:  # if the X button is clicked
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fireLaser()  # create laser sprite

    # draw background
    screen.fill(BLACK)
    screen.blit(background,backgroundRect)
    showTextBox()

    # MAIN GAMEPLAY
    if window == "gameplay":
        # update the game
        timer()  # start timer
        all_sprites.update()
        playerCollide()
        laserCollide()
        # draw sprites
        all_sprites.draw(screen)

    # GAMEOVER
    if score < 0 or round(elapse_time/1000) == TIME_LIMIT:
        # print gameover
        showGameOver()
        window = "gameover"

    # update and draw game screen
    pygame.display.flip()

# quit pygame window
pygame.quit()
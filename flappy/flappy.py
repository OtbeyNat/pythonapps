import pygame
import math
from time import sleep
from pygame.sprite import Group
from random import randint, choice
from sys import exit

class Bird(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        yellow_down = pygame.image.load("sprites/yellowbird-downflap.png").convert_alpha()
        yellow_mid = pygame.image.load("sprites/yellowbird-midflap.png").convert_alpha()
        yellow_up = pygame.image.load("sprites/yellowbird-upflap.png").convert_alpha()
        red_down = pygame.image.load("sprites/redbird-downflap.png").convert_alpha()
        red_mid = pygame.image.load("sprites/redbird-midflap.png").convert_alpha()
        red_up = pygame.image.load("sprites/redbird-upflap.png").convert_alpha()
        blue_down = pygame.image.load("sprites/bluebird-downflap.png").convert_alpha()
        blue_mid = pygame.image.load("sprites/bluebird-midflap.png").convert_alpha()
        blue_up = pygame.image.load("sprites/bluebird-upflap.png").convert_alpha()
        yellow_bird = [yellow_down,yellow_mid,yellow_up]
        red_bird = [red_down,red_mid,red_up]
        blue_bird = [blue_down,blue_mid,blue_up]
        self.bird_index = 0
        self.increment = 0.1

        match color:
            case "yellow":
                self.fly = yellow_bird
            case "red":
                self.fly = red_bird
            case "blue":
                self.fly = blue_bird
                
        self.image = self.fly[self.bird_index]
        self.rect = self.image.get_rect(center = (150,250))
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = 0
        self.flap_sound = pygame.mixer.Sound("audio/wing.wav")
        self.flap_sound.set_volume(0.25)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -10
            #self.flap_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

    def animation_state(self):
        self.bird_index += self.increment
        if self.bird_index >= len(self.fly):
            self.increment = -0.1
            self.bird_index -= 1
        if self.bird_index <= 0: self.increment = 0.1  
        self.image = self.fly[int(self.bird_index)]

    def destroy(self):
        if self.rect.y >= 600: self.kill()

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.destroy()
             
class Pipe(pygame.sprite.Sprite):
    def __init__(self, color, direction):
        super().__init__()
        pipe_green = pygame.image.load("sprites/pipe-green.png").convert_alpha()
        pipe_red = pygame.image.load("sprites/pipe-red.png").convert_alpha()

        if color == 'G':
            self.image = pipe_green
            self.rect = pipe_green.get_rect()
        else:
            self.image = pipe_red
            self.rect = pipe_red.get_rect()
        if direction == "D":
            print('D')
            #rotate 180
        self.rect.midbottom = (700,800)
        self.mask = pygame.mask.from_surface(self.image)

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.rect.x -= 4
        self.destroy()

        # need to update score logic

def sprite_collision():
    if pygame.sprite.spritecollide(bird.sprite,pipe_group,False):
        if pygame.sprite.spritecollide(bird.sprite,pipe_group,False,pygame.sprite.collide_mask):
            pipe_group.empty()
            return False
        else: return True
    else: return True

SCREEN_WIDTH = 560
SCREEN_HEIGHT = 700
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.Font("font/FlappyBird.ttf")
clock = pygame.time.Clock()

sky_surface = pygame.image.load("sprites/background-day.png").convert_alpha()
sky_surface = pygame.transform.rotozoom(sky_surface,0,2)
sky_surface_rect = sky_surface.get_rect(topleft = (0,-210))

base_surface = pygame.image.load("sprites/base.png").convert()

sky_scroll = 0
base_scroll = 0
sky_width = sky_surface.get_width()
base_width = base_surface.get_width()
base_tiles = math.ceil(SCREEN_WIDTH/base_width) + 1

game_active = False
screen.blit(sky_surface,sky_surface_rect)
for j in range(base_tiles):
    screen.blit(base_surface,(j * base_width + base_scroll,600))

bird = pygame.sprite.GroupSingle()
pipe_group = pygame.sprite.Group()

pipe_timer = pygame.USEREVENT + 1
pipe_time = 2000
speed_up_time = 0 # value to compare when to speed up game
pygame.time.set_timer(pipe_timer,pipe_time)

score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pipe_timer:
                pipe_group.add(Pipe('G','U'))
                # NEEDS WEIGHTED CHOICE BETWEEN R/G
                # NEEDS HEIGHT OF UP AND DOWN
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                bird.add(Bird("yellow"))
    
    if game_active:
        base_scroll -= 4
        screen.blit(sky_surface,sky_surface_rect)
        
        pipe_group.draw(screen)
        pipe_group.update()
        
        for j in range(base_tiles):
            screen.blit(base_surface,(j * base_width + base_scroll,600))
        if abs(base_scroll) > base_width: base_scroll = 0

        bird.draw(screen)
        bird.update()

        game_active = sprite_collision()
        if not bird.sprites(): 
            game_active = False

        #show score if available
    pygame.display.update() #update display surface
    clock.tick(60)
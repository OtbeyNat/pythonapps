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
            case 'Y':
                self.fly = yellow_bird
            case 'R':
                self.fly = red_bird
            case 'B':
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
            self.gravity = -7
            #self.flap_sound.play()

    def apply_gravity(self):
        self.gravity += 0.7
        self.rect.y += self.gravity

    def animation_state(self):
        self.bird_index += self.increment
        if self.bird_index >= len(self.fly):
            self.increment = -0.1
            self.bird_index -= 1
        if self.bird_index <= 0: self.increment = 0.1  
        self.image = self.fly[int(self.bird_index)]

    def destroy(self):
        if self.rect.y >= 475: self.kill()

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.destroy()
             
class Pipe(pygame.sprite.Sprite):
    def __init__(self, color, direction,height):
        super().__init__()
        pipe_green = pygame.image.load("sprites/pipe-green.png").convert_alpha()
        pipe_red = pygame.image.load("sprites/pipe-red.png").convert_alpha()
        self.color = color
        self.direction = direction
        self.height = height
        self.point = 1
        if self.color == 'G':
            self.image = pipe_green
            self.set_direction() 
        else: # red pipe
            self.image = pipe_red
            self.set_direction()
               
        self.mask = pygame.mask.from_surface(self.image)

    def set_direction(self,):
        if self.direction == "D":
            self.image = pygame.transform.rotate(self.image,180)
            self.rect = self.image.get_rect()
            self.rect.midbottom = (600,self.height)
        else:
            self.rect = self.image.get_rect()
            self.rect.midtop = (600,self.height)

    def destroy(self):
        if self.rect.right <= 0:
            self.kill()

    def update(self):
        self.rect.x -= speed
        self.destroy()
        # need to update score logic

def sprite_collision():
    if pygame.sprite.spritecollide(bird.sprite,pipe_group,False):
        if pygame.sprite.spritecollide(bird.sprite,pipe_group,False,pygame.sprite.collide_mask):
            pipe_group.empty()
            return False
        else: return True
    else: return True

def display_score():
    score_surface = font.render(f'{score}',False,'White')
    score_surface_rect = score_surface.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/4))
    if not game_active:
        high_score_surface = font.render("Best: "+f'{high_score}',False,'White')
        high_score_surface_rect = high_score_surface.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/4 + 50))
        screen.blit(high_score_surface,high_score_surface_rect)
    screen.blit(score_surface,score_surface_rect)

def display_bird():
    match bird_color_index:
        case 0:
            bir = pygame.image.load("sprites/redbird-upflap.png").convert_alpha()
        case 1:
            bir = pygame.image.load("sprites/yellowbird-upflap.png").convert_alpha()  
        case 2:
            bir = pygame.image.load("sprites/bluebird-upflap.png").convert_alpha()
    bir_rect = bir.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
    screen.blit(bir,bir_rect)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 550
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.Font("font/FlappyBird.ttf",50)
clock = pygame.time.Clock()

day_surface = pygame.image.load("sprites/background-day.png").convert_alpha()
day_surface = pygame.transform.rotozoom(day_surface,0,2)
day_surface_rect = day_surface.get_rect(topleft = (0,-330))
night_surface = pygame.image.load("sprites/background-night.png").convert_alpha()
night_surface = pygame.transform.rotozoom(night_surface,0,2)
night_surface_rect = night_surface.get_rect(topleft = (0,-330))
theme = "day"
sky_surface = day_surface
sky_surface_rect = day_surface_rect
base_surface = pygame.image.load("sprites/base.png").convert()

sun = pygame.image.load("sprites/sun.png").convert_alpha()
sun = pygame.transform.scale(sun,(70,70))
sun_rect = sun.get_rect(bottomleft = (20,530))
moon = pygame.image.load("sprites/moon.png").convert_alpha()
moon = pygame.transform.scale(moon,(70,70))
moon_rect = moon.get_rect(bottomleft = (20,530))

sky_scroll = 0
base_scroll = 0
sky_width = sky_surface.get_width()
base_width = base_surface.get_width()
base_tiles = math.ceil(SCREEN_WIDTH/base_width) + 1

title = font.render("FlappyBird",False,'Orange')
title_rect = title.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/4))
left = font.render("<",False,'White')
right = font.render(">",False,'White')
left_rect = left.get_rect(center = (SCREEN_WIDTH/2 - 100,SCREEN_HEIGHT/2))
right_rect = right.get_rect(center = (SCREEN_WIDTH/2 + 100,SCREEN_HEIGHT/2))
start_surf = pygame.image.load("sprites/start_btn.png").convert_alpha()
start_surf = pygame.transform.scale_by(start_surf,0.5)
start_rect = start_surf.get_rect(bottomright = (SCREEN_WIDTH - 20,SCREEN_HEIGHT - 20))
exit_surf = pygame.image.load("sprites/exit_btn.png").convert_alpha()
exit_surf = pygame.transform.scale_by(exit_surf,0.5)
exit_rect = exit_surf.get_rect(bottomright = (SCREEN_WIDTH - 20,SCREEN_HEIGHT - 20))
game_over = pygame.image.load("sprites/gameover.png").convert_alpha()
game_over_rect = game_over.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/7))

bird = pygame.sprite.GroupSingle()
pipe_group = pygame.sprite.Group()

pipe_timer = pygame.USEREVENT + 1
pipe_time = 1500
speed = 3

speeds = [[1500,3],[1250,3],[1000,3],[900,4],[850,4],[650,5]]
score_increment = [0,5,10,25,50,75]
speed_index = 0

pygame.time.set_timer(pipe_timer,pipe_time)

distances = [100,110,110,110,125,125,125,150]
colors = ['R','G','G','G','G','G','G','G','G','G','G','G']
bird_color = 'Y'
bird_colors = ['R','Y','B']
bird_color_index = 1

game_active = False
score = 0
high_score = 0
start = False
quit = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit = True
            exit()
        if quit: break
        if game_active:
            if event.type == pipe_timer:
                pipe_color = choice(colors)
                dist = choice(distances)
                if pipe_color == 'R': dist = 100
                choose_p = choice([0,1])
                if choose_p:
                    up_height = randint(155,450)
                    down_height = up_height - dist
                    if down_height > 320: down_height = 320
                else:
                    down_height = randint(10,320)
                    up_height = down_height + dist
                    if up_height < 155: up_height = 155

                pipe_group.add(Pipe(pipe_color,'D', down_height))
                pipe_group.add(Pipe(pipe_color,'U', up_height))
                
                # Down Heights [5,320]
                # Up Heights [155,475]
        else: 
            if start:
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse = pygame.mouse.get_pos()
                    if exit_rect.collidepoint(mouse): start = False
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse = pygame.mouse.get_pos()
                    if left_rect.collidepoint(mouse):
                        if bird_color_index == 0: bird_color_index = 2
                        else: bird_color_index -= 1
                    if right_rect.collidepoint(mouse):
                        if bird_color_index == 2: bird_color_index = 0
                        else: bird_color_index += 1
                    if start_rect.collidepoint(mouse): 
                        start = True
                        game_active = True
                        score = 0
                        bird.add(Bird(bird_colors[bird_color_index]))
                        speed = 3
                        pipe_time = 1500
                        speed_index = 0
                    if sun_rect.collidepoint(mouse) and theme == "day":
                        theme = "night"
                        sky_surface = night_surface
                        sky_surface_rect = night_surface_rect
                        break
                    if moon_rect.collidepoint(mouse) and theme == "night":
                        theme = "day"
                        sky_surface = day_surface
                        sky_surface_rect = day_surface_rect

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start = True
                game_active = True
                score = 0
                bird.add(Bird(bird_colors[bird_color_index]))
                speed = 3
                pipe_time = 1500
                speed_index = 0
    
    if quit: break
    if game_active:
        base_scroll -= speed
        screen.blit(sky_surface,sky_surface_rect)
        
        pipe_group.draw(screen)
        pipe_group.update()
        
        for j in range(base_tiles):
            screen.blit(base_surface,(j * base_width + base_scroll,475))
        if abs(base_scroll) > base_width: base_scroll = 0

        bird.draw(screen)
        bird.update()

        if not bird.sprites(): 
            game_active = False
            pipe_group.empty()
            
        if game_active: game_active = sprite_collision()
        
        for pipe in pipe_group:
            if pipe.direction == 'U' and pipe.rect.right < 133 and pipe.point:
                pipe.point = 0
                if pipe.color == 'R': score += 5
                else: score += 1
                break
        high_score = max(high_score,score)
        display_score()
        if speed_index < 5 and score >= score_increment[speed_index]:
            pipe_time = speeds[speed_index][0]
            speed = speeds[speed_index][1]
            speed_index += 1
            pygame.time.set_timer(pipe_timer,pipe_time)

    else:
        if start:
            screen.blit(game_over,game_over_rect)
            display_score()
            screen.blit(exit_surf,exit_rect)
        else: # main menu
            screen.blit(sky_surface,sky_surface_rect)
            for j in range(base_tiles):
                screen.blit(base_surface,(j * base_width + base_scroll,475))
            screen.blit(title,title_rect)
            if theme == "day": screen.blit(moon,moon_rect)
            else: screen.blit(sun,sun_rect)
            display_bird()
            screen.blit(left,left_rect)
            screen.blit(right,right_rect)
            screen.blit(start_surf,start_rect)
    pygame.display.update() #update display surface
    clock.tick(60)
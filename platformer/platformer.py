import pygame
from pygame.locals import *

import pickle
from os import path

from pygame.sprite import Group

pygame.init()

screen_width,screen_height = 1000,1000
screen = pygame.display.set_mode((screen_width,screen_width))
pygame.display.set_caption("Platformer")

font_score = pygame.font.SysFont('Bauhaus 93', 30)
msg_font = pygame.font.SysFont('Bauhaus 93', 70)

clock = pygame.time.Clock()
fps = 60

tile_size = 50
game_over = 0
menu = True
max_level = 7

sun_img = pygame.image.load('img/sun.png')
#sun_img = pygame.transform.scale(sun_img, (tile_size, tile_size))
bg_img = pygame.image.load('img/sky.png')
#bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
restart_img = pygame.image.load('img/restart_btn.png')

start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')

coin_sound = pygame.mixer.Sound('img/coin.wav')
coin_sound.set_volume(0.5)
jump_sound = pygame.mixer.Sound('img/jump.wav')
jump_sound.set_volume(0.5)
go_sound = pygame.mixer.Sound('img/game_over.wav')
go_sound.set_volume(0.5)
pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1,0,5000)

class World():
    def __init__(self,data):
        self.tiles = []
        dirt_img = pygame.image.load('img/dirt.png')
        self.dirt_img = pygame.transform.scale(dirt_img,(tile_size,tile_size))
        grass_img = pygame.image.load('img/grass.png')
        self.grass_img = pygame.transform.scale(grass_img,(tile_size,tile_size))
        platform_x_img = pygame.image.load('img/platform_x.png')
        self.platform_x_img = pygame.transform.scale(platform_x_img,(tile_size,0.5*tile_size))
        platform_y_img = pygame.image.load('img/platform_y.png')
        self.platform_y_img = pygame.transform.scale(platform_y_img,(tile_size,0.5*tile_size))
        
        self.set_world(data)

    def set_world(self,data):
        self.tiles = []
        row = 0
        for row_data in data:
            col = 0
            for col_data in row_data:
                if col_data > 0:
                    match col_data:
                        case 1:
                            img = self.dirt_img
                            img_rect = img.get_rect()
                            img_rect.x = col * tile_size
                            img_rect.y = row * tile_size
                            tile = (img,img_rect)
                            self.tiles.append(tile)
                        case 2:
                            img = self.grass_img
                            img_rect = img.get_rect()
                            img_rect.x = col * tile_size
                            img_rect.y = row * tile_size
                            tile = (img,img_rect)
                            self.tiles.append(tile) 
                        case 3:
                            blob = Enemy(col*tile_size,row*tile_size+15)
                            blob_group.add(blob)                     
                        case 4:
                            platform = Platform(col*tile_size,row*tile_size,0)
                            platform_group.add(platform)
                        case 5:
                            platform = Platform(col*tile_size,row*tile_size,1)
                            platform_group.add(platform)
                        case 6:
                            lava = Lava(col*tile_size,row*tile_size + (tile_size//2))
                            lava_group.add(lava)
                        case 7:
                            coin = Coin(col*tile_size + (tile_size//2),row*tile_size + (tile_size//2))
                            coin_group.add(coin)
                        case 8:
                            exit = Exit(col*tile_size,row*tile_size - (tile_size//2))
                            exit_group.add(exit)
                col += 1
            row += 1

    def draw(self):
        for tile in self.tiles:
            screen.blit(tile[0],tile[1])

class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img,(tile_size,tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,move):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform.png')
        self.image = pygame.transform.scale(img,(tile_size,tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.count = 0
        self.move = move
    
    def update(self):
        if self.move: self.rect.y += self.direction
        else: self.rect.x += self.direction
        self.count += 1
        if abs(self.count) > 100:
            self.direction *= -1
            self.count *= -1 

class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(img,(tile_size//2,tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y) -> None:
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img,(tile_size, int(tile_size*1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.count = 0

    def update(self):
        self.rect.x += self.direction
        self.count += 1
        if abs(self.count) > 50:
            self.direction *= -1
            self.count *= -1

class Player():
    def __init__(self,x,y):
        self.reset(x,y)

    def reset(self,x,y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right,(40,80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_img = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 1
        self.mid_air = True

    def update(self,g_o):
        key = pygame.key.get_pressed()
        dx = 0
        dy = 0
        walk_cd = 5
        col_threshold = 20
        if not game_over:
            if key[pygame.K_SPACE] and not self.jumped and not self.mid_air: 
                jump_sound.play()
                self.vel_y = -15
                self.jumped = True
            if not key[pygame.K_SPACE]: self.jumped = False
            if key[pygame.K_LEFT]: 
                self.counter += 1
                dx -= 5
                self.direction = 0
            if key[pygame.K_RIGHT]: 
                self.counter += 1
                dx += 5
                self.direction = 1
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]: 
                self.counter = 0
                self.index = 0
                if self.direction == 1: self.image = self.images_right[self.index]
                else: self.image = self.images_left[self.index]

            # animation
            if self.counter > walk_cd:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right): 
                    self.index = 0
                if self.direction: self.image = self.images_right[self.index]
                else: self.image = self.images_left[self.index]

            self.vel_y += 1
            dy += self.vel_y
            
            # collision
            self.mid_air = True
            for tile in world.tiles:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0: # jumping
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0: # falling
                        dy = tile[1].top - self.rect.bottom
                        self.mid_air = False
                        self.vel_y = 0

            if pygame.sprite.spritecollide(self,blob_group,False): g_o = 1
            if pygame.sprite.spritecollide(self,lava_group,False): g_o = 1 
            if g_o == 1:
                go_sound.play() 
            if pygame.sprite.spritecollide(self,exit_group,False): g_o = 2

            for platform in platform_group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_threshold:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_threshold:
                        self.rect.bottom = platform.rect.top - 1
                        self.mid_air = False
                        self.vel_y = 0
                        dy = 0
            
            self.rect.x += dx
            self.rect.y += dy
        else:
            self.image = self.dead_img
            if self.rect.y > 100: self.rect.y -= 5
        screen.blit(self.image,self.rect)
        return g_o

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked: 
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0: self.clicked = False
        screen.blit(self.image,self.rect)
        
        return action

def load_world(lvl):
    if path.exists(f'level{lvl}_data'):
        pickle_in = open(f'level{lvl}_data', 'rb')
        data = pickle.load(pickle_in)
    else: data = None
    return data

def show_text(text,font,col,x,y):
    img = font.render(text,True,col)
    screen.blit(img,(x,y))

score = 0
level = 0
world_data = load_world(level)

    #print(world_data)
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
world = World(world_data)
player = Player(100, screen_height - 130)

restart = Button(screen_width//2 - 50, screen_height//2 + 100, restart_img)
start = Button(screen_width//2 - 350, screen_height//2, start_img)
exit_btn = Button(screen_width//2 + 150, screen_height//2, exit_img)

run = True
while run:
    clock.tick(fps)

    screen.blit(bg_img,(0,0))
    screen.blit(sun_img,(100,100))

    if menu:
        if start.draw(): menu = False
        if exit_btn.draw(): run = False
    else:
        world.draw()
        if not game_over:
            blob_group.update()
            platform_group.update()
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_sound.play()
            show_text('X ' + str(score), font_score, 'White', tile_size - 10, 10)

        blob_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        coin_group.draw(screen)
        platform_group.draw(screen)

        game_over = player.update(game_over)
        if game_over == 1:
            show_text('GAME OVER',msg_font,'Blue',(screen_width//2) - 140,(screen_height//2))
            if restart.draw():
                game_over = 0
                player.reset(100,screen_height - 130)
        if game_over == 2:
            level += 1
            if level <= max_level:
                game_over = 0
                blob_group.empty()
                lava_group.empty()
                exit_group.empty()
                coin_group.empty()
                platform_group.empty()
                world_data = load_world(level)
                world.set_world(world_data)
                player.reset(100,screen_height - 130)
            else: # game done
                show_text('WIN',msg_font,'Blue',(screen_width//2) - 140,(screen_height//2))
                if restart.draw():
                    game_over = 0
                    level = 0
                    score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    
pygame.quit()



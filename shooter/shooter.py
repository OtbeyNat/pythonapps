import pygame
import os
import random
import csv
import button

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()
fps = 60

BG = (144,201,120)
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
SCROLL_THRESH = 200
MAX_LEVELS = 3

screen_scroll = 0
bg_scroll = 0

start_game = False
level = 1
level_complete = False

moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()

health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
item_boxes = {
	'Health'	: health_box_img,
	'Ammo'		: ammo_box_img,
	'Grenade'	: grenade_box_img
}

img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile/{x}.png').convert_alpha()
    img_list.append(pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE)))

pine1_img = pygame.image.load("img/Background/pine1.png").convert_alpha()
pine2_img = pygame.image.load("img/Background/pine2.png").convert_alpha()
mountain_img = pygame.image.load("img/Background/mountain.png").convert_alpha()
sky_img = pygame.image.load("img/Background/sky_cloud.png").convert_alpha()

start_img = pygame.image.load("img/start_btn.png").convert_alpha()
exit_img = pygame.image.load("img/exit_btn.png").convert_alpha()
restart_img = pygame.image.load("img/restart_btn.png").convert_alpha()

font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5): # scrolling background
        screen.blit(sky_img,((x*width) - bg_scroll * 0.5,0))
        screen.blit(mountain_img, ((x*width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x*width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x*width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

def reset_level(level):
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    with open(f'level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x,row in enumerate(reader):
            for y,tile in enumerate(row):
                data[x][y] = int(tile)
    return data

class Soldier(pygame.sprite.Sprite):
    def __init__(self,type,x,y,scale,speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True
        self.char_type = type
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        #load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(center = (x,y))

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.facing_left = 0
        self.jump = False
        self.in_air = True
        self.flip = False   
        self.shoot_cd = 0
        self.start_ammo = ammo
        self.ammo = ammo
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.hit_cd = 0 # account for damage one per explosion
        self.update_time = pygame.time.get_ticks()
        #ai variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 300, 20)
        self.idling = False
        self.idling_counter = 0

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cd > 0: self.shoot_cd -= 1
        if self.hit_cd > 0: self.hit_cd -= 1

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.facing_left,False),self.rect)
    
    def move(self,moving_left,moving_right):
        dx = 0
        dy = 0
        screen_scroll = 0
        level_complete = False

        if moving_left:
            dx = -self.speed
            self.facing_left = 1
            self.direction = -1
        if moving_right: 
            dx = self.speed
            self.facing_left = 0
            self.direction = 1

        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -14
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += 1
        self.vel_y = min(self.vel_y,10)
        dy += self.vel_y

        #check collision with world
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.in_air = False
                    self.vel_y = 0

        # death from terrain
        if pygame.sprite.spritecollide(self,water_group,False): self.health = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.health = 0

        # complete level
        if pygame.sprite.spritecollide(self,exit_group,False): level_complete = True
        if self.char_type == "player":
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        self.rect.x += dx
        self.rect.y += dy

        # scroll
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll,level_complete

    def shoot(self):
        if self.shoot_cd == 0 and self.ammo > 0:
            bullet = Bullet(self.rect.centerx + (0.75 * (self.rect.size[0]) * self.direction),self.rect.centery,self.direction)
            bullet_group.add(bullet)
            self.shoot_cd = 20
            self.ammo -= 1

    def grenade(self):
        if self.grenades > 0:
            grenade = Grenade(self.rect.centerx + (0.5 * self.rect.size[0] * self.direction), \
                            self.rect.top, self.direction)
            grenade_group.add(grenade)
            self.grenades -= 1
        
    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idling_counter = 50

            # need to account for obstacles vision
            if self.vision.colliderect(player.rect):
				#stop running and face the player
                self.update_action(0)#0: idle
                # attack
                # if random.randint(1,200) == 1 and self.grenades > 0: self.grenade()
                if abs(player.rect.centerx - self.rect.centerx) <= 350 and self.grenades > 0: self.grenade()
                else: self.shoot()
            else: # player not spotted
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right

                    # make them not fall into water or void 
                    self.move(ai_moving_left,ai_moving_right)
                    self.update_action(1)#1: run
                    self.move_counter += 1	
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 150 * self.direction, self.rect.centery)
                    
                    if self.move_counter > 20: # turn around
                        self.direction *= -1
                        self.move_counter = 0
                else: # count down for idle
                    self.idling_counter -= 1 
                    if self.idling_counter <= 0:
                        self.idling = False
        
        self.rect.x += screen_scroll    

    def update_animation(self):
        ANIMATION_CD = 100
        if pygame.time.get_ticks() - self.update_time >= ANIMATION_CD:
            self.frame_index += 1
            if self.frame_index == len(self.animation_list[self.action]): 
                if self.action == 3: self.frame_index -= 1
                else: self.frame_index = 0
            self.image = self.animation_list[self.action][self.frame_index]
            self.update_time = pygame.time.get_ticks()

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.speed = 0
            self.update_action(3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)

        self.speed = 12
        self.image = bullet_img
        self.rect = self.image.get_rect(center = (x,y))
        self.direction = direction
        self.timer = 40

    def update(self):
        self.rect.x += (self.direction * self.speed) + screen_scroll
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH: self.kill()

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect): self.kill()

        if pygame.sprite.spritecollide(player,bullet_group,False):
            if player.alive:
                self.kill()
                player.health -= 5
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy,bullet_group,False):
                if enemy.alive:
                    self.kill()
                    enemy.health -= 25
        self.timer -= 1
        if self.timer <= 0: self.kill()

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)

        self.timer = 80
        self.image = grenade_img
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect(center = (x,y))
        self.direction = direction
        self.vel_y = -16
        self.speed = 8

    def update(self):
        self.vel_y += 1
        dx = self.speed * self.direction
        dy = self.vel_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.speed = max(self.speed - 0.25, 0)

        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x,self.rect.top,1.5)
            explosion_group.add(explosion)

            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and\
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
                player.hit_cd = 60
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and\
                abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 100
                    enemy.hit_cd = 60

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f"img/explosion/exp{num}.png").convert_alpha()
            self.images.append(pygame.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale))))
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect(center = (x,y))
        self.counter = 0 
    
    def update(self):
        EXPLOSION_SPEED = 4
        self.counter += 1
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images): self.kill()
            else: self.image = self.images[self.frame_index]
        self.rect.x += screen_scroll
        # if pygame.sprite.spritecollide(player,explosion_group,False):
        #     if player.alive and player.hit_cd == 0:
        #         player.health -= 50
        #         player.hit_cd = 60
        # for enemy in enemy_group:
        #     if pygame.sprite.spritecollide(enemy,explosion_group,False):
        #         if enemy.alive and enemy.hit_cd == 0:
        #             enemy.health -= 100
        #             enemy.hit_cd = 60

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
		#check if the player has picked up the box
        self.rect.x += screen_scroll
        if pygame.sprite.collide_rect(self, player):
            #check what kind of box it was
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 15
            elif self.item_type == 'Grenade':
                player.grenades += 3
            #delete the item box
            self.kill()

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect(midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect(midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect(midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class HealthBar():
	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health

	def draw(self, health):
		#update with new health
		self.health = health
		#calculate health ratio
		ratio = self.health / self.max_health
		pygame.draw.rect(screen, 'Black', (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(screen, 'Red', (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, 'Green', (self.x, self.y, 150 * ratio, 20))   

class World():
    def __init__(self):
        self.obstacle_list = []
        
    def process(self,data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()   
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    # dirt blocks
                    if tile >= 0 and tile <= 8: self.obstacle_list.append(tile_data)
                    # water
                    elif tile == 9 or tile == 10:
                        water = Water(img, x * TILE_SIZE,y * TILE_SIZE)
                        water_group.add(water)
                    # decor
                    elif tile >= 11 and tile <= 14:
                        decor = Decoration(img, x * TILE_SIZE,y * TILE_SIZE)
                        decoration_group.add(decor)
                    elif tile == 15:
                        player = Soldier("player",x * TILE_SIZE,(y * TILE_SIZE) -2 ,1.65,5,20,5)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16:
                        enemy = Soldier("enemy",x * TILE_SIZE,y * TILE_SIZE,1.65,5,50,2)
                        enemy_group.add(enemy)
                    elif tile == 17:
                        item_box = ItemBox('Ammo', x * TILE_SIZE,y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:
                        item_box = ItemBox('Grenade', x * TILE_SIZE,y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:
                        item_box = ItemBox('Health', x * TILE_SIZE,y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
        return player, health_bar
    
    def draw(self):
        for tile in self.obstacle_list: 
            tile[1][0] += screen_scroll
            screen.blit(tile[0],tile[1])

start_btn = button.Button(SCREEN_WIDTH//2 - 130, SCREEN_HEIGHT // 2 - 120, start_img,1)
exit_btn = button.Button(SCREEN_WIDTH//2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img,1)
restart_btn = button.Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT // 2 - 120, restart_img,2)

enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


# world_data = []
# for row in range(ROWS):
#     r = [-1] * COLS
#     world_data.append(r)
# with open(f'level{level}_data.csv', newline='') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     for x,row in enumerate(reader):
#         for y,tile in enumerate(row):
#             world_data[x][y] = int(tile) # read in as strings initially

world_data = reset_level(level)
world = World()
player, health_bar = world.process(world_data)

run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: moving_left = True
            if event.key == pygame.K_d: moving_right = True
            if event.key == pygame.K_q: grenade = True
            if event.key == pygame.K_SPACE: shoot = True
            if event.key == pygame.K_w and player.alive: player.jump = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: moving_left = False
            if event.key == pygame.K_d: moving_right = False
            if event.key == pygame.K_q: 
                grenade = False
                grenade_thrown = False
            if event.key == pygame.K_SPACE: shoot = False

    if not start_game:
        screen.fill(BG)
        if start_btn.draw(screen): start_game = True
        if exit_btn.draw(screen): run = False
    else:
        draw_bg()
        world.draw()

        health_bar.draw(player.health)
        draw_text('AMMO: ', font, 'White', 10, 35)
        for x in range(player.ammo):
            screen.blit(bullet_img, (90 + (x * 10), 40))
        draw_text('GRENADES: ', font, 'White', 10, 60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (135 + (x * 15), 60))

        
        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()

        player.update()
        player.draw()

        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        if player.alive:
            if shoot: 
                player.shoot()
            elif grenade and grenade_thrown == False:
                player.grenade()
                grenade_thrown = True
            if player.in_air:
                player.update_action(2)#2: jump
            elif moving_left or moving_right:
                player.update_action(1)#1: run
            else:
                player.update_action(0)#0: idle
            screen_scroll,level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            if level_complete:
                bg_scroll = 0
                level += 1
                if level <= MAX_LEVELS:
                    world_data = reset_level(level)
                    world = World()
                    player, health_bar = world.process(world_data)
                level_complete = False
                
        else:
            screen_scroll = 0
            if restart_btn.draw(screen): # restart level
                bg_scroll = 0
                world_data = reset_level(level)
                world = World()
                player, health_bar = world.process(world_data)
                
        

    pygame.display.update()
    
pygame.quit()
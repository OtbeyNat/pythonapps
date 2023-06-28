import pygame

class Character():
    def __init__(self,x,y,pnum,width,height,char_data,spritesheet,animation_frames,sound,proj_sheet):
        self.rect = pygame.Rect((x,y,80,180))
        self.pnum = pnum
        self.screen_width = width
        self.screen_height = height
        self.vel_y = 0
        self.running = False
        self.jumped = False
        if pnum == 2: self.facing_left = 1
        else: self.facing_left = 0
        self.attack_num = 0
        self.attacking = False
        self.attack_cd = 0
        self.check_atk = 1
        self.hit = False
        self.alive = True
        self.max_hp = 100
        self.health = self.max_hp
        self.projectile = False
        self.projectile_index = 0
        self.projectile_start_time = 0
        self.projectile_time = 0
        self.proj_left = 0
        self.proj_width,self.proj_height = 187.5,180
        self.proj_scale = 0.65
        self.img_size = char_data[0]
        self.img_scale = char_data[1]
        self.offset = char_data[2]
        self.animation_frames = animation_frames
        self.animation_list,self.projectile_list = self.load_images(spritesheet,proj_sheet)
        self.action = 0 
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.sound = sound
        self.blocking = False
        self.block_start = 0
        self.block_cd = 0
        # 0=idle 1=run 2=jump 3=atk1 4=atk2 5=hit 6=death

    def load_images(self,sprite_sheet,proj_sheet):
        animation_list = []
        projectile_list = []
        block_img = None
        for y,num in enumerate(self.animation_frames):
            tmp_img_list = []
            for x in range(num):
                tmp_img = sprite_sheet.subsurface(x*self.img_size,y*self.img_size,self.img_size,self.img_size)
                tmp_img_list.append(pygame.transform.scale(tmp_img,(self.img_size*self.img_scale,self.img_size*self.img_scale)))
            animation_list.append(tmp_img_list)
            if y == 3: block_img = tmp_img_list[-1]
            if self.pnum == 2 and y == 4: block_img = tmp_img_list[-1]
        animation_list.append([block_img])
        self.animation_frames.append(1)
        
        if self.pnum == 1: height = 20
        else: height = 0
        for n in range(4):
            tmp = proj_sheet.subsurface(n*self.proj_width,height,self.proj_width,self.proj_height)
            projectile_list.append(pygame.transform.scale(tmp,(self.proj_width*self.proj_scale,self.proj_height*self.proj_scale)))
        return animation_list,projectile_list
    
    def move(self):
        speed = 10
        dx = 0
        dy = 0
        gravity = 2
        self.running = False
        key = pygame.key.get_pressed()
        # movement
        if self.pnum == 1 and self.alive: # player 1 keys
            if not self.blocking:
                if key[pygame.K_a]: 
                    dx = -speed
                    self.facing_left = 1
                    self.running = True
                if key[pygame.K_d]: 
                    dx = speed
                    self.facing_left = 0
                    self.running = True
                if key[pygame.K_w] and not self.jumped: 
                    self.vel_y = -30
                    self.jumped = True
                #include block
                if key[pygame.K_s]:
                    if pygame.time.get_ticks() - self.block_cd >= 1500:
                        self.blocking = True
                        self.block_start = pygame.time.get_ticks()
                # attack
                if (key[pygame.K_r] or key[pygame.K_t]) and not self.attacking:
                    if key[pygame.K_t]: self.attack_num = 1
                    else: self.attack_num = 2
                    if pygame.time.get_ticks() - self.attack_cd >= 1000:
                        self.attacking = True
                        self.sound.play()

        if self.pnum == 2 and self.alive: # player 2 keys
            if not self.blocking:
                if key[pygame.K_LEFT]: 
                    dx = -speed
                    self.facing_left = 1
                    self.running = True
                if key[pygame.K_RIGHT]: 
                    dx = speed
                    self.facing_left = 0
                    self.running = True
                if key[pygame.K_UP] and not self.jumped: 
                    self.vel_y = -30
                    self.jumped = True
                if key[pygame.K_DOWN]:
                    if pygame.time.get_ticks() - self.block_cd >= 1500:
                        self.blocking = True
                        self.block_start = pygame.time.get_ticks()
                if (key[pygame.K_SLASH] or key[pygame.K_PERIOD]) and not self.attacking:
                    if key[pygame.K_SLASH]: self.attack_num = 2
                    else: self.attack_num = 1
                    if pygame.time.get_ticks() - self.attack_cd >= 1000:
                        self.attacking = True
                        self.sound.play()
        
        # set dx,dy
        # gravity
        self.vel_y += gravity
        dy += self.vel_y

        # stay on screen
        if self.rect.left + dx < 0: dx = -self.rect.left
        if self.rect.right + dx > self.screen_width: dx = self.screen_width - self.rect.right
        if self.rect.bottom + dy > self.screen_height - 110:
            self.vel_y = 0
            self.jumped = False
            dy = self.screen_height - 110 - self.rect.bottom
    
        # update rect
        self.rect.x += dx
        self.rect.y += dy
        
    def update(self,target):
        animation_cd = 75
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.change_action(6)
        elif self.hit: self.change_action(5)
        elif self.blocking: self.change_action(7) #blocking
        elif self.attacking:
            if self.attack_num == 1: self.change_action(3)
            else: self.change_action(4)
        elif self.jumped: self.change_action(2)
        elif self.running: self.change_action(1)
        else: self.change_action(0)

        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= animation_cd:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.projectile:
            curr_time = pygame.time.get_ticks()
            if curr_time - self.projectile_start_time >= 750:
                self.projectile = False
            elif curr_time - self.projectile_time >= animation_cd:
                self.projectile_index += 1
                self.projectile_time = pygame.time.get_ticks()
            else: self.proj_rect.x += 17.5 * self.proj_left
        if self.blocking and pygame.time.get_ticks() - self.block_start >= 500:
            self.blocking = False
            self.block_cd = pygame.time.get_ticks()
        if self.attacking and self.frame_index == 4 and self.check_atk:
            if self.attack(target): pass
            elif (self.attack_num == 1 and self.pnum == 1) or (self.pnum == 2 and self.attack_num == 2):
                self.projectile = True
                self.projectile_start_time = pygame.time.get_ticks()
                self.projectile_time = self.projectile_start_time
                #draw projectile
                self.proj_img = self.projectile_list[self.projectile_index]
                self.proj_rect = self.proj_img.get_rect()
                self.proj_rect.x = self.rect.centerx - (2 * self.rect.width * self.facing_left)
                self.proj_rect.y = self.rect.y + 50
                if self.facing_left: self.proj_left = -1
                else: self.proj_left = 1

            self.check_atk = False # ensures only take dmg once per attack
        if self.projectile_index >= 4:
            self.projectile_index = 0
        if self.frame_index >= self.animation_frames[self.action]: 
            # end of animation cycle 
            if not self.alive: self.frame_index = self.animation_frames[self.action] -1
            else:
                if self.attacking:
                    self.attacking = False
                    self.check_atk = True
                    self.attack_cd = pygame.time.get_ticks()
                if self.hit: self.hit = False
                self.frame_index = 0
    def change_action(self, new_action):
        if self.action != new_action: 
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def attack(self,target): # returns true if attack collides with target
        attack_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.facing_left), self.rect.y, 2 * self.rect.width,self.rect.height)
        if attack_rect.colliderect(target.rect):
            if not target.blocking:
                target.health -= 10
                target.hit = True
            return True
        return False
    def draw(self,surface):
        #pygame.draw.rect(surface, 'Red', self.rect)
        # flips image if facing left
        img = pygame.transform.flip(self.image,self.`facing_left`,False)
        surface.blit(img,(self.rect.x - (self.offset[0] * self.img_scale),self.rect.y - (self.offset[1] * self.img_scale)))

        if self.projectile:
            proj_img = self.projectile_list[self.projectile_index]
            if self.proj_left == -1:
                proj_img = pygame.transform.flip(proj_img,True,False)
            surface.blit(proj_img,(self.proj_rect.x,self.proj_rect.y))
            
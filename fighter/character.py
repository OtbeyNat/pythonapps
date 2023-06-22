import pygame

class Character():
    def __init__(self,x,y,pnum,width,height) -> None:
        self.rect = pygame.Rect((x,y,80,180))
        self.pnum = pnum
        self.screen_width = width
        self.screen_height = height
        self.vel_y = 0
        self.jumped = False
        self.facing_left = 1
        self.attack_num = 0
        self.attacking = False
        self.health = 100
        self.max_hp = 100
        # self.mid_air = False

    def move(self,surface,target):
        speed = 10
        dx = 0
        dy = 0
        gravity = 2

        key = pygame.key.get_pressed()
        # movement
        if self.pnum == 1: # player 1 keys
            if key[pygame.K_a]: 
                dx = -speed
                self.facing_left = 1
            if key[pygame.K_d]: 
                dx = speed
                self.facing_left = 0
            if key[pygame.K_w] and not self.jumped: 
                dy = -30
                self.jumped = True

            # attack
            if (key[pygame.K_r] or key[pygame.K_t]) and not self.attacking:
                if key[pygame.K_r]: self.attack_num = 1
                else: self.attack_num = 2
                self.attack(surface,target)

        if self.pnum == 2: # player 2 keys
            if key[pygame.K_LEFT]: 
                dx = -speed
                self.facing_left = 1
            if key[pygame.K_RIGHT]: 
                dx = speed
                self.facing_left = 0
            if key[pygame.K_UP] and not self.jumped: 
                dy = -30
                self.jumped = True
        
        # set dx,dy
        # gravity
        self.vel_y += gravity
        dy += self.vel_y

        # stay on screen
        if self.rect.left + dx < 0: dx = -self.rect.left
        if self.rect.right + dx > self.screen_width: dx = self.screen_width - self.rect.right
        if self.rect.bottom + dy > self.screen_height - 110:
            self.vel_y = 0
            dy = self.screen_height - 110 - self.rect.bottom
            self.jumped = False

        # update rect
        self.rect.x += dx
        self.rect.y += dy
        
    def attack(self,surface,target):
        self.attacking = True
        attack_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.facing_left), self.rect.y, 2 * self.rect.width,self.rect.height)
        if attack_rect.colliderect(target.rect):
            target.health -= 10
        
        # pygame.draw.rect(surface,'Green', attack_rect)

    def draw(self,surface):
        pygame.draw.rect(surface, 'Red', self.rect)
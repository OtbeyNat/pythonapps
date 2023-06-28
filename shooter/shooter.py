import pygame

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()
fps = 60

BG = (144,201,120)
moving_left = False
moving_right = False

class Soldier(pygame.sprite.Sprite):
    def __init__(self,type,x,y,scale,speed):
        pygame.sprite.Sprite.__init__(self)

        self.char_type = type
        self.animation_list = []
        self.index = 0
        img = pygame.image.load(f'img/{self.char_type}/Idle/0.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale),int(img.get_height() * scale)))
        self.rect = self.image.get_rect(center = (x,y))
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.gravity = 2
        self.facing_left = 0

    def move(self,moving_left,moving_right):
        dx = 0
        dy = 0
        
        if moving_left:
            dx = -self.speed
            self.facing_left = 1
        if moving_right: 
            dx = self.speed
            self.facing_left = 0

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.facing_left,False),self.rect)

def draw_bg():
    screen.fill(BG)

player = Soldier("player",200,200,3,5)

run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
    
    draw_bg()

    player.move(moving_left,moving_right)
    player.draw()

    pygame.display.update()
    
pygame.quit()
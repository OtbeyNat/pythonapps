import pygame
from character import Character

pygame.init()

SCREEN_WIDTH,SCREEN_HEIGHT = 1000,600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("2D Fighter")
clock = pygame.time.Clock()
fps = 60

background = pygame.image.load('assets/images/background/background.jpg').convert_alpha()
background = pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))

#spritesheets
warrior_sheet = pygame.image.load('assets/images/warrior/Sprites/warrior.png').convert_alpha()
wizard_sheet = pygame.image.load('assets/images/wizard/Sprites/wizard.png').convert_alpha()
victory = pygame.image.load('assets/images/icons/victory.png').convert_alpha()

#num frames in animation
WARRIOR_FRAMES_ANIMATION = [10,8,1,7,7,3,7]
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72,56]
warrior_data = [WARRIOR_SIZE,WARRIOR_SCALE,WARRIOR_OFFSET]

WIZARD_FRAMES_ANIMATION = [8,8,1,8,8,3,7]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112,107]
wizard_data = [WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]

# pygame.mixer.music.load("assets/audio/music.mp3")
# pygame.mixer.music.set_volume(0.1)
# pygame.mixer.music.play(-1,0.0,3000)
sword = pygame.mixer.Sound("assets/audio/sword.wav")
sword.set_volume(0.3)
magic = pygame.mixer.Sound("assets/audio/magic.wav")
magic.set_volume(0.4)
red_proj = pygame.image.load("assets/images/projectiles/red.png")
blue_proj = pygame.image.load("assets/images/projectiles/blue.png")

def draw_bg():
    screen.blit(background,(0,0))

def draw_hp(hp,max_hp,x,y):
    percent_hp = hp / max_hp
    pygame.draw.rect(screen,'White',(x-2,y-2,404,34))
    pygame.draw.rect(screen,'Red',(x,y,400,30))
    pygame.draw.rect(screen,'Yellow',(x,y,400*percent_hp,30))

player1 = Character(200,310,1,SCREEN_WIDTH,SCREEN_HEIGHT,warrior_data,warrior_sheet,WARRIOR_FRAMES_ANIMATION,sword,blue_proj)
player2 = Character(700,310,2,SCREEN_WIDTH,SCREEN_HEIGHT,wizard_data,wizard_sheet,WIZARD_FRAMES_ANIMATION,magic,red_proj)

countdown = 3
countdown_time = pygame.time.get_ticks()
countdown_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

scores = [0,0]
round_over = False
round_over_cd = 5000

def draw_text(text,font,color,x,y):
    img = font.render(text,True,color)
    screen.blit(img,(x,y))

run = True
while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    draw_bg()
    draw_hp(player1.health,player1.max_hp,20,20)
    draw_hp(player2.health,player2.max_hp,580,20)
    draw_text("P1: "+str(scores[0]),score_font,'RED',20,60)
    draw_text("P2: "+str(scores[1]),score_font,'RED',925,60)

    if countdown <= 0:
        player1.move()
        player2.move()
    else:
        draw_text(str(countdown),countdown_font,'RED',SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        if pygame.time.get_ticks() - countdown_time >= 1000:
            countdown -= 1
            countdown_time = pygame.time.get_ticks()
    
    player1.update(player2)
    player2.update(player1)
    player1.draw(screen)
    player2.draw(screen)

    if player1.projectile and player2.projectile:
        # 2 projectiles at each other cancel out
        if player1.proj_rect.colliderect(player2.proj_rect) or player2.proj_rect.colliderect(player1.proj_rect):
            player1.projectile = False
            player2.projectile = False
    if player1.projectile:
        if player1.proj_rect.colliderect(player2.rect):
            player2.hit = True
            player2.health -= 10
            player1.projectile = False
    if player2.projectile:
        if player2.proj_rect.colliderect(player1.rect):
            player1.hit = True
            player1.health -= 10
            player2.projectile = False

    if not round_over:
        if not player1.alive:
            scores[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        if not player2.alive:
            scores[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        if not player1.alive: screen.blit(victory,(640,75))
        else:  screen.blit(victory,(80,75))
        if pygame.time.get_ticks() - round_over_time > round_over_cd:
            round_over = False
            countdown = 3
            player1.animation_frames.pop()
            player2.animation_frames.pop()
            player1 = Character(200,310,1,SCREEN_WIDTH,SCREEN_HEIGHT,warrior_data,warrior_sheet,WARRIOR_FRAMES_ANIMATION,sword,blue_proj)
            player2 = Character(700,310,2,SCREEN_WIDTH,SCREEN_HEIGHT,wizard_data,wizard_sheet,WIZARD_FRAMES_ANIMATION,magic,red_proj)

    pygame.display.update()
    
pygame.quit()
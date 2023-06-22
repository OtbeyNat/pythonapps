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

def draw_bg():
    screen.blit(background,(0,0))

def draw_hp(hp,max_hp,x,y):
    percent_hp = hp / max_hp
    pygame.draw.rect(screen,'White',(x-2,y-2,404,34))
    pygame.draw.rect(screen,'Red',(x,y,400,30))
    pygame.draw.rect(screen,'Yellow',(x,y,400*percent_hp,30))

player1 = Character(200,310,1,SCREEN_WIDTH,SCREEN_HEIGHT)
player2 = Character(700,310,2,SCREEN_WIDTH,SCREEN_HEIGHT)

run = True
while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    draw_bg()
    draw_hp(player1.health,player1.max_hp,20,20)
    draw_hp(player2.health,player2.max_hp,580,20)

    player1.draw(screen)
    player2.draw(screen)
    player1.move(screen,player2)
    player2.move(screen,player1)

    pygame.display.update()
    
pygame.quit()
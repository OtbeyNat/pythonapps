import pygame
import time
import random

# window size
window_x = 500
window_y = 500

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255,255,0)
color_light = pygame.Color(170,170,170)
color_dark = pygame.Color(100,100,100)
b_width,b_height = 80,40

pygame.init()
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((window_x,window_y))
img = pygame.image.load('python_icon.png')
pygame.display.set_icon(img)

fps = pygame.time.Clock()

snake_speed = 15
start_speed = 15
increment = 0

score = 0
snake_position = [100,50]
snake_body = [ [100,50], [90,50], [80,50], [70,50] ]
direction = 'RIGHT'
change_to = direction

fruit_position = [random.randrange(10, ((window_x-10)//10)) * 10,
                  random.randrange(20, ((window_y-10)//10)) * 10]
fruit_spawn = True
gold_spawn = False
gold_despawn_time = 0
gold_position = [-1,-1]
despawn_time = 5
tens = 0 # increment every 10 seconds for amount of time elasped

high_score = 0

red_snake_position = [400,450]
red_snake_body = [ [400,450], [410,450], [420,450], [430,450] ]
red_direction = 'LEFT'
red_change_to = direction
red_score = 0
multiplayer = False

def select_difficulty(mp):
    
    title_font = pygame.font.SysFont('times new roman', 50)
    level_font = pygame.font.SysFont('times new roman', 17)
    dim_e = [(window_x/5)-40,3*window_y/4]
    dim_n = [2*(window_x/5)-40,3*window_y/4]
    dim_h = [3*(window_x/5)-40,3*window_y/4]
    dim_i = [4*(window_x/5)-40,3*window_y/4]
    dim_2p = [(window_x/2)-40,2*(window_y/3)-20]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    #quit()
                    return None
        
        game_window.fill(black)
        title_surface = title_font.render('SNAKE GAME', True, green)
        title_rect = title_surface.get_rect()
        title_rect.midtop = (window_x/2,window_y/4)
        game_window.blit(title_surface, title_rect)
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button = 0

        if mp:
            pygame.draw.rect(game_window,color_light,[dim_2p[0],dim_2p[1],b_width,b_height])
        else:
            pygame.draw.rect(game_window,color_dark,[dim_2p[0],dim_2p[1],b_width,b_height])

        if dim_2p[0]+b_width > mouse[0] > dim_2p[0] and dim_2p[1]+b_height > mouse[1] > dim_2p[1]:
            button = -1
        if dim_e[0]+b_width > mouse[0] > dim_e[0] and dim_e[1]+b_height > mouse[1] > dim_e[1]:
            pygame.draw.rect(game_window,color_light,[dim_e[0],dim_e[1],b_width,b_height])
            button = 1
        else:
            pygame.draw.rect(game_window,color_dark,[dim_e[0],dim_e[1],b_width,b_height])
        
        if dim_n[0]+b_width > mouse[0] > dim_n[0] and dim_n[1]+b_height > mouse[1] > dim_n[1]:
            pygame.draw.rect(game_window,color_light,[dim_n[0],dim_n[1],b_width,b_height])
            button = 2
        else:
            pygame.draw.rect(game_window,color_dark,[dim_n[0],dim_n[1],b_width,b_height])
        
        if dim_h[0]+b_width > mouse[0] > dim_h[0] and dim_h[1]+b_height > mouse[1] > dim_h[1]:
            pygame.draw.rect(game_window,color_light,[dim_h[0],dim_h[1],b_width,b_height])
            button = 3
        else:
            pygame.draw.rect(game_window,color_dark,[dim_h[0],dim_h[1],b_width,b_height])
        
        if dim_i[0]+b_width > mouse[0] > dim_i[0] and dim_i[1]+b_height > mouse[1] > dim_i[1]:
            pygame.draw.rect(game_window,color_light,[dim_i[0],dim_i[1],b_width,b_height])
            button = 4    
        else:
            pygame.draw.rect(game_window,color_dark,[dim_i[0],dim_i[1],b_width,b_height])
    
        easy = level_font.render('EASY',True,white)
        easy_rect = easy.get_rect()
        easy_rect.center = (dim_e[0]+(b_width/2),dim_e[1]+(b_height/2))
        normal = level_font.render('NORMAL',True,white)
        normal_rect = normal.get_rect()
        normal_rect.center = (dim_n[0]+(b_width/2),dim_n[1]+(b_height/2))
        hard = level_font.render('HARD',True,white)
        hard_rect = hard.get_rect()
        hard_rect.center = (dim_h[0]+(b_width/2),dim_h[1]+(b_height/2))
        insane = level_font.render('INSANE',True,white)
        insane_rect = insane.get_rect()
        insane_rect.center = (dim_i[0]+(b_width/2),dim_i[1]+(b_height/2))
        multi = level_font.render('1 VS 1',True,white)
        multi_rect = insane.get_rect()
        multi_rect.center = (dim_2p[0]+(b_width/2)+7,dim_2p[1]+(b_height/2))

        game_window.blit(easy,easy_rect)
        game_window.blit(normal,normal_rect)
        game_window.blit(hard,hard_rect)
        game_window.blit(insane,insane_rect)
        game_window.blit(multi,multi_rect)
        res = None
        if click[0] == 1:
            match button:
                case -1: # toggle single/multiplayer
                    if mp:
                        mp = False
                    else:
                        mp = True
                case 1:
                    res = [15,0,0]
                case 2:
                    res = [15,0.5,5]
                case 3:
                    res = [15,1,3]
                case 4:
                    res = [20,1.5,1.5]
        if res != None:
            res.append(mp)
            return res
        pygame.display.update()
        fps.tick(snake_speed)

def show_time(start,current,mp):
    elapsed = int(current - start)
    minutes = int(elapsed // 60)
    seconds = elapsed % 60
    minutes = str(minutes).zfill(2)
    seconds = str(seconds).zfill(2)
    time_font = pygame.font.SysFont('times new roman',20)
    time_surface = time_font.render(minutes+ ':' + seconds, True, white)
    time_rect = time_surface.get_rect()
    if mp:
        time_rect.center = (window_x/2,10)
    game_window.blit(time_surface, time_rect)

def show_score(mp):
    score_font = pygame.font.SysFont('times new roman',20)
    
    if not mp:
        score_surface = score_font.render('Score :' + str(score), True, white)
        score_rect = score_surface.get_rect()
        score_rect.center = (window_x/2,10)
    else:
        score_surface = score_font.render('Score :' + str(score), True, green)
        score_rect = score_surface.get_rect()
        red_score_surface = score_font.render('Score :' + str(red_score), True, red)
        red_score_rect = score_surface.get_rect()
        red_score_rect.center = (410,10)
        game_window.blit(red_score_surface, red_score_rect)
    game_window.blit(score_surface, score_rect)
    
def show_high_score():
    high_score_font = pygame.font.SysFont('times new roman',20)

    high_score_surface = high_score_font.render('High Score :' + str(high_score), True, white)

    high_score_rect = high_score_surface.get_rect()

    high_score_rect.center = (410,10)

    game_window.blit(high_score_surface, high_score_rect)

def game_over(end,mp,winner):
    width,height = 100,50 #for difficulty button
    game_window.fill(black)
    
    show_time(start_time,end,mp)
    # creating font object my_font
    if mp:
        result_font = pygame.font.SysFont('times new roman', 50)
        match winner:
            case 0:
                result_surface = result_font.render('TIE',True,white)
            case 1:
                result_surface = result_font.render('GREEN WINS',True,green)
            case 2:
                result_surface = result_font.render('RED WINS',True,red)
        result_rect = result_surface.get_rect()
        result_rect.midtop = (window_x/2,window_y/4)

        score_font = pygame.font.SysFont('times new roman', 50)
        score_surface = score_font.render(str(score), True, green)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (window_x/2 - 50,window_y/4 + 50)

        red_score_surface = score_font.render(str(red_score), True, red)
        red_score_rect = red_score_surface.get_rect()
        red_score_rect.midtop = (window_x/2 + 50,window_y/4 + 50)
        game_window.blit(score_surface, score_rect)
        game_window.blit(red_score_surface, red_score_rect)

        game_window.blit(result_surface, result_rect)

    else:
        show_high_score()
        my_font = pygame.font.SysFont('times new roman', 50)
        # creating a text surface on which text will be drawn
        game_over_surface = my_font.render('FINAL SCORE', True, red)
        # create a rectangular object for the text surface object
        game_over_rect = game_over_surface.get_rect()
        # setting position of the text
        game_over_rect.midtop = (window_x/2,window_y/4)
        # blit will draw the text on screen
        game_window.blit(game_over_surface, game_over_rect)
        
        score_font = pygame.font.SysFont('times new roman', 50)
        score_surface = score_font.render(str(score), True, red)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (window_x/2,window_y/4 + 50)
        game_window.blit(score_surface, score_rect)

    my_font = pygame.font.SysFont('times new roman', 30)   
    # creating a text surface on which text will be drawn
    game_over_surface = my_font.render('[ENTER] Restart / [ESC] Quit ', True, white)
    # create a rectangular object for the text surface object
    game_over_rect = game_over_surface.get_rect()
    # setting position of the text
    game_over_rect.midtop = (window_x/2,3*window_y/4)
    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.update()

    while True:
        button = 0
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        dim = [(window_x/2),2*(window_y/3)]
        if dim[0]+width > mouse[0] > dim[0] and dim[1]+height > mouse[1] > dim[1]:
            pygame.draw.rect(game_window,color_light,[dim[0]-(width/2),dim[1]-(height/2),width,height])
            button = 1
        else:
            pygame.draw.rect(game_window,color_dark,[dim[0]-(width/2),dim[1]-(height/2),width,height])

        if click[0] == 1 and button == 1:
            return select_difficulty(mp)
        level_font = pygame.font.SysFont('times new roman', 16)
        level = level_font.render('DIFFICULTY',True,white)
        level_rect = level.get_rect()
        level_rect.center = (dim[0],dim[1])
        game_window.blit(level,level_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return [start_speed,increment,despawn_time,mp]
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    #quit()
                    return None

diff = select_difficulty(multiplayer)
if diff != None:
    start_time = time.time()
    start_speed = diff[0]
    increment = diff[1]
    despawn_time = diff[2]
    multiplayer = diff[3]
    snake_speed = start_speed

game_quit = False
# game running
while diff != None:
    #handling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            game_quit = True
            #quit()
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                change_to = 'UP'
            if event.key == pygame.K_s:
                change_to = 'DOWN'
            if event.key == pygame.K_a:
                change_to = 'LEFT'
            if event.key == pygame.K_d:
                change_to = 'RIGHT'
            if multiplayer:
                if event.key == pygame.K_UP:
                    red_change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    red_change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    red_change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    red_change_to = 'RIGHT'
                
    if game_quit:
        break
    
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    #top-left = [0,0]
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    snake_body.insert(0,list(snake_position))
    # check if snake head position is same as the fruit position
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        snake_speed += increment
        fruit_spawn = False
        #snake body grows tail end stays
    elif snake_position[0] == gold_position[0] and snake_position[1] == gold_position[1]:
        gold_spawn = False
        gold_position = [-1,-1]
        score += 50
        snake_speed += increment
    else:
        snake_body.pop() #remove tail end of snake body since it did not grow

    if multiplayer:
        if red_change_to == 'UP' and red_direction != 'DOWN':
            red_direction = 'UP'
        if red_change_to == 'DOWN' and red_direction != 'UP':
            red_direction = 'DOWN'
        if red_change_to == 'LEFT' and red_direction != 'RIGHT':
            red_direction = 'LEFT'
        if red_change_to == 'RIGHT' and red_direction != 'LEFT':
            red_direction = 'RIGHT'

        if red_direction == 'UP':
            red_snake_position[1] -= 10
        if red_direction == 'DOWN':
            red_snake_position[1] += 10
        if red_direction == 'LEFT':
            red_snake_position[0] -= 10
        if red_direction == 'RIGHT':
            red_snake_position[0] += 10
        red_snake_body.insert(0,list(red_snake_position))
    
        if fruit_spawn and red_snake_position[0] == fruit_position[0] and red_snake_position[1] == fruit_position[1]:
            red_score += 10
            snake_speed += increment
            fruit_spawn = False
        elif gold_spawn and red_snake_position[0] == gold_position[0] and red_snake_position[1] == gold_position[1]:
            gold_spawn = False
            gold_position = [-1,-1]
            red_score += 50
            snake_speed += increment
        else:
            red_snake_body.pop() #remove tail end of snake body since it did not grow

    if not fruit_spawn:
        fruit_position = [random.randrange(10, ((window_x-10)//10)) * 10,
                          random.randrange(20, ((window_y-10)//10)) * 10]         
    fruit_spawn = True 

    duration = int(time.time() - start_time)
    if duration % 10 == 0 and duration != tens:
        tens = duration
        rand = True
    else:
        rand = False
    if not gold_spawn and rand: #every 10 seconds chance for gold
        chance = random.randint(1,100)
        if 20 <= chance <= 40:
            gold_spawn = True
            if despawn_time != 0:
                gold_despawn_time = time.time() + despawn_time
            else:
                gold_despawn_time = 0
            gold_position = [random.randrange(10, ((window_x-10)//10)) * 10,
                            random.randrange(20, ((window_y-10)//10)) * 10]
        first = False
    else:
        if gold_despawn_time != 0 and time.time() >= gold_despawn_time:
            pygame.draw.rect(game_window, black, pygame.Rect(gold_position[0],gold_position[1],10,10))  
            gold_spawn = False
            gold_position = [-1,-1]
            first = True

    if game_window != None:
        #fill entire window black
        game_window.fill(black)

        # draw each part of snake
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        if multiplayer:
            for pos in red_snake_body:
                pygame.draw.rect(game_window, red, pygame.Rect(pos[0], pos[1], 10, 10))

        # draw fruit square
        pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        if gold_spawn:
            pygame.draw.rect(game_window, yellow, pygame.Rect(gold_position[0],gold_position[1],10,10))
        
    # Game Over conditions
    res = None
    gameOver = False
    # out of bounds
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        res = game_over(time.time(),multiplayer,2)
        gameOver = True
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        res = game_over(time.time(),multiplayer,2)
        gameOver = True
     
    # touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            res = game_over(time.time(),multiplayer,2)
            gameOver = True

    if multiplayer:
        #tie; head to head collision
        if red_snake_position[0] == snake_position[0] and red_snake_position[1] == snake_position[1]:
            res = game_over(time.time(),multiplayer,0)
            gameOver = True

        if red_snake_position[0] < 0 or red_snake_position[0] > window_x-10:
            res = game_over(time.time(),multiplayer,1)
            gameOver = True
        if red_snake_position[1] < 0 or red_snake_position[1] > window_y-10:
            res = game_over(time.time(),multiplayer,1)
            gameOver = True
     
        for block in red_snake_body[1:]:
            if red_snake_position[0] == block[0] and red_snake_position[1] == block[1]:
                res = game_over(time.time(),multiplayer,1)
                gameOver = True
        
        #red snake hits green body
        for block in snake_body[1:]:
            if red_snake_position[0] == block[0] and red_snake_position[1] == block[1]:
                res = game_over(time.time(),multiplayer,1)
                gameOver = True
        #green snake hits red body
        for block in red_snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                res = game_over(time.time(),multiplayer,2)
                gameOver = True

    if gameOver and res == None:
        break
    if res != None:
        start_speed = res[0]
        increment = res[1]
        despawn_time = res[2]
        multiplayer = res[3]
        snake_speed = start_speed
        snake_position = [100,50]
        snake_body = [ [100,50], [90,50], [80,50], [70,50] ]
        direction = 'RIGHT'
        change_to = direction
        score = 0

        fruit_position = [random.randrange(10, ((window_x-10)//10)) * 10,
                        random.randrange(20, ((window_y-10)//10)) * 10]
        fruit_spawn = True
        
        if multiplayer:
            red_snake_position = [400,450]
            red_snake_body = [ [400,450], [410,450], [420,450], [430,450] ]
            red_direction = 'LEFT'
            red_change_to = direction
            red_score = 0
        
        start_time = time.time()

    # displaying score continuously
    show_score(multiplayer)
    if score > high_score:
        high_score = score
    if not multiplayer:
        show_high_score() 
    show_time(start_time,time.time(),multiplayer)
    # Refresh game screen
    pygame.display.update()
    # Frame Per Second /Refresh Rate
    fps.tick(min(snake_speed,60))

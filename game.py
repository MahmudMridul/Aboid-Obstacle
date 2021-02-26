import pygame
import sys
import random

pygame.init() # must initialize pygame

WIDTH = 800
HEIGHT = 600
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (167,214,255)
player_size = 50
player_pos = [WIDTH/2,HEIGHT-(2*player_size)]
enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size),0]
enemy_list = [enemy_pos]
SPEED = 20
SCORE = 0

def set_level(score,SPEED):
    if score<100:
        SPEED = 10
    elif score<500:
        SPEED = 15
    elif score<1000:
        SPEED = 20
    elif score<1500:
        SPEED = 25
    elif score<2000:
        SPEED = 30
    elif score<2500:
        SPEED = 35
    elif score<3000:
        SPEED = 50
    return SPEED
def drop_enemies(enemy_list):
    delay = random.random()
    if(len(enemy_list)<10) and delay<0.3:
        e_left = random.randint(0,WIDTH-enemy_size)
        e_top = 0
        enemy_list.append([e_left,e_top])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemyPosition(enemy_list,SCORE):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1]>=0 and enemy_pos[1]<HEIGHT:
            enemy_pos[1]+=SPEED
        else:
            enemy_list.pop(idx)
            SCORE+=5
    return SCORE

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if(detect_collision(player_pos,enemy_pos)):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_left = player_pos[0]
    p_top = player_pos[1]
    e_left = enemy_pos[0]
    e_top = enemy_pos[1]

    if (e_left>= p_left and e_left < (p_left+player_size)) or (p_left>=e_left and p_left<(e_left+enemy_size)):
        if(e_top>=p_top and e_top<(p_top+player_size)) or (p_top>=e_top and p_top<(e_top+enemy_size)):
            return True
    return False

screen = pygame.display.set_mode((WIDTH,HEIGHT)) # setting screen size

game_over = False
clock = pygame.time.Clock() # to set fps
font = pygame.font.SysFont('arial',35)
while True:
    for event in pygame.event.get(): #gets all the events in pygame, tracks every event in the screen
        #print(event)
        if event.type==pygame.QUIT: # if exit is clicked on the window, game will close
            sys.exit()
        if event.type==pygame.KEYDOWN: #if key is pressed
            left = player_pos[0]
            top = player_pos[1]
            if event.key==pygame.K_LEFT: # if left arrow key is pressed
               left-=player_size
            elif event.key==pygame.K_RIGHT:
               left+=player_size
            player_pos = [left,top]
    screen.fill(BLACK)  # fills black, so that we can see change
    drop_enemies(enemy_list)
    if not game_over:
        SCORE = update_enemyPosition(enemy_list,SCORE)
    else:
        SCORE = SCORE
    SPEED = set_level(SCORE,SPEED)
    text = 'Score: '+ str(SCORE)
    label = font.render(text,1,BLUE)
    screen.blit(label,(WIDTH-200,HEIGHT-40)) #adding score to the screen
    if collision_check(enemy_list,player_pos):
        game_over = True
        #break
    if game_over:
        text = 'Game Over!'
        label = font.render(text, 1, BLUE)
        screen.blit(label, (300,0))
    draw_enemies(enemy_list)

    pygame.draw.rect(screen, BLUE, (player_pos[0],player_pos[1],player_size,player_size)) #draws rect, on screen, RGB color, (left,top,width,height)
    clock.tick(20) #setting frames per second
    pygame.display.update() #updates screen in each iteration
import random
import pygame
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

# variable
screen = width, heigth = 1000, 800

BLACK = 0, 0, 0
WHITE = 255, 255, 255
YELLOW = 255, 234, 0
BLUE = 0, 0, 255
RED = 255, 0 , 0
GREEN = 124, 252, 0

main_surface = pygame.display.set_mode(screen)

IMGS_PATH = 'goose'

player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in os.listdir(IMGS_PATH)]
player = player_imgs[0]
player_rect = player.get_rect()
player_speed = 10

# enemy
def create_enemy():
    # enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (100, 50))
    enemy_rect = pygame.Rect(width, random.randint(0, heigth), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)    

enemies = []    

# bonus
def create_bonus():
    # bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (100, 100))
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonus_speed = random.randint(2, 5)
    return [bonus, bonus_rect, bonus_speed]

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)    

bonuses = [] 

CREATE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CREATE_IMG, 125) 

img_index = 0
scores = 0
font = pygame.font.SysFont('Verdana', 20)

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
           is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CREATE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]  
            

    pressed_keys = pygame.key.get_pressed()
    
    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()    

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(player, player_rect)

    main_surface.blit(font.render(str(scores), True, BLACK), (width - 30, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0) 
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
           is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2]) 
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= heigth:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))    
            scores += 1   

    if pressed_keys[K_DOWN] and not player_rect.bottom >= heigth:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_UP] and not player_rect.top >= heigth:
        player_rect = player_rect.move(0, -player_speed)    

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)   

    if pressed_keys[K_LEFT] and not player_rect.left >= width:
        player_rect = player_rect.move(-player_speed, 0)    
       
    # print(len(enemies))   

    pygame.display.flip()


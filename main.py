import pygame
import random
from os import listdir
from pygame. constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 800, 600

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

font = pygame.font.SysFont('Verdana', 20)

ANIMATION_PATH = 'animation'

main_surface = pygame.display.set_mode(screen)

player_animation = [pygame.image.load(ANIMATION_PATH + '/' + file).convert_alpha() for file in listdir(ANIMATION_PATH)]
player = player_animation[0]
player_rect = player.get_rect()
player_speed = 5

def create_enemy():
    enemy = pygame.image.load('enemy.png')
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    bonus = pygame.image.load('bonus.png')
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonus_speed = random.randint(1, 6)
    return [bonus, bonus_rect, bonus_speed]

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bg_start_position = 0
bg_moves = bg.get_width()
bg_speed = 3

CREATE_ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY_EVENT, 1500)

CREATE_BONUS_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS_EVENT, 2000)

CREATE_ANIMATION = pygame.USEREVENT + 3
pygame.time.set_timer(CREATE_ANIMATION, 175)

scores = 0
img_index = 0

enemies = []
bonuses = []

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY_EVENT:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS_EVENT:
            bonuses.append(create_bonus())

        if event.type == CREATE_ANIMATION:
            img_index += 1
            if img_index == len(player_animation):
                img_index = 0
            player = player_animation[img_index]
            

    pressed_key = pygame.key.get_pressed()

    # main_surface.blit(bg, (0, 0))

    bg_start_position -= bg_speed
    bg_moves -= bg_speed

    if bg_start_position < -bg.get_width():
        bg_start_position = bg.get_width()

    if bg_moves < -bg.get_width():
        bg_moves = bg.get_width()

    main_surface.blit(bg, (bg_start_position, 0))
    main_surface.blit(bg, (bg_moves, 0))

    
    main_surface.blit(player, player_rect)

    main_surface.blit(font.render(str(scores), True, BLUE), (width - 30, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            scores = 0
            is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom > height:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressed_key[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)

    if pressed_key[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_key[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)

    if pressed_key[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)
    
    pygame.display.flip()
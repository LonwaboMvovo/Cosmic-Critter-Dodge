import pygame
from sys import exit
from random import randint


def display_score(start_time):
    current_time = (pygame.time.get_ticks() - start_time) // 100
    score_surf = pixel_type_font.render(f"{current_time}", False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)

    return current_time


def obstacle_movement(obstacle_rect_list):
    if obstacle_rect_list:
        for obstacle_rect in obstacle_rect_list:
            obstacle_rect.x -= 5

            screen.blit(snail_surf, obstacle_rect)

    return obstacle_rect_list


pygame.init()
# beninging - starting variables
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Game boi!")
clock = pygame.time.Clock()
pixel_type_font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = False
start_time = 0

# Surfaces:
sky_surf = pygame.image.load("graphics/Sky.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()

obstacle_rect_list = []
# text_surf = pixel_type_font.render("My game lmao xd ^.^", False, "Black")

# Obstacles:
snail_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (650, 300))

player_surf = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
# my new favourite method name
player_rect = player_surf.get_rect(midbottom = (69, 300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

title = pixel_type_font.render("Cosmic Critter Dodge", False, (111,196,169))
title_rect = title.get_rect(center = (400, 50))

instructions = pixel_type_font.render("PRESS SPACE TO PLAY!", False, (111,196,169))
instructions_rect = instructions.get_rect(center = (400, 350))

# Timer:
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# score_surf = pixel_type_font.render(f"My game lmao xd ^.^ Score: {player_score}", False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400, 50))

player_score = 0

while True:
    # checking for all the types of player input is called an event loop
    # event_list = pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                # player_rect.y -= 150
                player_gravity = -20
                # print("I crouch")
            elif event.type == pygame.MOUSEBUTTONDOWN and player_rect.collidepoint(event.pos) and player_rect.bottom >= 300 and pygame.mouse.get_pressed()[0]:
                player_gravity = -20

            if event.type == obstacle_timer:
                obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # print("hello")
                game_active = True
                start_time = pygame.time.get_ticks()

            # print("Key down bad")
    if game_active:
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_SPACE:
                # print("I yump")
            # print("Key uptown funk")

        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):
        #         print("ouch you collide wif me!")

        # if event.type == pygame.MOUSEBUTTONUP:
        #     print("Mouse down with it")
    
        # draw and update all our elements in here
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        # screen.blit(text_surf, (250, 50))
        # pygame.draw.rect(screen, "#c0e8ec", score_rect)
        # pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        # pygame.draw.ellipse(screen, "Brown", pygame.Rect(50, 200, 100, 100))
        # screen.blit(score_surf, score_rect)
        display_score(start_time)

        # pygame.draw.line(screen, "Red", (0,0), pygame.mouse.get_pos(), 10)
        # pygame.draw.line(screen, "Red", (0, 400), (800,0), 20)

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print("yump")

        # if player_rect.right > 900:
        #     player_rect.right = 0
        # else:
        #     player_rect.x += 1
        
        # Player:
        player_rect.y += (player_gravity)

        if player_rect.bottom >= 300:
            player_rect.bottom = 300
            # player_gravity = 0
        else:
            player_gravity += 1
        screen.blit(player_surf, player_rect)

        # Obstacle movements
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        if snail_rect.left > -100:
            snail_rect.x -= 6.28
        else:
            snail_rect.left = 800
        screen.blit(snail_surf, snail_rect)
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title, title_rect)
        screen.blit(instructions, instructions_rect)
        # display_score(start_time)
    # if player_rect.colliderect(snail_rect):
    #     print("ouch")

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     # print("ayo wtf")
    #     print(pygame.mouse.get_pressed())

    # Collision
    if player_rect.colliderect(snail_rect):
        # print("Game Over dud!!"
        player_score = (pygame.time.get_ticks() - start_time) // 100
        instructions = pixel_type_font.render(f"Score: {player_score}", False, (111,196,169))
        instructions_rect = instructions.get_rect(center = (400, 350))

        snail_rect.right = 650
        game_active = False
        # pygame.quit()
        # quit()

    pygame.display.update()
    clock.tick(60)
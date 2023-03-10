import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walk[int(self.player_index)]
        self.rect = self.image.get_rect(midbottom = (169, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.wav")
        self.jump_sound.set_volume(0.05)
    

    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20
            self.jump_sound.play()


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0


    def animation_state(self):
        if self.rect.bottom == 300:
            self.player_index = self.player_index + 0.1

            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
        else:
            self.image = self.player_jump


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "snail":
            obstacle_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            obstacle_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [obstacle_frame_1, obstacle_frame_2]
            y_pos = 300
        else:
            fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 200
        
        self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))


    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0

        self.image = self.frames[int(self.animation_index)]


    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()


def display_score(start_time):
    current_time = (pygame.time.get_ticks() - start_time) // 100
    score_surf = pixel_type_font.render(f"{current_time}", False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)

    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True


pygame.init()
# beninging - starting variables
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Game boi!")
clock = pygame.time.Clock()
pixel_type_font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = False
start_time = 0

bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.set_volume(0.05)
bg_music.play(loops = -1)

# Surfaces:
sky_surf = pygame.image.load("graphics/Sky.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()


# Intro screen
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

title = pixel_type_font.render("Cosmic Critter Dodge", False, (111,196,169))
title_rect = title.get_rect(center = (400, 50))

instructions = pixel_type_font.render("PRESS SPACE TO PLAY!", False, (111,196,169))
instructions_rect = instructions.get_rect(center = (400, 350))

# Timers:
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

player_score = 0

# Groups:
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

while True:
    # checking for all the types of player input is called an event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail"])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        display_score(start_time)

        # New with class
        player.draw(screen)
        player.update() 

        obstacle_group.draw(screen)
        obstacle_group.update()
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title, title_rect)
        screen.blit(instructions, instructions_rect)

    if not collision_sprite():
        player_score = (pygame.time.get_ticks() - start_time) // 100
        instructions = pixel_type_font.render(f"Score: {player_score}", False, (111,196,169))
        instructions_rect = instructions.get_rect(center = (400, 350))
        game_active = False

    pygame.display.update()
    clock.tick(60)

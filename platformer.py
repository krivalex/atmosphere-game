import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((800, 416))
pygame.display.set_caption("Runner")
icon = pygame.image.load("images/server-icon.png").convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load("images/bg.png").convert_alpha()

walk_right = [
    pygame.image.load("images/player-right/right1.png"),
    pygame.image.load("images/player-right/right2.png"),
    pygame.image.load("images/player-right/right3.png"),
    pygame.image.load("images/player-right/right4.png"),
]

walk_left = [
    pygame.image.load("images/player-left/left1.png"),
    pygame.image.load("images/player-left/left2.png"),
    pygame.image.load("images/player-left/left3.png"),
    pygame.image.load("images/player-left/left4.png"),
]

running = True

player_animation_count = 0
bg_x = 0

bg_sound = pygame.mixer.Sound("sounds/music.mp3")
bg_sound.play(-1)

while running:
    
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x+800, 0))
    screen.blit(walk_right[player_animation_count], (100, 323))

    if player_animation_count == 3:
        player_animation_count = 0
    else:
        player_animation_count += 1

    bg_x -= 4
    if bg_x == -800:
        bg_x = 0

    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    
    clock.tick(10)

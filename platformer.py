# --------------------------
# НАЧАЛЬНАЯ ЧАСТЬ
# --------------------------

# импортируем библиотеку pygame
import pygame

# создаем игровой цикл
clock = pygame.time.Clock()

# инициализируем библиотеку pygame
pygame.init()

# задаем размеры окна
WIDTH = 800
HEIGHT = 416

# создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# задаем заголовок окна
pygame.display.set_caption("Atmosphere - Platformer")

# загружаем иконку
icon = pygame.image.load("images/server-icon.png").convert_alpha()

# устанавливаем иконку
pygame.display.set_icon(icon)

# загружаем фон
bg = pygame.image.load("images/bg.png").convert_alpha()

# загружаем анимацию персонажа (вправо)
walk_right = [
    pygame.image.load("images/player-right/right1.png").convert_alpha(),
    pygame.image.load("images/player-right/right2.png").convert_alpha(),
    pygame.image.load("images/player-right/right3.png").convert_alpha(),
    pygame.image.load("images/player-right/right4.png").convert_alpha(),
]

# загружаем анимацию персонажа (влево)
walk_left = [
    pygame.image.load("images/player-left/left1.png").convert_alpha(),
    pygame.image.load("images/player-left/left2.png").convert_alpha(),
    pygame.image.load("images/player-left/left3.png").convert_alpha(),
    pygame.image.load("images/player-left/left4.png").convert_alpha(),
]

# загружаем анимацию врага
enemy_move = [
    pygame.image.load("images/enemy/enemy1.png").convert_alpha(),
    pygame.image.load("images/enemy/enemy2.png").convert_alpha(),
    pygame.image.load("images/enemy/enemy3.png").convert_alpha(),
    pygame.image.load("images/enemy/enemy4.png").convert_alpha(),
    pygame.image.load("images/enemy/enemy5.png").convert_alpha(),
    pygame.image.load("images/enemy/enemy6.png").convert_alpha(),
]


# создаем переменную для игрового цикла
running = True

# создаем переменную для игрового процесса
gameplay = True

# создаем переменную для анимации персонажа
player_animation_count = 0
enemy_animation_count = 0

# создаем переменную для фона
bg_x = 0

# создаем переменную для скорости персонажа
player_speed = 5

# создаем переменную для направления персонажа
player_x = 100
player_y = 323

# создаем переменную для прыжка персонажа
is_jump = False
jump_count = 9

# создаем переменную для направления врага
enemy_x = 810
enemy_y = 300

label = pygame.font.Font("./fonts/bionicle.ttf", 50)
lose_label = label.render("YOU LOSE", False, (255, 255, 255))
restart_label = label.render("Play Again", False, (255, 255, 255))
restart_label_rect = restart_label.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))

# создаем переменную для таймера врага
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 4000)
enemy_list = []

# загружаем музыку
bg_sound = pygame.mixer.Sound("sounds/music.mp3")
# воспроизводим музыку
bg_sound.play(-1)

death_sound = pygame.mixer.Sound("sounds/death.mp3")

bullet = pygame.image.load("images/bullet.png").convert_alpha()
bullet_list = []
bullets_left = 10


# --------------------------
# ОСНОВНАЯ ЧАСТЬ
# --------------------------

# пока игра идет
while running:

    # пока игровой цикл идет
    if gameplay:
        
        # рисуем фон и персонажа и врага
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x+800, 0))
        
        # создаем прямоугольники для персонажа и врага
        player_rect = walk_left[player_animation_count].get_rect(topleft=(player_x, player_y))

        if enemy_list:
            for (i, el) in enumerate(enemy_list):
                screen.blit(enemy_move[enemy_animation_count], (el[0], el[1]))
                el[0] -= 10

            if el.x < -10:
                enemy_list.pop(i)

            # проверяем столкновение персонажа и врага
            if player_rect.colliderect(el):
                bg_sound.stop()
                gameplay = False

        # создаем событие для упрвеления персонажем
        keys = pygame.key.get_pressed()

        # анимации персонажа
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_animation_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_animation_count], (player_x, player_y))

        # движение персонажа
        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < 750:
            player_x += player_speed

        # прыжок персонажа
        if not(is_jump):
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -9:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                jump_count = 9
                is_jump = False
        

        # переключение анимации персонажа
        if player_animation_count == 3:
            player_animation_count = 0
        else:
            player_animation_count += 1

        # переключение анимации врага
        if enemy_animation_count == 5:
            enemy_animation_count = 0
        else:
            enemy_animation_count += 1

        # перемещение фона
        bg_x -= 4
        if bg_x == -800:
            bg_x = 0

        if bullet_list:
            for (index_bullet, value_bullet) in enumerate(bullet_list):
                screen.blit(bullet, (value_bullet.x, value_bullet.y))
                value_bullet.x += 10

                if value_bullet.x > 800:
                    bullet_list.pop(index_bullet)

                if enemy_list:
                    for (index_enemy, value_enemy) in enumerate(enemy_list):
                        if value_enemy.colliderect(value_bullet):
                            enemy_list.pop(index_enemy)
                            bullet_list.pop(index_enemy)
                            bullets_left += 1

    # если игра закончена
    else:
        death_sound.play()
        # рисуем фон
        screen.fill((87, 87, 87))
        # рисуем текст
        screen.blit(lose_label, (WIDTH//2.75, HEIGHT//2-50))
        # воспроизводим звук смерти
        screen.blit(restart_label, restart_label_rect)

        # проверяем нажатие кнопки мыши
        mouse = pygame.mouse.get_pos()
        # если нажали на кнопку
        if restart_label_rect.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                # перезапускаем игру
                gameplay = True
                screen.fill((0, 0, 0))
                player_x = 100
                enemy_list = []
                bullet_list = []
                death_sound.stop()
                bg_sound.play(-1)
                bullets_left = 10

        
    # обновляем окно
    pygame.display.update()
    
    # обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
            pygame.quit()
        if event.type == enemy_timer:
            enemy_list.append(enemy_move[enemy_animation_count].get_rect(topleft=(enemy_x, enemy_y)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left > 0:
            bullet_list.append(bullet.get_rect(topleft=(player_x+30, player_y+10)))
            bullets_left -= 1

    # задержка
    clock.tick(10)

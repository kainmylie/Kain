import pygame
import random


pygame.init()

WIDTH = 500
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yellow Jump")

clock = pygame.time.Clock()

BG = (180, 230, 255)
YELLOW = (255, 220, 40)
GREEN = (80, 200, 120)
RED = (230, 60, 60)
BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
BLUE = (80, 140, 255)
BROWN = (120, 70, 30)
PINK = (255, 170, 180)

font = pygame.font.SysFont("arial", 32)
small_font = pygame.font.SysFont("arial", 24)

player = pygame.Rect(230, 550, 40, 45)
speed_x = 0
speed_y = -16

platforms = []
enemies = []

score = 0
game_over = False


def reset_game():
    global player, speed_x, speed_y, platforms, enemies, score, game_over
    
    #возврощаю все в начальное состояние

    player = pygame.Rect(230, 550, 40, 45)
    speed_x = 0
    speed_y = -16
    score = 0
    game_over = False

    platforms = [
        [pygame.Rect(180, 650, 125, 15), 0, 0],
        [pygame.Rect(70, 540, 125, 15), 0, 0],
        [pygame.Rect(275, 430, 125, 15), 0, 0],
        [pygame.Rect(120, 320, 125, 15), 2, 2],
        [pygame.Rect(300, 210, 125, 15), 1, 0],
        [pygame.Rect(90, 100, 125, 15), 0, 0],
    ]

    enemies = []


def draw_text(text, font_name, color, x, y):
    text_img = font_name.render(text, True, color)
    screen.blit(text_img, (x, y))


def make_platform():
    
    #новая платформа чтоб была выше
    
    highest_y = HEIGHT

    for item in platforms:
        if item[0].y < highest_y:
            highest_y = item[0].y

    x = random.randint(0, WIDTH - 125)
    y = highest_y - random.randint(90, 115)

    kind = 0
    move_speed = 0

    chance = random.randint(1, 5)

    if chance == 1:
        kind = 1

    chance = random.randint(1, 5)

    if chance == 1:
        kind = 2
        move_speed = random.choice([-2, 2])

    return [pygame.Rect(x, y, 125, 15), kind, move_speed]


def make_enemy():
    x = random.randint(0, WIDTH - 35)
    y = random.randint(-350, -80)
    move_speed = random.choice([-2, 0, 0, 2])

    return [pygame.Rect(x, y, 35, 35), move_speed]


def draw_player():
    
    #рисую гг
    
    pygame.draw.rect(screen, YELLOW, player, border_radius=12)

    pygame.draw.rect(
        screen,
        BROWN,
        (player.x + 5, player.y - 2, 30, 10),
        border_radius=5
    )

    pygame.draw.circle(screen, BLACK, (player.x + 12, player.y + 17), 3)
    pygame.draw.circle(screen, BLACK, (player.x + 28, player.y + 17), 3)

    pygame.draw.circle(screen, PINK, (player.x + 8, player.y + 27), 3)
    pygame.draw.circle(screen, PINK, (player.x + 32, player.y + 27), 3)

    pygame.draw.line(
        screen,
        BLACK,
        (player.x + 15, player.y + 32),
        (player.x + 25, player.y + 32),
        2
    )


def draw_platforms():
    for item in platforms:
        rect = item[0]
        kind = item[1]

        if kind == 1:
            glass = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(
                glass,
                (80, 200, 120, 120),
                (0, 0, rect.width, rect.height),
                border_radius=8
            )
            screen.blit(glass, (rect.x, rect.y))

        elif kind == 2:
            pygame.draw.rect(screen, BLUE, rect, border_radius=8)

        else:
            pygame.draw.rect(screen, GREEN, rect, border_radius=8)


def draw_enemies():
    for item in enemies:
        rect = item[0]

        pygame.draw.rect(screen, RED, rect, border_radius=50)
        pygame.draw.circle(screen, BLACK, (rect.x + 10, rect.y + 12), 4)
        pygame.draw.circle(screen, BLACK, (rect.x + 25, rect.y + 12), 4)
        pygame.draw.line(
            screen,
            BLACK,
            (rect.x + 10, rect.y + 25),
            (rect.x + 25, rect.y + 25),
            2
        )


def move_platforms():
    for item in platforms:
        rect = item[0]
        kind = item[1]

        if kind == 2:
            rect.x += item[2]

            if rect.left < 0 or rect.right > WIDTH:
                item[2] = -item[2]


def move_enemies():
    for item in enemies:
        rect = item[0]
        rect.x += item[1]

        if rect.left < 0 or rect.right > WIDTH:
            item[1] = -item[1]


def move_player():
    global speed_x, speed_y, game_over, score

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        speed_x = -6
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        speed_x = 6
    else:
        speed_x = 0

    player.x += speed_x

    if player.right < 0:
        player.left = WIDTH

    if player.left > WIDTH:
        player.right = 0

    speed_y += 0.45
    player.y += speed_y

    broken_platform = None

    for item in platforms:
        rect = item[0]
        kind = item[1]

        if player.colliderect(rect) and speed_y > 0:
            if player.bottom <= rect.bottom + 8:
                speed_y = -16

                if kind == 1:
                    broken_platform = item

    if broken_platform in platforms:
        platforms.remove(broken_platform)

    for item in enemies:
        if player.colliderect(item[0]):
            game_over = True

    #когда игрок выше середины, двигаю вниз платформы и врагов
    if player.y < HEIGHT // 2:
        shift = HEIGHT // 2 - player.y
        player.y = HEIGHT // 2
        score += shift

        for item in platforms:
            item[0].y += shift

        for item in enemies:
            item[0].y += shift

    if player.top > HEIGHT:
        game_over = True


def clean_old_objects():
    
    #чистка ушедших штук
    
    global platforms, enemies

    good_platforms = []

    for item in platforms:
        if item[0].y < HEIGHT:
            good_platforms.append(item)

    platforms = good_platforms

    good_enemies = []

    for item in enemies:
        if item[0].y < HEIGHT:
            good_enemies.append(item)

    enemies = good_enemies


def add_objects():
    
    #и добавляю новые
    
    while len(platforms) < 6:
        platforms.append(make_platform())

    if score > 250:
        if len(enemies) < 3 and random.randint(1, 170) == 1:
            enemies.append(make_enemy())


def draw_game_over():
    draw_text("Ты проиграла!", font, BLACK, 150, 280)
    draw_text("Счет: " + str(score // 10), small_font, BLACK, 205, 330)

    restart_button = pygame.Rect(150, 380, 200, 60)
    pygame.draw.rect(screen, BLUE, restart_button, border_radius=15)
    draw_text("Перезапуск", small_font, WHITE, 190, 398)


reset_game()

running = True

while running:
    clock.tick(60)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            restart_button = pygame.Rect(150, 380, 200, 60)

            if restart_button.collidepoint(mouse_pos):
                reset_game()

    if game_over == False:
        move_platforms()
        move_enemies()
        move_player()
        clean_old_objects()
        add_objects()

    draw_player()
    draw_platforms()
    draw_enemies()

    draw_text("Score: " + str(score // 10), small_font, BLACK, 15, 15)

    if game_over:
        draw_game_over()

    pygame.display.update()

pygame.quit()

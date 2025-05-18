import pygame
import platform
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90
BALL_SIZE = 15
FPS = 30

#ЦВЕТА
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

DIFFICULTY_LEVELS = {
    1: {"bot_speed": 5, "ball_speed": 6, "bot_error_rate": 0.5},
    2: {"bot_speed": 7, "ball_speed": 9, "bot_error_rate": 0.2},
    3: {"bot_speed": 9, "ball_speed": 11, "bot_error_rate": 0.1},
}

high_scores = []
SCORE_FILE = "high_scores.txt"

def load_score():
    global high_scores
    high_scores = []
    try:
        with open(SCORE_FILE, "r") as file:
            for line in file:
                if line.strip():
                    player_s, bot_s = map(int, line.strip().split(":"))
                    high_scores.append((player_s, bot_s))
    except FileNotFoundError:
        high_scores = []


screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("ping pong :o")
clock = pygame.time.Clock()


player = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
bot = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE, BALL_SIZE, BALL_SIZE)

#состояния игры
ball_speed_x, ball_speed_y = 0, 0
player_speed = 7
bot_speed = 5
game_state = "menu"
difficulty = 1
player_score = 0
bot_score = 0
font = pygame.font.Font(None, 36)

#пункты игры
menu_items = ["Играть", "Ривнь сложности: 1", "Рекорды", "Выход"]

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = DIFFICULTY_LEVELS[difficulty]["ball_speed"] * random.choice((1, -1))
    ball_speed_y = DIFFICULTY_LEVELS[difficulty]["ball_speed"] * random.choice((1, -1))

def setup():
    global ball_speed_x, ball_speed_y, player_score, bot_score
    player_score = 0
    bot_score = 0
    reset_ball()
    player.center = (50, HEIGHT // 2)
    bot.center = (WIDTH - 50, HEIGHT // 2)

def draw_menu(mouse_pos):
    screen.fill(BLACK)
    title = font.render("Ping Pong", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    for i, item in enumerate(menu_items):
        text = font.render(item, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50 - 50))
        if text_rect.collidepoint(mouse_pos):
            text = font.render(item, True, RED)
        screen.blit(text, text_rect)

def update_menu():
    global game_state, difficulty
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, item in enumerate(menu_items):
                text = font.render(item, True, WHITE)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50 - 50))
                if text_rect.collidepoint(mouse_pos):
                    if i == 0:
                        game_state = "playing"
                        setup()
                    elif i == 1:
                        difficulty = (difficulty % 3) + 1
                        menu_items[1] = f"Уровень сложности: {difficulty}"
                    elif i == 2:
                        pygame.quit()
                        return False
    draw_menu(mouse_pos)
    return True

def update_game():
    global ball_speed_x, ball_speed_y, player_score, bot_score, game_state


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.top > 0:
        player.y -= player_speed
    if keys[pygame.K_s] and player.bottom < HEIGHT:
        player.y += player_speed


    bot_speed = DIFFICULTY_LEVELS[difficulty]["bot_speed"]
    error_rate = DIFFICULTY_LEVELS[difficulty]["bot_error_rate"]

    if random.random() > error_rate:
        if bot.centery < ball.centery and bot.bottom < HEIGHT:
            bot.y += bot_speed
        if bot.centery > ball.centery and bot.top > 0:
            bot.y -= bot_speed
    else:
        bot.y += random.choice((-bot_speed, bot_speed))


    ball.x += ball_speed_x
    ball.y += ball_speed_y


    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    if ball.colliderect(player) or ball.colliderect(bot):
        soundd_file = 'gluhoy-stuk.wav'
        soundd_effect = pygame.mixer.Sound(soundd_file)
        soundd_effect.set_volume(15.0)
        soundd_effect.play()
        ball_speed_x *= -1


    if ball.left <= 0:
        bot_score += 1
        if bot_score >= 3:
            game_state = "game_over"
        else:
            reset_ball()
    if ball.right >= WIDTH:
        player_score += 1
        reset_ball()


    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, player)
    pygame.draw.rect(screen, BLUE, bot)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))


    player_text = font.render(str(player_score), True, WHITE)
    bot_text = font.render(str(bot_score), True, WHITE)
    screen.blit(player_text, (WIDTH // 4, 20))
    screen.blit(bot_text, (3 * WIDTH // 4, 20))


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = "menu"
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def draw_game_over():
    screen.fill(BLACK)
    sound_file = 'pukane-11.wav'
    sound_effect = pygame.mixer.Sound(sound_file)
    sound_effect.play()
    game_over_text = font.render("Game Over", True, WHITE)
    restart_text = font.render("Нажми r для перезапуска", True, WHITE)
    menu_text = font.render("нажми m для захода в меню", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 50))


def main():
    global game_state
    running = True
    while running:
        if game_state == "menu":
            running = update_menu()
        elif game_state == "playing":
            update_game()
        elif game_state == "game_over":
            draw_game_over()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        setup()
                        game_state = "playing"
                    elif event.key == pygame.K_m:
                        game_state = "menu"
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()




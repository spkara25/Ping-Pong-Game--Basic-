import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong game!")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game elements
paddle_width, paddle_height = 80, 10
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 30
paddle_speed = 8

ball_radius = 8
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5 * random.choice([-1, 1])
ball_speed_y = -5
initial_ball_speed = 5  # Store initial speed for reference

# Score
score = 0
font = pygame.font.SysFont('Arial', 20)

# Game loop
clock = pygame.time.Clock()
game_over = False

def draw_paddle(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, paddle_width, paddle_height))

def draw_ball(x, y):
    pygame.draw.circle(screen, RED, (x, y), ball_radius)

def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_x = initial_ball_speed * random.choice([-1, 1])
    ball_speed_y = -initial_ball_speed

def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def show_game_over():
    game_over_text = font.render("GAME OVER! Press R to restart", True, WHITE)
    screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))

def increase_ball_speed():
    # Increase speed by 10% with each hit
    global ball_speed_x, ball_speed_y
    ball_speed_x *= 1.1
    ball_speed_y *= 1.1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                game_over = False
                score = 0
                reset_ball()

    if not game_over:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
            paddle_x += paddle_speed

        # Ball movement
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball collision with walls
        if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
            ball_speed_x *= -1
        if ball_y <= ball_radius:
            ball_speed_y *= -1

        # Ball collision with paddle
        if (ball_y + ball_radius >= paddle_y and 
            ball_x >= paddle_x and 
            ball_x <= paddle_x + paddle_width):
            ball_speed_y *= -1
            score += 2  # Double the score per hit (2 points instead of 1)
            increase_ball_speed()  # Increase speed with each hit

        # Game over condition
        if ball_y >= HEIGHT:
            game_over = True

    # Drawing
    screen.fill(BLACK)
    draw_paddle(paddle_x, paddle_y)
    draw_ball(ball_x, ball_y)
    show_score()
    
    if game_over:
        show_game_over()

    pygame.display.flip()
    clock.tick(60)
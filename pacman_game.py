import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
PACMAN_SIZE = 30
ENEMY_SIZE = 30
PACMAN_SPEED = 7
ENEMY_SPEED =4
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
TRAIL_LENGTH = 20

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Game state variables
game_over = False
game_active = False

clock = pygame.time.Clock()

def start_window():
    # Display start window
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

        screen.fill(BLACK)
        start_font = pygame.font.Font(None, 50)
        start_text = start_font.render("Press ENTER to Start", True, RED)
        start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(start_text, start_text_rect)
        pygame.display.update()

def game_over_window(points):
    screen.fill(BLACK)
    game_over_font = pygame.font.Font(None, 50)
    game_over_text = game_over_font.render(f"Game Over - Points: {points}. Press ENTER to Restart", True, RED)
    game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, game_over_text_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return  # Return from the function when 'ENTER' key is pressed

def game_loop():
    pacman_x = WIDTH // 2
    pacman_y = HEIGHT // 2
    pacman_direction = "RIGHT"
    pacman_trail = []

    enemy1_x = random.randint(0, WIDTH - ENEMY_SIZE)
    enemy1_y = random.randint(0, HEIGHT - ENEMY_SIZE)
    enemy1_trail = []

    pellets = []
    for _ in range(20):
        pellet_x = random.randint(0, WIDTH)
        pellet_y = random.randint(0, HEIGHT)
        pellets.append((pellet_x, pellet_y))

    global game_over
    points = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pacman_direction = "LEFT"
        elif keys[pygame.K_RIGHT]:
            pacman_direction = "RIGHT"
        elif keys[pygame.K_UP]:
            pacman_direction = "UP"
        elif keys[pygame.K_DOWN]:
            pacman_direction = "DOWN"

        if pacman_direction == "LEFT":
            pacman_x -= PACMAN_SPEED
        elif pacman_direction == "RIGHT":
            pacman_x += PACMAN_SPEED
        elif pacman_direction == "UP":
            pacman_y -= PACMAN_SPEED
        elif pacman_direction == "DOWN":
            pacman_y += PACMAN_SPEED

        # Enemy AI (chase the player)
        if enemy1_x < pacman_x:
            enemy1_x += ENEMY_SPEED
        elif enemy1_x > pacman_x:
            enemy1_x -= ENEMY_SPEED

        if enemy1_y < pacman_y:
            enemy1_y += ENEMY_SPEED
        elif enemy1_y > pacman_y:
            enemy1_y -= ENEMY_SPEED

        # Check collision with enemies
        if (pacman_x < enemy1_x + ENEMY_SIZE and pacman_x + PACMAN_SIZE > enemy1_x and
            pacman_y < enemy1_y + ENEMY_SIZE and pacman_y + PACMAN_SIZE > enemy1_y):
            game_over = True

        # Check collision with pellets
        for pellet in pellets[:]:
            pellet_x, pellet_y = pellet
            if (pacman_x < pellet_x + 5 and pacman_x + PACMAN_SIZE > pellet_x and
                pacman_y < pellet_y + 5 and pacman_y + PACMAN_SIZE > pellet_y):
                points += 10
                pellets.remove(pellet)

        # character trails
        pacman_trail.append((pacman_x, pacman_y))
        if len(pacman_trail) > TRAIL_LENGTH:
            pacman_trail.pop(0)

        enemy1_trail.append((enemy1_x, enemy1_y))
        if len(enemy1_trail) > TRAIL_LENGTH:
            enemy1_trail.pop(0)

        # Pac-Man
        screen.fill(BLACK)
        pygame.draw.circle(screen, YELLOW, (pacman_x, pacman_y), PACMAN_SIZE)

        # Pac-Man's trail
        for trail_pos in pacman_trail:
            pygame.draw.circle(screen, YELLOW, trail_pos, PACMAN_SIZE // 2)

        # Enemies
        pygame.draw.rect(screen, RED, (enemy1_x, enemy1_y, ENEMY_SIZE, ENEMY_SIZE))

        # Draw Enemy's trail
        for trail_pos in enemy1_trail:
            pygame.draw.rect(screen, RED, (trail_pos[0], trail_pos[1], ENEMY_SIZE, ENEMY_SIZE))

        for pellet in pellets:
            pygame.draw.circle(screen, BLUE, pellet, 5)

        # Display points
        font = pygame.font.Font(None, 36)
        text = font.render(f"Points: {points}", True, RED)
        screen.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(30)

    return points

start_window()
points = game_loop()
game_over_window(points)

pygame.quit()
sys.exit()
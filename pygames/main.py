import pygame
import random

from config import *

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple 2D Game")

# Player properties
player_width = 50
player_height = 50
player_x = (WIDTH - player_width) // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Enemy properties
enemy_width = 50
enemy_height = 50
enemy_x = random.randint(0, WIDTH - enemy_width)
enemy_y = 0
enemy_speed = 3

# Game loop
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Move enemy
    enemy_y += enemy_speed

    # Collision detection
    if player_x < enemy_x + enemy_width and player_x + player_width > enemy_x and player_y < enemy_y + enemy_height and player_y + player_height > enemy_y:
        running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw player and enemy
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_width, enemy_height))

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
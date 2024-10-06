import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Click the Circle!")

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Circle settings
circle_size = 100  # Initial size of the circle
MIN_CIRCLE_SIZE = 20  # Minimum size for the circle
circle_position = (random.randint(circle_size, width - circle_size), 
                   random.randint(circle_size, height - circle_size))
is_red_circle = random.choice([True, False])  # Randomly choose if the circle is red

# Font settings
font = pygame.font.Font(None, 36)  # Default font, size 36
large_font = pygame.font.Font(None, 72)  # Large font for final score

# Timer settings
timer_seconds = 10  # Starting time in seconds
start_ticks = pygame.time.get_ticks()  # Get the starting ticks

# Score settings
score = 0  # Initial score

# Game state settings
game_over = False  # Track if the game has ended

# Function to get points based on circle size
def get_points(size):
    return max(1, int(10 / (size / 20)))  # More points for smaller circles

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Allow quitting by pressing 'Q' after the game is over
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_q:
                running = False
        
        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            # Check if the mouse click is within the circle
            if (mouse_x - circle_position[0]) ** 2 + (mouse_y - circle_position[1]) ** 2 <= (circle_size / 2) ** 2:
                # Check the color of the circle and the button clicked
                if is_red_circle:
                    if event.button == 1:  # Left click
                        score -= get_points(circle_size)  # Deduct points for red circle
                        circle_size += 10  # Increase size
                        print("Clicked on a red circle with left click! Lost points.")
                    elif event.button == 3:  # Right click
                        score += get_points(circle_size)  # Gain points for red circle
                        circle_size = max(MIN_CIRCLE_SIZE, int(circle_size * 0.8))  # Shrink size but respect minimum
                        print("Clicked on a red circle with right click! Gained points.")
                else:  # Green circle
                    if event.button == 1:  # Left click
                        score += get_points(circle_size)  # Gain points for green circle
                        circle_size = max(MIN_CIRCLE_SIZE, int(circle_size * 0.8))  # Shrink size but respect minimum
                        print("Clicked on a green circle with left click! Gained points.")
                    elif event.button == 3:  # Right click
                        score -= get_points(circle_size)  # Deduct points for green circle
                        circle_size += 10  # Increase size
                        print("Clicked on a green circle with right click! Lost points.")
                
                # If circle size is too small to continue
                if circle_size < MIN_CIRCLE_SIZE:
                    print("The circle is too small to continue!")
                    running = False
                else:
                    # Move the circle to a new random position and change its color
                    circle_position = (random.randint(circle_size, width - circle_size), 
                                       random.randint(circle_size, height - circle_size))
                    is_red_circle = random.choice([True, False])  # Randomly choose the new circle color

    if not game_over:
        # Calculate elapsed time
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000  # Convert milliseconds to seconds
        remaining_time = timer_seconds - elapsed_time  # Calculate remaining time

        # Check if the timer has reached zero
        if remaining_time <= 0:
            game_over = True  # End the game
            remaining_time = 0  # To avoid negative values in the display
            print("Time's up! Final Score:", score)

    # Fill the screen with white
    screen.fill(WHITE)

    if not game_over:
        # Draw the circle
        color = RED if is_red_circle else GREEN
        pygame.draw.circle(screen, color, circle_position, int(circle_size / 2))
    
    # Render the timer
    timer_text = font.render(f"Time: {remaining_time}s", True, BLACK)
    screen.blit(timer_text, (width - 150, height - 50))  # Position the timer in the bottom right corner
    
    # Render the score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))  # Position the score in the top left corner
    
    # If the game is over, display the final score in the center of the screen
    if game_over:
        final_score_text = large_font.render(f"Final Score: {score}", True, BLACK)
        screen.blit(final_score_text, (width // 2 - final_score_text.get_width() // 2, height // 2 - final_score_text.get_height() // 2))
        
        # Display instruction to quit
        quit_text = font.render("Press 'Q' to quit", True, BLACK)
        screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 50))

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()


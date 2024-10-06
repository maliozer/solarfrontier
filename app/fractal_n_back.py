import pygame as pg
import random
import os
from config import *

# Initialize pygame
pg.init()

# Constants
WIDTH, HEIGHT = 800, 600
SIGN_SIZE = 100  # Assuming SIGN_SIZE is defined as 100

# Set up the display
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Random Object Display')

# Clock and timer for switching objects
clock = pg.time.Clock()
switch_event = pg.USEREVENT + 1
pg.time.set_timer(switch_event, 500)  # Switch every 500 milliseconds

# Button class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.font = pg.font.SysFont("Droid Sans Mono", 40)
        self.color = (200, 200, 200)  # Default button color
        self.hover_color = (150, 150, 150)  # Hover color
        self.active = False  # To check if the button is active

    def draw(self, screen):
        color = self.hover_color if self.active else self.color
        pg.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False


# Sign class
class Sign(pg.sprite.Sprite):
    def __init__(self, game, x=50, y=50, shape='triangle'):
        self.game = game
        self.groups = game.sign_sprites
        self.size = SIGN_SIZE
        pg.sprite.Sprite.__init__(self, self.groups)

        # Create a surface to hold the shape or object using self.size
        self.image = pg.Surface((self.size, self.size), pg.SRCALPHA)

        # Choose a random color for the shape
        color = random.choice([
            WHITE, BLACK, RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK, CYAN, MAGENTA, BROWN, GRAY, LIGHT_BLUE, DARK_GREEN
        ])

        # Draw basic shapes based on the 'shape' parameter
        if shape == 'triangle':
            self.draw_triangle(color)
        elif shape == 'square':
            self.draw_square(color)
        elif shape == 'diamond':
            self.draw_diamond(color)
        elif shape == 'star':
            self.draw_star(color)
        elif shape == 'line':
            self.draw_line(color)
        elif shape == 'circle':
            self.draw_circle(color)
        elif shape == 'ellipse':
            self.draw_ellipse(color)

        self.rect = self.image.get_rect(center=(x, y))  # Set the rect position directly

    def draw_triangle(self, color):
        points = [(self.size // 2, 0), (0, self.size), (self.size, self.size)]
        pg.draw.polygon(self.image, color, points)

    def draw_square(self, color):
        pg.draw.rect(self.image, color, (0, 0, self.size, self.size))

    def draw_diamond(self, color):
        half_size = self.size // 2
        points = [(half_size, 0), (0, half_size), (half_size, self.size), (self.size, half_size)]
        pg.draw.polygon(self.image, color, points)

    def draw_star(self, color):
        points = [
            (self.size // 2, 0), (self.size * 6 // 10, self.size * 35 // 100), (self.size, self.size * 4 // 10),
            (self.size * 7 // 10, self.size * 65 // 100), (self.size * 8 // 10, self.size),
            (self.size // 2, self.size * 8 // 10), (self.size * 2 // 10, self.size),
            (self.size * 3 // 10, self.size * 65 // 100), (0, self.size * 4 // 10), (self.size * 4 // 10, self.size * 35 // 100)
        ]
        pg.draw.polygon(self.image, color, points)

    def draw_line(self, color):
        pg.draw.line(self.image, color, (0, 0), (self.size, self.size), max(self.size // 20, 1))

    def draw_circle(self, color):
        pg.draw.circle(self.image, color, (self.size // 2, self.size // 2), self.size // 2)

    def draw_ellipse(self, color):
        pg.draw.ellipse(self.image, color, (self.size // 10, self.size // 4, self.size * 8 // 10, self.size // 2))

    def update(self):
        pass


class Game:
    def __init__(self):
        self.sign_sprites = pg.sprite.Group()
        self.shape_sequence = ['triangle', 'square', 'diamond', 'star', 'line', 'circle', 'ellipse']
        self.current_index = 0  # Index to keep track of the current shape
        self.answer = None  # Variable to store the correct answer
        self.options = []  # Variable to store answer options
        self.buttons = []  # List to hold buttons for options
        self.question_displayed = False

    def show_next_sign(self):
        if self.current_index < len(self.shape_sequence):
            # Clear the previous sign
            self.sign_sprites.empty()

            # Create a Sign with the next shape from the sequence
            random_shape = self.shape_sequence[self.current_index]
            Sign(self, x=WIDTH // 2, y=HEIGHT // 2, shape=random_shape)

            self.current_index += 1
        else:
            # Prepare to ask a question after showing all shapes
            self.prepare_question()

    def prepare_question(self):
        print("asking questions")
        # Choose a random nth shape to ask about
        nth_shape = random.randint(1, len(self.shape_sequence))
        self.answer = self.shape_sequence[-nth_shape]  # Get the correct answer

        # Generate incorrect options
        options = random.sample(self.shape_sequence, 3)  # Get three random shapes
        if self.answer in options:  # Ensure the correct answer is included
            options.remove(self.answer)
        options = options[:2] + [self.answer]  # Get two incorrect options and add the correct one
        random.shuffle(options)  # Shuffle the options
        self.options = options  # Store the options for display

        # Clear the display
        self.sign_sprites.empty()
        font = pg.font.SysFont("Droid Sans Mono", 40)

        # Create a question surface
        question_surface = font.render(f"What was the {nth_shape} shape?", True, (0, 0, 0))  # Black text

        screen.fill((255, 255, 255))
        screen.blit(question_surface, (50, HEIGHT // 2 - 30))

        # Display answer options as buttons
        self.buttons = []  # Clear previous buttons
        for i, option in enumerate(options):
            button = Button(50, HEIGHT // 2 + i * 60, 200, 50, option)  # Create a new button
            self.buttons.append(button)

        pg.display.flip()  # Update the display to show the question and options
        self.question_displayed = True  # Mark that the question is displayed

    def check_answer(self, answer):
        return answer == self.answer

    def update(self):
        self.sign_sprites.update()

    def draw(self):
        screen.fill((255, 255, 255))
        self.sign_sprites.draw(screen)
        for button in self.buttons:  # Draw all buttons
            button.draw(screen)
        pg.display.flip()


# Create the game instance
game = Game()
# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == switch_event and not game.question_displayed:
            # Show the next shape in the sequence every 0.5 seconds
            game.show_next_sign()
        elif event.type == pg.MOUSEBUTTONDOWN:  # Check for mouse button clicks
            if game.question_displayed:
                for button in game.buttons:
                    if button.check_click(event.pos):  # Check if a button was clicked
                        selected_option = button.text
                        if game.check_answer(selected_option):
                            result_surface = pg.font.SysFont(None, 48).render("Correct!", True, (0, 255, 0))
                        else:
                            result_surface = pg.font.SysFont(None, 48).render("Wrong!", True, (255, 0, 0))

                        # Clear the display and show result
                        screen.fill((255, 255, 255))
                        screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, HEIGHT // 2))
                        pg.display.flip()
                        pg.time.delay(2000)  # Show result for 2 seconds
                        game.sign_sprites.empty()  # Clear display for next round
                        game.question_displayed = False  # Reset question display status
                        game.current_index = 0  # Reset the current index for the next round

    # Update and draw the game
    game.update()
    game.draw()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pg.quit()

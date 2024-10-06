import pygame
import sys
import random  # Import the random module

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GRAY = (200, 200, 200)  # Light gray background for the boxes

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Font
FONT = pygame.font.SysFont("Droid Sans Mono", 40)

class Game:
    def __init__(self, puzzles, answers):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Semantic Difference Puzzle Game")
        self.clock = pygame.time.Clock()
        self.puzzles = puzzles
        self.answers = answers
        self.current_puzzle = 0
        self.boxes = []
        self.score = 0  # Initialize score
        self.start_time = pygame.time.get_ticks()  # Start time in milliseconds
        self.feedback_message = ""  # Initialize feedback message
        self.feedback_color = BLACK  # Default color for feedback

    def create_boxes(self, words):
        # Shuffle the words to display them in random order
        random.shuffle(words)
        
        # Calculate box size and positions
        self.boxes = []
        box_width = 150
        box_height = 50
        padding = 20
        x_start = (SCREEN_WIDTH - (box_width * 3 + padding * 2)) // 2  # Center horizontally
        y_start = (SCREEN_HEIGHT - (box_height + padding * (len(words) // 3))) // 2  # Center vertically

        for i, word in enumerate(words):
            x = x_start + (i % 3) * (box_width + padding)  # Adjust for 3 boxes per row
            y = y_start + (i // 3) * (box_height + padding)
            box = pygame.Rect(x, y, box_width, box_height)
            self.boxes.append((box, word))

    def draw_gradient_background(self):
        # Draw gradient background from light to dark blue
        top_color = (173, 216, 230)  # Light blue
        bottom_color = (0, 0, 139)   # Dark blue
        
        for y in range(SCREEN_HEIGHT):
            # Interpolate color between top_color and bottom_color
            r = top_color[0] + (bottom_color[0] - top_color[0]) * y // SCREEN_HEIGHT
            g = top_color[1] + (bottom_color[1] - top_color[1]) * y // SCREEN_HEIGHT
            b = top_color[2] + (bottom_color[2] - top_color[2]) * y // SCREEN_HEIGHT
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def draw_puzzle(self):
        # Draw the gradient background
        self.draw_gradient_background()
        
        # Draw the words in boxes
        for box, word in self.boxes:
            # Draw background for the box
            pygame.draw.rect(self.screen, LIGHT_GRAY, box)
            pygame.draw.rect(self.screen, BLACK, box, 2)  # Draw the border
            text_surface = FONT.render(word, True, BLACK)
            text_rect = text_surface.get_rect(center=box.center)  # Center the text in the box
            self.screen.blit(text_surface, text_rect.topleft)  # Position the text in the box

        # Draw the score at the bottom-left corner in white
        score_text = FONT.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, SCREEN_HEIGHT - 40))  # Position at bottom-left

        # Calculate and display the elapsed time in white
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Convert to seconds
        timer_text = FONT.render(f"Time: {elapsed_time}s", True, WHITE)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 40))  # Position at bottom-right

        # Draw feedback message at the bottom center
        feedback_surface = FONT.render(self.feedback_message, True, self.feedback_color)
        feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        self.screen.blit(feedback_surface, feedback_rect.topleft)  # Position the feedback message

    def check_answer(self, selected_word):
        # Check if the selected word is correct
        if selected_word == self.answers[self.current_puzzle]:
            self.score += 1  # Increase score when correct answer is chosen
            self.feedback_message = "Correct!"  # Set feedback message
            self.feedback_color = GREEN  # Set feedback color to green
        else:
            self.feedback_message = "Wrong!"  # Set feedback message
            self.feedback_color = RED  # Set feedback color to red

        # Delay before moving to the next puzzle
        pygame.time.delay(1000)  # Delay for 1 second before moving on

        # Move to the next puzzle regardless of the answer correctness
        self.current_puzzle += 1
        if self.current_puzzle < len(self.puzzles):
            self.create_boxes(self.puzzles[self.current_puzzle])
        else:
            # Game completed, show total time and score
            total_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Total time spent
            print(f"You've completed all puzzles! Total time: {total_time}s, Final Score: {self.score}")
            pygame.quit()
            sys.exit()

    def run(self):
        self.create_boxes(self.puzzles[self.current_puzzle])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for box, word in self.boxes:
                        if box.collidepoint(mouse_pos):
                            self.check_answer(word)

            self.draw_puzzle()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    puzzles = [
        ["apple", "banana", "car"],         # "car" is different from fruits
        ["dog", "cat", "airplane"],         # "airplane" is different from animals
        ["house", "tree", "fish"],          # "fish" is different from land-based objects
        ["sun", "moon", "laptop"],          # "laptop" is different from celestial objects
        ["table", "chair", "lion"],         # "lion" is different from furniture
        ["bus", "bicycle", "spoon"],        # "spoon" is different from vehicles
        ["shirt", "pants", "elephant"],     # "elephant" is different from clothing
        ["river", "mountain", "pen"],       # "pen" is different from natural features
        ["chicken", "cow", "phone"],        # "phone" is different from animals
        ["book", "magazine", "ocean"]       # "ocean" is different from reading materials
    ]

    answers = [
        "car",          # Different from fruits
        "airplane",     # Different from animals
        "fish",         # Different from land-based objects
        "laptop",       # Different from celestial objects
        "lion",         # Different from furniture
        "spoon",        # Different from vehicles
        "elephant",     # Different from clothing
        "pen",          # Different from natural features
        "phone",        # Different from animals
        "ocean"         # Different from reading materials
    ]

    game = Game(puzzles, answers)
    game.run()

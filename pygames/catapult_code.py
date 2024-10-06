import pygame as pg
from config import *
from sprites import Player, Sign

# Define a maximum level constant
MAX_LEVEL = 3  # Set this to the maximum level you want

class Game:
    def __init__(self):
        # Initialize Pygame
        pg.init()

        self.all_sprites = pg.sprite.Group()
        self.sign_sprites = pg.sprite.Group()

        self.previous_answers = []
        self.score = 0  # Initialize score

        # Create the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(WHITE)

        pg.display.set_caption("Cognitive Games")
        self.font = pg.font.Font(None, 36)  # Initialize font for rendering text

        self.clock = pg.time.Clock()

        # Get screen width and height for centering
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        # Calculate the center x and y positions
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        self.level_sequence = self.generate_level_sequence(1)  # Start with level 1

        self.turn = 0
        self.level = 1
        self.run()

    def run(self):
        # Game loop - set self.playing = False to end the game
        self.playing = True
        self.player = Player(self)

        while self.playing:
            self.dt = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:  # Check for 'Q' key press
                    self.playing = False
                
                response = self.check_answer(event.key)
                if response:  # If the answer is correct
                    self.turn += 1
                    self.score += 100  # Increment score on correct answer
                else:
                    self.turn = 0
                    self.score -= 150  # Deduct points on incorrect answer

    def update(self):
        # Clear all the previous signs from the sign_sprites group
        self.sign_sprites.empty()

        # Check if the turn index is within the bounds of level_sequence
        if self.turn < len(self.level_sequence):
            # Get the current level sequence data
            s_x = self.level_sequence[self.turn]['x']
            s_y = self.level_sequence[self.turn]['y']
            s_color = self.level_sequence[self.turn]['color']
            s_shape = self.level_sequence[self.turn]['shape']
            s_object_type = self.level_sequence[self.turn]['object_type']
            self.s_answer = self.level_sequence[self.turn]['answer']

            # Create a new Sign sprite and add it to the sign_sprites group
            self.shape1 = Sign(self, x=s_x, y=s_y, color=s_color, shape=s_shape, object_type=s_object_type)

            # Update the sign_sprites group (which now only contains the new sprite)
            self.sign_sprites.update()
        else:
            # Handle level completion or other logic when there are no more turns
            self.handle_level_complete()

        # Update the display
        pg.display.update()

    def handle_level_complete(self):
        # Check if the maximum level is reached
        if self.level >= MAX_LEVEL:
            self.display_final_score()
            self.playing = False  # End the game
        else:
            # Prepare for the next level
            self.level += 1
            self.previous_answers = []  # Reset previous answers for the new level
            self.level_sequence = self.generate_level_sequence(self.level)  # Generate the new level sequence
            self.turn = 0  # Reset turn to the first item of the new level

    def generate_level_sequence(self, level):
        # Define the sequences for each level
        level_sequences = {
            1: [
                    {
                        'x': self.screen_width // 2 - (SIGN_SIZE // 2),
                        'y': self.screen_height // 2 - (SIGN_SIZE // 2),
                        'color': YELLOW,
                        'shape': 'triangle',
                        'object_type': None,
                        'answer': 'RIGHT'  # Base rule (first occurrence)
                    },
                    {
                        'x': self.screen_width // 2 - (SIGN_SIZE // 2),
                        'y': self.screen_height // 2 + SIGN_SIZE // 2,
                        'color': BLUE,
                        'shape': 'square',
                        'object_type': None,
                        'answer': 'DOWN'  # 90 degrees clockwise from RIGHT
                    },
                    {
                        'x': self.screen_width // 2 - (SIGN_SIZE // 2),
                        'y': self.screen_height // 2 + SIGN_SIZE,
                        'color': GREEN,
                        'shape': 'square',
                        'object_type': None,
                        'answer': 'DOWN'  # Always DOWN
                    }
                ],
            2: [
                {'x': self.screen_width // 2 - (SIGN_SIZE // 2), 'y': self.screen_height // 2 - (SIGN_SIZE // 2), 'color': YELLOW, 'shape': 'triangle', 'object_type': None, 'answer': 'RIGHT'},
                {'x': self.screen_width // 2 - (SIGN_SIZE // 2), 'y': self.screen_height // 2 + SIGN_SIZE // 2, 'color': BLUE, 'shape': 'square', 'object_type': None, 'answer': 'LEFT'},
                {'x': self.screen_width // 2 - (SIGN_SIZE // 2), 'y': self.screen_height // 2 + SIGN_SIZE, 'color': ORANGE, 'shape': 'circle', 'object_type': None, 'answer': 'LEFT'},
                {'x': self.screen_width // 2 - (SIGN_SIZE // 2), 'y': self.screen_height // 2 - SIGN_SIZE, 'color': GREEN, 'shape': 'square', 'object_type': None, 'answer': 'DOWN'},
            ],

            3: [
                {'x': self.screen_width // 2 - (SIGN_SIZE // 2), 'y': self.screen_height // 2 - (SIGN_SIZE // 2), 'color': BLUE, 'shape': 'square', 'object_type': None, 'answer': 'LEFT'},        # Base rule (first occurrence)
                {'x': self.screen_width // 2 - (SIGN_SIZE // 2), 'y': self.screen_height // 2 + SIGN_SIZE // 2, 'color': GREEN, 'shape': 'square', 'object_type': None, 'answer': 'DOWN'},       # Always DOWN
                {'x': self.screen_width // 2 - (SIGN_SIZE // 2), 'y': self.screen_height // 2 + SIGN_SIZE, 'color': YELLOW, 'shape': 'triangle', 'object_type': None, 'answer': 'RIGHT'},   # Opposite of LEFT
                {'x': self.screen_width // 2 - (SIGN_SIZE // 2), 'y': self.screen_height // 2 + SIGN_SIZE * 2, 'color': ORANGE, 'shape': 'circle', 'object_type': None, 'answer': 'DOWN'},      # Same as DOWN
                {'x': self.screen_width // 2 - (SIGN_SIZE // 2), 'y': self.screen_height // 2 - SIGN_SIZE, 'color': PURPLE, 'shape': 'rectangle', 'object_type': None, 'answer': 'UP'},     # 90 degrees clockwise from DOWN
                {'x': self.screen_width // 2 - (SIGN_SIZE // 2), 'y': self.screen_height // 2 - SIGN_SIZE * 2, 'color': RED, 'shape': 'circle', 'object_type': None, 'answer': 'LEFT'},          # Same as previous answer (LEFT)
            ]
            # Add more levels as needed
        }

        # Return the sequence for the requested level, or an empty list if the level is not defined
        return level_sequences.get(level, [])

    def draw(self):
        self.screen.fill(WHITE)
        self.sign_sprites.draw(self.screen)

        # Draw the turn number
        turn_text = self.font.render(f'Turn: {self.turn + 1}', True, (0, 0, 0))  # Increment turn for turn display
        self.screen.blit(turn_text, (10, 50))  # Position below level text

        # Draw the level number
        level_text = self.font.render(f'Level: {self.level}', True, (0, 0, 0))  # Level display
        self.screen.blit(level_text, (10, 10))  # Position at (10, 10)

        # Draw the score (Commented out to hide score during game)
        # score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))  # Score display
        # self.screen.blit(score_text, (10, 90))  # Position below turn text

    def check_answer(self, key):
        key_mapping = {
            pg.K_UP: "UP",
            pg.K_DOWN: "DOWN",
            pg.K_LEFT: "LEFT",
            pg.K_RIGHT: "RIGHT"
        }

        answer = key_mapping.get(key)
        if answer:
            # Append the current answer to previous answers
            self.previous_answers.append(answer)

            # Check if the answer is correct
            if answer == self.level_sequence[self.turn]['answer']:
                return True  # Correct answer
            else:
                self.turn = 0  # Reset turn if the answer is incorrect
                return False  # Incorrect answer

    def display_final_score(self):
        self.screen.fill(WHITE)
        
        final_score_text = self.font.render(f'Final Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
        pg.display.update()

        # Wait for a moment before exiting
        pg.time.delay(2000)  # Display for 2 seconds

if __name__ == "__main__":
    game = Game()

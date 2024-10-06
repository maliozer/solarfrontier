import pygame as pg
import random
import os

from config import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x=0, y=0, color=GREEN):

        # self.groups = game.all_sprites
        self.groups = game.all_sprites

        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((100, 100))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == "up":
            dy = 5
            self.y -= dy

        elif direction == "down":
            dy = 5
            self.y += dy

        elif direction == "left":
            dx = 5
            self.x -= dx

        elif direction == "right":
            dx = 5
            self.x += dx
        else:
            pass


    def update(self):
        self.rect.x = self.x * 20
        self.rect.y = self.y * 20

    def decision(self):
        pass



class Sign(pg.sprite.Sprite):
    def __init__(self, game, x=50, y=50, color=BLUE, shape='triangle', object_type=None):
        self.game = game
        self.groups = game.sign_sprites
        self.size = SIGN_SIZE
        pg.sprite.Sprite.__init__(self, self.groups)

        # Create a surface to hold the shape or object
        self.image = pg.Surface((100, 100), pg.SRCALPHA)

        # Check if object_type is provided (for objects like hammer, table, etc.)
        if object_type is not None:
            self.load_object(object_type)
        else:
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

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def load_object(self, object_type):
        """Load an image based on the object_type from the images folder."""
        # Get the current directory path
        current_path = os.path.dirname(__file__)

        # Build the full path to the 'images' folder
        images_path = os.path.join(current_path, 'images')

        # Load the appropriate image based on the object_type
        if object_type == 'hammer':
            self.image = pg.image.load(os.path.join(images_path, 'hammer.png')).convert_alpha()  # Load hammer image
        elif object_type == 'table':
            self.image = pg.image.load(os.path.join(images_path, 'table.png')).convert_alpha()   # Load table image
        elif object_type == 'rock':
            self.image = pg.image.load(os.path.join(images_path, 'rock.png')).convert_alpha()    # Load rock image
        elif object_type == 'dog':
            self.image = pg.image.load(os.path.join(images_path, 'dog.png')).convert_alpha()     # Load dog image
        elif object_type == 'bird':
            self.image = pg.image.load(os.path.join(images_path, 'bird.png')).convert_alpha()    # Load bird image

    # Resizable triangle
    def draw_triangle(self, color):
        size = self.size
        points = [(size // 2, 0), (0, size), (size, size)]  # Adjust triangle points based on size
        pg.draw.polygon(self.image, color, points)

    # Resizable square
    def draw_square(self, color):
        size = self.size
        pg.draw.rect(self.image, color, (0, 0, size, size))  # Adjust square dimensions based on size

    # Resizable diamond
    def draw_diamond(self, color):
        size = self.size
        half_size = size // 2
        points = [(half_size, 0), (0, half_size), (half_size, size), (size, half_size)]  # Adjust diamond points
        pg.draw.polygon(self.image, color, points)

    # Resizable star
    def draw_star(self, color):
        size = self.size
        points = [
            (size // 2, 0), (size * 6 // 10, size * 35 // 100), (size, size * 4 // 10),
            (size * 7 // 10, size * 65 // 100), (size * 8 // 10, size),
            (size // 2, size * 8 // 10), (size * 2 // 10, size),
            (size * 3 // 10, size * 65 // 100), (0, size * 4 // 10), (size * 4 // 10, size * 35 // 100)
        ]  # Adjust star points based on size
        pg.draw.polygon(self.image, color, points)

    # Resizable line
    def draw_line(self, color):
        size = self.size
        pg.draw.line(self.image, color, (0, 0), (size, size), max(size // 20, 1))  # Adjust line thickness

    # Resizable circle
    def draw_circle(self, color):
        size = self.size
        pg.draw.circle(self.image, color, (size // 2, size // 2), size // 2)  # Adjust circle radius

    # Resizable ellipse
    def draw_ellipse(self, color):
        size = self.size
        pg.draw.ellipse(self.image, color, (size // 10, size // 4, size * 8 // 10, size // 2))  # Adjust ellipse dimensions

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
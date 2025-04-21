import pygame as py
import random

TILE_SIZE = 64

class TileMap:
    def __init__(self, tile_paths, screen_width, screen_height):
        self.tiles = [py.image.load(path).convert_alpha() for path in tile_paths]
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw(self, surface):
        cols = self.screen_width // TILE_SIZE + 1
        rows = self.screen_height // TILE_SIZE + 1

        for row in range(rows):
            for col in range(cols):
                tile = random.choice(self.tiles)  # możesz tu dodać wzór zamiast random
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                surface.blit(tile, (x, y))

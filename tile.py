import pygame

class Tilesheet:
    def __init__(self, path, width, height, cols, rows):
        self.image = pygame.image.load(path).convert()
        self.tiles = []
        for y in range(rows):
            for x in range(cols):
                rect = (x * width, y * height, width, height)
                self.tiles.append(self.image.subsurface(rect))
    
    def get_tile(self, pos):
        return self.tiles[pos]
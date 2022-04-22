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

class PlayerAnimation:
    def __init__(self, texture, width, height, frames):
        self.image = pygame.image.load(texture).convert()
        self.frames = []
        for i in range(frames):
            rect = (i * width, 0, width, height)
            self.frames.append(self.image.subsurface(rect))

    def get_idle(self):
        return self.frames[0]
    
    def get_reverse_idle(self):
        return pygame.transform.flip(self.get_idle(), True, False)

    def get_run(self):
        return self.frames[1:4]
    
    def get_jump(self):
        return self.frames[5]
    
    def get_reverse_jump(self):
        return pygame.transform.flip(self.get_jump(), True, False)
    
    def get_death(self):
        return self.frames[6]
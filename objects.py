import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, texture):
        super().__init__()

        self.image = texture
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class TBlock(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, texture):
        super().__init__()

        self.image = texture
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pass

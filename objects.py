import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, texture):
        super().__init__()

        self.image = texture
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.hitedY = self.rect.y
        self.hited = False
        self.time = 0

class BreakBlock(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, texture):
        super().__init__()

        self.image = texture
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.hitedY = self.rect.y
        self.hited = False
        self.time = 0
    
    def hit(self):
        if self.hited: return
        
        self.rect.y -= 8
        self.hited = True
        self.time = 0
    
    def update(self, sprites):
        if self.hited:
            if self.time >= 1:
                self.hited = False
                self.rect.y += 8
            
            self.time += 0.1


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

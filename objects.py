import pygame

GRAVITY = 0.3

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
    def __init__(self, x, y):
        super().__init__()
        
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.dir = 1
        self.speed = 0.01

        self.velX = self.speed
        self.velY = 0

        self.on_ground = False

        self.alive = True

    def update(self, sprites):
        self.on_ground = False

        self.rect.x += self.velX
        self.collide(sprites, self.velX, 0)

        self.rect.y += self.velY
        self.collide(sprites, 0, self.velY)

        if not self.on_ground:
            self.velX += GRAVITY


    def collide(self, sprites, velX, velY):
        if not self.alive: return
        
        x = self.rect.x
        y = self.rect.y
        
        sprs = filter(lambda sprite: sprite.rect.x >= x - 64 and sprite.rect.x <= x + 64 and sprite.rect.y >= y - 64 and sprite.rect.y <= y + 64, sprites)

        for sprite in sprs:
            if type(sprite) is TBlock: continue

            if pygame.sprite.collide_rect(self, sprite):
                if velX > 0:
                    self.rect.right = sprite.rect.left
                    self.velX = -self.speed
                if velX < 0:
                    self.rect.left = sprite.rect.right
                    self.velX = self.speed
                
                if velY > 0:
                    self.rect.bottom = sprite.rect.top
                    self.on_ground = True
                    self.velY = 0
                
                if velY < 0:
                    self.rect.top = sprite.rect.bottom
                    self.velY = 0

                    if type(sprite) is BreakBlock:
                        sprite.hit()
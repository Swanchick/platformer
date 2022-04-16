import pygame


GRAVITY = 0.3

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velX = 0
        self.velY = 0
        self.speed = 5
        self.on_ground = False
        self.jump_force = 10
    
    def update(self, sprites: list):
        self.movement()

        self.on_ground = False

        self.rect.x += self.velX
        self.collide(sprites, self.velX, 0)

        self.rect.y += self.velY
        self.collide(sprites, 0, self.velY)

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velY = -self.jump_force

        if not self.on_ground:
            self.velY += GRAVITY

        if keys[pygame.K_RIGHT]:
            self.velX = self.speed
        elif keys[pygame.K_LEFT]:
            self.velX = -self.speed
        else:
            self.velX = 0
    
    def collide(self, sprites, velX, velY):
        x = self.rect.x
        y = self.rect.y
        
        for sprite in sprites:
            if type(sprite) is Player: continue
            
            if sprite.rect.x >= x - 100 and sprite.rect.x <= x + 100 and sprite.rect.y >= y - 100 and sprite.rect.y <= y + 100:
                if pygame.sprite.collide_rect(self, sprite):
                    if velX > 0:
                        self.rect.right = sprite.rect.left
                        self.velX = 0
                    if velX < 0:
                        self.rect.left = sprite.rect.right
                        self.velX = 0
                    
                    if velY > 0:
                        self.rect.bottom = sprite.rect.top
                        self.on_ground = True
                        self.velY = 0
                    
                    if velY < 0:
                        self.rect.top = sprite.rect.bottom
                        self.velY = 0
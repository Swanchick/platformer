import pygame
from objects import Block, TBlock, BreakBlock
from tile import PlayerAnimation

GRAVITY = 0.3

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.frames = PlayerAnimation("src/images/characters.png", 32, 32, 14)
        self.image = self.frames.get_idle()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velX = 0
        self.velY = 0
        self.speed = 5
        self.on_ground = False
        self.jump_force = 10
        
        self.alive = True
        
        self.animation_speed = 0.2
        self.frame = 0
        self.reversed = False
    
    def death(self):
        self.alive = False
        self.velY = -self.jump_force
        self.velX = 0
        self.image = self.frames.get_death()

    def update(self, sprites: list):
        self.movement()

        self.on_ground = False

        self.rect.x += self.velX
        self.collide(sprites, self.velX, 0)

        self.rect.y += self.velY
        self.collide(sprites, 0, self.velY)

        self.animation()

        if self.rect.y >= 600 and self.alive:
            self.death()

    def animation(self):
        if not self.alive: return

        if self.velY >= 0 and self.velY < 1:
            if self.velX == 0:
                if self.reversed:
                    self.image = self.frames.get_reverse_idle()
                else:
                    self.image = self.frames.get_idle()

                self.frame = 0

            else:
                if self.frame >= 2.8:
                    self.frame = 0
                self.reversed = self.velX < 0
                
                self.frame += self.animation_speed
                image = pygame.transform.flip(self.frames.get_run()[int(self.frame)], self.reversed, False)
                self.image = image
        else:
            if self.reversed:
                self.image = self.frames.get_reverse_jump()
            else:
                self.image = self.frames.get_jump()

    def movement(self):        
        if not self.on_ground:
            self.velY += GRAVITY
        
        if not self.alive: return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velY = -self.jump_force

        if keys[pygame.K_RIGHT]:
            self.velX = self.speed
        elif keys[pygame.K_LEFT]:
            self.velX = -self.speed
        else:
            self.velX = 0
    
    def collide(self, sprites, velX, velY):
        if not self.alive: return
        
        x = self.rect.x
        y = self.rect.y
        
        sprs = filter(lambda sprite: sprite.rect.x >= x - 64 and sprite.rect.x <= x + 64 and sprite.rect.y >= y - 64 and sprite.rect.y <= y + 64, sprites)

        for sprite in sprs:
            if type(sprite) is Player: continue
            if type(sprite) is TBlock: continue

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

                    if type(sprite) is BreakBlock:
                        sprite.hit()
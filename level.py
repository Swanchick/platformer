import pygame
import json
from objects import Block
from player import Player

TILE = 50

class Level(pygame.sprite.Group):
    def build(self, path):
        file = open(path, "r").read()

        lines = file.split("\n")

        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] == "-":
                    block = Block(x * TILE, y * TILE, TILE, TILE)
                    self.add(block)
                elif lines[y][x] == "p":
                    player = Player(x * TILE, y * TILE)
                    self.player = player
                    self.add(player)
        
        self.sprites = self.sprites()
    
    def update(self):
        sprites = filter(lambda sprite: sprite.rect.x >= x - 100 and sprite.rect.x <= x + 100 and sprite.rect.y >= y - 100 and sprite.rect.y <= y + 100, self.sprites)

        player = self.player
        x = player.rect.x
        y = player.rect.y
        
        for sprite in self.sprites:
            sprite.update(self.sprites)
    
    def draw(self, surface, pos):
        x = pos[0]
        y = pos[1]

        sprites = filter(lambda sprite: sprite.rect.x >= x - 50 and sprite.rect.x <= x + 850 and sprite.rect.y >= y - 50 and sprite.rect.y <= y + 650, self.sprites)

        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(sprites, surface.blits((spr.image, spr.rect) for spr in sprites))
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, spr.rect)
        self.lostsprites = []
        dirty = self.lostsprites

        return dirty

    def get_player(self) -> Player:
        return self.player
    
    def get_player_pos(self) -> tuple:
        return (self.player.rect.x, self.player.rect.y)
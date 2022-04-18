import pygame
import json
from objects import Block, TBlock
from player import Player

TILE = 32

class Level(pygame.sprite.Group):
    def __init__(self, tiles):
        super().__init__()

        self.tiles = tiles
    
    def build(self, path):
        file = open(path, "r").read()

        lines = file.split("\n")

        for y in range(len(lines)):
            line = lines[y].split(",")
            for x in range(len(line)):
                if line[x] == "p":
                    player = Player(x * TILE, y * TILE)
                    self.player = player
                if line[x][0].isalpha():
                    tex = line[x][1:]
                    if line[x][0] == "t":
                        block = TBlock(x * TILE, y * TILE, TILE, TILE, self.tiles.get_tile(int(tex)))
                    
                    
                    self.add(block)
                else:
                    if line[x] == "-1": continue

                    block = Block(x * TILE, y * TILE, TILE, TILE, self.tiles.get_tile(int(line[x])))
                    self.add(block)

        lines.sort(key=lambda x: len(x.split(",")))
        self.lenght = len(lines[0]) * TILE

        self.add(self.player)
        
        self.sprites = self.sprites()
    
    def update(self):
        player = self.player
        x = player.rect.x
        y = player.rect.y
        d = TILE * 2

        sprites = filter(lambda sprite: sprite.rect.x >= x - d and sprite.rect.x <= x + d and sprite.rect.y >= y - d and sprite.rect.y <= y + d, self.sprites)
        
        for sprite in self.sprites:
            sprite.update(self.sprites)
    
    def draw(self, surface):
        player = self.player
        
        x = player.rect.x
        y = player.rect.y

        sx = x - 864 // 2
        ex = x + 864 // 2

        sprites = filter(lambda spr: spr.rect.x >= sx and spr.rect.x <= ex, self.sprites)

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
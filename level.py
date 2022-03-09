import pygame
import json
from objects import Block
from player import Player


class Level(pygame.sprite.Group):
    def build(self, path):
        file = open(path, "r").read()

        data = json.loads(file)

        for object in data:
            if object["class"] == "Settings":
                self.width = object["width"]
                self.height = object["height"]
                self.static_camera = object["static_camera"]
            elif object["class"] == "Player":
                player = Player(object["x"], object["y"])
                self.player = player
                self.add(player)
            elif object["class"] == "Wall":
                block = Block(object["x"], object["y"], object["width"], object["height"])
                self.add(block)
    
    def update(self):
        for sprite in self.sprites():
            sprite.update(self.sprites())
        
    def get_player(self) -> Player:
        return self.player
    
    def get_player_pos(self) -> tuple:
        return (self.player.rect.x, self.player.rect.y)
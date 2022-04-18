import pygame
import level
import ui
from objects import Block
from tile import Tilesheet


FPS = 60
RES = WIDTH, HEIGHT = (800, 600)

TILE = 32

class Game:
    def __init__(self):
        pygame.init()

        self.display = pygame.display.set_mode(RES)

        self.current_scene = 0
        self.clock = pygame.time.Clock()

    def run(self):
        self.scene()
    
    def scene_manager(self):
        if self.current_scene == 0:
            self.scene()
        
    def scene_pos(self, player_pos: tuple, screen_x: int, screen_y: int):
        pass
    
    def move_camera(self, player, lenght):
        self.scene_x = min(-player.rect.x + WIDTH // 2, 0)


    def scene(self):
        game = True

        tiles = Tilesheet("src/images/textures.jpg", TILE, TILE, 19, 12)

        lev = level.Level(tiles)
        lev.build("test.txt")

        scene = pygame.Surface((lev.lenght, HEIGHT * 2))

        self.scene_x = 0
        self.scene_y = 0

        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False

            lev.update()
            self.display.fill((0, 0, 0))
            
            self.move_camera(lev.player, lev.lenght)

            self.display.blit(scene, (self.scene_x, self.scene_y))
            scene.fill((107, 140, 255))

            lev.draw(scene)

            ui.draw_text(self.display, str(int(self.clock.get_fps())), (0, 0), 24, (0, 0, 0))

            pygame.display.flip()
            self.clock.tick(FPS)

            
if __name__ == "__main__":
    game = Game()
    game.run()
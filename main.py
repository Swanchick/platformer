import pygame
from objects import Block
import level


FPS = 60
RES = WIDTH, HEIGHT = (800, 600)

class Game:
    def __init__(self):
        pygame.init()

        self.display = pygame.display.set_mode(RES)

        self.current_scene = 0
        self.clock = pygame.time.Clock()
    
    def run(self):
        self.scene()
        
        pygame.quit()
    
    def scene_manager(self):
        if self.current_scene == 0:
            self.scene()
        
    def scene_pos(self, player_pos: tuple, screen_x: int, screen_y: int):
        pass

    def scene(self):
        game = True

        lev = level.Level()
        lev.build("test.json")

        scene = pygame.Surface((lev.width, lev.height))

        scene_x = 0
        scene_y = 0

        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
            
            self.display.fill((0, 0, 0))
            
            self.display.blit(scene, (0, 0))
            scene.fill((0, 0 ,0))
            
            lev.draw(scene)
            lev.update()

            pygame.display.flip()
            self.clock.tick(FPS)

            
if __name__ == "__main__":
    game = Game()
    game.run()
import pygame
import level
import ui
from objects import Block
from tile import Tilesheet
import os


FPS = 60
RES = WIDTH, HEIGHT = (800, 600)

TILE = 32

LEVEL_COLOR = (107, 140, 255)

class Game:
    def __init__(self):
        pygame.init()

        self.display = pygame.display.set_mode(RES)

        self.current_scene = "menu"
        self.clock = pygame.time.Clock()

        self.tiles = Tilesheet("src/images/textures.jpg", TILE, TILE, 19, 12)

    def run(self):
        self.scene_manager()

        pygame.quit()
    
    def scene_manager(self):
        work = True

        while work:
            if self.current_scene == "menu":
                self.menu()
            elif self.current_scene == "quit":
                work = False
            else:
                self.scene()
    
    def move_camera(self, player, lenght):
        self.scene_x = min(-player.rect.x + WIDTH // 2, 0)


    def scene(self):
        game = True

        lev = level.Level(self.tiles)
        lev.build(self.current_scene)

        scene = pygame.Surface((lev.lenght, HEIGHT * 2))

        self.scene_x = 0
        self.scene_y = 0

        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                    self.current_scene = "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game = False
                        self.current_scene = "menu"

            lev.update()
            self.display.fill((0, 0, 0))
            
            self.move_camera(lev.player, lev.lenght)

            self.display.blit(scene, (self.scene_x, self.scene_y))
            scene.fill(LEVEL_COLOR)

            lev.draw(scene)

            ui.draw_text(self.display, str(int(self.clock.get_fps())), (0, 0), 24, (0, 0, 0))

            pygame.display.flip()
            self.clock.tick(FPS)

    def change_level(self, level):
        self.game = False
        self.current_scene = level

    def menu(self):
        self.game = True

        files = os.listdir("src/levels/")

        text_menu = ui.TextMenu(WIDTH // 2 - 300 // 2, 0, 300, 600)
        
        for i in files:
            if i[-3:] != "lev": return

            text_menu.add(i, self.change_level, [f"src/levels/{i}"])
        
        ui_group = pygame.sprite.Group()

        ui_group.add(text_menu)

        while self.game:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.game = False
                    self.current_scene = "quit"
                
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        text_menu.up()
                    elif e.key == pygame.K_DOWN:
                        text_menu.down()
                    elif e.key == pygame.K_RETURN:
                        text_menu.click()
            
            self.display.fill(LEVEL_COLOR)

            ui_group.update()
            ui_group.draw(self.display)

            ui.draw_mario_text(self.display, "Super Mario Bros", (90, 20), 48, (255, 255, 255))

            pygame.display.flip()
            self.clock.tick(FPS)
            
if __name__ == "__main__":
    game = Game()
    game.run()
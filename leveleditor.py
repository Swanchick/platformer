import pygame
import ui
import level
from tile import Tilesheet
from player import PlayerAnimation, Player
from objects import Block, TBlock

RES = WIDTH, HEIGHT = (800, 600)
FPS = 60

TILE = 32

class Window:
    def __init__(self):
        pygame.init()

        self.display = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()

        self.tiles = Tilesheet("src/images/textures.jpg", TILE, TILE, 19, 12)
        self.playertiles = PlayerAnimation("src/images/characters.png", 32, 32, 14)

        self.camera_speed = 5

        self.block = self.tiles.tiles[0]
        self.type = "block"
    
    def choose_block(self, texture, block_type):
        if texture != '':
            self.block = texture
        
        if block_type != "":
            self.type = block_type
        
        print(self.type)

    def save(self):
        file = open("src/levels/test.lev", "w")
        
        for spr in self.lev.sprites():
            x = int(spr.rect.x / 32)
            y = int(spr.rect.y / 32)

            if type(spr) is Player:
                self.lines[y][x] = "p"
            elif type(spr) is TBlock:
                img = str(self.tiles.tiles.index(spr.image))
                
                self.lines[y][x] = f"t{img}"
            else:
                img = str(self.tiles.tiles.index(spr.image))

                self.lines[y][x] = img
        
        text = ""

        for y in range(len(self.lines)):
            line = ""
            
            for x in range(len(self.lines[y])):
                line += str(self.lines[y][x]) + ","
            
            line = line[:-1]
            line += "\n"
            text += line
        
        file.write(text)
        file.close()

    def start(self):
        
        self.lines = []
        
        for y in range(19):
            line = []
            for x in range(50):
                line.append("-1")
            self.lines.append(line)
        
        self.scene_x = 0
        self.scene_y = 0

        self.ui_elements = ui.VerticalScroll(0, HEIGHT-100, WIDTH, 100)

        save_button = ui.Button(WIDTH-100, HEIGHT-100, 100, 25, "Save", self.save, [])
        
        self.ui_elements.add(save_button)

        player_button = ui.ImageButton(0, HEIGHT-100, 50, 50, self.playertiles.get_idle(), self.choose_block, [self.playertiles.get_idle(), "player"])
        self.ui_elements.add(player_button)

        b_button = ui.Button(50, HEIGHT-100, 50, 50, "B", self.choose_block, ['', "block"])
        self.ui_elements.add(b_button)


        t_button = ui.Button(100, HEIGHT-100, 50, 50, "T", self.choose_block, ['', "tblock"])
        self.ui_elements.add(t_button)

        for i in range(len(self.tiles.tiles)):
            but = ui.ImageButton(50 * i, HEIGHT - 50, 50, 50, self.tiles.tiles[i], self.choose_block, [self.tiles.tiles[i], ""])
            self.ui_elements.add(but)

        self.constructor()

        pygame.quit()

    def camera(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.scene_x -= self.camera_speed
        
        if keys[pygame.K_a]:
            self.scene_x += self.camera_speed
        
        if keys[pygame.K_w]:
            self.scene_y += self.camera_speed
        
        if keys[pygame.K_s]:
            self.scene_y -= self.camera_speed

    def show_block(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        x = int((mouse_pos[0] - self.scene_x) / 32) * 32 
        y = int((mouse_pos[1] - self.scene_y) / 32) * 32

        image = self.block
        image = image.convert_alpha()
        image.fill((0, 0, 0, 100))

        surface.blit(image, (x, y))

    def spawn_block(self):
        mouse_pos = pygame.mouse.get_pos()

        x = int((mouse_pos[0] - self.scene_x) / 32) * 32 
        y = int((mouse_pos[1] - self.scene_y) / 32) * 32

        if self.type == "player":
            block = Player(x, y)
        elif self.type == "tblock":
            block = TBlock(x, y, 32, 32, self.block)
        else:
            block = Block(x, y, 32, 32, self.block)
        
        self.lev.add(block)

    def remove_block(self):
        mouse_pos = pygame.mouse.get_pos()

        x = int((mouse_pos[0] - self.scene_x) / 32) * 32 
        y = int((mouse_pos[1] - self.scene_y) / 32) * 32

        for sprite in self.lev.sprites():
            if sprite.rect.x == x and sprite.rect.y == y:
                self.lev.remove(sprite)

    def constructor(self):
        work = True

        self.lev = pygame.sprite.Group()
        
        scene = pygame.Surface((50 * TILE, HEIGHT))

        ui_surface = pygame.Surface((WIDTH, 150))

        while work:
            self.camera()
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    work = False
                
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        if self.ui_elements.is_hover():
                            for but in self.ui_elements.sprites():
                                but.click()
                        else:
                            self.spawn_block()
                    
                    if e.button == 3:
                        self.remove_block()

                    if e.button == 4:
                        self.ui_elements.scroll_right()
                    elif e.button == 5:
                        self.ui_elements.scroll_left()

            self.display.fill((0, 0, 0))
            self.display.blit(scene, (self.scene_x, self.scene_y))
            scene.fill((50, 50, 50))
            
            self.display.blit(ui_surface, (0, HEIGHT-100))
            ui_surface.fill((255, 255, 255))
            
            ui.draw_text(self.display, str(int(self.clock.get_fps())), (0, 0), 24, (255, 255, 255))

            self.ui_elements.draw(self.display)
            self.ui_elements.update()

            self.lev.draw(scene)

            self.show_block(scene)

            pygame.display.flip()
            self.clock.tick(FPS)
    
if __name__ == '__main__':
    win = Window()
    win.start()
import pygame


def draw_text(surface, text: str, pos: tuple, size: float, color: tuple):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    
    font_surface = font.render(text, True, color)
    surface.blit(font_surface, pos)

def draw_mario_text(surface, text: str, pos: tuple, size: float, color: tuple):
    font = pygame.font.Font("src\\font\\mario.ttf", size)

    font_surface = font.render(text, True, color)
    surface.blit(font_surface, pos)

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, func, args):
        super().__init__()
        
        self.image = pygame.Surface((width, height))
        self.image.fill((75, 75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.text = text
        self.func = func
        self.args = args

    def is_hover(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()

        x = mouse_pos[0]
        y = mouse_pos[1]

        return (x >= self.rect.x) and (x <= self.rect.x + self.width) and (y >= self.rect.y) and (y <= self.rect.y + self.height)

    def click(self):
        if not self.is_hover(): return
        
        self.func(*self.args)
    
    def update(self):
        if self.is_hover():
            self.image.fill((100, 100, 100))
        else:
            self.image.fill((75, 75, 75))
        
        draw_text(self.image, self.text, (0, 0), 24, (0, 0, 0))

class ImageButton(Button):
    def __init__(self, x, y, width, height, texture, func, args):
        super().__init__(x, y, width, height, "", func, args)

        self.texture = texture
    
    def update(self):
        if self.is_hover():
            self.image.fill((100, 100, 100))
        else:
            self.image.fill((75, 75, 75))
        
        self.image.blit(self.texture, (9, 9))

class VerticalScroll(pygame.sprite.Group):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.scrolled = 0
        self.speed = 50

    def is_hover(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()

        x = mouse_pos[0]
        y = mouse_pos[1]

        return (x >= self.x) and (x <= self.x + self.width) and (y >= self.y) and (y <= self.y + self.height)

    def scroll_right(self):
        if not self.is_hover(): return
        if self.scrolled >= 0: return


        for spr in self.sprites():
            spr.rect.x += self.speed
            self.scrolled += self.speed

    def scroll_left(self):
        if not self.is_hover(): return

        for spr in self.sprites():
            spr.rect.x -= self.speed
            self.scrolled -= self.speed
    
    def draw(self, surface):
        sprites = filter(lambda spr: spr.rect.x >= -50 and spr.rect.x <= 850, self.sprites())

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

class TextButton:
    def __init__(self, text, func, args):
        self.text = text
        self.func = func
        self.args = args
    
    def click(self):
        self.func(*self.args)

class TextMenu(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill((107, 140, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.buttons = []
        self.button = 0
    
    def add(self, text, func, args):
        button = TextButton(f"  {text}", func, args)
        self.buttons.append(button)
    
    def draw(self):
        for i in range(len(self.buttons)):
            draw_mario_text(self.image, f"- {self.buttons[i].text}" if self.button == i else f"  {self.buttons[i].text}", (0, 200+30*i), 24, (255, 255, 255))

    def up(self):
        if self.button == 0: return

        self.button -= 1

    def down(self):
        if self.button == len(self.buttons)-1: return
        
        self.button += 1

    def click(self):
        button = self.buttons[self.button]

        button.click()

    def update(self):
        self.image.fill((107, 140, 255))

        self.draw()

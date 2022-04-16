import pygame


def draw_text(surface, text: str, pos: tuple, size: float, color: tuple):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    
    font_surface = font.render(text, True, color)
    surface.blit(font_surface, pos)
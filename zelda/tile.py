import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__()
        self.image = pygame.image.load('../graphics/test')
        self.rect = self.image.get_rect(topleft = pos)

import pygame

class Level:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()
        

        # sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

    def run(self):
        pass
import numpy as np
import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.width = width
        self.height = height
        self.color = (255, 0, 255)

        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill(self.color)
        # pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])
        self.image = pygame.image.load("images/spaceShips_008.png").convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

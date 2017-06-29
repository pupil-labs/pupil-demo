import random
import numpy as np
import pygame

class Meteor(pygame.sprite.Sprite):
    def __init__(self, display_width, display_height):
        super().__init__()
        self.width = random.randrange(70, 150)
        self.height = self.width
        self.display_width = display_width
        self.display_height= display_height
        self.color = (53, 115, 255)

        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill(self.color)
        # pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])
        paths = [
            "images/spaceMeteors_001.png",
            "images/spaceMeteors_002.png",
            "images/spaceMeteors_003.png",
            "images/spaceMeteors_004.png",
        ]
        self.image = pygame.image.load(paths[random.randrange(4)]).convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image.set_colorkey((0,0,0))

        self.rect = self.image.get_rect()

        self.reset()

    def reset(self):
        self.rect.x = random.randrange(0, self.display_width - self.width)
        self.rect.y = -self.height

        self.speed = random.uniform(5, 9)
        self.direction = np.array((random.uniform(-12,12), 10))
        self.direction = self.direction / np.linalg.norm(self.direction)


    def update(self):
        # Reset if no longer in bounds
        if self.rect.y > self.display_height or self.rect.x > self.display_width or self.rect.x + self.width < 0:
            self.reset()

        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]

    # def draw(self):
    #     pygame.draw.rect(gameDisplay, meteor_color, [int(self.x), int(self.y), self.width, self.height])
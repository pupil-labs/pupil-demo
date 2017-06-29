import random
import numpy as np
import pygame
from meteor import Meteor

class Projectile(pygame.sprite.Sprite):
    def __init__(self, direction, shipx, shipy, ship_width, meteor_list, projectile_list, display_width, display_height):
        super().__init__()
        self.alive=True
        self.meteor_list = meteor_list
        self.projectile_list = projectile_list
        projectile_list.add(self)
        self.display_width = display_width
        self.display_height = display_height

        self.speed = 20
        self.direction = direction / np.linalg.norm(direction)
        self.color =  (0, 125, 125)
        self.width = 15
        self.height = 15

        choice = random.choice(list(range(1,27)) + list(range(37,41)))
        self.image = pygame.image.load("images/spaceMissiles_{0:03d}.png".format(choice)).convert()
        self.image = pygame.transform.rotate(self.image, self.ang(self.direction, np.array((1,0))) -90)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        self.rect.x = shipx + ship_width // 2
        self.rect.y = shipy


    def update(self):
        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]

        if self.rect.x > self.display_width or self.rect.x < 0 or self.rect.y > self.display_height or self.rect.y > self.display_height:
            self.projectile_list.remove(self)
            return

        blocks_hit_list = pygame.sprite.spritecollide(self, self.meteor_list, True)
        if blocks_hit_list:
            self.projectile_list.remove(self)
            for i in range(len(blocks_hit_list)):
                self.meteor_list.add(Meteor(self.display_width, self.display_height))

    def ang(self, v1, v2):
        cosang = np.dot(v1, v2)
        sinang = np.linalg.norm(np.cross(v1, v2))
        return np.rad2deg(np.arctan2(sinang, cosang))
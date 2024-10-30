import pygame
import math

class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_height, angle=0):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill((243, 216, 63))
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.screen_height = screen_height
        self.angle = angle 

    def update(self):
        radians = math.radians(self.angle) 
        self.rect.x += self.speed * math.sin(radians) 
        self.rect.y -= self.speed * math.cos(radians) 

        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            self.kill()

    @classmethod
    def create_quadrant_laser(cls, position, speed, screen_height):
        angles = [-15, 0, 15]  # Các góc bắn
        lasers = []
        for angle in angles:
            laser = cls(position, speed, screen_height, angle)
            lasers.append(laser)
        return lasers

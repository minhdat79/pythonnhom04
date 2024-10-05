import pygame
import random
from spaceship import Spaceship
from obstacle import Obstacle, grid

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height))
        self.obstacle_width = len(grid[0]) * 3  # Assuming grid[0] defines the width of one obstacle
        self.num_obstacles = 4  # Number of obstacles in a row
        self.obstacles = self.create_obstacles()

    def create_obstacles(self):
        # Calculate the total space used by all obstacles plus the gaps
        total_obstacles_width = self.num_obstacles * self.obstacle_width
        total_gap_width = self.screen_width - total_obstacles_width
        gap = total_gap_width / (self.num_obstacles + 1)  # Gaps between obstacles

        obstacles = []
        for i in range(self.num_obstacles):
            offset_x = gap + i * (self.obstacle_width + gap)  # Gap between each obstacle
            obstacle = Obstacle(offset_x, self.screen_height - 100)  # Adjust Y position as needed
            obstacles.append(obstacle)

        return obstacles

import pygame, random
from spaceship import Spaceship
from obstacle import Obstacle, grid
from Graphics.alien import Alien
from laser import Laser
class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height))
        self.obstacle_width = len(grid[0]) * 3  # Assuming grid[0] defines the width of one obstacle
        self.num_obstacles = 4  # Number of obstacles in a row
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()

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
    def create_aliens(self):
        for row in range(5):
            for column in range(11):
                x = 75 + column * 55
                y = 110 + row * 55

                if row == 0:
                    alien_type = 3
                elif row in (1,2):
                    alien_type = 2
                else:
                    alien_type =1

                alien = Alien (alien_type, x, y)
                self.aliens_group.add(alien)

    def move_aliens (self):
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <=0:
                self.aliens_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height)
            self.alien_lasers_group.add(laser_sprite)

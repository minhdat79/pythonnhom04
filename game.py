import pygame
import random
from spaceship import Spaceship
from obstacle import Obstacle, grid
from Graphics.alien import Alien
from laser import Laser
from Graphics.alien import MysteryShip
import math

class Game:
    def __init__(self, screen_width, screen_height, offset):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))
        
        self.level = 1
        self.current_level = 1
        self.obstacle_width = len(grid[0]) * 3  # Assuming grid[0] defines the width of one obstacle
        self.num_obstacles = 4  # Number of obstacles in a row
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        
        self.lasers_group = pygame.sprite.Group()

        # Set aliens movement direction
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        
        # Game state variables
        self.lives = 3
        self.run = True
        self.score = 0
        self.highscores = {1: 0, 2: 0, 3: 0}
        self.load_highscore()
        
        # Sounds
        self.explosion_sound = pygame.mixer.Sound("Sounds/explosion.ogg")
        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)

        self.set_initial_lives()

    def set_initial_lives(self):
        """Thiết lập số mạng dựa trên level."""
        if self.level == 3:
            self.lives = 6
        else:
            self.lives = 3    
            
    def set_sound_volume(self, volume):
        """Điều chỉnh âm lượng hiệu ứng âm thanh."""
        self.explosion_sound.set_volume(volume)  

    def set_music_volume(self, volume):
        """Điều chỉnh âm lượng nhạc nền."""
        pygame.mixer.music.set_volume(volume)

    def create_obstacles(self):
        total_obstacles_width = self.num_obstacles * self.obstacle_width
        total_gap_width = self.screen_width + self.offset - total_obstacles_width
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

                if self.level == 1:
                    if row == 0:
                        alien_type = 3
                    elif row in (1, 2):
                        alien_type = 2
                    else:
                        alien_type = 1
                elif self.level == 2:
                    alien_type = 1
                elif self.level == 3:
                    alien_type = 1  

                alien = Alien(alien_type, x + self.offset / 2, y)
                self.aliens_group.add(alien)

    def move_aliens(self):
        if self.level == 1 or self.level == 3:
            self.aliens_group.update(self.aliens_direction)
            alien_sprites = self.aliens_group.sprites()
            for alien in alien_sprites:
                if alien.rect.right >= self.screen_width + self.offset / 2:
                    self.aliens_direction = -1
                    self.alien_move_down(2)
                elif alien.rect.left <= self.offset / 2:
                    self.aliens_direction = 1
                    self.alien_move_down(2)
        else:
            self.move_aliens_sin_wave() 

    def move_aliens_sin_wave(self):
        for alien in self.aliens_group:
            alien.rect.x += self.aliens_direction * 2
        
            wave_offset = 1.5 * math.sin(pygame.time.get_ticks() / 200 + alien.rect.x / 100) 
            alien.rect.y += wave_offset

    # Kiểm tra va chạm với tường
        if any(alien.rect.right >= self.screen_width + self.offset / 2 for alien in self.aliens_group):
            self.aliens_direction = -1
            self.alien_move_down(2)
        elif any(alien.rect.left <= self.offset / 2 for alien in self.aliens_group):
            self.aliens_direction = 1
            self.alien_move_down(2)

    def alien_shoot_laser(self):
        if self.level == 1:
            if self.aliens_group.sprites():
                random_alien = random.choice(self.aliens_group.sprites())
                laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height, color=(255, 0, 0))
                self.alien_lasers_group.add(laser_sprite)

        elif self.level == 2:
            self.alien_shoot_laser_level_2()
        elif self.level == 3: 
            self.alien_shoot_laser_level_2() 

    def alien_shoot_laser_level_2(self):
        if self.aliens_group:
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite_center = (random_alien.rect.centerx, random_alien.rect.bottom)
        
            # Bắn 3 viên laser theo dạng quạt
            lasers = Laser.create_quadrant_laser(laser_sprite_center, -6, self.screen_height, color=(255, 0, 0)) 
            for laser in lasers:
                self.alien_lasers_group.add(laser)

    def alien_move_down(self, distance):
        for alien in self.aliens_group:
            alien.rect.y += distance

    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))
    
    
    def check_for_collisions(self):
        # Check collisions with spaceship lasers
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                if aliens_hit:
                    self.explosion_sound.play()
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        if self.level == 3:
                            laser_sprites = Laser.create_eight_direction_lasers(alien.rect.center, -6, self.screen_height, color=(255, 0, 0))
                            self.alien_lasers_group.add(*laser_sprites)
                        laser_sprite.kill()

                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    self.score += 500
                    self.explosion_sound.play()
                    self.check_for_highscore()
                    laser_sprite.kill()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        # Check collisions with alien lasers
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                    laser_sprite.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

                if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    self.game_over()

    def game_over(self):
        self.current_level = self.level  
        self.run = False

    def reset(self):
        self.run = True
        self.lives = 6 if self.level == 3 else 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0

    def check_for_highscore(self):
        if self.score > self.highscores[self.level]:
            self.highscores[self.level] = self.score
            with open(f"highscore_level_{self.level}.txt", "w") as file:
                file.write(str(self.highscores[self.level]))

    def load_highscore(self):
        for level in self.highscores.keys():
            try:
                with open(f"highscore_level_{level}.txt", "r") as file:
                    self.highscores[level] = int(file.read())
            except FileNotFoundError:
                self.highscores[level] = 0

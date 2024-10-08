import pygame, sys
from game import Game
pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700

GREY = (29, 29, 27)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Space Invader")

clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH,SCREEN_HEIGHT)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 50)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SHOOT_LASER:
            game.alien_shoot_laser()


#updating
    game.spaceship_group.update()
    game.move_aliens()

    game.alien_lasers_group.update()

    screen.fill(GREY)
    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)

    pygame.display.update()
    clock.tick(60)

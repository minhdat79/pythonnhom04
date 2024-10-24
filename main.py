import pygame, sys, random
from game import Game

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

GREY = (29, 29, 27)
YELLOW = (243, 216, 63)
WHITE = (255, 255, 255)

# Font và Text
font = pygame.font.Font("Font/monogram.ttf", 40)
menu_font = pygame.font.Font("Font/monogram.ttf", 150)
title_font = pygame.font.Font("Font/monogram.ttf", 100)

level_surface = font.render("LEVEL 01", False, YELLOW)
game_over_surface = font.render("GAME OVER", False, YELLOW)
screen_text_surface = font.render("SCORE", False, YELLOW)
highscore_text_surface = font.render("HIGH SCORE", False, YELLOW)

# Màn hình và Clock
screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
pygame.display.set_caption("Python Space Invader")
clock = pygame.time.Clock()

# Game Object
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

# Event Timer
SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

# Biến điều khiển Menu
menu_active = True  # Trạng thái menu
paused = False  # Trạng thái pause

# Tải background cho menu và game
menu_background = pygame.image.load("background.jpg").convert()
game_background = pygame.image.load("game_background.jpg").convert()

# Hàm vẽ nút
def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, WHITE, (x, y, w, h), 0, 15)  # Vẽ nút với viền bo góc
    button_text = font.render(text, True, GREY)
    screen.blit(button_text, (x + (w - button_text.get_width()) // 2, y + (h - button_text.get_height()) // 2))

# Thêm text cho hướng dẫn điều khiển
move_font = pygame.font.SysFont("Arial", 40)
move_text = move_font.render("← →: Move", True, WHITE)
shoot_font = pygame.font.SysFont("Arial", 40)
shoot_text = shoot_font.render("SPACE: Shoot", True, WHITE)
pause_font = pygame.font.SysFont("Arial", 40)
pause_text = shoot_font.render("ESC: Pause game", True, WHITE)

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if menu_active:  # Kiểm tra sự kiện trong Menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Xử lý khi nhấn nút Play hoặc Quit
                if 300 <= mouse_pos[0] <= 450 and 300 <= mouse_pos[1] <= 370:
                    menu_active = False  # Vào game
                elif 300 <= mouse_pos[0] <= 450 and 400 <= mouse_pos[1] <= 470:
                    pygame.quit()
                    sys.exit()

        elif event.type == SHOOT_LASER and game.run and not paused:
            game.alien_shoot_laser()

        elif event.type == MYSTERYSHIP and game.run and not paused:
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not game.run:
            game.reset()
        
        # Xử lý nhấn ESC để tạm dừng
        if keys[pygame.K_ESCAPE] and game.run:
            paused = not paused  # Chuyển đổi trạng thái pause

    # Hiển thị Menu
    if menu_active:
        screen.blit(menu_background, (0, 0))  # Vẽ background menu

        # Vẽ tiêu đề
        title_surface = title_font.render("Space Invader", True, YELLOW)
        screen.blit(title_surface, ((SCREEN_WIDTH + OFFSET - title_surface.get_width()) // 2, 150))

        # Vẽ nút Play và Quit
        draw_button("Play", 300, 300, 150, 70)
        draw_button("Quit", 300, 400, 150, 70)

         # Vẽ hướng dẫn điều khiển chỉ trong menu
        screen.blit(move_text, (20, SCREEN_HEIGHT + OFFSET - 110))  
        screen.blit(shoot_text, (20, SCREEN_HEIGHT + OFFSET - 60))
        screen.blit(pause_text, (20, SCREEN_HEIGHT + OFFSET - 10))

    else:  # Vòng lặp game khi menu tắt
        if not paused:  # Chỉ cập nhật game khi không bị tạm dừng
            if game.run:
                game.spaceship_group.update()
                game.move_aliens()
                game.alien_lasers_group.update()
                game.mystery_ship_group.update()
                game.check_for_collisions()

        # Vẽ background game
        screen.blit(game_background, (0, 0))

        # Vẽ UI
        pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
        pygame.draw.line(screen, YELLOW, (25, 730), (775, 730), 3)

        if game.run:
            screen.blit(level_surface, (570, 740, 50, 50))
        else:
            screen.blit(game_over_surface, (570, 740, 50, 50))

        x = 50
        for life in range(game.lives):
            screen.blit(game.spaceship_group.sprite.image, (x, 745))
            x += 50

        screen.blit(screen_text_surface, (50, 15, 50, 50))
        formatted_score = str(game.score).zfill(5)
        score_surface = font.render(formatted_score, False, YELLOW)
        screen.blit(score_surface, (50, 40, 50, 50))

        screen.blit(highscore_text_surface, (550, 15, 50, 50))
        formatted_highscore = str(game.highscore).zfill(5)
        highscore_surface = font.render(formatted_highscore, False, YELLOW)
        screen.blit(highscore_surface, (625, 40, 50, 50))

        game.spaceship_group.draw(screen)
        game.spaceship_group.sprite.lasers_group.draw(screen)

        for obstacle in game.obstacles:
            obstacle.blocks_group.draw(screen)

        game.aliens_group.draw(screen)
        game.alien_lasers_group.draw(screen)
        game.mystery_ship_group.draw(screen)

        # Hiển thị menu tạm dừng nếu trò chơi đang tạm dừng
        if paused:
            pause_surface = menu_font.render("PAUSED", True, WHITE)
            screen.blit(pause_surface, ((SCREEN_WIDTH + OFFSET - pause_surface.get_width()) // 2, 150))
            # Kích thước và khoảng cách cho nút
            button_width = 200  # Đặt chiều rộng mới cho nút
            button_height = 70  # Chiều cao cho nút
            button_spacing = 20  # Khoảng cách giữa các nút

            # Vẽ các nút với kích thước và khoảng cách mới
            draw_button("Resume", 300, 300, button_width, button_height)
            draw_button("Back to Menu", 300, 300 + button_height + button_spacing, button_width, button_height)
            draw_button("Quit", 300, 300 + 2 * (button_height + button_spacing), button_width, button_height)


            # Xử lý khi nhấn nút Resume hoặc Quit
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 450 and 300 <= mouse_pos[1] <= 370:
                    paused = False  # Tiếp tục trò chơi
                elif 300 <= mouse_pos[0] <= 450 and 400 <= mouse_pos[1] <= 470:
                    menu_active = True  # Quay về menu
                    paused = False 
                elif 300 <= mouse_pos[0] <= 450 and 500 <= mouse_pos[1] <= 570:
                    pygame.quit() # Thoát trò chơi
                    sys.exit()

    pygame.display.update()
    clock.tick(60)

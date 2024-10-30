import pygame, sys, random
from game import Game
from spaceship import Spaceship

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
level_surface_2 = font.render("LEVEL 02", False, YELLOW)
level_surface_3 = font.render("LEVEL 03", False, YELLOW)
game_over_surface = font.render("GAME OVER", False, YELLOW)
screen_text_surface = font.render("SCORE", False, YELLOW)
highscore_text_surface = font.render("HIGH SCORE", False, YELLOW)
volume_text_surface = font.render("Volume", True, YELLOW)

# Màn hình và Clock
screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
pygame.display.set_caption("Python Space Invader")
clock = pygame.time.Clock()

# Game Object
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

# Event Timer
SHOOT_LASER = pygame.USEREVENT

# Thay đổi thời gian bắn đạn dựa trên cấp độ
def set_shoot_timer(level):
    if level == 1:
        pygame.time.set_timer(SHOOT_LASER, 300)  
    elif level == 2:
        pygame.time.set_timer(SHOOT_LASER, 800)  
    elif level == 3:
        pygame.time.set_timer(SHOOT_LASER, 1030) 

set_shoot_timer(game.level)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

# Biến điều khiển Menu
menu_active = True  
level_selection_active = False  
paused = False 
name_input_active = False
settings_active = False

# Tải background cho menu và game
menu_background = pygame.image.load("background.jpg").convert()
game_background = pygame.image.load("game_background.jpg").convert()

# Điều chỉnh âm lượng
music_volume = 0.2
laser_volume = 0.2
explosion_volume = 0.2

game.set_music_volume(music_volume)
game.set_sound_volume(explosion_volume)
game.spaceship_group.sprite.set_laser_volume(laser_volume)

# Thêm các biến cho thanh Volume
volume_bar_x = 250
volume_bar_y = 300
volume_bar_width = 250
volume_bar_height = 20
volume_level = int(music_volume * 100)

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

# Hàm vẽ thanh Volume và các nút
def draw_volume_controls():
    # Vẽ thanh âm lượng
    pygame.draw.rect(screen, WHITE, (volume_bar_x, volume_bar_y, volume_bar_width, volume_bar_height))
    pygame.draw.rect(screen, YELLOW, (volume_bar_x, volume_bar_y, volume_level * 2.5, volume_bar_height))

    # Vẽ các nút + và -
    draw_button("-", volume_bar_x - 50, volume_bar_y - 10, 40, 40)
    draw_button("+", volume_bar_x + volume_bar_width + 10, volume_bar_y - 10, 40, 40)

    screen.blit(volume_text_surface, (volume_bar_x + (volume_bar_width - volume_text_surface.get_width()) // 2, volume_bar_y - 40))
# Hàm cập nhật âm lượng
def update_volume(change):
    global music_volume, laser_volume, explosion_volume, volume_level
    volume_level = min(100, max(0, volume_level + change))  # Giới hạn âm lượng từ 0 đến 100

    new_volume = volume_level / 100  # Chuyển đổi thành giá trị từ 0.0 đến 1.0
    music_volume = laser_volume = explosion_volume = new_volume

    # Áp dụng âm lượng mới cho game
    game.set_music_volume(music_volume)
    game.set_sound_volume(explosion_volume)
    game.spaceship_group.sprite.set_laser_volume(laser_volume)

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if menu_active:  # Kiểm tra sự kiện trong Menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Xử lý khi nhấn nút Play, Setting hoặc Quit
                if 300 <= mouse_pos[0] <= 450 and 250 <= mouse_pos[1] <= 320:
                    level_selection_active = True  # Vào menu chọn cấp độ
                    menu_active = False  
                elif 300 <= mouse_pos[0] <= 450 and 350 <= mouse_pos[1] <= 420:
                    settings_active = True  # Mở menu cài đặt
                    menu_active = False
                elif 300 <= mouse_pos[0] <= 450 and 450 <= mouse_pos[1] <= 520:
                    pygame.quit()
                    sys.exit()

        elif settings_active:  # Menu Cài Đặt
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Quay lại menu chính từ cài đặt
                if 300 <= mouse_pos[0] <= 450 and 600 <= mouse_pos[1] <= 670:
                    settings_active = False
                    menu_active = True

                # Kiểm tra nút - được nhấn
                elif volume_bar_x - 50 <= mouse_pos[0] <= volume_bar_x - 10 and \
                     volume_bar_y - 10 <= mouse_pos[1] <= volume_bar_y + 30:
                    update_volume(-5)  # Giảm âm lượng 5%

                # Kiểm tra nút + được nhấn
                elif volume_bar_x + volume_bar_width + 10 <= mouse_pos[0] <= volume_bar_x + volume_bar_width + 50 and \
                     volume_bar_y - 10 <= mouse_pos[1] <= volume_bar_y + 30:
                    update_volume(5)  # Tăng âm lượng 5%

        elif level_selection_active:  # Xử lý chọn cấp độ
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Chọn Level 1
                if 300 <= mouse_pos[0] <= 450 and 300 <= mouse_pos[1] <= 370:
                    game.level = 1 
                    set_shoot_timer(game.level)  
                    name_input_active = True
                    game.run = True 
                    level_selection_active = False 
                # Chọn Level 2
                elif 300 <= mouse_pos[0] <= 450 and 400 <= mouse_pos[1] <= 470:
                    game.level = 2  
                    set_shoot_timer(game.level)  
                    name_input_active = True
                    game.run = True  
                    level_selection_active = False 
                elif 300 <= mouse_pos[0] <= 450 and 500 <= mouse_pos[1] <= 570: 
                    game.level = 3  
                    set_shoot_timer(game.level)  
                    name_input_active = True
                    game.run = True  
                    level_selection_active = False 
                elif 300 <= mouse_pos[0] <= 450 and 600 <= mouse_pos[1] <= 670:
                    menu_active = True
                    level_selection_active = False

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
        draw_button("Play", 300, 250, 150, 70)
        draw_button("Setting", 300, 350, 150, 70) 
        draw_button("Quit", 300, 450, 150, 70)

         # Vẽ hướng dẫn điều khiển chỉ trong menu
        screen.blit(move_text, (20, SCREEN_HEIGHT + OFFSET - 110))  
        screen.blit(shoot_text, (20, SCREEN_HEIGHT + OFFSET - 60))
        screen.blit(pause_text, (20, SCREEN_HEIGHT + OFFSET - 10))

    elif settings_active:
        screen.blit(menu_background, (0, 0))  # Vẽ background cho cài đặt

        # Vẽ tiêu đề cho menu cài đặt
        settings_title = title_font.render("Settings", True, YELLOW)
        screen.blit(settings_title, ((SCREEN_WIDTH + OFFSET - settings_title.get_width()) // 2, 150))

        draw_volume_controls()
        draw_button("Back to Menu", 300, 600, 150, 70)

    # Hiển thị Menu Chọn Cấp Độ
    elif level_selection_active:
        screen.blit(menu_background, (0, 0))  # Vẽ background menu chọn cấp độ

        # Vẽ tiêu đề
        title_surface = title_font.render("Select Level", True, YELLOW)
        screen.blit(title_surface, ((SCREEN_WIDTH + OFFSET - title_surface.get_width()) // 2, 150))

        # Vẽ nút chọn cấp độ
        draw_button("Level 1", 300, 300, 150, 70)
        draw_button("Level 2", 300, 400, 150, 70)  
        draw_button("Level 3", 300, 500, 150, 70) 
        draw_button("Back to Menu", 300, 600, 150, 70)
     
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
            if game.level == 1:
                screen.blit(level_surface, (570, 740, 50, 50))
            elif game.level == 2:
                screen.blit(level_surface_2, (570, 740, 50, 50))
            elif game.level == 3:
                screen.blit(level_surface_3, (570, 740, 50, 50))
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
        formatted_highscore = str(game.highscores[game.level]).zfill(5)
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
            button_width = 200  
            button_height = 70 
            button_spacing = 20  

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
                    game.reset()
                    paused = False 
                elif 300 <= mouse_pos[0] <= 450 and 500 <= mouse_pos[1] <= 570:
                    pygame.quit() # Thoát trò chơi
                    sys.exit()

    pygame.display.flip()
    clock.tick(60)

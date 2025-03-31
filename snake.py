import pygame
import time
import random

pygame.init()
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zaroon's Snake Game")

black = (0, 0, 0)
white = (255, 255, 255)
gray = (50, 50, 50)
apple_red = (255, 0, 0)
dark_red = (180, 0, 0)
gold = (255, 215, 0)
obstacle_color = (100, 100, 100)

pause = False

timer_font = pygame.font.SysFont("bahnschrift", 20)
font = pygame.font.SysFont("bahnschrift", 25)
menu_font = pygame.font.SysFont("bahnschrift", 40)

highest_score = 0

def draw_background():
    win.fill(black)

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, white)
    win.blit(score_text, (10, 10))

def draw_highest_score():
    high_text = font.render(f"Highest Score: {highest_score}", True, gold)
    win.blit(high_text, (width - 200, 10))

def draw_timer(time_left):
    timer_text = timer_font.render(f"Golden Apple: {time_left}s", True, gold)
    win.blit(timer_text, (width - 180, 35))

def draw_pause_screen():
    s = pygame.Surface((width, height))
    s.set_alpha(180)
    s.fill(gray)
    win.blit(s, (0, 0))
    pause_text = menu_font.render("Paused", True, white)
    win.blit(pause_text, (width//2 - 50, height//2 - 20))
    pygame.display.update()

def countdown():
    for i in range(3, 0, -1):
        win.fill(black)
        count_text = menu_font.render(str(i), True, white)
        win.blit(count_text, (width//2 - 10, height//2 - 20))
        pygame.display.update()
        time.sleep(1)

def main_menu():
    running = True
    while running:
        win.fill(gray)
        pygame.draw.rect(win, gold, (50, 50, width-100, height-100), 5, border_radius=15)
        title = menu_font.render("Zaroon's Snake Game", True, white)
        win.blit(title, (width//2 - 120, 60))
        start_text = font.render("Press ENTER to Start", True, white)
        quit_text = font.render("Press Q to Quit", True, white)
        win.blit(start_text, (width//2 - 80, height//2 - 20))
        win.blit(quit_text, (width//2 - 50, height//2 + 20))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def gameLoop():
    global highest_score, pause
    
    game_over = False
    game_close = False
    x, y = width // 2, height // 2
    x_change, y_change = 0, 0
    snake = [[x, y]]
    length = 1
    food_x = random.randrange(0, width - 10, 10)
    food_y = random.randrange(0, height - 10, 10)
    clock = pygame.time.Clock()
    
    obstacles = [(random.randrange(0, width, 20), random.randrange(0, height, 20)) for _ in range(5)]
    
    while not game_over:
        while game_close:
            win.fill(black)
            msg = font.render("Game Over! Press C-Continue or Q-Quit", True, dark_red)
            win.blit(msg, [width / 6, height / 3])
            pygame.display.update()
            
            if length - 1 > highest_score:
                highest_score = length - 1
                
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause
                    if pause:
                        draw_pause_screen()
                    else:
                        countdown()
                elif not pause:
                    if event.key == pygame.K_LEFT and x_change == 0:
                        x_change = -10
                        y_change = 0
                    elif event.key == pygame.K_RIGHT and x_change == 0:
                        x_change = 10
                        y_change = 0
                    elif event.key == pygame.K_UP and y_change == 0:
                        y_change = -10
                        x_change = 0
                    elif event.key == pygame.K_DOWN and y_change == 0:
                        y_change = 10
                        x_change = 0
        
        if not pause:
            if x >= width or x < 0 or y >= height or y < 0:
                game_close = True
            
            x += x_change
            y += y_change
            
            snake.append([x, y])
            if len(snake) > length:
                del snake[0]
            
            draw_background()
            draw_score(length - 1)
            draw_highest_score()
            
            for ox, oy in obstacles:
                pygame.draw.rect(win, obstacle_color, (ox, oy, 20, 20))
            
            pygame.draw.ellipse(win, apple_red, (food_x, food_y, 10, 10))
            
            for segment in snake[:-1]:
                if segment == [x, y]:
                    game_close = True
            
            if [x, y] == [food_x, food_y]:
                food_x = random.randrange(0, width - 10, 10)
                food_y = random.randrange(0, height - 10, 10)
                length += 1
            
            for segment in snake:
                pygame.draw.circle(win, white, (segment[0] + 5, segment[1] + 5), 5)
            
            pygame.display.update()
            
            for ox, oy in obstacles:
                if ox <= x < ox + 20 and oy <= y < oy + 20:
                    game_close = True
            
            clock.tick(10)
    
    pygame.quit()
    quit()

main_menu()

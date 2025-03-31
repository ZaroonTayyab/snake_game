import pygame
import time
import random
pygame.init()
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zaroon's Snake Game")
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 200, 0)
blue = (50, 153, 213)
dark_blue = (25, 25, 112)
light_blue = (70, 130, 180)
apple_red = (255, 0, 0)
dark_red = (180, 0, 0)
gold = (255, 215, 0)
gray = (100, 100, 100)
font = pygame.font.SysFont("bahnschrift", 25)
menu_font = pygame.font.SysFont("bahnschrift", 40)
def draw_background():
    win.fill(dark_blue)
    for x in range(0, width, 20):
        for y in range(0, height, 20):
            pygame.draw.rect(win, light_blue, [x, y, 10, 10], border_radius=2)
def draw_score(score):
    score_text = font.render(f"Score: {score}", True, white)
    win.blit(score_text, (10, 10))
def draw_timer(time_left):
    timer_text = font.render(f"Golden Apple: {time_left}s", True, gold)
    win.blit(timer_text, (width - 180, 10))
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
    game_over = False
    game_close = False
    x, y = width // 2, height // 2
    x_change, y_change = 0, 0
    snake = []
    length = 1
    food_x = random.randrange(0, width - 10, 10)
    food_y = random.randrange(0, height - 10, 10)
    golden_apple = None
    golden_timer = 0
    clock = pygame.time.Clock()
    while not game_over:
        while game_close:
            win.fill(black)
            msg = font.render("Game Over! Press C-Continue or Q-Quit", True, red)
            win.blit(msg, [width / 6, height / 3])
            pygame.display.update()
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
                if event.key == pygame.K_LEFT:
                    x_change = -10
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = 10
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -10
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = 10
                    x_change = 0
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True
        x += x_change
        y += y_change
        draw_background()
        pygame.draw.circle(win, apple_red, (food_x + 5, food_y + 5), 5)
        pygame.draw.circle(win, dark_red, (food_x + 5, food_y + 5), 3)
        draw_score(length - 1)
        if golden_apple:
            pygame.draw.circle(win, gold, (golden_apple[0] + 5, golden_apple[1] + 5), 7)
            time_left = int(golden_timer - time.time())
            if time_left > 0:
                draw_timer(time_left)
            else:
                golden_apple = None
        elif random.randint(0, 100) < 1:
            golden_apple = (random.randrange(0, width - 10, 10), random.randrange(0, height - 10, 10))
            golden_timer = time.time() + 10  # Extended time
        snake.append([x, y])
        if len(snake) > length:
            del snake[0]
        for segment in snake:
            pygame.draw.circle(win, green, (segment[0] + 5, segment[1] + 5), 5)
        pygame.display.update()
        if x == food_x and y == food_y:
            food_x = random.randrange(0, width - 10, 10)
            food_y = random.randrange(0, height - 10, 10)
            length += 1
        if golden_apple and x == golden_apple[0] and y == golden_apple[1]:
            golden_apple = None
            length += 3 
        clock.tick(7)
    pygame.quit()
    quit()
main_menu()

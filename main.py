import pygame
import random

# Initialize Pygame / Инициализация Pygame
pygame.init()

# Screen settings / Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title and icon / Установка заголовка и иконки
pygame.display.set_caption("My Shooting Game")
icon = pygame.image.load("img/icon.png")
pygame.display.set_icon(icon)

# Load the target image / Загрузка изображения цели
target_image = pygame.image.load("img/target.png")
target_width = 80
target_height = 80

# Score panel height / Высота панели результатов
score_panel_height = 50

# Initial target position, considering the score panel / Начальное положение цели, учитывая панель результатов
target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(score_panel_height, SCREEN_HEIGHT - target_height)

# Background color / Цвет фона
color = (255, 255, 255)

# Score panel settings / Настройки панели результатов
score = 0
score_font = pygame.font.Font(None, 36)
score_color = (0, 0, 0)
score_x = 10
score_y = 10

running = True

while running:
    # Fill the background / Заполнение фона
    screen.fill(color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if target is hit / Проверка попадания по цели
            if target_x <= mouse_x <= target_x + target_width and target_y <= mouse_y <= target_y + target_height:
                # Randomize target position again, making sure it's below the score panel /
                # Случайное новое положение цели, убедившись, что она ниже панели результатов
                target_x = random.randint(0, SCREEN_WIDTH - target_width)
                target_y = random.randint(score_panel_height, SCREEN_HEIGHT - target_height)
                score += 1  # Increase score on hit / Увеличение счета при попадании

    # Display the target / Отображение цели
    screen.blit(target_image, (target_x, target_y))

    # Display the score / Отображение счета
    score_text = score_font.render(f"Score: {score}", True, score_color)
    screen.blit(score_text, (score_x, score_y))

    pygame.display.update()

pygame.quit()

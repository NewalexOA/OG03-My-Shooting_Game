import pygame
import random
import time

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

# Load the target image and set its new dimensions / Загрузка изображения цели и установка новых размеров
target_image = pygame.image.load("img/target.png").convert_alpha()
target_image = pygame.transform.scale(target_image, (80, 80))
target_width = 80
target_height = 80

# Score panel height / Высота панели результатов
score_panel_height = 50

# Initial target position, considering the score panel / Начальное положение цели, учитывая панель результатов
target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(score_panel_height, SCREEN_HEIGHT - target_height)

# Background color / Цвет фона
color = (255, 255, 255)

# Score and highscore settings / Настройки счета и рекорда
score = 0
hits = 0  # Track number of successful hits / Отслеживание количества успешных попаданий
highscore = 0
speed_highscore = 0.0  # Highscore for hits per minute / Рекорд по количеству попаданий в минуту
start_time = time.time()  # Start time of the game / Время начала игры

# Attempt to read highscore and speed highscore from file / Попытка прочитать рекорд и рекорд скорости из файла
try:
    with open("highscore.txt", "r") as f:
        scores = f.readline().split()
        highscore = int(scores[0])
        speed_highscore = float(scores[1]) if len(scores) > 1 else 0.0
except FileNotFoundError:
    highscore = 0
    speed_highscore = 0.0

# Fonts / Шрифты
result_font = pygame.font.Font(None, 24)  # Font for all result panel text / Шрифт для всего текста на панели результатов
score_color = (0, 0, 0)

# Vertical position for score display / Вертикальное положение для отображения счета
score_y = 10

running = True

while running:
    screen.fill(color)
    current_time = time.time()  # Current time for calculating hit speed / Текущее время для расчета скорости попаданий
    total_time = (current_time - start_time) / 60  # Total time in minutes / Общее время в минутах

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if target_x <= mouse_x <= target_x + target_width and target_y <= mouse_y <= target_y + target_height:
                target_x = random.randint(0, SCREEN_WIDTH - target_width)
                target_y = random.randint(score_panel_height, SCREEN_HEIGHT - target_height)
                score += 1  # Increase score on hit / Увеличение счета при попадании
                hits += 1  # Increment hits / Увеличение количества попаданий

    # Display the target / Отображение цели
    screen.blit(target_image, (target_x, target_y))

    # Display the score / Отображение счета
    score_text = result_font.render(f"Score: {score}", True, score_color)
    screen.blit(score_text, (10, score_y))

    # Calculate and display speed highscore / Расчет и отображение рекорда скорости попаданий в минуту
    speed_highscore_text = result_font.render(f"Speed High Score: {speed_highscore:.2f}", True, score_color)
    speed_highscore_x = SCREEN_WIDTH / 2 - speed_highscore_text.get_width() / 2  # Center the speed highscore text / Центрирование текста рекорда скорости
    screen.blit(speed_highscore_text, (speed_highscore_x, score_y))

    # Display the highscore / Отображение рекорда
    highscore_text = result_font.render(f"High Score: {highscore}", True, score_color)
    highscore_text_x = SCREEN_WIDTH - highscore_text.get_width() - 10  # Right align the highscore text / Выравнивание текста рекорда по правому краю
    screen.blit(highscore_text, (highscore_text_x, score_y))

    pygame.display.update()

# Update and save highscore and speed highscore regardless of score being greater / Обновление и сохранение рекорда и рекорда скорости независимо от того, превышен ли счет
if score > highscore or hits_per_minute > speed_highscore:
    with open("highscore.txt", "w") as f:
        f.write(f"{max(score, highscore)} {speed_highscore:.2f}")

pygame.quit()

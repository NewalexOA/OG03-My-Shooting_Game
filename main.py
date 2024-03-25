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

# Attempt to read hit highscore and speed highscore from file / Попытка прочитать рекорд попаданий и рекорд скорости из файла
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
timer_font = pygame.font.Font(None, 76)  # Font for the countdown timer / Шрифт для таймера обратного отсчёта
final_result_font = pygame.font.Font(None, 32)  # Font for final result display / Шрифт для отображения итоговых результатов
score_color = (0, 0, 0)

# Vertical position for score display / Вертикальное положение для отображения счета
score_y = 10

running = True
game_duration = 10  # Game duration in seconds / Продолжительность игры в секундах

while running:
    screen.fill(color)
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Check if the game duration is over / Проверка, не закончилась ли игра
    if elapsed_time >= game_duration:
        screen.fill((255, 247, 153))  # Pale yellow background for final result display / Бледно-желтый фон для отображения итоговых результатов

        hits_per_minute = hits / (elapsed_time / 60) if elapsed_time > 0 else 0
        speed_text = final_result_font.render(f"Your speed: {hits_per_minute:.2f} hits/min", True, (0, 0, 0))
        hits_text = final_result_font.render(f"Hits count: {hits}", True, (0, 0, 0))

        speed_text_rect = speed_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20))
        hits_text_rect = hits_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))

        screen.blit(speed_text, speed_text_rect)
        screen.blit(hits_text, hits_text_rect)

        pygame.display.update()

        time.sleep(5)  # Display results for 5 seconds / Отображение результатов 5 секунд
        running = False
        continue

    # Timer display / Отображение таймера
    remaining_time = int(game_duration - elapsed_time)
    timer_text = timer_font.render(f"{remaining_time}", True, (255, 0, 0))
    timer_text_rect = timer_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(timer_text, timer_text_rect.topleft)  # Рисуем текст напрямую на экран


    # Create a semi-transparent surface for the timer text / Создание полупрозрачной поверхности для текста таймера
    timer_surface = pygame.Surface((timer_text_rect.width, timer_text_rect.height))
    timer_surface.set_alpha(0)  # Set semi-transparency / Установка полупрозрачности
    timer_surface.blit(timer_text, (0, 0))  # Drawing text on the surface / Рисование текста на поверхности

    screen.blit(timer_surface, timer_text_rect.topleft)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if target_x <= mouse_x <= target_x + target_width and target_y <= mouse_y <= target_y + target_height:
                target_x = random.randint(0, SCREEN_WIDTH - target_width)
                target_y = random.randint(score_panel_height, SCREEN_HEIGHT - target_height)
                score += 1
                hits += 1

    # Display the target / Отображение цели
    screen.blit(target_image, (target_x, target_y))

    # Display the score / Отображение счета
    score_text = result_font.render(f"Score: {score}", True, score_color)
    screen.blit(score_text, (10, score_y))

    pygame.display.update()

# Update and save highscore and speed highscore if necessary / Обновление и сохранение рекорда и скоростного рекорда при необходимости
if score > highscore or hits_per_minute > speed_highscore:
    with open("highscore.txt", "w") as f:
        f.write(f"{max(score, highscore)} {max(hits_per_minute, speed_highscore):.2f}")

pygame.quit()

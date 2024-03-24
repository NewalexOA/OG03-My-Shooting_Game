import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title and icon
pygame.display.set_caption("My Shooting Game")
icon = pygame.image.load("img/icon.png")
pygame.display.set_icon(icon)

# Load the target image and set its new dimensions
target_image = pygame.image.load("img/target.png").convert_alpha()
target_image = pygame.transform.scale(target_image, (80, 80))
target_width = 80
target_height = 80

# Score panel height
score_panel_height = 50

# Initial target position, considering the score panel
target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(score_panel_height, SCREEN_HEIGHT - target_height)

# Background color
color = (255, 255, 255)

# Score and highscore settings
score = 0
hits = 0  # Track number of successful hits
highscore = 0
start_time = time.time()  # Start time of the game
hit_times = []  # Store times of hits to calculate average speed

try:
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
except FileNotFoundError:
    highscore = 0

score_font = pygame.font.Font(None, 36)
score_color = (0, 0, 0)
score_x = 10
score_y = 10

running = True

while running:
    screen.fill(color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if target_x <= mouse_x <= target_x + target_width and target_y <= mouse_y <= target_y + target_height:
                target_x = random.randint(0, SCREEN_WIDTH - target_width)
                target_y = random.randint(score_panel_height, SCREEN_HEIGHT - target_height)
                score += 1  # Increase score on hit
                hits += 1  # Increment hits
                hit_times.append(time.time())  # Record time of hit

    # Display the target
    screen.blit(target_image, (target_x, target_y))

    # Display the score
    score_text = score_font.render(f"Score: {score}", True, score_color)
    screen.blit(score_text, (score_x, score_y))

    # Display the highscore, aligned to the right
    highscore_text = score_font.render(f"High Score: {highscore}", True, score_color)
    highscore_x = SCREEN_WIDTH - highscore_text.get_width() - 10
    screen.blit(highscore_text, (highscore_x, score_y))

    # Calculate and display average hit speed if there are hits
    if hits > 0:
        avg_speed = sum(hit_times) / hits
        avg_speed_text = score_font.render(f"Avg Hit Speed: {avg_speed:.2f}s", True, score_color)
        avg_speed_x = SCREEN_WIDTH / 2 - avg_speed_text.get_width() / 2
        screen.blit(avg_speed_text, (avg_speed_x, score_y))

    pygame.display.update()

# Save highscore if score is greater
if score > highscore:
    with open("highscore.txt", "w") as f:
        f.write(str(score))

pygame.quit()

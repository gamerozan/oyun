import pygame
import random

# =====================
# AYARLAR
# =====================
WIDTH, HEIGHT = 500, 600
FPS = 60

ROAD_COLOR = (50, 50, 50)
CAR_COLOR = (0, 200, 255)
ENEMY_COLOR = (255, 50, 50)
TEXT_COLOR = (255, 255, 255)

# =====================
# PYGAME BAŞLAT
# =====================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Araba Oyunu 🚗🔥")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# =====================
# OYUNCU
# =====================
player = pygame.Rect(220, 480, 60, 100)
player_speed = 6

# =====================
# DÜŞMANLAR
# =====================
enemy_count = 4
enemy_speed = 4
enemies = []

for _ in range(enemy_count):
    x = random.randint(50, 390)
    y = random.randint(-600, -100)
    enemies.append(pygame.Rect(x, y, 60, 100))

# =====================
# SKOR
# =====================
score = 0
speed_timer = 0

# =====================
# ANA OYUN DÖNGÜSÜ
# =====================
running = True
while running:
    clock.tick(FPS)
    speed_timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 50:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < 450:
        player.x += player_speed

    # -----------------
    # DÜŞMAN HAREKETİ
    # -----------------
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemy.y = random.randint(-200, -100)
            enemy.x = random.randint(50, 390)
            score += 1

        if player.colliderect(enemy):
            running = False

    # -----------------
    # HIZ ARTIŞI
    # -----------------
    if speed_timer > 300:
        enemy_speed += 0.5
        speed_timer = 0

    # -----------------
    # ÇİZİM
    # -----------------
    screen.fill((0, 150, 0))  # çimen
    pygame.draw.rect(screen, ROAD_COLOR, (50, 0, 400, HEIGHT))

    pygame.draw.rect(screen, CAR_COLOR, player)
    for enemy in enemies:
        pygame.draw.rect(screen, ENEMY_COLOR, enemy)

    score_text = font.render(f"Skor: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()


import pygame
import sys
import random
import csv
import os

# pygame başlatma
pygame.init()

# Ekran boyutları
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Yılan Oyunu")

# Renkler
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Font
font = pygame.font.SysFont('arial', 30)

# Yılanın başlangıç parametreleri
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction
speed = 10

# Yiyecek (food) başlangıç parametreleri
food_pos = [
    random.randrange(5, (screen_width - 5) // 10) * 10,
    random.randrange(5, (screen_height - 5) // 10) * 10
]
food_spawn = True

# Puan
score = 0

sp = 15

# Oyun saati
clock = pygame.time.Clock()

# Skor dosyası
score_file = "scores.csv"

# Skorları okuma fonksiyonu
def read_scores():
    if not os.path.exists(score_file):
        return []
    with open(score_file, mode='r') as file:
        reader = csv.reader(file)
        return list(reader)

# Skorları yazma fonksiyonu
def write_score(player_name, player_id, score):
    scores = read_scores()
    updated = False
    for row in scores:
        if row[1] == player_id:
            if int(row[2]) < score:
                row[2] = str(score)
            updated = True
            break

    if not updated:
        scores.append([player_name, player_id, str(score)])

    with open(score_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(scores)

# Oyun başlatma fonksiyonu (start_game)
def start_game(player_name, player_id):
    global snake_pos, snake_body, food_pos, food_spawn, score, direction, change_to
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction
    food_pos = [
        random.randrange(5, (screen_width - 5) // 10) * 10,
        random.randrange(5, (screen_height - 5) // 10) * 10
    ]
    food_spawn = True
    score = 0

   

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Yılanın yönünü kontrol et
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Yılanın başını hareket ettir
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Yılanın vücudunu hareket ettir
        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 10
            food_spawn = False
        else:
            snake_body.pop()

        # Yeni yemek doğurulması
        
        if not food_spawn:
            food_pos = [
                random.randrange(5, (screen_width - 5) // 10) * 10,
                random.randrange(5, (screen_height - 5) // 10) * 10
            ]
            food_spawn = True

         

        # Ekranı temizle
        screen.fill(black)

        # Yılanın kenara çarpıp çarpmadığını kontrol et
        if snake_pos[0] < 0 or snake_pos[0] >= screen_width or snake_pos[1] < 0 or snake_pos[1] >= screen_height:
            game_over(player_name, player_id)

        # Yılanın kendi gövdesine çarpıp çarpmadığını kontrol et
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over(player_name, player_id)

        

        # Yılanı çiz
        for block in snake_body:
            pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], 10, 10))

        # Yemeği çiz
        pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Ekranın kenarlarını çiz (100 puan sonrası)
        if score >= 100:
            pygame.draw.rect(screen, white, pygame.Rect(0, 0, screen_width, 10))  # Üst kenar
            pygame.draw.rect(screen, white, pygame.Rect(0, 0, 10, screen_height))  # Sol kenar
            pygame.draw.rect(screen, white, pygame.Rect(screen_width - 10, 0, 10, screen_height))  # Sağ kenar
            pygame.draw.rect(screen, white, pygame.Rect(0, screen_height - 10, screen_width, 10))  # Alt kenar

        # Puanı yazdır
        score_text = font.render(f"Puan: {score}", True, white)
        screen.blit(score_text, [10, 10])

        # Ekranı güncelle
        pygame.display.update()

        # Oyun hızını ayarla
        clock.tick(sp)



# Oyun bittiğinde geri dönme fonksiyonu
def game_over(player_name, player_id):
    global score
    screen.fill(black)
    
    # Oyun bitti metni
    game_over_text = font.render("Oyun Bitti! Yeni Oyun (Y) / Çıkış (Q)", True, red)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_text, game_over_rect)

    # Skoru göster
    score_text = font.render(f"Puan: {score}", True, white)
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 1.5))
    screen.blit(score_text, score_rect)

    # Skorları kaydet
    write_score(player_name, player_id, score)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Çıkış
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_y:  # Yeni oyun başlat
                    waiting_for_input = False
                    start_game(player_name, player_id)  # Yeni oyunu başlat
                    return  # Yeni oyun başlatıldı, döngüyü sonlandır

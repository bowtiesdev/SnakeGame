import pygame
import sys
import random

# pygame başlatma
pygame.init()

# Ekran boyutları
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Yılan Oyunu")

# Yılanın başlangıç parametreleri
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

# Yılanın hareket yönü
direction = 'RIGHT'
change_to = direction

# Yılanın hızı
speed = 10

# Renkler
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
gray = (169, 169, 169)

# Yiyecek (food) başlangıç parametreleri
food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
food_spawn = True

# Puan
score = 0

# Engeller
obstacles = []

# Oyun saati
clock = pygame.time.Clock()

# Engelleri oluşturma fonksiyonu
def create_obstacles():
    global obstacles
    obstacle_length = random.randint(5, 15)  # Engelin uzunluğu 3 ile 7 arasında
    orientation = random.choice(['horizontal', 'vertical', 'L'])  # Engel yatay, dikey veya L şeklinde olabilir

    # Engel başlangıç pozisyonu
    start_x = random.randrange(1, (screen_width // 10)) * 10
    start_y = random.randrange(1, (screen_height // 10)) * 10

    new_obstacle = []

    if orientation == 'horizontal':
        for i in range(obstacle_length):
            new_obstacle.append([start_x + i * 10, start_y])
    elif orientation == 'vertical':
        for i in range(obstacle_length):
            new_obstacle.append([start_x, start_y + i * 10])
    elif orientation == 'L':
        for i in range(obstacle_length):
            if i < obstacle_length // 2:
                new_obstacle.append([start_x + i * 10, start_y])  # Yatay kısmı
            else:
                new_obstacle.append([start_x + (obstacle_length // 2) * 10, start_y + (i - obstacle_length // 2) * 10])  # Dikey kısmı

    obstacles.append(new_obstacle)

# Yılanın hareketini kontrol eden fonksiyon
def oyun():
    global direction, change_to, snake_pos, snake_body, food_pos, food_spawn, score, obstacles

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
            snake_pos[1] -= speed
        if direction == 'DOWN':
            snake_pos[1] += speed
        if direction == 'LEFT':
            snake_pos[0] -= speed
        if direction == 'RIGHT':
            snake_pos[0] += speed

        # Yılanın vücudunu hareket ettir
        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 10
            food_spawn = False  # Yılan yediği zaman yeni yemek doğurulacak
        else:
            snake_body.pop()

        # Yeni yemek doğurulması
        if not food_spawn:
            food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
        food_spawn = True

        # Engelleri oluştur
        if score % 100 == 0 and len(obstacles) < (score // 100):  # Her 10 yemek yediğinde yeni engel ekle
            create_obstacles()

        # Ekranı temizle
        screen.fill(black)

        # Yılanın kenara çarpıp çarpmadığını kontrol et
        if snake_pos[0] < 0 or snake_pos[0] >= screen_width or snake_pos[1] < 0 or snake_pos[1] >= screen_height:
            game_over()

        # Yılanın kendi gövdesine çarpıp çarpmadığını kontrol et
        for block in snake_body[1:]:  # Yılanın başı hariç tüm gövdeyi kontrol et
            if snake_pos == block:
                game_over()

        # Yılanı çiz
        for block in snake_body:
            pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], 10, 10))

        # Yemeği çiz
        pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Engelleri çiz
        for obstacle in obstacles:
            for block in obstacle:
                pygame.draw.rect(screen, gray, pygame.Rect(block[0], block[1], 10, 10))

        # Puanı yazdır
        font = pygame.font.SysFont('arial', 20)
        score_text = font.render("Puan: " + str(score), True, white)
        screen.blit(score_text, [0, 0])

        # Ekranı güncelle
        pygame.display.update()

        # Oyun hızını ayarla
        clock.tick(15)

# Oyun bittiğinde çağrılacak fonksiyon

# Oyun bittiğinde çağrılacak fonksiyon
def game_over():
    font = pygame.font.SysFont('arial', 50)
    game_over_text = font.render("Oyun Bitti! Q: Çıkış Y: Yeni Oyun", True, red)
    screen.blit(game_over_text, [screen_width // 4, screen_height // 3])
    pygame.display.update()

    # Kullanıcıdan yeni oyun veya çıkış seçeneği al
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
                    reset_game()
                    waiting_for_input = False

# Oyunu sıfırlama fonksiyonu
def reset_game():
    global snake_pos, snake_body, food_pos, food_spawn, score, obstacles, direction, change_to
    # Yılanın başlangıç durumu
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction
    food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
    food_spawn = True
    score = 0
    obstacles = []


# Oyun başlatma
if __name__ == "__main__":
    oyun()

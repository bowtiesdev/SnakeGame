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

# Önce tüm global değişkenleri tanımlayalım
def init_globals(start_level=1):
    global snake_pos, snake_body, food_pos, score, direction, change_to, maze_walls, food_spawn, game_started, current_level
    global base_speed, current_speed, speed_multiplier, key_press_time, speed_up_delay
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [0, 0]
    score = (start_level - 1) * 150
    direction = 'STOP'
    change_to = direction
    maze_walls = []
    food_spawn = True
    game_started = False
    current_level = start_level
    base_speed = 15  # Temel FPS
    current_speed = base_speed  # Mevcut FPS
    speed_multiplier = 1.8  # Hız artış çarpanı
    key_press_time = 0  # Tuşa basılma zamanı
    speed_up_delay = 350  # Hızlanma için gereken süre (0.75 saniye = 750 ms)

# Yılanın hızı
speed = 10

# Renkler
black = pygame.Color(18, 18, 18)        # Koyu arka plan
white = pygame.Color(236, 240, 241)     # Duvarlar için açık gri
green = pygame.Color(46, 204, 113)      # Yılan gövdesi
green_head = pygame.Color(39, 174, 96)  # Yılan başı
red = pygame.Color(231, 76, 60)         # Yem rengi
wall_color = pygame.Color(52, 73, 94)   # Labirent duvarları

# Yiyecek (food) başlangıç parametreleri
food_spawn = True

# Engeller
obstacles = []

# Oyun saati
clock = pygame.time.Clock()

# Oyun başlangıcında
def main():
    # Komut satırı argümanlarını kontrol et
    start_level = 1  # Varsayılan seviye
    
    if len(sys.argv) > 1:
        try:
            requested_level = int(sys.argv[1])
            if 1 <= requested_level <= 5:
                start_level = requested_level
            else:
                print("Uyarı: Seviye 1-5 arasında olmalıdır. Varsayılan seviye 1 kullanılıyor.")
        except ValueError:
            print("Uyarı: Geçersiz seviye numarası. Varsayılan seviye 1 kullanılıyor.")
    
    pygame.init()
    init_globals(start_level)
    maze_walls = create_maze(start_level)
    init_game()
    oyun()

def init_game():
    global snake_pos, snake_body, food_pos, score, maze_walls, direction, change_to
    
    # Başlangıç pozisyonunu güvenli bir yere ayarla
    snake_pos = [100, 100]  # Labirentin içinde güvenli bir başlangıç noktası
    snake_body = [[100, 100], [90, 100], [80, 100]]
    direction = 'RIGHT'
    change_to = direction
    
    # Labirenti oluştur
    maze_walls = create_maze(current_level)
    
    # İlk yemeği yerleştir
    place_food()
    score = 0

def oyun():
    global snake_pos, snake_body, food_pos, score, direction, change_to, maze_walls, food_spawn
    global game_started, current_speed, base_speed, key_press_time
    
    while True:
        current_time = pygame.time.get_ticks()  # Mevcut zaman
        keys = pygame.key.get_pressed()
        
        # Yön tuşlarının durumunu kontrol et
        if ((keys[pygame.K_RIGHT] and direction == 'RIGHT') or
            (keys[pygame.K_LEFT] and direction == 'LEFT') or
            (keys[pygame.K_UP] and direction == 'UP') or
            (keys[pygame.K_DOWN] and direction == 'DOWN')):
            
            # Tuşa ilk kez basıldığında zamanı kaydet
            if key_press_time == 0:
                key_press_time = current_time
            
            # 0.75 saniye geçtiyse hızı artır
            if current_time - key_press_time >= speed_up_delay:
                current_speed = base_speed * speed_multiplier
        else:
            # Tuş bırakıldığında zamanı ve hızı sıfırla
            key_press_time = 0
            current_speed = base_speed
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                    game_started = True
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                    game_started = True
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                    game_started = True
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                    game_started = True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYUP:
                # Tuş bırakıldığında zamanı ve hızı sıfırla
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    key_press_time = 0
                    current_speed = base_speed
        
        # Yılan sadece oyun başladıysa hareket eder
        if game_started:
            # Yön değişimlerini kontrol et
            if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'
                
            # Yılanın hareketini güncelle
            if direction == 'UP':
                snake_pos[1] -= 10
            if direction == 'DOWN':
                snake_pos[1] += 10
            if direction == 'LEFT':
                snake_pos[0] -= 10
            if direction == 'RIGHT':
                snake_pos[0] += 10
                
            # Yılanın gövdesini güncelle
            snake_body.insert(0, list(snake_pos))
            
            # Çarpışma kontrolü
            # Labirent duvarlarıyla çarpışma
            if snake_pos in maze_walls:
                game_over()
                return
            
            # Ekran sınırlarıyla çarpışma
            if (snake_pos[0] < 0 or snake_pos[0] > screen_width-10 or
                snake_pos[1] < 0 or snake_pos[1] > screen_height-10):
                game_over()
                return
            
            # Kendi vücuduyla çarpışma
            for segment in snake_body[1:]:
                if snake_pos == segment:
                    game_over()
                    return
            
            # Yemi yeme kontrolü
            if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
                score += 10
                food_spawn = False
                check_level_up()  # Seviye kontrolü
            else:
                snake_body.pop()
            
            if not food_spawn:
                place_food()
                food_spawn = True
        
        draw_game()
        pygame.time.Clock().tick(current_speed)

def draw_snake_segment(surface, position, is_head=False):
    # Yılan segmentini çiz
    x, y = position
    segment_size = 10
    
    if is_head:
        # Yılan başı - daha büyük ve farklı renk
        pygame.draw.circle(surface, green_head, (x + 5, y + 5), 6)
        # Gözler
        pygame.draw.circle(surface, black, (x + 3, y + 3), 2)
        pygame.draw.circle(surface, black, (x + 7, y + 3), 2)
    else:
        # Yılan gövdesi - yuvarlak segmentler
        pygame.draw.circle(surface, green, (x + 5, y + 5), 5)

def draw_food(surface, position):
    # Yemi çiz - elma şeklinde
    x, y = position
    
    # Ana kırmızı daire
    pygame.draw.circle(surface, red, (x + 5, y + 5), 5)
    
    # Yaprak (yeşil üçgen)
    leaf_points = [
        (x + 5, y),      # Üst
        (x + 2, y + 3),  # Sol
        (x + 8, y + 3)   # Sağ
    ]
    pygame.draw.polygon(surface, green, leaf_points)

def draw_game():
    screen.fill(black)
    
    # Labirent duvarlarını çiz
    for wall in maze_walls:
        pygame.draw.rect(screen, wall_color, pygame.Rect(wall[0], wall[1], 10, 10))
        pygame.draw.rect(screen, white, pygame.Rect(wall[0], wall[1], 10, 10), 1)
    
    # Yılanı çiz
    for i, pos in enumerate(snake_body):
        draw_snake_segment(screen, pos, is_head=(i == 0))
    
    # Yemi çiz
    draw_food(screen, food_pos)
    
    show_score()
    pygame.display.flip()

# Oyun bittiğinde çağrılacak fonksiyon
def game_over():
    global snake_pos, snake_body, food_pos, score, direction, change_to, maze_walls
    
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Oyun Bitti! Skor: ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (screen_width/2, screen_height/4)
    
    restart_surface = my_font.render('Yeniden başlatmak için Y\'ye basın', True, white)
    restart_rect = restart_surface.get_rect()
    restart_rect.midtop = (screen_width/2, screen_height/2)
    
    screen.fill(black)
    screen.blit(game_over_surface, game_over_rect)
    screen.blit(restart_surface, restart_rect)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    # Oyunu yeniden başlat
                    init_globals()  # Global değişkenleri sıfırla
                    init_game()     # Oyunu başlat
                    oyun()          # Oyun döngüsünü başlat
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

def create_maze(level):
    walls = []
    
    # Dış duvarlar
    for x in range(0, screen_width, 10):
        walls.append([x, 0])
        walls.append([x, screen_height - 10])
    for y in range(0, screen_height, 10):
        walls.append([0, y])
        walls.append([screen_width - 10, y])
    
    if level == 1:
        # Seviye 1 aynı
        for x in range(200, 400, 10):
            walls.append([x, 200])
        for y in range(200, 400, 10):
            walls.append([400, y])
            
    elif level == 2:
        # Seviye 2 - geçiş boşlukları 30px
        for x in range(200, 600, 10):
            if x < 385 or x > 415:  # 30px boşluk
                walls.append([x, 150])
                walls.append([x, 450])
        
        for y in range(150, 450, 10):
            if y < 285 or y > 315:  # 30px boşluk
                walls.append([200, y])
                walls.append([600, y])
            
    elif level == 3:
        # Seviye 3 - "Artı" şeklinde engel, 30px boşluklar
        # Yatay çizgi
        for x in range(100, 700, 10):
            if x < 385 or x > 415:  # 30px boşluk
                walls.append([x, 300])
        
        # Dikey çizgi
        for y in range(100, 500, 10):
            if y < 285 or y > 315:  # 30px boşluk
                walls.append([400, y])
                
        # Köşelerde küçük engeller
        for i in range(50):
            walls.append([150 + i*10, 150])
            walls.append([600 + i*10, 150])
            walls.append([150 + i*10, 450])
            walls.append([600 + i*10, 450])
            
    elif level == 4:
        # Seviye 4 aynı
        for i in range(0, 5):
            x = 150 + i * 120
            for y in range(100, 500, 10):
                if i % 2 == 0:
                    walls.append([x, y])
                else:
                    if y < 200 or y > 400:
                        walls.append([x, y])
                        
    elif level == 5:
        # # şekli - yılan için uygun geçiş boşlukları ile
        
        # Merkez noktaları
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Yatay çizgiler (üç adet)
        y_positions = [150, center_y, 450]  # Üst, orta ve alt çizgiler
        for y in y_positions:
            for x in range(200, 600, 10):
                # Her yatay çizgide üç geçiş boşluğu (25-30px)
                if (x < 285 or                  # Sol kısım
                    (x > 315 and x < 485) or    # Orta kısım
                    x > 515):                   # Sağ kısım
                    # Her 50 pikselde bir 25-30px'lik geçiş boşluğu bırak
                    if not (285 <= x <= 315 or  # Sol geçiş
                           385 <= x <= 415 or   # Orta sol geçiş
                           485 <= x <= 515):    # Sağ geçiş
                        walls.append([x, y])
        
        # Dikey çizgiler (iki adet)
        x_positions = [300, 500]  # Sol ve sağ dikey çizgiler
        for x in x_positions:
            for y in range(150, 450, 10):
                # Her dikey çizgide üç geçiş boşluğu
                if not (200 <= y <= 230 or      # Üst geçiş
                       285 <= y <= 315 or       # Orta geçiş
                       370 <= y <= 400):        # Alt geçiş
                    walls.append([x, y])
    
    return walls

def place_food():
    global food_pos
    margin = 40  # Kenarlardan uzaklık (4 birim = 40 piksel)
    
    while True:
        # Kenarlardan margin kadar uzakta rastgele pozisyon seç
        food_pos = [
            random.randrange(margin, screen_width - margin, 10),
            random.randrange(margin, screen_height - margin, 10)
        ]
        
        # Yemeğin labirent duvarlarına veya yılanın üzerine denk gelmediğinden emin ol
        if food_pos not in maze_walls and food_pos not in snake_body:
            break

def show_score():
    # Skor gösterimini güzelleştir
    score_font = pygame.font.SysFont('arial', 20)
    level_font = pygame.font.SysFont('arial', 16)
    
    # Skor
    score_surface = score_font.render(f'Skor: {score}', True, white)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)
    
    # Seviye
    level_surface = level_font.render(f'Seviye: {current_level}', True, white)
    level_rect = level_surface.get_rect()
    level_rect.topleft = (10, 35)
    
    # Ekrana çiz
    screen.blit(score_surface, score_rect)
    screen.blit(level_surface, level_rect)

def check_level_up():
    global current_level, score, maze_walls, snake_pos, direction, change_to, game_started
    
    # Her 150 puanda bir seviye atlama kontrolü
    if score > 0 and score % 150 == 0:
        show_level_up_screen()
        new_level = min(5, (score // 150) + 1)
        
        if new_level != current_level:
            print(f"Seviye yükseltiliyor: {current_level} -> {new_level}")
            current_level = new_level
            maze_walls = create_maze(current_level)
            
            # Yılanın mevcut uzunluğunu koru, sadece pozisyonunu sıfırla
            current_length = len(snake_body)
            snake_pos = [100, 50]
            
            # Yılanın gövdesini mevcut uzunlukta yeniden oluştur
            snake_body.clear()
            for i in range(current_length):
                snake_body.append([100 - (i * 10), 50])
            
            direction = 'STOP'
            change_to = direction
            game_started = False
            
            place_food()

def show_level_up_screen():
    screen.fill(black)
    font = pygame.font.SysFont('times new roman', 50)
    
    level_text = font.render(f'Seviye {current_level} Tamamlandı!', True, green)
    next_level_text = font.render(f'Seviye {min(5, current_level + 1)} için ENTER\'a basın', True, white)
    score_text = font.render(f'Skor: {score}', True, white)
    
    screen.blit(level_text, (screen_width/2 - level_text.get_rect().width/2, screen_height/3))
    screen.blit(next_level_text, (screen_width/2 - next_level_text.get_rect().width/2, screen_height/2))
    screen.blit(score_text, (screen_width/2 - score_text.get_rect().width/2, 2*screen_height/3))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Ana programı başlat
if __name__ == "__main__":
    main()
import pygame
import time
import random

# Pygame'i başlat
pygame.init()

# Renkler
beyaz = (255, 255, 255)
siyah = (0, 0, 0)
kirmizi = (213, 50, 80)
yesil = (0, 255, 0)
mavi = (50, 153, 213)

# Ekran boyutu
genislik = 600
yukseklik = 400

# Pencereyi oluştur
displey = pygame.display.set_mode((genislik, yukseklik))
pygame.display.set_caption('Yılan Oyunu')

# Saat (FPS kontrolü için)
clock = pygame.time.Clock()

# Yılanın hızı
yilan_hizi = 15

# Yılanın boyutları
yilan_boyut = 10

# Yazı fontu
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Skoru gösteren fonksiyon
def skor_goster(skor):
    value = score_font.render("Skor: " + str(skor), True, siyah)
    displey.blit(value, [0, 0])

# Yılanı çizme fonksiyonu
def yilan_ciz(yilan_boyut, yilan_listesi):
    for x in yilan_listesi:
        pygame.draw.rect(displey, yesil, [x[0], x[1], yilan_boyut, yilan_boyut])

# Mesaj gösterme fonksiyonu
def mesaj_goster(msg, color):
    mesaj = font_style.render(msg, True, color)
    displey.blit(mesaj, [genislik / 6, yukseklik / 3])

# Ana oyun döngüsü
def oyun():
    oyun_bitti = False
    oyun_bitti_mi = False

    x1 = genislik / 2
    y1 = yukseklik / 2

    x1_degisiklik = 0
    y1_degisiklik = 0

    yilan_listesi = []
    uzunluk = 1

    # Yiyecek yerini rastgele oluştur
    yemekx = round(random.randrange(0, genislik - yilan_boyut) / 10.0) * 10.0
    yemeki = round(random.randrange(0, yukseklik - yilan_boyut) / 10.0) * 10.0

    while not oyun_bitti:

        while oyun_bitti_mi:
            displey.fill(mavi)
            mesaj_goster("Oyunu Kaybettiniz! Q-Quit veya C-Yeni Oyun", kirmizi)
            skor_goster(uzunluk - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        oyun_bitti = True
                        oyun_bitti_mi = False
                    if event.key == pygame.K_c:
                        oyun()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                oyun_bitti = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_degisiklik = -yilan_boyut
                    y1_degisiklik = 0
                elif event.key == pygame.K_RIGHT:
                    x1_degisiklik = yilan_boyut
                    y1_degisiklik = 0
                elif event.key == pygame.K_UP:
                    y1_degisiklik = -yilan_boyut
                    x1_degisiklik = 0
                elif event.key == pygame.K_DOWN:
                    y1_degisiklik = yilan_boyut
                    x1_degisiklik = 0

        if x1 >= genislik or x1 < 0 or y1 >= yukseklik or y1 < 0:
            oyun_bitti_mi = True
        x1 += x1_degisiklik
        y1 += y1_degisiklik
        displey.fill(mavi)
        pygame.draw.rect(displey, siyah, [yemekx, yemeki, yilan_boyut, yilan_boyut])
        yilan_head = []
        yilan_head.append(x1)
        yilan_head.append(y1)
        yilan_listesi.append(yilan_head)
        if len(yilan_listesi) > uzunluk:
            del yilan_listesi[0]

        for x in yilan_listesi[:-1]:
            if x == yilan_head:
                oyun_bitti_mi = True

        yilan_ciz(yilan_boyut, yilan_listesi)
        skor_goster(uzunluk - 1)

        pygame.display.update()

        # Yılan yemek yediğinde
        if x1 == yemekx and y1 == yemeki:
            yemekx = round(random.randrange(0, genislik - yilan_boyut) / 10.0) * 10.0
            yemeki = round(random.randrange(0, yukseklik - yilan_boyut) / 10.0) * 10.0
            uzunluk += 1

        clock.tick(yilan_hizi)

    pygame.quit()
    quit()

# Oyunu başlat, first
oyun()

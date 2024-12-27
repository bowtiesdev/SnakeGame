import pygame
import sys
import random
from game import start_game

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Yılan Oyunu")

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

font = pygame.font.SysFont('arial', 30)

def generate_unique_id():
    return ''.join([random.choice('0123456789') for _ in range(8)])

def show_start_screen():
    input_box = pygame.Rect(screen_width // 4, screen_height // 3, 400, 50)
    active = False
    text = ''
    clock = pygame.time.Clock()

    while True:
        screen.fill(black)

        title_text = font.render("Yılan Oyunu - Lütfen İsminizi Girin", True, white)
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(title_text, title_rect)

        pygame.draw.rect(screen, blue if active else white, input_box, 2)

        txt_surface = font.render(text, True, white)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_name = text
                    player_id = generate_unique_id()
                    start_game(player_name, player_id)
                    return
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)

        clock.tick(30)

if __name__ == "__main__":
    show_start_screen()

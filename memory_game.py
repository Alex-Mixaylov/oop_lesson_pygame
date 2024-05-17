import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Основные параметры окна
GRID_SIZE = 6  # Размер сетки 6x6
CARD_SIZE = 50
MARGIN = 10
SCREEN_WIDTH = GRID_SIZE * (CARD_SIZE + MARGIN) - MARGIN
SCREEN_HEIGHT = GRID_SIZE * (CARD_SIZE + MARGIN) - MARGIN

# Установим размеры экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра на память")

# Создадим карты
def create_deck():
    symbols = list(range(1, (GRID_SIZE * GRID_SIZE // 2) + 1)) * 2
    random.shuffle(symbols)
    deck = []
    for row in range(GRID_SIZE):
        deck_row = []
        for col in range(GRID_SIZE):
            deck_row.append(symbols.pop())
        deck.append(deck_row)
    return deck

# Рисование карты
def draw_card(screen, symbol, x, y, show):
    rect = pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)
    if show:
        pygame.draw.rect(screen, WHITE, rect)
        font = pygame.font.Font(None, 36)
        text = font.render(str(symbol), True, BLACK)
        text_rect = text.get_rect(center=(x + CARD_SIZE // 2, y + CARD_SIZE // 2))
        screen.blit(text, text_rect)
    else:
        pygame.draw.rect(screen, GRAY, rect)

# Основной цикл игры
def main():
    clock = pygame.time.Clock()
    deck = create_deck()
    revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    first_card = None
    second_card = None
    matched_pairs = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    col = x // (CARD_SIZE + MARGIN)
                    row = y // (CARD_SIZE + MARGIN)
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                        if not revealed[row][col]:
                            if first_card is None:
                                first_card = (row, col)
                                revealed[row][col] = True
                            elif second_card is None:
                                second_card = (row, col)
                                revealed[row][col] = True

        if first_card and second_card:
            row1, col1 = first_card
            row2, col2 = second_card
            if deck[row1][col1] == deck[row2][col2]:
                matched_pairs += 1
            else:
                pygame.time.wait(500)
                revealed[row1][col1] = False
                revealed[row2][col2] = False
            first_card = None
            second_card = None

        screen.fill(BLACK)

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * (CARD_SIZE + MARGIN)
                y = row * (CARD_SIZE + MARGIN)
                draw_card(screen, deck[row][col], x, y, revealed[row][col])

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

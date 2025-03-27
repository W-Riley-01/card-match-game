import pygame
import random
import sys

# Init Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Match Game")
FONT = pygame.font.SysFont('arial', 20)
BIG_FONT = pygame.font.SysFont('arial', 32)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
GREEN = (34, 139, 34)
RED = (200, 0, 0)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)

# Card dimensions
CARD_WIDTH = 120
CARD_HEIGHT = 180

# Clock
clock = pygame.time.Clock()

def generate_deck():
    royal = ['Ace', 'King', 'Queen', 'Jack']
    suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
    deck = [f"{v} of {s}" for s in suits for v in list(map(str, range(2,11))) + royal]
    random.shuffle(deck)
    return deck

def check_match(card1, card2):
    return card1.split()[0] == card2.split()[0]

def reset_game():
    deck = generate_deck()
    half1 = deck[::2]
    half2 = deck[1::2]
    return half1, half2, [], random.choice([True, False])

def draw_card(x, y, card_text, glow=False):
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    pygame.draw.rect(SCREEN, YELLOW if glow else LIGHT_GRAY, rect, border_radius=12)
    pygame.draw.rect(SCREEN, BLACK, rect, 3, border_radius=12)
    text = FONT.render(card_text, True, BLACK)
    text_rect = text.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
    SCREEN.blit(text, text_rect)

def draw_text(text, x, y, font=FONT, color=BLACK):
    SCREEN.blit(font.render(text, True, color), (x, y))

def animate_card(card_text, from_y, to_y, x=WIDTH//2 - CARD_WIDTH//2):
    steps = 20
    delta = (to_y - from_y) / steps
    for i in range(steps):
        SCREEN.fill(WHITE)
        draw_game_state()
        draw_card(x, from_y + delta*i, card_text)
        pygame.display.flip()
        clock.tick(60)

# Initial game state
plyr_a, plyr_b, board, curr_plyr = reset_game()
status = "Press SPACE to play a turn"
plyr_a_score = 0
plyr_b_score = 0

def draw_game_state():
    # Background
    SCREEN.fill(WHITE)

    # Player Decks
    draw_text(f"Player A Deck: {len(plyr_a)}", 50, HEIGHT - 50)
    draw_text(f"Player B Deck: {len(plyr_b)}", 50, 20)

    # Score
    draw_text(f"Score - A: {plyr_a_score} | B: {plyr_b_score}", 600, 20, FONT, GREEN)

    # Board cards
    if len(board) >= 1:
        draw_card(WIDTH//2 - CARD_WIDTH//2, HEIGHT//2 - CARD_HEIGHT//2, board[-1])
    if len(board) >= 2:
        draw_card(WIDTH//2 - CARD_WIDTH//2 - 140, HEIGHT//2 - CARD_HEIGHT//2, board[-2], glow=check_match(board[-1], board[-2]))

    # Status
    draw_text(status, 50, HEIGHT//2 + 100, BIG_FONT, BLUE)

    # Help text
    draw_text("SPACE = Play Turn | R = Reset | Q = Quit", 50, HEIGHT - 25, FONT, RED)

running = True

while running:
    draw_game_state()
    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

            elif event.key == pygame.K_r:
                plyr_a, plyr_b, board, curr_plyr = reset_game()
                status = "Game reset!"

            elif event.key == pygame.K_SPACE:
                if len(plyr_a) == 0 or len(plyr_b) == 0:
                    winner = "A" if len(plyr_b) == 0 else "B"
                    if winner == "A":
                        plyr_a_score += 1
                    else:
                        plyr_b_score += 1
                    status = f"Player {winner} wins the round! Press R to restart."
                    continue

                if curr_plyr:
                    card = plyr_a.pop()
                    animate_card(card, HEIGHT - CARD_HEIGHT - 20, HEIGHT//2 - CARD_HEIGHT//2)
                    board.append(card)
                    if len(board) >= 2 and check_match(board[-1], board[-2]):
                        status = "Player A found a match!"
                        plyr_a.extend(board)
                        random.shuffle(plyr_a)
                        board.clear()
                        curr_plyr = True
                    else:
                        curr_plyr = False
                        status = "Player A played a card."
                else:
                    card = plyr_b.pop()
                    animate_card(card, 20, HEIGHT//2 - CARD_HEIGHT//2)
                    board.append(card)
                    if len(board) >= 2 and check_match(board[-1], board[-2]):
                        status = "Player B found a match!"
                        plyr_b.extend(board)
                        random.shuffle(plyr_b)
                        board.clear()
                        curr_plyr = False
                    else:
                        curr_plyr = True
                        status = "Player B played a card."

pygame.quit()
sys.exit()

import asyncio
import pygame
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1000, 1000
TITLE_WIDTH = WIDTH
TITLE_HEIGHT = 100
TITLE_FONT_SIZE = 50
TITLE_COLOR = (255, 255, 255)
FOOTER_HEIGHT = TITLE_HEIGHT
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 200
BODY_HEIGHT = HEIGHT - TITLE_HEIGHT - FOOTER_HEIGHT

LINE_WIDTH = 10
LINE_WIDTH_2 = 5
WIN_LINE_WIDTH = 15
SQUARE_SIZE = 200
BOARD_WIDTH = 3 * SQUARE_SIZE + 4 * LINE_WIDTH
BOARD_HEIGHT = 3 * SQUARE_SIZE + 4 * LINE_WIDTH
BOARD_LEFT_MARGIN = (WIDTH - BOARD_WIDTH) // 2
# BOARD_TOP_MARGIN = TITLE_HEIGHT + TITLE_HEIGHT
BOARD_TOP_MARGIN = TITLE_HEIGHT + (BODY_HEIGHT - BOARD_HEIGHT) // 2
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

FOOTER_TOP_MARGIN = HEIGHT - FOOTER_HEIGHT
# RGB
"""
  color: rgb(107, 230, 224);
  color: rgb(162, 107, 230); 
  color: rgb(230, 106, 112);
  color: rgb(174, 230, 106);
"""
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
BG_COLOR = (107, 230, 224)
BUTTON_BG_COLOR = pygame.Color(0, 0, 0)
BUTTON_BG_COLOR.hsla = (177, 71, 50, 1)
BUTTON_HOVER_BG_COLOR = pygame.Color(0, 0, 0)
BUTTON_HOVER_BG_COLOR.hsla = (177, 71, 70, 1)
BUTTON_BORDER_RADIUS = 10
# TITLE_BG_COLOR = (162, 107, 230)
TITLE_BG_COLOR = (95, 30, 174)
FOOTER_BG_COLOR = TITLE_BG_COLOR
TITLE_COLOR = WHITE
BOARD_COLOR = (113, 125, 141)
X_COLOR = (230, 106, 112)
O_COLOR = (174, 230, 106)
# BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
LINE_COLOR = BG_COLOR
LINE_COLOR = (255, 255, 255)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

arial_30 = pygame.font.Font("arial.ttf", size=30)
arial_30_bold = pygame.font.SysFont("arial", 30, bold=True)


def create_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TIC TAC TOE")
    screen.fill(BG_COLOR)
    return screen


def draw_title(screen):
    # title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
    title_font = arial_30_bold
    title_text = title_font.render("TIC TAC TOE", True, TITLE_COLOR)
    title_rect = title_text.get_rect(center=(TITLE_WIDTH // 2, TITLE_HEIGHT // 2))
    pygame.draw.rect(screen, TITLE_BG_COLOR, (0, 0, TITLE_WIDTH, TITLE_HEIGHT))
    screen.blit(title_text, title_rect)


def create_button(action=None):
    left = (WIDTH - BUTTON_WIDTH) // 2
    top = FOOTER_TOP_MARGIN + (FOOTER_HEIGHT - BUTTON_HEIGHT) // 2
    button = Button(
        text="Reset Game",
        left=left,
        top=top,
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        font=arial_30_bold,
        text_color=WHITE,
        button_color=BUTTON_BG_COLOR,
        button_hover_color=BUTTON_HOVER_BG_COLOR,
        border_radius=20,
        action=action,
    )
    return button


def draw_footer(screen, button=None):
    pygame.draw.rect(
        screen,
        FOOTER_BG_COLOR,
        (0, FOOTER_TOP_MARGIN, WIDTH, FOOTER_HEIGHT),
    )
    if button:
        button.draw(screen)


def draw_board(screen):
    screen.fill(BG_COLOR)
    # draw a filled rectangle before the lines
    pygame.draw.rect(
        screen,
        BOARD_COLOR,
        (BOARD_LEFT_MARGIN, BOARD_TOP_MARGIN, BOARD_WIDTH, BOARD_HEIGHT),
    )
    x = BOARD_LEFT_MARGIN
    y = BOARD_TOP_MARGIN + LINE_WIDTH_2
    # draw horizontal lines
    for row in range(BOARD_ROWS + 1):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (x, y),
            (x + BOARD_WIDTH, y),
            LINE_WIDTH,
        )
        y += SQUARE_SIZE + LINE_WIDTH

    # draw vertical lines
    # y = BOARD_TOP_MARGIN
    x = BOARD_LEFT_MARGIN + LINE_WIDTH_2
    y = BOARD_TOP_MARGIN
    for col in range(BOARD_COLS + 1):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (x, y),
            (x, y + BOARD_HEIGHT),
            LINE_WIDTH,
        )
        x += SQUARE_SIZE + LINE_WIDTH


class Button:
    def __init__(
        self,
        top,
        left,
        width,
        height,
        text,
        font=None,
        text_color=BLACK,
        button_color=BUTTON_BG_COLOR,
        button_hover_color=BUTTON_HOVER_BG_COLOR,
        border_radius=BUTTON_BORDER_RADIUS,
        action=None,
    ):
        self.rect = pygame.Rect(
            left,
            top,
            width,
            height,
        )
        self.text = text
        if font:
            self.font = font
        else:
            self.font = pygame.font.SysFont("arial", 30, bold=True)
        self.text_color = text_color
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.border_radius = border_radius
        self.action = action
        self.color = button_color
        self.hover_color = button_hover_color
        self.is_hovered = False

    def set_action(self, action):
        self.action = action

    def draw(self, surface):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(
            surface, current_color, self.rect, border_radius=self.border_radius
        )

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    # return True if the hover state changes
    def redraw(self, event):
        is_hovered = False
        if event.type == pygame.MOUSEMOTION:
            is_hovered = self.rect.collidepoint(event.pos)
            if is_hovered != self.is_hovered:
                self.is_hovered = is_hovered
                return True
        elif (
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        ):  # Left mouse button
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if (
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        ):  # Left mouse button
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()


class Square:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.xy1 = (x, y)
        self.xy2 = (x + size, y + size)
        self.size = size
        # marker can be None, "X", or "O"
        self.marker = None
        # when 3 markers are in a straight line
        self.highlight = False

    def point_in_square(self, x, y):
        return (
            x > self.x
            and x < self.x + self.size
            and y > self.y
            and y < self.y + self.size
        )

    def draw(self, screen):
        if not self.marker:
            return

        if self.highlight:
            color = BG_COLOR
        else:
            color = BLACK
        pygame.draw.rect(
            screen,
            color,
            (self.x, self.y, self.size, self.size),
        )
        if self.marker == "X":
            start = (self.x + SPACE, self.y + SPACE)
            end = (self.x + self.size - SPACE, self.y + self.size - SPACE)
            pygame.draw.line(screen, X_COLOR, start, end, CROSS_WIDTH)
            start = (self.x + self.size - SPACE, self.y + SPACE)
            end = (self.x + SPACE, self.y + self.size - SPACE)
            pygame.draw.line(screen, X_COLOR, start, end, CROSS_WIDTH)
        elif self.marker == "O":
            pygame.draw.circle(
                screen,
                O_COLOR,
                (self.x + self.size // 2, self.y + self.size // 2),
                CIRCLE_RADIUS,
                CIRCLE_WIDTH,
            )


class Board:
    def __init__(self):
        self.squares = [[None] * 3 for _ in range(3)]
        # create Square objects and store them in the 2D list
        for row in range(3):
            for col in range(3):
                x = BOARD_LEFT_MARGIN + col * (SQUARE_SIZE + LINE_WIDTH) + LINE_WIDTH
                y = BOARD_TOP_MARGIN + row * (SQUARE_SIZE + LINE_WIDTH) + LINE_WIDTH
                square = Square(x, y, SQUARE_SIZE)
                self.squares[row][col] = square

    def reset(self):
        for row in range(3):
            for col in range(3):
                self.squares[row][col].marker = None
                self.squares[row][col].highlight = False


def handle_click(x, y, board):
    for row in range(3):
        for col in range(3):
            square = board.squares[row][col]
            if square.point_in_square(x, y):
                # return row, col
                return square
    return None


def draw_markers(board, screen):
    for row in range(3):
        for col in range(3):
            square = board.squares[row][col]
            square.draw(screen)


def check_win(board):
    for row in range(3):
        if (
            board.squares[row][0].marker
            == board.squares[row][1].marker
            == board.squares[row][2].marker
        ):
            if not board.squares[row][0].marker:
                continue
            # add highlight to the winning row
            for col in range(3):
                board.squares[row][col].highlight = True
            return board.squares[row][0].marker
    for col in range(3):
        if (
            board.squares[0][col].marker
            == board.squares[1][col].marker
            == board.squares[2][col].marker
        ):
            if not board.squares[0][col].marker:
                continue
            # add highlight to the winning column
            for row in range(3):
                board.squares[row][col].highlight = True
            return board.squares[0][col].marker
    if (
        board.squares[0][0].marker
        == board.squares[1][1].marker
        == board.squares[2][2].marker
    ):
        if not board.squares[0][0].marker:
            return
        # add highlight to the diagonal
        for row in range(3):
            board.squares[row][row].highlight = True
        return board.squares[0][0].marker
    if (
        board.squares[0][2].marker
        == board.squares[1][1].marker
        == board.squares[2][0].marker
    ):
        if not board.squares[0][2].marker:
            return
        # add highlight to the diagonal
        for row in range(3):
            board.squares[row][2 - row].highlight = True
        return board.squares[0][2].marker
    return None


async def main():

    board = Board()
    screen = create_screen()
    draw_board(screen)
    draw_title(screen)
    button = create_button(action=board.reset)
    draw_footer(screen, button)
    pygame.display.flip()
    running = True
    current_marker = "X"
    game_started = False
    winner = None
    while running:

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()
        for event in pygame.event.get():
            # Check if the user closed the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                # running = False
            elif event.type == pygame.KEYDOWN:
                if game_started:
                    game_started = True  # Set the flag to True to avoid calling start_screen repeatedly
                    continue  # Skip the rest of the loop until the game has started

        update = False
        keys = pygame.key.get_pressed()
        # q quits the game
        if keys[pygame.K_q]:
            running = False
        elif not winner and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                x, y = event.pos
                square = handle_click(x, y, board)
                if square and square.marker is None:
                    square.marker = current_marker
                    current_marker = "O" if current_marker == "X" else "X"
                    update = True
                button.handle_event(event)
        if button.redraw(event):
            update = True

        if update:
            draw_board(screen)
            draw_title(screen)
            draw_footer(screen, button)
            winner = check_win(board)
            draw_markers(board, screen)
            if winner:
                print(f"Player {winner} wins!")
            pygame.display.flip()
        await asyncio.sleep(0)  # Let other tasks run


# This is the program entry point
asyncio.run(main())
# if __name__ == "__main__":
#     run()

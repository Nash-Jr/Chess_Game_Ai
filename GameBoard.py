from pygame.locals import (
    MOUSEBUTTONUP,
    MOUSEBUTTONDOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)
import pygame
import sys
import numpy as np


def convert_to_notation(row, col):
    file = chr(97 + col)
    rank = str(8 - row)
    return file + rank


def convert_from_notation(notation):
    file = notation[0]
    rank = notation[1]
    col = ord(file) - 97
    row = 8 - int(rank)
    return (row, col)


pieces_paths = {
    "w_king": r"C:\Users\nacho\New folder\Chess\Chess_Pieces\Chess_klt60.png",
    "w_queen": r"C:\Users\nacho\New folder\Chess\Chess_Pieces\Chess_qlt60.png",
    "w_bishop": r"C:\Users\nacho\New folder\Chess\Chess_Pieces\Chess_blt60.png",
    "w_knight": r"C:\Users\nacho\New folder\Chess\Chess_Pieces\Chess_nlt60.png",
    "w_rook": r"C:\Users\nacho\New folder\Chess\Chess_Pieces\Chess_rlt60.png",
    "w_pawn": r"C:\Users\nacho\New folder\Chess\Chess_Pieces\Chess_plt60.png",
    "b_king": r"C:\Users\nacho\New folder\Chess\Chess_Pieces\Chess_kdt60.png",
    "b_queen": r"C:\Users\nacho\New folder\Chess\Chess_Pieces\Chess_qdt60.png",
    "b_bishop": r"C:\Users\nacho\New folder\Chess\Chess_Pieces\Chess_bdt60.png",
    "b_knight": r"C:\Users\nacho\New folder\Chess\Chess_Pieces\Chess_ndt60.png",
    "b_rook": r"C:\Users\nacho\New folder\Chess\Chess_Pieces\Chess_rdt60.png",
    "b_pawn": r"C:\Users\nacho\New folder\Chess\Chess_Pieces\Chess_pdt60.png",
}


class Piece_Movement:
    def __init__(self, type, colour, position, pieces_dict):
        self.type = type
        self.colour = colour
        self.Position = position
        self.pieces_dict = pieces_dict
        self.image = None
        self.load_image()

    def load_image(self):
        piece_key = f"{self.colour}_{self.type}"
        if piece_key in self.pieces_dict:
            image_path = self.pieces_dict[piece_key]
            self.image = pygame.image.load(image_path).convert_alpha()

        else:
            raise ValueError(f"No image path found for {piece_key}")

    def can_capture(self, board, start_pos, end_pos):
        if 0 <= end_pos[0] < 8 and 0 <= end_pos[1] < 8:
            if board[end_pos[0]][end_pos[1]] is not None:
                if board[end_pos[0]][end_pos[1]].colour != self.colour:
                    return True
        return False

    def is_valid_move(self, board, start_pos, end_pos):
        if self.type == "pawn":
            if not (0 <= end_pos[0] < 8 and 0 <= end_pos[1] < 8):
                return False

            if self.colour == "b":
                if end_pos[0] == start_pos[0] + 1:
                    if board[end_pos[0]][end_pos[1]] is None:
                        return True

                elif start_pos[0] == 1 and end_pos[0] == start_pos[0] + 2:
                    if board[start_pos[0] + 1][end_pos[1]] is None and board[end_pos[0]][end_pos[1]] is None:
                        return True

                elif abs(start_pos[1] - end_pos[1]) == 1 and start_pos[0] + 1 == end_pos[0]:
                    if self.can_capture(board, start_pos, end_pos):
                        return True

            if self.colour == "w":
                if end_pos[0] == start_pos[0] - 1:
                    if board[end_pos[0]][end_pos[1]] is None:
                        return True

                elif start_pos[0] == 6 and end_pos[0] == start_pos[0] - 2:
                    if board[start_pos[0] - 1][end_pos[1]] is None and board[end_pos[0]][end_pos[1]] is None:
                        return True

                elif abs(start_pos[1] - end_pos[1]) == 1 and start_pos[0] - 1 == end_pos[0]:
                    if self.can_capture(board, start_pos, end_pos):
                        return True

        if self.type == 'Rook':
            if self.colour == 'b':

                if start_pos[0] == end_pos[0]:  # It's a vertical move
                    if end_pos[0] - start_pos[0] > 0:
                        step = 1
                    else:
                        step = -1

                    for row in range(start_pos[0] + step, end_pos[0], step):
                        if board[row][start_pos[1]] is not None:
                            return False
                step = 1 if start_pos[1] < end_pos[1] else -1
                for col in range(start_pos[1] + step, end_pos[1], step):
                    pass  # Placeholder for obstacle-checking logic
            elif start_pos[1] == end_pos[1]:  # It's a vertical move
                step = 1 if start_pos[0] < end_pos[0] else -1
                for row in range(start_pos[0] + step, end_pos[0], step):
                    pass  # Placeholder for obstacle-checking logic
            else:
                return False  # Invalid move (not horizontal or vertical)


pygame.init()
WINDOW_SIZE = 650
SQUARE_SIZE = WINDOW_SIZE // 8

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))


def draw_board():
    for row in range(8):
        for col in range(8):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            if (col + row) % 2 == 0:
                pygame.draw.rect(screen, (255, 255, 255),
                                 (x, y, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, (128, 128, 128),
                                 (x, y, SQUARE_SIZE, SQUARE_SIZE))


pieces = {}
for key, value in pieces_paths.items():
    loaded_images = pygame.image.load(value).convert_alpha()
    loaded_images = pygame.transform.scale(
        loaded_images, (SQUARE_SIZE, SQUARE_SIZE))
    pieces[key] = loaded_images


board = [
    [Piece_Movement("rook", "b", (0, 0), pieces_paths), Piece_Movement("knight", "b", (0, 1), pieces_paths), Piece_Movement("bishop", "b", (0, 2), pieces_paths), Piece_Movement("queen", "b", (0, 3), pieces_paths),
        Piece_Movement("king", "b", (0, 4), pieces_paths), Piece_Movement("bishop", "b", (0, 5), pieces_paths), Piece_Movement("knight", "b", (0, 6), pieces_paths), Piece_Movement("rook", "b", (0, 7), pieces_paths)],
    [Piece_Movement("pawn", "b", (1, 0), pieces_paths), Piece_Movement("pawn", "b", (1, 1), pieces_paths), Piece_Movement("pawn", "b", (1, 2), pieces_paths), Piece_Movement("pawn", "b", (1, 3), pieces_paths),
        Piece_Movement("pawn", "b", (1, 4), pieces_paths), Piece_Movement("pawn", "b", (1, 5), pieces_paths), Piece_Movement("pawn", "b", (1, 6), pieces_paths), Piece_Movement("pawn", "b", (1, 7), pieces_paths)],
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [Piece_Movement("pawn", "w", (6, 0), pieces_paths), Piece_Movement("pawn", "w", (6, 1), pieces_paths), Piece_Movement("pawn", "w", (6, 2), pieces_paths), Piece_Movement("pawn", "w", (6, 3), pieces_paths),
        Piece_Movement("pawn", "w", (6, 4), pieces_paths), Piece_Movement("pawn", "w", (6, 5), pieces_paths), Piece_Movement("pawn", "w", (6, 6), pieces_paths), Piece_Movement("pawn", "w", (6, 7), pieces_paths)],
    [Piece_Movement("rook", "w", (7, 0), pieces_paths), Piece_Movement("knight", "w", (7, 1), pieces_paths), Piece_Movement("bishop", "w", (7, 2), pieces_paths), Piece_Movement("queen", "w", (7, 3), pieces_paths),
        Piece_Movement("king", "w", (7, 4), pieces_paths), Piece_Movement("bishop", "w", (7, 5), pieces_paths), Piece_Movement("knight", "w", (7, 6), pieces_paths), Piece_Movement("rook", "w", (7, 7), pieces_paths)],
]


selected_p = None
running = True
selected_square = None
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

        # Process mouse clicks
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            col = pos[0] // SQUARE_SIZE
            row = pos[1] // SQUARE_SIZE
            if selected_square is not None and selected_square == (row, col):
                selected_square = None  # Deselect the square

            else:
                if isinstance(board[row][col], Piece_Movement):  # Select the piece
                    selected_square = (row, col)

    # draw the board with the updated state
    draw_board()
    for row_idx, row in enumerate(board):
        for col_idx, piece in enumerate(row):
            if selected_square is not None:
                selected_row, selected_col = selected_square
                if row_idx == selected_row and col_idx == selected_col:
                    pygame.draw.rect(screen, (200, 230, 0),
                                     (col_idx * SQUARE_SIZE, row_idx * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Draw the piece on the board
            if isinstance(piece, Piece_Movement):
                x = col_idx * SQUARE_SIZE
                y = row_idx * SQUARE_SIZE
                piece_key = f"{piece.colour}_{piece.type}"
                screen.blit(pieces[piece_key], (x, y))

    pygame.display.flip()


pygame.quit()

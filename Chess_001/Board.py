import pygame
import chess
import pygame.mixer
import time

# Initialize Pygame
pygame.init()

# Load the moving sound
pygame.mixer.init()
moving_sound = pygame.mixer.Sound('sounds/moving_pieces.mp3')

# Set up display
WIDTH, HEIGHT = 500, 600
BOARD_SIZE = min(WIDTH, HEIGHT - 100)
screen = None

def main1():
    global screen, WIDTH, HEIGHT, BOARD_SIZE
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Resizable Chess Game')

# Define constants
HIGHLIGHT_COLOR = (250, 213, 65)
WHITE = (232, 227, 227)
BLACK = (26, 176, 39)
GRAY = (128, 128, 128)

# Load images
piece_images = {}

def load_images(square_size):
    pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['w', 'b']
    for color in colors:
        for piece in pieces:
            try:
                image = pygame.image.load(f'/home/goku/Desktop/ROUGH/python/Chess_001/images/{color}_{piece}.png')
                piece_images[f'{color}_{piece}'] = pygame.transform.scale(image, (square_size, square_size))
            except pygame.error as e:
                print(f'Failed to load image for {color}_{piece}: {e}')

# Function to draw the chessboard
def draw_board(screen, board, square_size, selected_square, highlighted_moves):
    for row in range(7, -1, -1):
        for col in range(8):
            rect = pygame.Rect(col * square_size, (7 - row) * square_size, square_size, square_size)
            color = WHITE if (row + col) % 2 == 0 else BLACK
            if selected_square and col == selected_square % 8 and row == selected_square // 8:
                color = HIGHLIGHT_COLOR
            pygame.draw.rect(screen, color, rect)
            piece = board.piece_at(chess.square(col, row))
            if piece:
                piece_color = 'w' if piece.color == chess.WHITE else 'b'
                piece_type = {chess.PAWN: 'pawn', chess.ROOK: 'rook', chess.KNIGHT: 'knight',
                              chess.BISHOP: 'bishop', chess.QUEEN: 'queen', chess.KING: 'king'}[piece.piece_type]
                piece_key = f'{piece_color}_{piece_type}'
                if piece_key in piece_images:
                    piece_image = piece_images[piece_key]
                    screen.blit(piece_image, rect.topleft)
                if piece_type == 'king' and board.is_check():
                    if (piece.color == chess.WHITE and board.turn == chess.WHITE) or (piece.color == chess.BLACK and board.turn == chess.BLACK):
                        pygame.draw.rect(screen, (255, 0, 0), rect, width=3)
            for move in highlighted_moves:
                if col == move % 8 and row == move // 8:
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, width=3)

    # Draw A-H labels
    font = pygame.font.Font(None, int(square_size * 0.4))
    for col in range(8):
        label_color = WHITE if col % 2 == 1 else BLACK
        label = font.render(chr(ord('A') + col), True, label_color)
        screen.blit(label, (col * square_size + 2, BOARD_SIZE + -20))

    # Draw 1-8 labels
    for row in range(8):
        label_color = BLACK if (row % 2 == 1) else WHITE
        label = font.render(str(8-row), True, label_color)
        screen.blit(label, (2, row * square_size + 2))

# Function to get the square from a position
def get_square_from_pos(pos, square_size):
    x, y = pos
    return chess.square(x // square_size, 7 - y // square_size)

# Function to get legal moves
def get_legal_moves(board):
    return [move for move in board.legal_moves]

# Function to move a piece
def move_piece(board, start_square, end_square):
    move = chess.Move(start_square, end_square)
    if move in board.legal_moves:
        board.push(move)
        moving_sound.play()
        return True
    return False

# Functions to check game state
def is_checkmate(board): return board.is_checkmate()
def is_stalemate(board): return board.is_stalemate()
def is_check(board): return board.is_check()
def is_insufficient_material(board): return board.is_insufficient_material()
def is_threefold_repetition(board): return board.can_claim_threefold_repetition()
def is_fifty_move_rule(board): return board.can_claim_fifty_moves()


def ask_rematch():
    font = pygame.font.Font(None, 36)
    
    # Define the message
    text = font.render("CheckMate! Rematch ??", True, (0, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    # Define the dimensions of the message box
    message_box_width = 300
    message_box_height = 180
    
    # Calculate the position based on width and height
    message_box_rect = pygame.Rect((WIDTH - message_box_width) // 2, (HEIGHT - message_box_height) // 2, message_box_width, message_box_height)

    # Create a semi-transparent surface for the message box
    semi_transparent_surface = pygame.Surface((message_box_rect.width, message_box_rect.height))
    semi_transparent_surface.fill((255, 255, 255))  # Fill with white
    semi_transparent_surface.set_alpha(200)  # Set transparency level (0-255)
    
    # Draw the semi-transparent surface
    screen.blit(semi_transparent_surface, message_box_rect.topleft)  

    # Draw the message text
    screen.blit(text, text_rect)

    # Draw the buttons
    yes_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 100, 50)  # Yes button
    no_button = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2, 100, 50)  # No button

    pygame.draw.rect(screen, (0, 255, 0), yes_button)  # Draw Yes button
    pygame.draw.rect(screen, (255, 0, 0), no_button)  # Draw No button

    yes_text = font.render("Yes", True, (0, 0, 0))
    yes_text_rect = yes_text.get_rect(center=yes_button.center)
    screen.blit(yes_text, yes_text_rect)

    no_text = font.render("No", True, (0, 0, 0))
    no_text_rect = no_text.get_rect(center=no_button.center)
    screen.blit(no_text, no_text_rect)

    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    return True
                elif no_button.collidepoint(event.pos):
                    return False

# Main game loop
def main2():
    global WIDTH, HEIGHT, BOARD_SIZE, screen
    while True:
        board = chess.Board()
        selected_square = None
        highlighted_moves = []
        turn = chess.WHITE
        move_history = []
        redo_stack = []
        start_time = time.time()

        while True:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.VIDEORESIZE:
                        WIDTH, HEIGHT = event.size
                        BOARD_SIZE = min(WIDTH, HEIGHT - 100)
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if undo_button.collidepoint(pos):
                            pygame.mixer.Sound.play(moving_sound)  # Play sound for Undo
                        elif redo_button.collidepoint(pos):
                            pygame.mixer.Sound.play(moving_sound)
                        x, y = pygame.mouse.get_pos()
                        square_size = BOARD_SIZE // 8
                        
                        # Check if undo button is clicked
                        if 10 <= x <= 110 and HEIGHT - 90 <= y <= HEIGHT - 50:
                            if move_history:
                                redo_stack.append(board.pop())
                                move_history.pop()
                                turn = chess.BLACK if turn == chess.WHITE else chess.WHITE
                                selected_square = None
                                highlighted_moves = []
                        # Check if redo button is clicked
                        elif 120 <= x <= 220 and HEIGHT - 90 <= y <= HEIGHT - 50:
                            if redo_stack:
                                move = redo_stack.pop()
                                board.push(move)
                                move_history.append(move)
                                turn = chess.BLACK if turn == chess.WHITE else chess.WHITE
                                selected_square = None
                                highlighted_moves = []
                        elif y < BOARD_SIZE:
                            square = get_square_from_pos((x, y), square_size)
                        
                            if selected_square is not None:
                                if move_piece(board, selected_square, square):
                                    move_history.append(board.move_stack[-1])
                                    redo_stack.clear()  # Clear redo stack after a new move
                                    selected_square = None
                                    highlighted_moves = []

                                    # Check for end conditions
                                    if is_checkmate(board):
                                        print("Checkmate! Game over.")
                                        if ask_rematch():
                                            return main2()
                                        else:
                                            pygame.quit()
                                            return
                                    elif is_stalemate(board) or is_insufficient_material(board) or \
                                         is_threefold_repetition(board) or is_fifty_move_rule(board):
                                        print("Draw! The game is a draw.")
                                        if ask_rematch():
                                            return main2()
                                        else:
                                            pygame.quit()
                                            return
                                    elif is_check(board):
                                        print("Check!")

                                    turn = chess.BLACK if turn == chess.WHITE else chess.WHITE
                                else:
                                    selected_square = square
                                    highlighted_moves = [move.to_square for move in get_legal_moves(board) if move.from_square == selected_square]
                            else:
                                if board.piece_at(square) and board.piece_at(square).color == turn:
                                    selected_square = square
                                    highlighted_moves = [move.to_square for move in get_legal_moves(board) if move.from_square == selected_square]

                # Draw the board and pieces
                square_size = BOARD_SIZE // 8
                load_images(square_size)
                screen.fill(GRAY)
                draw_board(screen, board, square_size, selected_square, highlighted_moves)

                # Draw undo and redo buttons
                font = pygame.font.Font(None, 36)
                undo_button = pygame.Rect(10, HEIGHT - 90, 100, 40)
                redo_button = pygame.Rect(120, HEIGHT - 90, 100, 40)
                pygame.draw.rect(screen, (200, 200, 200), undo_button)
                pygame.draw.rect(screen, (200, 200, 200), redo_button)
                undo_text = font.render("Undo", True, (255, 50,20))
                redo_text = font.render("Redo", True, ("green"))
                screen.blit(undo_text, (30, HEIGHT - 85))
                screen.blit(redo_text, (140, HEIGHT - 85))
                
                # Draw timer
                elapsed_time = int(time.time() - start_time)
                minutes, seconds = divmod(elapsed_time, 60)
                timer_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (0, 0, 0))
                screen.blit(timer_text, (WIDTH - 150, HEIGHT - 85))

                pygame.display.flip()
            except Exception as e:
                print(f"An error occurred: {e}")
                pygame.quit()
                return

if __name__ == "__main__":
    main1()
    main2()
# board.py: quản lý bàn cờ
import os
import pygame
from src.pieces.piece import Piece

class Board:
    # Game board constants
    WIDTH = 521
    HEIGHT = 577
    GRID_SIZE = 57
    PIECE_SIZE = 57
    MARGIN_LEFT = 9
    MARGIN_TOP = 51

    def __init__(self):
        # Initialize empty 10x9 board (rowx x cols)
        self.board = [[None for _ in range(9)] for _ in range(10)]
        self.current_player = 'red' # First player is red
        self.move_history = []
        self.selected_piece = None
        self.valid_moves = []
        
        # Load images
        self.load_images()
        
        # Set up pieces
        self.setup_pieces()

    def load_images(self):
        """Load all images needed for the game"""
        self.images = {}
        
        # Board background
        self.images['board'] = pygame.image.load(os.path.join('src', 'res', 'bg.bmp'))
        
        # Piece icon
        piece_types = {
            'jiang_shuai': {'red': 'R_K', 'black': 'B_K'},  # Kings/Generals
            'shi': {'red': 'R_A', 'black': 'B_A'},          # Abvisors
            'xiang': {'red': 'R_E', 'black': 'B_E'},        # Elephant
            'ma': {'red': 'R_H', 'black': 'B_H'},           # Horse
            'ju': {'red': 'R_R', 'black': 'B_R'},           # Chariots/Rooks
            'pao': {'red': 'R_C', 'black': 'B_C'},          # Cannons
            'bing_zu': {'red': 'R_S', 'black': 'B_S'},          # Pawns/Soldier
        }
        
        # Load each piece image
        for piece_type, colors in piece_types.items():
            for color, file_prefix in colors.items():
                file_path = os.path.join('src', 'res', f"{file_prefix}.ico")
                self.images[f"{color}_{piece_type}"] = pygame.image.load(file_path)

        # UI elements
        self.images['select'] = pygame.image.load(os.path.join('src', 'res', 'select.ico'))
        self.images['valid'] = pygame.image.load(os.path.join('src', 'res', 'valid.ico'))
        self.images['attack'] = pygame.image.load(os.path.join('src', 'res', 'attack.ico'))

    def setup_pieces(self):
        """Set up the initial board position with all pieces"""
        from src.pieces.jiang_shuai import JiangShuai
        from src.pieces.shi import Shi
        from src.pieces.xiang import Xiang
        from src.pieces.ma import Ma
        from src.pieces.ju import Ju
        from src.pieces.pao import Pao
        from src.pieces.bing_zu import BingZu
        
        # Place generals/kings
        self.place_piece(JiangShuai('red', (0, 4)))
        self.place_piece(JiangShuai('black', (9, 4)))
        
        # Place advisor/guards
        self.place_piece(Shi('red', (0, 3)))
        self.place_piece(Shi('red', (0, 5)))
        self.place_piece(Shi('black', (9, 3)))
        self.place_piece(Shi('black', (9, 5)))
        
        # Place elephant/bishops
        self.place_piece(Xiang('red', (0, 2)))
        self.place_piece(Xiang('red', (0, 6)))
        self.place_piece(Xiang('black', (9, 2)))
        self.place_piece(Xiang('black', (9, 6)))
        
        # Place horse/knights
        self.place_piece(Ma('red', (0, 1)))
        self.place_piece(Ma('red', (0, 7)))
        self.place_piece(Ma('black', (9, 1)))
        self.place_piece(Ma('black', (9, 7)))
        
        # Place chariots/rooks
        self.place_piece(Ju('red', (0, 0)))
        self.place_piece(Ju('red', (0, 8)))
        self.place_piece(Ju('black', (9, 0)))
        self.place_piece(Ju('black', (9, 8)))
        
        # Place cannons
        self.place_piece(Pao('red', (2, 1)))
        self.place_piece(Pao('red', (2, 7)))
        self.place_piece(Pao('black', (7, 1)))
        self.place_piece(Pao('black', (7, 7)))
        
        # Place pawns/soldiers
        for i in range(0, 9, 2):
            self.place_piece(BingZu('red', (3, i))) # 1 3 5 7 9
            self.place_piece(BingZu('black', (6, i)))

    def place_piece(self, piece):
        """Place a piece at its position on the board"""
        row, col = piece.position
        self.board[row][col] = piece
    
    def get_piece(self, position):
        """Get piece at the given position"""
        row, col = position
        if 0 <= row < 10 and 0 <= col < 9:
            return self.board[row][col]
        return None
    
    def move_piece(self, from_pos, to_pos):
        """Move a piece from one position to another"""
        piece = self.get_piece(from_pos)
        
        # Check if the move is valid or piece is None
        if (to_pos not in piece.get_valid_moves(self)) or (not piece):
            return False

        # Execute the move
        captured_piece = self.get_piece(to_pos)
        self.board[from_pos[0]][from_pos[1]] = None
        self.board[to_pos[0]][to_pos[1]] = piece
        piece.position = to_pos
        
        # Switch player 
        self.current_player = 'black' if self.current_player == 'red' else 'red'

        # Clear selection and valid moves
        self.selected_piece = None
        self.valid_moves = []
        
        return True
    
    def is_in_check(self, color):
        """Check if the player of given color is in check (bị chiếu tướng)"""
        # pind the generals/king
        king_pos  = next(((row, col) for row in range(10) for col in range(9) if (piece := self.board[row][col] and self.board[row][col].color == color and self.board[row][col].__class__.__name__ == 'JiangShuai')), None)
        
        if not king_pos: return False
        
        # Check if any opponent piece can capture the king
        opposite_color = 'black' if color == 'red' else 'red'
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece and piece.color == opposite_color:
                    if king_pos in piece.get_valid_moves(self):
                        return True

        return False

    def is_checkmate(self, color):
        """Check if the player of given color is in checkmate."""
        if not self.is_in_check(color):
            return False
        
        # Try all possible moves to see if any can get out of check
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    for move in piece.get_valid_moves(self):
                        # Try the move
                        original_pos = piece.position
                        captured = self.get_piece(move)
                        
                        self.board[original_pos[0]][original_pos[1]] = None
                        self.board[move[0]][move[1]] = piece
                        piece.position = move
                        
                        # Check if still in check
                        still_in_check = self.is_in_check(color)
                        
                        # Undo the move
                        self.board[original_pos[0]][original_pos[1]] = piece
                        piece.position = original_pos
                        self.board[move[0]][move[1]] = captured
                        
                        if not still_in_check:
                            return False
        return True
    
    def is_game_over(self):
        """Check if the game is over (checkmate)"""
        return self.is_checkmate('red') or self.is_checkmate('black')
    
    def get_legal_moves(self, color):
        """Get all legal moves for the player of given color"""
        moves = []
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    for move in piece.get_valid_moves(self):
                        # Only include that dont leave the player in check
                        original_pos = piece.position
                        captured = self.get_piece(move)
                        
                        self.board[original_pos[0]][original_pos[1]] = None
                        self.board[move[0]][move[1]] = piece
                        piece.position = move
                        
                        # Check if the move leaves the player in check
                        in_check = self.is_in_check(color)
                        
                        # Undo the move
                        self.board[original_pos[0]][original_pos[1]] = piece
                        piece.position = original_pos
                        self.board[move[0]][move[1]] = captured
                        
                        if not in_check:
                            moves.append((original_pos, move)) # ((r, c), (r, c))
        return moves
    
    def screen_to_board(self, screen_pos):
        """Convert screen coordinates to board position"""
        x, y = screen_pos
        # Adjust for margin
        x -= self.MARGIN_LEFT
        y -= self.MARGIN_TOP

        # Calculate board position
        col = round(x / self.GRID_SIZE)
        row = round(y / self.GRID_SIZE)

        # Check if within board bounds
        if 0 <= row < 10 and 0 <= col < 9:
            return (row, col)
        return None

    def board_to_screen(self, board_pos):
        """Convert board position to screen coordinates"""
        row, col = board_pos
        x = self.MARGIN_LEFT + col * self.GRID_SIZE
        y = self.MARGIN_TOP + row * self.GRID_SIZE
        return (x, y)

    def select_piece(self, position):
        """Select a piece on the board"""
        piece = self.get_piece(position)
        if piece and piece.color == self.current_player:
            self.selected_piece = piece
            self.valid_moves = []
            # Calculate valid moves that don't leave player in check
            for move in piece.get_valid_moves(self):
                # Temporarily make the move
                original_pos = piece.position
                captured = self.get_piece(move)

                self.board[original_pos[0]][original_pos[1]] = None
                self.board[move[0]][move[1]] = piece
                piece.position = move
                
                # Check if the move leaves the player in check
                in_check = self.is_in_check(piece.color)
                
                # Undo the move
                self.board[original_pos[0]][original_pos[1]] = piece
                piece.position = original_pos
                self.board[move[0]][move[1]] = captured
                
                if not in_check:
                    self.valid_moves.append(move)
            return True
        return False
        
    def handle_click(self, pos):
        """Handle a click on the board"""
        board_pos = self.screen_to_board(pos)
        if not board_pos:
            return False

        # If a piece is already selected
        if self.selected_piece:
            # Try to move the selected piece to the clicked position
            if board_pos in self.valid_moves:
                return self.move_piece(self.selected_piece.position, board_pos)
            else:
                # Try to select another piece
                new_piece = self.get_piece(board_pos)
                if new_piece and new_piece.color == self.current_player:
                    self.select_piece(board_pos)
                    return True
                # Deselect if clicking on empty square or opponent's piece
                self.selected_piece = None
                self.valid_moves = []
                return True
        else:
            # Try to select a piece
            return self.select_piece(board_pos)
    
    def draw(self, screen):
        """Draw the board and pieces on the screen"""
        # Draw the board background
        screen.blit(self.images['board'], (0, 0))

        # Draw highlights for selected piece and valid moves
        if self.selected_piece:
            # Highlight selected piece
            pos = self.board_to_screen(self.selected_piece.position)
            screen.blit(self.images['select'], (pos[0] - self.PIECE_SIZE // 2, pos[1] - self.PIECE_SIZE // 2))

            # Highlight valid moves
            for move in self.valid_moves:
                pos = self.board_to_screen(move)
                # Use attack icon if there's an opponent's piece, otherwise valid move icon
                if self.get_piece(move) and self.get_piece(move).color != self.current_player:
                    screen.blit(self.images['attack'], (pos[0] - self.PIECE_SIZE // 2, pos[1] - self.PIECE_SIZE // 2))
                else:
                    screen.blit(self.images['valid'], (pos[0] - self.PIECE_SIZE // 2, pos[1] - self.PIECE_SIZE // 2))
                    
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece:
                    # Get the correct image for this piece
                    piece_type = piece.__class__.__name__.lower()
                    image_key = f"{piece.color}_{piece_type}"
                    if image_key in self.images:
                        pos = self.board_to_screen((row, col))
                        screen.blit(self.images[image_key], (pos[0] - self.PIECE_SIZE // 2, pos[1] - self.PIECE_SIZE // 2))
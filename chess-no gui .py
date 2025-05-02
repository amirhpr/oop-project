# -----------------------------------------------------
from copy import deepcopy as dcp
import pygame
import sys


class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    # check is the pos in list_pos

    def match(self, list_pos):
        for pos in list_pos:
            if pos.row == self.row and pos.col == self.col:
                return True


class Piece:
    def __init__(self, color, board, position=None):
        self.color = color
        self.board = board
        self.has_moved = False
        self.position = position

    # return a list include all of the possible moves piece can do

    def possible_moves(self):
        pass

    # check the move is possible

    def check_move(self, end_pos):
        return end_pos.match(self.possible_moves())

        # to ger print from piece

    def __str__(self):
        pass


# ------------------------------ pieces ------------------------------------------
class King(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "king"

    def possible_moves(self):
        moves = []
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1),
                   (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (
                    self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        # Castling
        if not self.board.board[self.position.row][self.position.col].has_moved:
            # Check kingside castling
            if self.board.board[self.position.row][7] and not self.board.board[self.position.row][7].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in
                       range(self.position.col + 1, 7)):
                    moves.append(
                        Position(self.position.row, self.position.col + 2))
            # Check queenside castling
            if self.board.board[self.position.row][0] and not self.board.board[self.position.row][0].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in range(1, self.position.col)):
                    moves.append(
                        Position(self.position.row, self.position.col - 2))
        return moves

    def __str__(self):
        return "K" if self.color == "White" else "k"


class Bishop(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "bishop"

    def possible_moves(self):
        moves = []
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
        coefficient = list(range(1, 8))
        for dr, dc in directions:
            for x in coefficient:
                new_pos = Position(self.position.row + (dr * x), self.position.col + (dc * x))
                if self.board.is_inside_board(new_pos) and (
                        self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                    moves.append(new_pos)
                    if not self.board.is_enemy_piece(new_pos, self.color):
                        continue
                break

        return moves

    def __str__(self):
        return "B" if self.color == "White" else "b"


class Pawn(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "pawn"

    def possible_moves(self):
        moves = []
        direction = 1 if self.color == "White" else -1
        coefficient = [1, 2]
        # Moves for regular pawn advance
        for x in coefficient:
            new_pos = Position(self.position.row +
                               (direction * x), self.position.col)
            if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos)):
                moves.append(new_pos)
                if not self.has_moved:
                    continue
                else:
                    break
        # Moves for capturing diagonally
        for x in [1, -1]:
            new_pos = Position(self.position.row +
                               direction, self.position.col + x)
            if self.board.is_inside_board(new_pos) and self.board.is_enemy_piece(new_pos, self.color):
                moves.append(new_pos)

        return moves

    def __str__(self):
        return "P" if self.color == "White" else "p"

    def is_promotion(self):
        end_row = 7 if self.color == "White" else 0
        if self.position.row == end_row:
            return True


class Rook(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "rook"

    def possible_moves(self):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        coefficient = list(range(1, 8))
        for dr, dc in directions:
            for x in coefficient:
                new_pos = Position(self.position.row + (dr * x),
                                   self.position.col + (dc * x))
                if self.board.is_inside_board(new_pos) and (
                        self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                    moves.append(new_pos)
                    if not self.board.is_enemy_piece(new_pos, self.color):
                        continue
                break
        return moves

    def __str__(self):
        return "R" if self.color == "White" else "r"


class Knight(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "knight"

    def possible_moves(self):
        moves = []
        offsets = [(1, -2), (2, 1), (1, 2), (-2, -1),
                   (-1, -2), (2, -1), (-1, 2), (-2, 1)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (
                    self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        return moves

    def __str__(self):
        return "N" if self.color == "White" else "n"


class Queen(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "queen"

    def possible_moves(self):
        moves = []
        coefficient = list(range(1, 8))
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1),
                      (1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            for x in coefficient:
                new_pos = Position(self.position.row + (dr * x),
                                   self.position.col + (dc * x))
                if self.board.is_inside_board(new_pos) and (
                        self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                    moves.append(new_pos)
                    if not self.board.is_enemy_piece(new_pos, self.color):
                        continue
                break
        return moves

    def __str__(self):
        return "Q" if self.color == "White" else "q"


# ------------------------------------------------------------------------


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)]
                      for _ in range(8)]  # initialize the board

    # place the piece on the selected poition:
    def place_piece(self, piece, position):
        self.board[position.row][position.col] = piece
        piece.position = position

    # make sure the positin is empety:
    def remove_piece(self, pos):
        self.board[pos.row][pos.col] = None

    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos.row][start_pos.col]
        if piece:
            if piece.check_move(end_pos):
                self.remove_piece(end_pos)
                self.place_piece(piece, end_pos)
                self.remove_piece(start_pos)
                piece.has_moved = True
                if piece.piece_type=="king" and abs(start_pos.col-end_pos.col)==2:
                    if start_pos.col-end_pos.col == 2:

                        if piece.color=="White":
                            piece2 = self.board[0][0]
                            self.place_piece(piece2, Position(0,2))
                            self.remove_piece(Position(0,0))
                        else:
                            piece2 = self.board[7][0]
                            self.place_piece(piece2, Position(7, 2))
                            self.remove_piece(Position(7, 0))
                    if start_pos.col - end_pos.col==-2:
                        
                        if piece.color == "White":
                            piece2 = self.board[0][7]
                            self.place_piece(piece2, Position(0, 4))
                            self.remove_piece(Position(0, 7))
                        else:
                            piece2 = self.board[7][7]
                            self.place_piece(piece2, Position(7, 4))
                            self.remove_piece(Position(7, 7))


                return True
        else:
            print("\n No piece at the starting position. ")
            return False

    def promot(self, pro_piece, piece, end_pos):
        self.remove_piece(end_pos)
        self.place_piece(pro_piece(piece.color, self, end_pos), end_pos)

    def is_square_empty(self, position):
        return self.board[position.row][position.col] is None

    def is_enemy_piece(self, position, color):
        piece = self.board[position.row][position.col]
        return True if piece and not piece.color == color else False

    def is_inside_board(self, position):
        return True if position.col > -1 and position.col < 8 and position.row > -1 and position.row < 8 else False

    def print_board(self):
        print("\n---------------------------------------------------------------\n\n")
        print(" | a b c d e f g h")
        print("------------------")
        for i, row in enumerate(self.board):
            row_str = str(i) + "| "
            for piece in row:
                if piece:
                    row_str += f"{piece} "
                else:
                    row_str += ". "
            print(row_str)
        print("\n")


class ChessSet:
    def __init__(self):
        self.board = Board()
        self.setup_board()

    def setup_board(self):
        # Place white pieces
        self.board.place_piece(Rook("White", self.board), Position(0, 0))
        self.board.place_piece(Knight("White", self.board), Position(0, 1))
        self.board.place_piece(Bishop("White", self.board), Position(0, 2))
        self.board.place_piece(King("White", self.board), Position(0, 3))
        self.board.place_piece(Queen("White", self.board), Position(0, 4))
        self.board.place_piece(Bishop("White", self.board), Position(0, 5))
        self.board.place_piece(Knight("White", self.board), Position(0, 6))
        self.board.place_piece(Rook("White", self.board), Position(0, 7))

        self.board.place_piece(Pawn("White", self.board), Position(1, 0))
        self.board.place_piece(Pawn("White", self.board), Position(1, 1))
        self.board.place_piece(Pawn("White", self.board), Position(1, 2))
        self.board.place_piece(Pawn("White", self.board), Position(1, 3))
        self.board.place_piece(Pawn("White", self.board), Position(1, 4))
        self.board.place_piece(Pawn("White", self.board), Position(1, 5))
        self.board.place_piece(Pawn("White", self.board), Position(1, 6))
        self.board.place_piece(Pawn("White", self.board), Position(1, 7))

        # Place black pieces
        self.board.place_piece(Rook("Black", self.board), Position(7, 0))
        self.board.place_piece(Knight("Black", self.board), Position(7, 1))
        self.board.place_piece(Bishop("Black", self.board), Position(7, 2))
        self.board.place_piece(King("Black", self.board), Position(7, 3))
        self.board.place_piece(Queen("Black", self.board), Position(7, 4))
        self.board.place_piece(Bishop("Black", self.board), Position(7, 5))
        self.board.place_piece(Knight("Black", self.board), Position(7, 6))
        self.board.place_piece(Rook("Black", self.board), Position(7, 7))

        self.board.place_piece(Pawn("Black", self.board), Position(6, 0))
        self.board.place_piece(Pawn("Black", self.board), Position(6, 1))
        self.board.place_piece(Pawn("Black", self.board), Position(6, 2))
        self.board.place_piece(Pawn("Black", self.board), Position(6, 3))
        self.board.place_piece(Pawn("Black", self.board), Position(6, 4))
        self.board.place_piece(Pawn("Black", self.board), Position(6, 5))
        self.board.place_piece(Pawn("Black", self.board), Position(6, 6))
        self.board.place_piece(Pawn("Black", self.board), Position(6, 7))

        # # ----------------------------------------------------------------------
        # self.board.place_piece(Rook("White", self.board), Position(0, 0))
        # # self.board.place_piece(Knight("White", self.board), Position(0, 1))
        # # self.board.place_piece(Bishop("White", self.board), Position(0, 2))
        # self.board.place_piece(King("White", self.board), Position(0, 3))
        # # self.board.place_piece(Queen("White", self.board), Position(6, 6))
        # # self.board.place_piece(Bishop("White", self.board), Position(0, 5))
        # # self.board.place_piece(Knight("White", self.board), Position(0, 6))
        # self.board.place_piece(Rook("White", self.board), Position(0, 7))
        #
        # # self.board.place_piece(Pawn("White", self.board), Position(6, 0))
        # # self.board.place_piece(Pawn("White", self.board), Position(1, 1))
        # # self.board.place_piece(Pawn("White", self.board), Position(1, 2))
        # # self.board.place_piece(Pawn("White", self.board), Position(1, 3))
        # # self.board.place_piece(Pawn("White", self.board), Position(1, 4))
        # # self.board.place_piece(Pawn("White", self.board), Position(1, 5))
        # # self.board.place_piece(Pawn("White", self.board), Position(1, 6))
        # # self.board.place_piece(Pawn("White", self.board), Position(1, 7))
        #
        # # Place black pieces
        # self.board.place_piece(Rook("Black", self.board), Position(7, 0))
        # # self.board.place_piece(Knight("Black", self.board), Position(7, 1))
        # # self.board.place_piece(Bishop("Black", self.board), Position(7, 2))
        # self.board.place_piece(King("Black", self.board), Position(7, 3))
        # # self.board.place_piece(Queen("Black", self.board), Position(7, 3))
        # # self.board.place_piece(Bishop("Black", self.board), Position(7, 5))
        # # self.board.place_piece(Knight("Black", self.board), Position(7, 6))
        # self.board.place_piece(Rook("Black", self.board), Position(7, 7))
        #
        # # self.board.place_piece(Pawn("Black", self.board), Position(6, 0))
        # # self.board.place_piece(Pawn("Black", self.board), Position(6, 1))
        # # self.board.place_piece(Pawn("Black", self.board), Position(6, 2))
        # # self.board.place_piece(Pawn("Black", self.board), Position(6, 3))
        # # self.board.place_piece(Pawn("Black", self.board), Position(6, 4))
        # # self.board.place_piece(Pawn("Black", self.board), Position(6, 5))
        # # self.board.place_piece(Pawn("Black", self.board), Position(6, 6))
        # # self.board.place_piece(Pawn("Black", self.board), Position(6, 7))

    def print_board(self):
        self.board.print_board()

class GUI:
    def __init__(self, board):
        self.board = board
        self.screen = pygame.display.set_mode((640, 640))
        self.clock = pygame.time.Clock()
        
        self.selected_cell = None

    def draw_board(self):
        colors = [(255, 255, 255), (100, 100, 100)]
        for i in range(8):
            for j in range(8):
                color = colors[(i + j) % 2] 
                rect = pygame.Rect(j*80, i*80, 80, 80)
                pygame.draw.rect(self.screen, color, rect)
                if self.board[i][j] :
                    text = self.font.render(str(self.board[i][j]), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

    def get_clicked_cell(self, pos):
        x, y = pos
        row = y // 80
        col = x // 80
        return row, col

    
            

            

class Chess:
    def __init__(self):
        self.chess_set = ChessSet()
        self.gui=GUI(self.chess_set.board.board)

    def start_game(self):
        print("Welcome to Chess!\n")
        current_player = "White"

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    self.gui.selected_cell = self.gui.get_clicked_cell(pos)
                    print("Selected cell:", self.gui.selected_cell)
                    if self.selected_cell :
                        print("Value in selected cell:", self.gui.board[self.gui.selected_cell[0]][self.gui.selected_cell[1]])



            self.chess_set.print_board()
            if self.is_checkmate(current_player):
                print(f"{current_player} is checkmate")
                break
            if self.is_pot(current_player):
                print("game is pot")
                break
            if self.is_check(current_player, self.chess_set.board):
                print(f"{current_player} is check")

            print(f"\n{current_player}'s turn:")
            start_pos = input(
                "Enter the position of the piece you want to move: ")
            end_pos = input(
                "Enter the position to move the piece to : ")

            # check if the input is according to the expected format
            if self.is_valid_input(start_pos, end_pos):
                start_pos, end_pos = self.from_algebraic(start_pos), self.from_algebraic(end_pos)

            else:
                print("\n is not valid input!")
                continue

            # move the piece if it is possible, otherwise notify the user to select other moves
            b2 = dcp(self.chess_set.board)
            piece = self.chess_set.board.board[start_pos.row][start_pos.col]
            if piece and piece.color == current_player and b2.move_piece(start_pos, end_pos):
                if not self.is_check(current_player, b2):
                    self.chess_set.board.move_piece(start_pos, end_pos)
                    if piece.piece_type == "pawn" and piece.is_promotion():
                        while 1:
                            pro_key = input('input "Q" or "R" or "N" or "B" \npawn promot to:    ').upper()
                            if pro_key in ["Q", "R", "N", "B"]:
                                if pro_key == "Q":
                                    pro_piece = Queen
                                if pro_key == "R":
                                    pro_piece = Rook
                                if pro_key == "N":
                                    pro_piece = Knight
                                if pro_key == "B":
                                    pro_piece = Bishop
                                self.chess_set.board.promot(pro_piece, piece, end_pos)
                                break

            else:
                print("\n it's impossible. enter again an other move: ")
                continue

            # switch the turns
            if current_player == "White":
                current_player = "Black"
            elif current_player == "Black":
                current_player = "White"
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)

    def is_valid_input(self, start_pos, end_pos):
        for i in [start_pos, end_pos]:
            i = list(i)
            if not (len(i) == 2 and (i[1].isdigit() and i[0].isalpha())):
                return False
        else:
            return True

    def is_check(self, current_player, board):
        enemy = "Black" if current_player == "White" else "White"
        # find position of currnt_pplayer's king
        for i in range(8):
            for j in range(8):
                piece = board.board[i][j]
                if piece and (piece.color == current_player and piece.piece_type == "king"):
                    king_pos = piece.position

        # check possible move of enemy pieces
        for i in range(8):
            for j in range(8):
                piece = board.board[i][j]
                if piece and piece.color == enemy and king_pos.match(piece.possible_moves()):
                    return True

    def is_checkmate(self, current_player):
        if self.is_check(current_player, self.chess_set.board):
            for i in range(8):
                for j in range(8):
                    piece = self.chess_set.board.board[i][j]
                    if piece and (piece.color == current_player) and piece.possible_moves():
                        for move in piece.possible_moves():
                            b2 = dcp(self.chess_set.board)
                            b2.move_piece(piece.position, move)
                            if not self.is_check(current_player, b2):
                                return False
            else:
                return True

    def is_pot(self, current_player):
        for i in range(8):
            for j in range(8):
                piece = self.chess_set.board.board[i][j]
                if piece and (piece.color == current_player) and piece.possible_moves():
                    for move in piece.possible_moves():
                        b2 = dcp(self.chess_set.board)
                        b2.move_piece(piece.position, move)
                        if not self.is_check(current_player, b2):
                            return False

        for i in range(8):
            for j in range(8):
                piece = self.chess_set.board.board[i][j]
                if piece and not piece.piece_type() == "king":
                    return False
        return True

    def from_algebraic(self, algebraic_notation):
        col = ord(algebraic_notation[0]) - ord('a')
        row = int(algebraic_notation[1])
        return Position(row, col)


if __name__ == "__main__":
    chess_game = Chess()
    chess_game.start_game()
pygame.init()

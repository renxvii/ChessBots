from copy import deepcopy, copy
class Game:      
    def startgame(self):
        pass

    def valuation(self, player:int, state):
        pass

    def valid_moves(self):
        pass

    def checkwinner(self):
        pass

    def render(self):
        pass

    def next(self):
        self.end = self.checkwinner()
        if self.end == 0:
            self.players[int((1 - self.turn)/2)].turn(self)
        elif not self.thinking and self.rendering:
            if self.end == 2:
                print("Tie")
            else:
                print("winner: " + str(int((1 - self.end)/2 + 1)))

    def playermove(self, move):
        pass

    def play(self, move):
        self.round += 1
        self.state = move[0]
        self.turn *= -1 
        self.value = move[1] * -1
        if not self.thinking:
            self.render()
            self.next()

    def __init__(self, Agent1, Agent2, render = True):
        self.thinking = False
        self.players = [Agent1, Agent2]
        Agent1.player = 1
        Agent2.player = -1
        self.end = 0
        self.round = 0
        self.turn = 1 ## 1 for player 1, -1 for player 2
        self.value = 0 ## always from the perspective of the player 1
        self.rendering = render
        self.state = self.startgame() 
        self.next()

class Connect4(Game):
    def startgame(self):
        board = [[],[],[],[],[],[],[]]
        return board

    def same(self, lst):
        if lst[0] == 0:
            return False
        for i in lst:
            if i != lst[0]:
                return False
        return True
    
    def valuation(self, board="default"):
        if board=="default":
            board = self.state
        if not board:
            return 0
        for i in board:
            while len(i) < 7:
                i.append(0)
        value = 0
        for column in board:
            for i in range(4):
                if self.same(column[i:i+4]):
                    value = column[i]   
        for column in range(4):
            for row in range(7):
                if self.same([board[column][row],board[column+1][row],board[column+2][row],board[column+3][row]]):
                    value = board[column][row]
            for row in range(4):
                if self.same([board[column][6-row],board[column+1][5-row],board[column+2][4-row],board[column+3][3-row]]):
                    value = board[column][6-row]
                elif self.same([board[column][row],board[column+1][row+1],board[column+2][row+2],board[column+3][row+3]]):
                    value = board[column][row]
        for i in board:
            while 0 in i:
                i.remove(0)
        return value*9999

    def valid_moves(self, turn=None, state=None):
        moveset = []
        if not state:
            state = self.state
        if not turn:
            turn = self.turn
        if self.checkwinner(state) != 0:
            return []
        for i in range(7):
            if len(state[i]) < 7:
                board = deepcopy(state)
                board[i].append(turn)
                moveset.append([board, self.valuation(board)])
        return moveset
    
    def render(self, state = None):
        if self.rendering:
            if not state:
                state = self.state
            board = deepcopy(state)
            for i in range(7):
                while len(board[i]) < 7:
                    board[i].append(0)
                for l in range(7):
                    if board[i][l] == -1:
                        board[i][l] = 2
            for i in range(5):
                print()
            for row in range(6,-1,-1):
                print([column[row] for column in board])

    def checkwinner(self, state="default"):
        if state=="default":
            state = self.state
        if not state:
            return 2
        if self.valuation(state) < 0:
            return -1
        elif self.valuation(state) > 0:
            return 1
        return 0

    def playermove(self, move):
        if self.end == 0:
            self.state[int(move)-1].append(self.turn)
            self.turn *= -1 
            self.value = self.valuation(self.state)
            self.end = self.checkwinner()
            if not self.thinking:
                self.render()
                self.next()
        elif not self.thinking:
            print("winner: " + str(int((1 - self.end)/2 + 1)))

class TicTacToe(Game):
    def startgame(self):
        board = [[0,0,0],[0,0,0],[0,0,0]]
        return board

    def same(self, lst):
        if lst[0] == 0:
            return False
        for i in lst:
            if i != lst[0]:
                return False
        return True
    
    def valuation(self, board=None):
        if not board:
            board = self.state
        value = 0
        for i in range(3):
            if self.same(board[i]) or self.same([board[0][i],board[1][i],board[2][i]]):
                value = board[i][i]*9999
        if self.same([board[1][1],board[2][2],board[0][0]]) or self.same([board[1][1],board[0][2],board[2][0]]):
            value = board[1][1]*9999
        return value
    
    def valid_moves(self, turn=None, state=None):  
        if not state:
            state = self.state
        if not turn:
            turn = self.turn
        moves = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    moves.append([deepcopy(state),0])
                    moves[-1][0][i][j] = turn
                    moves[-1][1] = self.valuation(moves[-1][0])
        return moves

    def render(self, state = None):
        if self.rendering:
            if not state:
                state = self.state
            print("\n\n\n")
            for i in state:
                for j in range(3):
                    if i[j] == -1:
                        i[j] = 2
                print(i)
                for j in range(3):
                    if i[j] == 2:
                        i[j] = -1

    def checkwinner(self, state="default"):
        if state=="default":
            state = self.state
        if sum(sum(i**2 for i in j)for j in state)==9:
            return 2
        if self.valuation(state) < 0:
            return -1
        elif self.valuation(state) > 0:
            return 1
        return 0

    def playermove(self, move):
        if self.end == 0:
            self.state[int((int(move)-1)/3)][(int(move)-1)%3] = self.turn
            self.turn *= -1 
            self.value = self.valuation(self.state)
            self.end = self.checkwinner()
            if not self.thinking:
                self.render()
                self.next()
        elif not self.thinking:
            print("winner: " + str(int((1 - self.end)/2 + 1)))


class Checkers(Game):      
    def startgame(self):
        # Initialize the board with pieces in the correct positions.
        # 1 for player 1, -1 for player 2, 0 for empty
        board = [[0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [-1, 0, -1, 0, -1, 0, -1, 0],
                 [0, -1, 0, -1, 0, -1, 0, -1],
                 [-1, 0, -1, 0, -1, 0, -1, 0]]
        return board

    def render(self, state=None):
        # Print the board in a human-readable format
        if self.rendering:
            
            if not state:
                state = self.state

            print("  0 1 2 3 4 5 6 7")
            for i, row in enumerate(state):
                print(i, end=" ")
                for cell in row:
                    if cell == 1:
                        print("b", end=" ")  # B for Black pieces
                    elif cell == -1:
                        print("w", end=" ")  # W for White pieces
                    elif cell == -2:
                        print("W", end=" ")  # W for White pieces
                    elif cell == 2:
                        print("B", end=" ")  # W for White pieces
                    else:
                        print(".", end=" ")  # . for empty squares
                print()
            print("\n\n\n")
    
    def valuation(self, board="default"):
        if board == "default":
            board = self.state
        if not board:
            return 0
        pos = 0
        neg = 0
        for i in board:
            for j in i:
                if j < 0:
                    neg += 1
                elif j >0:
                    pos += 1
        if neg == 0:
            return 9999
        elif pos == 0:
            return -9999
        return sum(sum(i) for i in board)
    
    def valid_moves(self, turn=None, state=None):
        if not state:
            state = self.state
        if not turn:
            turn = self.turn
        moves = []
        captures_exist = False
        for i in range(8):
            for j in range(8):
                if state[i][j] == turn or state[i][j] == turn * 2:  # Check for regular and king pieces
                    captures = self.get_all_captures(i, j, state, turn)
                    if captures:
                        captures_exist = True
                        moves.extend(captures)

        if captures_exist:
            return moves  # Return only capture moves if they exist

        # Add regular moves if no captures are available
        for i in range(8):
            for j in range(8):
                if state[i][j] == turn or state[i][j] == turn * 2:  # Check for regular and king pieces
                    self.add_regular_moves(i, j, state, moves, turn)
        return moves


    def add_regular_moves(self, i, j, state, moves, turn):
        is_king = state[i][j] == 2 * turn
        directions = self.get_directions(turn, is_king)

        for d in directions:
            new_i, new_j = i + d[0], j + d[1]
            if 0 <= new_i < 8 and 0 <= new_j < 8 and state[new_i][new_j] == 0:
                new_state = deepcopy(state)
                new_state[i][j] = 0
                new_state[new_i][new_j] = state[i][j]  # Keep the same value (king or not)
                if new_i == 3.5 +  3.5*turn and abs(state[i][j]) == 1:
                    new_state[new_i][new_j] = state[i][j]*2
                    is_king == True
                moves.append([new_state,self.valuation(board=new_state)])

    def get_all_captures(self, i, j, state, turn):
        is_king = state[i][j] == 2 * turn
        captures = []
        self.recursive_captures(i, j, state, turn, is_king, [], captures)
        return captures

    def recursive_captures(self, i, j, state, turn, is_king, current_sequence, all_sequences):
        directions = self.get_directions(turn, is_king)
        has_capture = False

        for d in directions:
            middle_i, middle_j = i + d[0], j + d[1]
            new_i, new_j = i + d[0]*2, j + d[1]*2
            if (0 <= new_i < 8 and 0 <= new_j < 8 and state[new_i][new_j] == 0 and
                    state[middle_i][middle_j] * turn < 0):
                has_capture = True
                new_state = deepcopy(state)
                new_state[i][j] = 0
                new_state[middle_i][middle_j] = 0
                new_state[new_i][new_j] = state[i][j]
                new_sequence = current_sequence + [(new_i, new_j)]
                if new_i == 3.5 +  3.5*turn and abs(state[i][j]) == 1:
                    new_state[new_i][new_j] = state[i][j]*2
                    is_king == True
                self.recursive_captures(new_i, new_j, new_state, turn, is_king, new_sequence, all_sequences)

        if not has_capture and current_sequence != []:
            all_sequences.append([state,self.valuation(state)])

    def get_directions(self, turn, is_king):
        if is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return [(-1, -1), (-1, 1)] if turn == -1 else [(1, -1), (1, 1)]

    def checkwinner(self, state="default"):
        if state=="default":
            state = self.state
        pos = 0
        neg = 0
        for i in state:
            for j in i:
                if j < 0:
                    neg += 1
                elif j >0:
                    pos += 1
        if neg == 0:
            return 1
        elif pos == 0:
            return -1
        elif self.valid_moves(state=state) == []:
            return 2
        return 0

    def algebraic_to_indices(self, move):
        # Converts algebraic notation like 'e4' to board indices (row, column)
        col_to_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        row = 8 - int(move[1])  # Row index
        col = col_to_index[move[0].lower()]  # Column index
        return row, col

    def playermove(self, move):
        if self.end == 0:
            move_sequence = [move[i:i+2] for i in range(0, len(move), 2)]
            start_row, start_col = self.algebraic_to_indices(move_sequence[0])

            for next_move in move_sequence[1:]:
                next_row, next_col = self.algebraic_to_indices(next_move)
                self.execute_move(start_row, start_col, next_row, next_col)
                start_row, start_col = next_row, next_col

            self.turn *= -1 
            self.value = self.valuation(self.state)
            self.end = self.checkwinner()
            if not self.thinking:
                self.render()
                self.next()
        else:
            print("Game over")

    def execute_move(self, start_row, start_col, end_row, end_col):
        # Execute a move from (start_row, start_col) to (end_row, end_col)
        piece = self.state[start_row][start_col]
        self.state[start_row][start_col] = 0  # Remove the piece from the starting square
        self.state[end_row][end_col] = piece  # Place the piece in the ending square

        # If the move is a capture, remove the captured piece
        if abs(end_row - start_row) > 1:
            mid_row, mid_col = (start_row + end_row) // 2, (start_col + end_col) // 2
            self.state[mid_row][mid_col] = 0  # Remove the captured piece

        # Check for promotion to king
        if (end_row == 0 or end_row == 7) and abs(piece) == 1:
            self.state[end_row][end_col] = 2 * piece  # Promote to king


class Chess(Game):
    def __init__(self, Agent1, Agent2, render=True):
        super().__init__(Agent1, Agent2, render)
        
    def startgame(self):
        # Initialize a chess board with pieces in starting positions
        board = [[
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p']*8,
            ['']*8,
            ['']*8,
            ['']*8,
            ['']*8,
            ['P']*8,
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        
        ], ["None","K","Q","k","q"]]
        return board

    def render(self, state=None):
        if self.rendering:
                
            if not state:
                state = self.state

            print("  a b c d e f g h")
            for i, row in enumerate(state[0]):
                print(8 - i, end=" ")
                for cell in row:
                    print(cell if cell else '.', end=" ")
                print()
            print("\n\n\n")

    def valuation(self, board="default"):
        # Evaluate the board based on piece values and positions
        if board == "default":
            board = self.state
        if not board:
            return 0

        value_dict = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 9999,
                      'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -9999}
        return sum(value_dict.get(cell, 0) for row in board[0] for cell in row)

    def valid_moves(self, turn=None, state=None):
        if not state:
            state = self.state
        if not turn:
            turn = self.turn
        moves = []
        # Logic to generate all valid moves for each piece type
        for row in range(8):
            for col in range(8):
                piece = state[0][row][col]
                if piece and (turn == 1 and piece.isupper() or turn == -1 and piece.islower()):
                    piece_moves = self.get_piece_moves(piece, row, col, state)
                    moves.extend(piece_moves)
        return moves

    def get_piece_moves(self, piece, row, col, state, checkcheck = False):
        # Implement specific movement logic for each piece type
        # This includes handling checks and special moves
        piece_type = piece.lower()
        if piece_type == 'p':   # Pawn
            return self.get_pawn_moves(piece, row, col, state)
        elif piece_type == 'n': # Knight
            return self.get_knight_moves(piece, row, col, state)
        elif piece_type == 'b': # Bishop
            return self.get_bishop_moves(piece, row, col, state)
        elif piece_type == 'r': # Rook
            return self.get_rook_moves(piece, row, col, state)
        elif piece_type == 'q': # Queen
            return self.get_queen_moves(piece, row, col, state)
        elif piece_type == 'k': # King
            return self.get_king_moves(piece, row, col, state, checkcheck)

    # Implement specific methods for each piece:
    # - get_pawn_moves
    # - get_knight_moves
    # - get_bishop_moves
    # - get_rook_moves
    # - get_queen_moves
    # - get_king_moves

    

# Additional methods for chess-specific logic would be added here

    def get_pawn_moves(self, pawn, row, col, state):
        moves = []
        direction = -1 if pawn.isupper() else 1  # Determines the movement direction based on the pawn's color
        start_row = 6 if pawn.isupper() else 1   # Starting row for each color

        # Forward move
        if self.is_empty(row + direction, col, state):
            moves.append(self.construct_move(row, col, row + direction, col, state))
            # Double move from starting position
            if row == start_row and self.is_empty(row + 2 * direction, col, state):
                moves.append(self.construct_move(row, col, row + 2 * direction, col, state))

        # Captures
        for dc in [-1, 1]:  # Check diagonals for captures
            if self.is_opponent_piece(row + direction, col + dc, pawn, state):
                moves.append(self.construct_move(row, col, row + direction, col + dc, state))

        # En Passant
        if self.can_en_passant(row, col, direction, state):
            moves.append(self.construct_en_passant_move(row, col, direction, state))

        return moves
    
    def get_knight_moves(self, knight, row, col, state):
        moves = []
        move_offsets = [
            (-2, -1), (-2, 1), 
            (-1, -2), (-1, 2), 
            (1, -2), (1, 2), 
            (2, -1), (2, 1)
        ]

        for dr, dc in move_offsets:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.is_empty(new_row, new_col, state) or self.is_opponent_piece(new_row, new_col, knight, state):
                    moves.append(self.construct_move(row, col, new_row, new_col, state))

        return moves
    
    def get_bishop_moves(self, bishop, row, col, state):
        moves = []
        move_directions = [
            (-1, -1), (-1, 1), 
            (1, -1), (1, 1)
        ]

        for dr, dc in move_directions:
            new_row, new_col = row, col
            while True:
                new_row += dr
                new_col += dc
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break

                if self.is_empty(new_row, new_col, state):
                    moves.append(self.construct_move(row, col, new_row, new_col, state))
                elif self.is_opponent_piece(new_row, new_col, bishop, state):
                    moves.append(self.construct_move(row, col, new_row, new_col, state))
                    break  # Bishop can't move past capturing
                else:
                    break  # Blocked by another piece

        return moves
    
    def get_rook_moves(self, rook, row, col, state):
        moves = []
        move_directions = [
            (-1, 0),  # Up
            (1, 0),   # Down
            (0, -1),  # Left
            (0, 1)    # Right
        ]

        for dr, dc in move_directions:
            new_row, new_col = row, col
            while True:
                new_row += dr
                new_col += dc
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break  # Stop if off the board
                new_status = None
                if state[0][row][col].lower() == 'r':
                    if row == 7 and col == 7:
                        new_status = state[1]
                        try:
                            new_status.remove("K")
                        except:
                            pass
                    elif row == 0 and col == 7:
                        new_status = state[1]
                        try:
                            new_status.remove("k")
                        except:
                            pass
                    elif row == 7 and col == 0:
                        new_status = state[1]
                        try:
                            new_status.remove("Q")
                        except:
                            pass
                    elif row == 0 and col == 0:
                        new_status = state[1]
                        try:
                            new_status.remove("q")
                        except:
                            pass                
                if self.is_empty(new_row, new_col, state):
                    moves.append(self.construct_move(row, col, new_row, new_col, state))
                elif self.is_opponent_piece(new_row, new_col, rook, state):
                    moves.append(self.construct_move(row, col, new_row, new_col, state))
                    break  # Rook can't move past capturing
                else:
                    break  # Blocked by another piece
                
        return moves
    
    def get_queen_moves(self, queen, row, col, state):
        # Combine rook and bishop moves for the queen
        return (self.get_rook_moves(queen, row, col, state) + self.get_bishop_moves(queen, row, col, state))

    def get_king_moves(self, king, row, col, state, checkcheck = False):
        moves = []
        move_offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for dr, dc in move_offsets:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.is_empty(new_row, new_col, state) or self.is_opponent_piece(new_row, new_col, king, state):
                    if row == 7:
                        new_status = state[1]
                        try:
                            new_status.remove("K")
                            new_status.remove("Q")
                        except:
                            pass
                    elif row == 0:
                        new_status = state[1]
                        try:
                            new_status.remove("k")
                            new_status.remove("q")
                        except:
                            pass
                    moves.append(self.construct_move(row, col, new_row, new_col, state))
                    
        # if not checkcheck:
        #     if self.can_castle(king, row, col, state):
        #         if row == 7:
        #             new_status = state[1]
        #             try:
        #                 new_status.remove("K")
        #                 new_status.remove("Q")
        #             except:
        #                 pass
        #         elif row == 0:
        #             new_status = state[1]
        #             try:
        #                 new_status.remove("k")
        #                 new_status.remove("q")
        #             except:
        #                 pass
        #         moves.extend(self.get_castle_moves(king, row, col, state))
        return moves
    
    # def can_castle(self, king, row, col, state):
    #     if self.is_in_check(state, 'white' if king == 'K' else 'black'):
    #         return False  # Can't castle out of check

    #     if king == 'K' and "K" in state[1]:
    #         # Check for King-side castling for White
    #         if state[7][5] == '' and state[7][6] == '' and not self.is_square_attacked(7, 5, state) and not self.is_square_attacked(7, 6, state):
    #             return True
    #     if king == 'K' and "Q" in state[1]:
    #         # Check for Queen-side castling for White
    #         if state[7][1] == '' and state[7][2] == '' and state[7][3] == '' and not self.is_square_attacked(7, 1, state) and not self.is_square_attacked(7, 2, state) and not self.is_square_attacked(7, 3, state):
    #             return True
    #     # Similar checks for Black
    #     # ...

    #     if king == 'k' and "k" in state[1]:
    #         # Check for King-side castling for White
    #         if state[0][5] == '' and state[0][6] == '' and not self.is_square_attacked(0, 5, state) and not self.is_square_attacked(0, 6, state):
    #             return True
    #     if king == 'k' and "q" in state[1]:
    #         # Check for Queen-side castling for White
    #         if state[0][1] == '' and state[0][2] == '' and state[0][3] == '' and not self.is_square_attacked(0, 1, state) and not self.is_square_attacked(0, 2, state) and not self.is_square_attacked(0, 3, state):
    #             return True

    #     return False
    
    # def get_castle_moves(self, king, row, col, state):
    #     moves = []
    #     if king == 'K' and self.castling_rights['K']:
    #         moves.append(self.construct_move(row, col, 7, 6, state))  # King-side castling move for White
    #     elif king == 'K' and self.castling_rights['Q']:
    #         moves.append(self.construct_move(row, col, 7, 2, state))  # Queen-side castling move for White
    #     # Similar for Black
    #     # ...

        return moves

    def is_in_check(self, state, king_color):
        king_row, king_col = self.find_king(state, king_color)
        if king_row is None:
            return False  # King not found (shouldn't happen)

        for row in range(8):
            for col in range(8):
                piece = state[0][row][col]
                if piece and ((king_color == 'white' and piece.islower()) or (king_color == 'black' and piece.isupper())):
                    moves = self.get_piece_moves(piece, row, col, state, checkcheck=True)
                    for move in moves:
                        if move[0][0][king_row][king_col] == piece:
                            return True
        return False

    def find_king(self, state, king_color):
        king = 'K' if king_color == 'white' else 'k'
        for row in range(8):
            for col in range(8):
                if state[0][row][col] == king:
                    return row, col
        return None, None

    def is_checkmate(self, state, king_color):
        if not self.is_in_check(state, king_color):
            return False

        king_row, king_col = self.find_king(state, king_color)
        king = 'K' if king_color == 'white' else 'k'
        king_moves = self.get_king_moves(king, king_row, king_col, state)

        for move in king_moves:
            if not self.is_in_check(move[0], king_color):
                return False  # There's a move that gets the king out of check

        return True  # No moves available to get the king out of check

    def is_stalemate(self, state, turn):
        """Check if the current state is a stalemate for the player with the given turn."""
        if self.is_in_check(state, 'white' if turn == 1 else 'black'):
            return False  # Not a stalemate if the player is in check

        for row in range(8):
            for col in range(8):
                piece = state[0][row][col]
                if piece and ((turn == 1 and piece.isupper()) or (turn == -1 and piece.islower())):
                    if any(self.is_legal_move(move, state) for move in self.get_piece_moves(piece, row, col, state)):
                        return False  # There's at least one legal move
        return True  # No legal moves available

    def is_legal_move(self, move, state):
        """Check if a move is legal (doesn't leave the king in check)."""
        new_state = move[0]
        turn = -self.turn
        return not self.is_in_check(new_state, 'white' if turn == 1 else 'black')

    def checkwinner(self, state="default"):
        """Check if the game is over (checkmate, stalemate, etc.)."""
        if state == "default":
            state = self.state
        if self.round >= 200:
            v = self.valuation()
            return 1 if v > 0 else -1 if v < 0 else 2
        if self.is_in_check(state, 'white' if self.turn == -1 else 'black'):
            return self.turn  # Return the winner
        elif self.is_checkmate(state, 'white' if self.turn == 1 else 'black'):
            return -self.turn  # Return the winner
        elif self.is_stalemate(state, self.turn):
            return 2  # Stalemate (draw)

        # Additional checks for other draw conditions can be added here
        return 0  # Game is still ongoing

    def is_empty(self, row, col, state):
        return 0 <= row < 8 and 0 <= col < 8 and state[0][row][col] == ''

    def is_opponent_piece(self, row, col, piece, state):
        if 0 <= row < 8 and 0 <= col < 8:
            target = state[0][row][col]
            return target.islower() if piece.isupper() else target.isupper()
        return False

    def construct_move(self, start_row, start_col, end_row, end_col, state, new_status = None):
        # Create a new state reflecting the move
        new_state = deepcopy(state)
        if new_status:
            new_state[1] = new_status
        new_state[0][end_row][end_col] = new_state[0][start_row][start_col]
        new_state[0][start_row][start_col] = ''
        return [new_state, self.valuation(new_state)]

    def can_en_passant(self, row, col, direction, state):
        # Logic to determine if en passant is possible
        # This would involve checking the last move of the opponent to see if it was a double pawn move
        # and if the current pawn is adjacent to that pawn
        return False  # Placeholder for en passant logic

    def construct_en_passant_move(self, row, col, direction, state):
        # Create a new state reflecting the en passant move
        new_state = deepcopy(state)
        new_state[0][row][col] = ''
        new_state[0][row + direction][col] = new_state[0][row][col]  # Move the pawn
        new_state[0][row][col + direction] = ''  # Capture the opponent's pawn
        return new_state

    def algebraic_to_indices(self, move):
        # Converts algebraic notation like 'e4' to board indices (row, column)
        col_to_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        row = 8 - int(move[1])  # Row index
        col = col_to_index[move[0].lower()]  # Column index
        return row, col

    def playermove(self, move):
        if self.end == 0:
            move_sequence = [move[i:i+2] for i in range(0, len(move), 2)]
            start_row, start_col = self.algebraic_to_indices(move_sequence[0])

            next_row, next_col = self.algebraic_to_indices(move_sequence[1])
            move = self.construct_move(start_row, start_col, next_row, next_col, self.state)

            self.state = move[0]
            self.turn *= -1 
            self.value = self.valuation(self.state)
            self.end = self.checkwinner()
            if not self.thinking:
                self.render()
                self.next()
        else:
            print("Game over")
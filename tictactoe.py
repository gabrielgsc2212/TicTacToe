import math

class Board:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, spot, letter):
        self.board[spot] = letter

    def check_winner(self, letter):
        for i in range(0, 9, 3):
            if all([self.board[i+j] == letter for j in range(3)]):
                self.current_winner = letter
                return True

        for i in range(3):
            if all([self.board[i+j*3] == letter for j in range(3)]):
                self.current_winner = letter
                return True

        if self.board[0] == letter and self.board[4] == letter and self.board[8] == letter:
            self.current_winner = letter
            return True
        if self.board[2] == letter and self.board[4] == letter and self.board[6] == letter:
            self.current_winner = letter
            return True

        if all([spot != ' ' for spot in self.board]):
            self.current_winner = 'draw'
            return True

        return False

def minimax(board, maximizing, depth):
    if board.current_winner is not None or depth == 0:
        if board.current_winner == 'X':
            return -1
        elif board.current_winner == 'O':
            return 1
        else:
            return 0

    if maximizing:
        max_eval = -math.inf
        for move in board.available_moves():
            board.make_move(move, 'O')
            if board.check_winner('O'):
                max_eval = 1
                board.make_move(move, ' ')
                break
            eval = minimax(board, False, depth - 1)
            board.make_move(move, ' ')
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for move in board.available_moves():
            board.make_move(move, 'X')
            if board.check_winner('X'):
                min_eval = -1
                board.make_move(move, ' ')
                break
            eval = minimax(board, True, depth - 1)
            board.make_move(move, ' ')
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(board):
    best_move = -1
    best_eval = -math.inf
    for move in board.available_moves():
        board.make_move(move, 'O')
        eval = minimax(board, False, 6)
        board.make_move(move, ' ')
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move

def alpha_beta_pruning(board, alpha, beta, maximizing, depth):
    if board.current_winner is not None or depth == 0:
        if board.current_winner == 'X':
            return -1
        elif board.current_winner == 'O':
            return 1
        else:
            return 0

    if maximizing:
        max_eval = -math.inf
        for move in board.available_moves():
            board.make_move(move, 'O')
            if board.check_winner('O'):
                max_eval = 1
                board.make_move(move, ' ')
                break
            eval = alpha_beta_pruning(board, alpha, beta, False, depth - 1)
            board.make_move(move, ' ')
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in board.available_moves():
            board.make_move(move, 'X')
            if board.check_winner('X'):
                min_eval = -1
                board.make_move(move, ' ')
                break
            eval = alpha_beta_pruning(board, alpha, beta, True, depth - 1)
            board.make_move(move, ' ')
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move_alpha_beta(board):
    best_move = -1
    alpha = -math.inf
    beta = math.inf
    best_eval = -math.inf
    for move in board.available_moves():
        board.make_move(move, 'O')
        if board.check_winner('O'):
            board.make_move(move, ' ')
            return move
        board.make_move(move, ' ')
        
    for move in board.available_moves():
        board.make_move(move, 'X')
        if board.check_winner('X'):
            board.make_move(move, ' ')
            return move
        board.make_move(move, ' ')
        
    for move in board.available_moves():
        board.make_move(move, 'O')
        eval = alpha_beta_pruning(board, alpha, beta, False, 4)
        board.make_move(move, ' ')
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move


if __name__ == '__main__':
    board = Board()
    board.print_board()
    while not board.check_winner('O'):
        human_move = int(input("Movimento do humano (0-8): "))
        if human_move not in board.available_moves():
            print("Movimento inválido! Tente novamente")
            continue
        board.make_move(human_move, 'X')
        board.print_board()

        if board.check_winner('X'):
            if board.current_winner == 'draw':
                print("Deu velha!")
                break
            print("Vitória da humanidade!")
            break

        computer_move = find_best_move_alpha_beta(board)
        print("Movimento do computador:", computer_move)
        board.make_move(computer_move, 'O')
        board.print_board()
        if board.check_winner('O'):
            print("Vitória do computador!")
            break
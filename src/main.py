from os import system, name


class Board:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.score = None
        self.children = []
    
    def __str__(self):
        output = ''
        for i, row in enumerate(self.data):
            output += '|'.join(f' {cell if cell else " "} ' for cell in row) + '\n'
            output += '---+---+---\n' if i < 2 else ''
        return output

    def add_child(self, data):
        self.children.append(Board(data, self))

    def play(self, row, column, player):
        if self.data[row][column] is None:
            new_data = [row[:] for row in self.data]
            new_data[row][column] = player
            self.add_child(new_data)
            return True
        return False

    def is_winner(self, player):
        if (all(self.data[i][i] == player for i in range(3))
            or all(self.data[i][2-i] == player for i in range(3))):
            return True
        for i in range(3):
            if (all(self.data[i][j] == player for j in range(3))
                or all(self.data[j][i] == player for j in range(3))):
                return True
        return False

    def is_draw(self):
        if not self.is_winner('X') and not self.is_winner('O'):
            return all(cell is not None for row in self.data for cell in row)
        return False


class MoveTree:
    def __init__(self, initial_board=None):
        if initial_board:
            self.root = Board(initial_board)
        else:
            self.root = Board([[None for _ in range(3)] for _ in range(3)])

    def display(self, root, level=0):
        if root is None:
            return None
        if level == 0:
            print('Árvore de possíveis jogadas:')
            print(root)
        else:
            board = str(root).replace('\n', '\n' + '           ' * (level))
            print('           ' * (level - 1) + '     └─────' + board)
        if root.children:
            for child in root.children:
                self.display(child, level + 1)

    def display_by_level(self, root):
        queue = [(root, 0)]
        current_level = -1
        while queue:
            board, level = queue.pop(0)
            if level != current_level:
                print(f'Level {level}')
                current_level = level
            print(board)
            print('\n')
            for child in board.children:
                queue.append((child, level + 1))
    
    def generate(self, board, player):
        if board.is_draw() or board.is_winner('X') or board.is_winner('O'):
            return
        for row in range(3):
            for column in range(3):
                if board.play(row, column, player):
                    next_player = 'X' if player == 'O' else 'O'
                    self.generate(board.children[-1], next_player)


def minimax(board, is_maximizing):
    if len(board.children) == 0:
        board.score = evaluate(board)
        return evaluate(board)
    if is_maximizing:
        max_eval = float('-inf')
        for child in board.children:              
            minimax(child, False)
            max_eval = max(child.score, max_eval)
        board.score = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for child in board.children:
            minimax(child, True)
            min_eval  = min(min_eval, child.score)
        board.score = min_eval
        return min_eval


def evaluate(board):
    if board.is_winner('X'):
        return 1
    elif board.is_winner('O'):
        return -1
    else:
        return 0


def find_best_move(board, player):
    best_moves = []
    minimax(board, True) if player == 'X' else minimax(board, False)
    for child in board.children:
        if child.score == board.score:
            best_moves.append(child)
    return best_moves


if __name__ == '__main__':
    move_tree = MoveTree()
    for row in range(3):
        for column in range(3):
            print('Forneça as jogadas de um tabuleiro inicial:')
            print(move_tree.root)
            player = input(f'Linha {row + 1}, Coluna {column + 1}: ').upper()
            move_tree.root.data[row][column] = None if player == '' else player
            system('cls' if name == 'nt' else 'clear')
    next_player = input('Quem será o próximo a jogar? [X / O] ').upper()
    system('cls' if name == 'nt' else 'clear')
    move_tree.generate(move_tree.root, next_player)
    move_tree.display(move_tree.root)
    best_moves = find_best_move(move_tree.root, next_player)
    print(f'Para que {next_player} vença, as próximas jogadas de {next_player} podem ser:')
    for move in best_moves:
        print(move)

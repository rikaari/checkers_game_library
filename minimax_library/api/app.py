from flask import Flask, request, jsonify, render_template
import os

# Constants
BOARD_SIZE = 8
EMPTY = '   '
PLAYER1_PIECE = 'o'
PLAYER2_PIECE = 'x'
HIGHLIGHT = '\033[93m * \033[0m'

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    return "Hello, Flask!"

def print_board(board, highlight_move=None):
    """Prints the current state of the board with labels and highlights, intended for terminal output."""
    print("   A   B   C   D   E   F   G   H")
    print("  +---+---+---+---+---+---+---+---+")
    for row_index, row in enumerate(board):
        row_display = []
        for col_index, cell in enumerate(row):
            if highlight_move and (row_index, col_index) in highlight_move:
                row_display.append(HIGHLIGHT)
            else:
                if cell == PLAYER1_PIECE:
                    row_display.append('\033[94m o \033[0m')
                elif cell == PLAYER2_PIECE:
                    row_display.append('\033[91m x \033[0m')
                else:
                    row_display.append(EMPTY)
        print(f"{row_index + 1} |" + "|".join(row_display) + "|")
        print("  +---+---+---+---+---+---+---+---+")
    print()

def position_to_indices(pos):
    col, row = pos
    return int(row) - 1, ord(col.lower()) - ord('a')

def make_move(board, start, end):
    piece = board[start[0]][start[1]]
    board[end[0]][end[1]] = piece
    board[start[0]][start[1]] = EMPTY

def is_valid_move(board, start, end, current_player_piece):
    if board[start[0]][start[1]] != current_player_piece:
        return False
    if board[end[0]][end[1]] != EMPTY:
        return False
    direction = 1 if current_player_piece == PLAYER1_PIECE else -1
    if (end[0] - start[0] != direction) or (abs(end[1] - start[1]) != 1):
        return False
    middle_row, middle_col = (start[0] + end[0]) // 2, (start[1] + end[1]) // 2
    if abs(end[0] - start[0]) == 2 and abs(end[1] - start[1]) == 2:
        if (0 <= middle_row < BOARD_SIZE and 0 <= middle_col < BOARD_SIZE and
            board[middle_row][middle_col] != EMPTY and
            board[middle_row][middle_col] != current_player_piece):
            return True
    return True

def read_board_from_file(filename):
    if not os.path.exists(filename):
        return None, f"File '{filename}' not found."
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                if not (line.startswith('o(') or line.startswith('x(')) or not line.endswith(')'):
                    return None, "Invalid line format in file."
                piece = 'o' if line.startswith('o(') else 'x'
                position = line[2:-1]
                row, col = position_to_indices(position)
                board[row][col] = PLAYER1_PIECE if piece == 'o' else PLAYER2_PIECE
        return board, None
    except Exception as e:
        return None, f"Error reading the file: {e}"

def evaluate_board(board):
    player1_pieces = sum(row.count(PLAYER1_PIECE) for row in board)
    player2_pieces = sum(row.count(PLAYER2_PIECE) for row in board)
    return player1_pieces - player2_pieces

def get_valid_moves(board, player_piece):
    direction = 1 if player_piece == PLAYER1_PIECE else -1
    moves = []
    opponent_piece = PLAYER2_PIECE if player_piece == PLAYER1_PIECE else PLAYER1_PIECE
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == player_piece:
                for dr, dc in [(direction, -1), (direction, 1)]:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                        if board[new_row][new_col] == EMPTY:
                            moves.append(((row, col), (new_row, new_col)))
                for dr, dc in [(direction * 2, -2), (direction * 2, 2)]:
                    middle_row, middle_col = row + dr // 2, col + dc // 2
                    new_row, new_col = row + dr, col + dc
                    if (0 <= middle_row < BOARD_SIZE and 0 <= middle_col < BOARD_SIZE and
                        0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE and
                        board[middle_row][middle_col] == opponent_piece and
                        board[new_row][new_col] == EMPTY):
                        moves.append(((row, col), (new_row, new_col)))
    return moves

def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or not get_valid_moves(board, PLAYER1_PIECE if maximizing_player else PLAYER2_PIECE):
        return evaluate_board(board), None
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_valid_moves(board, PLAYER1_PIECE):
            new_board = [row[:] for row in board]
            make_move(new_board, *move)
            eval, _ = minimax(new_board, depth-1, False, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_valid_moves(board, PLAYER2_PIECE):
            new_board = [row[:] for row in board]
            make_move(new_board, *move)
            eval, _ = minimax(new_board, depth-1, True, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

@app.route('/predict_move', methods=['POST'])
def predict_move():
    app.logger.debug('Received data: %s', request.json)
    data = request.json
    filename = data.get('filename')
    print(f"Received filename: {filename}")  # Debugging line

    if not filename:
        return jsonify({"error": "Please provide a filename in the request."}), 400

    board, error = read_board_from_file(filename)
    if error:
        print(f"Error reading board from file: {error}")  # Debugging line
        return jsonify({"error": error}), 400

    print("Current board after reading from file:", board)  # Debugging line
    _, best_move = minimax(board, 3, False, float('-inf'), float('inf'))

    if best_move:
        move = {
            "from": f"{chr(best_move[0][1] + ord('A'))}{best_move[0][0] + 1}",
            "to": f"{chr(best_move[1][1] + ord('A'))}{best_move[1][0] + 1}"
        }
        # Make the move on the board
        make_move(board, best_move[0], best_move[1]) 

        # Instead of rendering a template, return the JSON response
        return jsonify({"best_move": move, "board": board})

    return jsonify({"error": "No valid moves available."}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
import os

# Constants
BOARD_SIZE = 8
# Symbols for board representation
EMPTY = '   '
PLAYER1_PIECE = 'o'  # Use plain 'o' for internal logic
PLAYER2_PIECE = 'x'  # Use plain 'x' for internal logic
HIGHLIGHT = '\033[93m * \033[0m'  # Yellow ' * '

def print_board(board, highlight_move=None):
    """Prints the current state of the board with labels and highlights."""
    print("   A   B   C   D   E   F   G   H")
    print("  +---+---+---+---+---+---+---+---+")
    for row_index, row in enumerate(board):
        row_display = []
        for col_index, cell in enumerate(row):
            if highlight_move and (row_index, col_index) in highlight_move:
                row_display.append(HIGHLIGHT)
            else:
                if cell == PLAYER1_PIECE:
                    row_display.append('\033[94m o \033[0m')  # Blue ' o '
                elif cell == PLAYER2_PIECE:
                    row_display.append('\033[91m x \033[0m')  # Red ' x '
                else:
                    row_display.append(EMPTY)
        print(f"{row_index + 1} |" + "|".join(row_display) + "|")
        print("  +---+---+---+---+---+---+---+---+")
    print()

def position_to_indices(pos):
    """Converts board position like 'b3' to indices."""
    col, row = pos
    return int(row) - 1, ord(col.lower()) - ord('a')

def make_move(board, start, end):
    """Moves a piece on the board."""
    piece = board[start[0]][start[1]]
    print(f"Moving piece {piece} from {start} to {end}")
    board[end[0]][end[1]] = piece
    board[start[0]][start[1]] = EMPTY
    print_board(board)  # Visualize board post-move

def is_valid_move(board, start, end, current_player_piece):
    """Checks if the move is valid."""
    
    # Boundary check for the indices
    if not (0 <= start[0] < BOARD_SIZE and 0 <= start[1] < BOARD_SIZE):
        print("Invalid start indices, out of range.")
        return False
    if not (0 <= end[0] < BOARD_SIZE and 0 <= end[1] < BOARD_SIZE):
        print("Invalid end indices, out of range.")
        return False
    
    print(f"Checking if move from {start} to {end} is valid for {current_player_piece}")

    # Check if the starting position has the player's piece
    if board[start[0]][start[1]] != current_player_piece:
        print("Invalid move: Start position does not have the player's piece.")
        return False

    # Check if the end position is empty
    if board[end[0]][end[1]] != EMPTY:
        print("Invalid move: End position is not empty.")
        return False

    # Determine direction for simple moves
    direction = 1 if current_player_piece == PLAYER1_PIECE else -1
    delta_row = end[0] - start[0]
    delta_col = end[1] - start[1]

    print(f"delta_row: {delta_row}, delta_col: {delta_col}")

    # Check for a simple diagonal move
    if delta_row == direction and abs(delta_col) == 1:
        print("Valid simple move detected.")
        return True

    # Check for jump (capturing move)
    if delta_row == 2 * direction and abs(delta_col) == 2:
        middle_row, middle_col = (start[0] + end[0]) // 2, (start[1] + end[1]) // 2
        middle_piece = board[middle_row][middle_col]
        if (middle_piece != EMPTY and middle_piece != current_player_piece):
            print("Valid jump move detected.")
            return True

    print("Invalid move: Did not meet any valid move conditions.")
    return False

def read_board_from_file(filename):
    """Reads the board state from a file in the format piece(position)."""
    if not os.path.exists(filename):
        print(f"File '{filename}' not found.")
        return None
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                if not (line.startswith('o(') or line.startswith('x(')) or not line.endswith(')'):
                    print("Invalid line format:", line)
                    return None
                piece = 'o' if line.startswith('o(') else 'x'
                position = line[2:-1]  # Extract the position part from the line
                row, col = position_to_indices(position)
                # Place the piece on the board
                board[row][col] = PLAYER1_PIECE if piece == 'o' else PLAYER2_PIECE
        return board
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def evaluate_board(board):
    """Simple evaluation function for the board."""
    player1_pieces = sum(row.count(PLAYER1_PIECE) for row in board)
    player2_pieces = sum(row.count(PLAYER2_PIECE) for row in board)
    return player1_pieces - player2_pieces

def get_valid_moves(board, player_piece):
    """Returns a list of valid moves for a given player piece, including jumps."""
    direction = 1 if player_piece == PLAYER1_PIECE else -1
    moves = []
    opponent_piece = PLAYER2_PIECE if player_piece == PLAYER1_PIECE else PLAYER1_PIECE
    
    print(f"Finding valid moves for {player_piece}")
    
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == player_piece:
                # Check for normal moves
                for dr, dc in [(direction, -1), (direction, 1)]:  # Diagonal directions
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                        if board[new_row][new_col] == EMPTY:
                            moves.append(((row, col), (new_row, new_col)))
                            print(f"Found valid simple move from {(row, col)} to {(new_row, new_col)}")

                # Check for jump moves
                for dr, dc in [(direction * 2, -2), (direction * 2, 2)]:
                    middle_row, middle_col = row + dr // 2, col + dc // 2
                    new_row, new_col = row + dr, col + dc
                    if (0 <= middle_row < BOARD_SIZE and
                        0 <= middle_col < BOARD_SIZE and
                        0 <= new_row < BOARD_SIZE and
                        0 <= new_col < BOARD_SIZE and
                        board[middle_row][middle_col] == opponent_piece and
                        board[new_row][new_col] == EMPTY):
                        moves.append(((row, col), (new_row, new_col)))
                        print(f"Found valid jump move from {(row, col)} to {(new_row, new_col)} via {(middle_row, middle_col)}")

    if not moves:
        print(f"No valid moves found for {player_piece}")
    return moves

def minimax(board, depth, maximizing_player, alpha, beta):
    """Minimax algorithm with alpha-beta pruning."""
    if depth == 0 or not get_valid_moves(board, PLAYER1_PIECE if maximizing_player else PLAYER2_PIECE):
        return evaluate_board(board), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_valid_moves(board, PLAYER1_PIECE):
            new_board = [row[:] for row in board]
            make_move(new_board, *move)
            eval, _ = minimax(new_board, depth - 1, False, alpha, beta)
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
            eval, _ = minimax(new_board, depth - 1, True, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def main():
    # Get the player input
    while True:
        player = input("Choose your player ('x' or 'o'): ").strip().lower()
        if player == 'o':
            current_player_piece = PLAYER1_PIECE
            ai_piece = PLAYER2_PIECE
            break
        elif player == 'x':
            current_player_piece = PLAYER2_PIECE
            ai_piece = PLAYER1_PIECE
            break
        else:
            print("Invalid input. Please enter 'x' or 'o'.")

    # Read the board from a file
    filename = input("Enter the filename for the board state: ")
    board = read_board_from_file(filename)
    if not board:
        return  # Exit if the board is invalid
    
    # Print the initial board state
    print_board(board)

    # Use minimax immediately for the player's piece choice
    print(f"Predicting best move for player {'1' if player == 'o' else '2'}...")
    _, best_move = minimax(board, 3, player == 'o', float('-inf'), float('inf'))

    # Highlight the predicted move
    if best_move:
        print(f"Predicted move for {'o' if player == 'o' else 'x'} is from {chr(best_move[0][1] + ord('A'))}{best_move[0][0] + 1} to {chr(best_move[1][1] + ord('A'))}{best_move[1][0] + 1}.")
        print_board(board, highlight_move=[best_move[0], best_move[1]])
    else:
        print("No valid moves available.")

if __name__ == "__main__":
    main()

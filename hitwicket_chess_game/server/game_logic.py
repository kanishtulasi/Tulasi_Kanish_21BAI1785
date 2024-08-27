# server/game_logic.py

GRID_SIZE = 5

def update_game_state(board, players, move, player):
    # Parse the move
    piece, direction = move.split(':')

    # Find the current position of the piece
    current_position = None
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == f"{player}-{piece}":
                current_position = (r, c)
                break
        if current_position:
            break

    if not current_position:
        return board, players, False  # Invalid move: piece not found

    r, c = current_position

    # Determine new position based on direction and piece type
    if piece.startswith('P'):  # Pawn
        dr, dc = pawn_move(direction)
    elif piece.startswith('H1'):  # Hero1
        dr, dc = hero1_move(direction)
    elif piece.startswith('H2'):  # Hero2
        dr, dc = hero2_move(direction)
    else:
        return board, players, False  # Invalid move: unknown piece

    # Calculate new position
    new_r, new_c = r + dr, c + dc

    # Check if the move is out of bounds
    if not (0 <= new_r < GRID_SIZE and 0 <= new_c < GRID_SIZE):
        return board, players, False  # Invalid move: out of bounds

    # Check for friendly fire
    if board[new_r][new_c].startswith(player):
        return board, players, False  # Invalid move: friendly fire

    # Handle combat (remove opponent piece if present)
    if board[new_r][new_c] and not board[new_r][new_c].startswith(player):
        opponent_piece = board[new_r][new_c]
        remove_piece(players, opponent_piece)

    # Move the piece
    board[r][c] = ''  # Clear the old position
    board[new_r][new_c] = f"{player}-{piece}"  # Place the piece in the new position

    return board, players, True  # Valid move

def pawn_move(direction):
    # Pawn moves one step in any direction
    moves = {
        'L': (0, -1),
        'R': (0, 1),
        'F': (-1, 0),
        'B': (1, 0)
    }
    return moves.get(direction, (0, 0))

def hero1_move(direction):
    # Hero1 moves two steps in any straight direction
    moves = {
        'L': (0, -2),
        'R': (0, 2),
        'F': (-2, 0),
        'B': (2, 0)
    }
    return moves.get(direction, (0, 0))

def hero2_move(direction):
    # Hero2 moves two steps in any diagonal direction
    moves = {
        'FL': (-2, -2),
        'FR': (-2, 2),
        'BL': (2, -2),
        'BR': (2, 2)
    }
    return moves.get(direction, (0, 0))

def remove_piece(players, piece):
    # Extract player and piece name
    player, piece_name = piece.split('-')
    # Remove the piece from the player's list
    if piece_name in players[player]['pieces']:
        players[player]['pieces'].remove(piece_name)

    # Check for game over condition
    if not players[player]['pieces']:
        print(f"Player {player} has lost all pieces!")

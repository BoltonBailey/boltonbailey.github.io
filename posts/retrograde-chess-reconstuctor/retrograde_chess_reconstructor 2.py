from chess import *
# import uci
import chess.engine
# import svg
import networkx as nx
import sys


board = Board(STARTING_FEN)


# Now we have our board ready, load your engine:
# handler = engine.InfoHandler()
# give correct address of your engine here
engine = chess.engine.SimpleEngine.popen_uci(
    '~/stockfish-11-mac/Mac/stockfish-11-64')

# Flag to ignore strategic plausibility of a game and just find one
IGNORE_SCORE = True


def score(position):

    if IGNORE_SCORE:
        return 0

    board = Board(position)

    info = engine.analyse(board, chess.engine.Limit(depth=20))

    white_cp_score = min(
        2000, max(-2000, int(info["score"].white().score(mate_score=10000))))

    # Return score
    # Clamped to -20, +20, since beyond this, it doesn't matter.
    return white_cp_score


def predecessors(board):
    """ List all positions that can lead to this in one move """

    # TODO this function is *deeply* inefficient. Improve it

    if isinstance(board, str):
        board = Board(board)

    final_fen = board.fen()

    print(final_fen)
    print(board)
    print(score(final_fen))

    # We first list possible previous board states,
    # ignoring the turn, e.p. square, and castling rights listed in the FEN
    prev_board_fens = set()
    board = board.copy()
    prev_turn = not board.turn
    board.turn = not board.turn
    board.ep_square = None

    # Set of squares of the color making the move
    possible_to_squares = board.pieces(
        KING, prev_turn) | board.pieces(QUEEN, prev_turn) | board.pieces(ROOK, prev_turn) | board.pieces(KNIGHT, prev_turn) | board.pieces(BISHOP, prev_turn) | board.pieces(PAWN, prev_turn)

    # Non Capture Normal Moves
    print("Non Capture Normal Moves")
    for to_square in possible_to_squares:
        for from_square in SQUARES:
            b = board.copy()
            b.set_piece_at(from_square, b.piece_at(to_square))
            b.remove_piece_at(to_square)
            prev_board_fens.add(b.fen())

    # Captures
    for to_square in possible_to_squares:
        for from_square in SQUARES:

            for piece_type in PIECE_TYPES:
                b = board.copy()
                b.set_piece_at(from_square, b.piece_at(to_square))
                b.set_piece_at((to_square), Piece(
                    piece_type, not b.piece_at(from_square).color))
                prev_board_fens.add(b.fen())

    # En Passant captures
    print("En Passant captures")
    # Black captures white
    for to_square in board.pieces(PAWN, board.turn) & SquareSet(BB_RANK_7):
        for from_square in SquareSet(BB_RANK_6):
            capture_square = square(square_file(to_square), 5)
            b = board.copy()
            b.set_piece_at(from_square, b.piece_at(to_square))
            b.remove_piece_at(to_square)
            b.set_piece_at(capture_square, Piece(PAWN, WHITE))
            prev_board_fens.add(b.fen())

    # White captures Black
    for to_square in board.pieces(PAWN, board.turn) & SquareSet(BB_RANK_2):
        for from_square in SquareSet(BB_RANK_3):
            capture_square = square(square_file(to_square), 2)
            b = board.copy()
            b.set_piece_at(from_square, b.piece_at(to_square))
            b.remove_piece_at(to_square)
            b.set_piece_at(capture_square, Piece(PAWN, BLACK))
            prev_board_fens.add(b.fen())

    # Castling
    print("Castling")
    # White kingside
    b = board.copy()
    b.set_piece_at(E1, Piece(KING, WHITE))
    b.set_piece_at(H1, Piece(ROOK, WHITE))
    b.remove_piece_at(F1)
    b.remove_piece_at(G1)
    prev_board_fens.add(b.fen())
    # White queenside
    b = board.copy()
    b.set_piece_at(E1, Piece(KING, WHITE))
    b.set_piece_at(A1, Piece(ROOK, WHITE))
    b.remove_piece_at(D1)
    b.remove_piece_at(C1)
    prev_board_fens.add(b.fen())
    # Black kingside
    b = board.copy()
    b.set_piece_at(E8, Piece(KING, BLACK))
    b.set_piece_at(H8, Piece(ROOK, BLACK))
    b.remove_piece_at(F8)
    b.remove_piece_at(G8)
    prev_board_fens.add(b.fen())
    # Black queenside
    b = board.copy()
    b.set_piece_at(E8, Piece(KING, BLACK))
    b.set_piece_at(A8, Piece(ROOK, BLACK))
    b.remove_piece_at(D8)
    b.remove_piece_at(C8)
    prev_board_fens.add(b.fen())

    # Promotions
    # White
    for to_square in possible_to_squares & SquareSet(BB_RANK_8):
        from_square = square(square_file(to_square), 6)
        b = board.copy()
        b.set_piece_at(from_square, Piece(PAWN, WHITE))
        b.remove_piece_at(to_square)
        prev_board_fens.add(b.fen())

    # Black
    for to_square in possible_to_squares & SquareSet(BB_RANK_1):
        from_square = square(square_file(to_square), 1)
        b = board.copy()
        b.set_piece_at(from_square, Piece(PAWN, BLACK))
        b.remove_piece_at(to_square)
        prev_board_fens.add(b.fen())

    print(f"{len(prev_board_fens)} possible states, not considering castling or ep")

    # For all constructed boards, add all possible e.p. squares
    # and castling rights

    # Possible castling rights must be superset of castling rights of final fen
    # Also
    possible_castling_fens = [
        "",
        "K",
        "Q",
        "KQ",
        "k",
        "Kk",
        "Qk",
        "KQk",
        "q",
        "Kq",
        "Qq",
        "KQq",
        "kq",
        "Kkq",
        "Qkq",
        "KQkq",
    ]
    for fen in list(prev_board_fens):
        for castling_fen in possible_castling_fens:
            b = Board(fen)
            b.set_castling_fen(castling_fen)
            if b.is_valid():
                prev_board_fens.add(b.fen())

    for fen in list(prev_board_fens):
        for ep_square in SquareSet(BB_RANK_3 | BB_RANK_6):
            b = Board(fen)
            b.ep_square = ep_square
            prev_board_fens.add(b.fen())

    print(f"{len(prev_board_fens)} possible states, counting castling or ep")

    for fen in prev_board_fens:

        b = Board(fen)
        if not b.is_valid():
            # print(fen, "Not valid")
            continue
        nexts = []

        for move in b.legal_moves:

            bc = b.copy()
            bc.push(move)
            # if fen == "3k4/q1P1R3/8/8/8/8/8/1N2K3 b - - 0 1":
            #     print(b)
            #     print(move)
            #     print(bc)
            #     print(bc.fen())
            #     print(board.fen()[:-4], bc.fen()[:-4])
            nexts.append(bc.fen())

        # trim the last 4 chars to ignore halfmove clock and fullmove number
        if not any(final_fen[:-4] == n[:-4] for n in nexts):
            # print(fen, "No right moves")
            continue

        yield fen

    print("Yielded all predecessors")


# for pred in predecessors("8/q1P1k3/8/8/8/8/8/1N2K3 w - - 0 1"):
#     print(pred)
#     print(Board(pred))


MOVE_WEIGHT_CONSTANT = 0.1


class ChessGraph(nx.DiGraph):

    def __contains__(self, position):
        return True

    def __getitem__(self, position):
        """ Dict of positions that can lead to this one in one move

        The weight of a position is
        the difference in eval between the positions
        plus a constant to punish needlessly long games
        """
        position_score = score(position)
        return {previous: {"weight": MOVE_WEIGHT_CONSTANT + abs(score(previous) - position_score)} for previous in predecessors(position)}


initial_position_score = score(chess.Board().fen())


def heuristic(source, target):
    """ An A-star heuristic for the position graph

    Formally, this should return a value at least the sum of edges on the 
    shortest path.
    """
    assert target == STARTING_FEN

    lower_bound_moves = 0
    for square in SQUARES:
        if Board(source).piece_at(square) != Board(target).piece_at(square):
            lower_bound_moves += 1

    # Above Assumes each move returns at most one piece to its target square
    # Technically, castling and across-the-board Rook and Queen captures can
    # return two pieces to their home squares, so this number can be up to 5
    # less
    lower_bound_moves = max(0, lower_bound_moves-5)

    path_length_lower_bound = lower_bound_moves * MOVE_WEIGHT_CONSTANT + \
        abs(score(source) - initial_position_score)

    return path_length_lower_bound * 10  # Multiply to cheat to make it faster


def reconstruct(position):

    path = nx.astar_path(ChessGraph(), position, STARTING_FEN,
                         heuristic=heuristic)

    print(f"Found solution of length {len(path)}")
    time.sleep(3)
    for position in path:
        print(Board(position))


reconstruct("8/q1P1k3/8/8/8/8/8/1N2K1N1 w - - 0 1")

engine.quit()

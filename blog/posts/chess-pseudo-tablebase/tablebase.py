import chess
# import chess.uci
import chess.engine
import chess.svg
import sys
from bloom_filter import BloomFilter

board = chess.Board(
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")


# Now we have our board ready, load your engine:
# handler = chess.engine.InfoHandler()
# give correct address of your engine here
engine = chess.engine.SimpleEngine.popen_uci(
    '~/stockfish-11-mac/Mac/stockfish-11-64')

info = engine.analyse(board, chess.engine.Limit(depth=20))

# print best move, evaluation and mainline:
print("Score:", info["score"])


bad_boards = []

for board in AllBoardsGenerator(3):
    info = engine.analyse(board, chess.engine.Limit(depth=20))
    score = info["score"]

    if score != todo_tablebase_query(board):
        bad_boards.add(board)


print(len(bad_boards), len(all_345_boards),
      len(bad_boards), len(all_345_boards),)

engine.quit()

chess.svg.board(board=board)


class AllBoardsGenerator:
    """Generates all boards of a given number of men."""

    TODO


from collections import Counter
from itertools import chain, combinations
from functools import lru_cache
import random

# A life board is represented as a set of (x, y) coordinate points


def step(board):

    next_to = Counter()

    for x, y in board:
        next_to[x-1, y+1] += 1
        next_to[x, y+1] += 1
        next_to[x+1, y+1] += 1
        next_to[x-1, y] += 1
        next_to[x+1, y] += 1
        next_to[x-1, y-1] += 1
        next_to[x, y-1] += 1
        next_to[x+1, y-1] += 1

    new = set()

    for x, y in board:
        if next_to[x, y] == 2 or next_to[x, y] == 3:
            new.add((x, y))

    for x, y in next_to:
        if next_to[x, y] == 3:
            new.add((x, y))

    return new


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


# Counts boards of size (2n+1)x(2n+1) resulting in on after n steps
def count_on(n):

    possible_squares = [(x, y) for x in range(2*n+1) for y in range(2*n+1)]

    count = 0

    for board in powerset(possible_squares):
        for _ in range(n):
            board = step(board)

        if (n-1, n-1) in board:
            count += 1

    return count


# The spacetime of a randomly initialized board
@lru_cache(maxsize=None)
def evaluate(x, y, t):
    if t == 0:
        return bool(random.randint(0, 1))

    count = sum(
        [
            evaluate(x-1, y+1, t-1),
            evaluate(x, y+1, t-1),
            evaluate(x+1, y+1, t-1),
            evaluate(x-1, y, t-1),
            evaluate(x+1, y, t-1),
            evaluate(x-1, y-1, t-1),
            evaluate(x, y-1, t-1),
            evaluate(x+1, y-1, t-1)
        ]
    )

    if evaluate(x, y, t-1):
        return 2 <= count <= 3
    else:
        return count == 3


def approximate(n):

    # possible_squares = [(x, y) for x in range(2*n+1) for y in range(2*n+1)]

    count = 0

    for x in range(1000):
        for y in range(1000):
            if evaluate(x, y, n):
                count += 1

    return count


for i in range(1, 2000):
    print(i, approximate(i))

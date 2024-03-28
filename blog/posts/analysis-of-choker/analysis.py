from choker import *


def print_tables(initial_cards=Hand()):

    if initial_cards.size() == 0:
        print()
        print(f"### Statistics for All Hands")
        print()

    if initial_cards.size() == 2:
        print()
        print(f"### Statistics for Flop: {initial_cards}")
        print()

    # A map from piecesets to probabilities thereof
    pieceset_probabilities = Counter()

    avg_score = 0.0

    avg_squared_score = 0.0

    score_pmf = [0] * 30

    print()
    print("#### Hand Statistics Table")
    print()

    print("| Hand | Piece Set | Points | Probability |")
    print("|------|-----------|--------|-------------|")

    for hand in Hand.list_all():

        pieceset = hand.pieceset()
        queens = pieceset["Q"]
        rooks = pieceset["R"]
        bishops = pieceset["B"]
        knights = pieceset["N"]
        pawns = pieceset["P"]
        to_tuple = (queens, rooks, bishops, knights, pawns)
        points = 9 * queens + 5 * rooks + 3 * bishops + 3 * knights + pawns

        probability = (
            hand-initial_cards).probability(missing_from_deck=initial_cards)

        avg_score += probability * points
        avg_squared_score += probability * points**2

        score_pmf[points] += probability

        pieceset_probabilities[pieceset] += probability

        if probability > 0:
            print(f"| {hand} | {pieceset} | {points} | {probability:.3%} |")

    std_dev = math.sqrt(avg_squared_score - avg_score**2)
    print()
    if initial_cards.size() == 0:
        print(
            f"The average score is {avg_score}, and the standard deviation is {std_dev}")
    if initial_cards.size() == 2:
        print(
            f"For flop {initial_cards} The average score is {avg_score:.3}, and the standard deviation is {std_dev:.3}")
    print()
    print("#### Point distribution Table")
    print()
    print("| | Prob. Less than | Prob Equal | Prob Greater Than |")
    print("|-|---------------- |------------|-------------------|")

    for i in range(9, 30, 2):
        less = sum(score_pmf[:i])
        more = sum(score_pmf[i+1:])
        print(f"| {i} | {less:.3%} | {score_pmf[i]:.3%} | {more:.3%} |")

    print()
    print("#### Piece Set table")
    print()
    print("| Piece Set | Points | Probability |")
    print("|-----------|--------|-------------|")
    for pieceset in pieceset_probabilities:
        prob = pieceset_probabilities[pieceset]
        # print(type(pieceset), pieceset)
        points = pieceset.points()
        if prob > 0:
            print(f"| {pieceset} | {points} | {prob:.3%} |")


# Flops analysis

print_tables()

flops = map(Hand, list(itertools.combinations_with_replacement(PIECES, 2)))

for flop in flops:
    print_tables(flop)

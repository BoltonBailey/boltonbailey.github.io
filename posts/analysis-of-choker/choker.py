
from collections import Counter
import itertools
import math

PIECES = ["Q", "R", "B", "N", "P"]
DECK = Counter({"Q": 4, "R": 8, "B": 8, "N": 8, "P": 16})

# turns = list(itertools.combinations_with_replacement(cards, 4))


class Hand(Counter):
    """A set of choker cards, ignoring order.

    Not necessarily five total cards
    """

    @classmethod
    def list_all(cls):
        return map(Hand, itertools.combinations_with_replacement(PIECES, 5))

    def __str__(self):
        # for p in "QRNBP":
        #     print(p, self[p], p*self[p])
        return "".join(p * self[p] for p in PIECES)

    def __sub__(self, other):
        return Hand(self - other)

    def size(self):
        return sum(self[p] for p in PIECES)

    def pieceset(self):
        """Returns the set of pieces a player is given for a 5-card hand.

        The hand is a counter on PIECES.

        The returned pieceset is in the form of a counter subclass,
        mapping pieces to the number of pieces in the hand.
        """
        assert self.size() == 5

        # The "Empress rule", in a full house, one of the triplet is converted to
        # a queen.

        if 2 in self.values() and 3 in self.values():
            pieceset = Counter({piece: 2 for piece in self})
            if "Q" in self:
                # If the triplet piece is a queen the empress rule causes the
                # third queen not to be demoted, but we must still apply the
                # demotion rule to the second queen.
                # If the pair piece is a queen, we demote it and queen the other
                # piece.
                # Either way, the result is two of each in the hand, plus a pawn
                pieceset["P"] += 1
                return PieceSet(pieceset)
            else:
                # Otherwise, a queen is the last piece.
                pieceset["Q"] += 1
                return PieceSet(pieceset)

        # The "Palace rule", in one of each, the pawn is converted to a queen.
        if all(self[piece] == 1 for piece in self):
            return PieceSet({"Q": 2, "R": 1, "B": 1, "N": 1})

        pieceset = Counter(self)

        # The "Demotion" rules
        if self["Q"] > 1:
            pieceset["Q"] = 1
            pieceset["P"] += self["Q"] - 1

        if self["R"] > 2:
            pieceset["R"] = 2
            pieceset["P"] += self["R"] - 2

        if self["B"] > 2:
            pieceset["B"] = 2
            pieceset["P"] += self["B"] - 2

        if self["N"] > 2:
            pieceset["N"] = 2
            pieceset["P"] += self["N"] - 2

        # The "Promotion" rule
        if self["P"] == 3:
            pieceset["P"] = 2
            pieceset["R"] += 1

        elif self["P"] == 4:
            pieceset["P"] = 2
            pieceset["R"] += 1
            pieceset["Q"] += 1

        elif self["P"] == 5:
            pieceset["P"] = 2
            pieceset["R"] += 1
            pieceset["Q"] += 2

        return PieceSet(pieceset)

    def probability(self, missing_from_deck=Counter()):
        """The probability of drawing this hand

        Specifically, given the standard 44-card choker deck, a counter of 
        cards that have been removed from the deck, this returns the 
        likelihood of the next k cards drawn from the deck comprising self, 
        where k is the size of self.
        """
        if not all(0 <= missing_from_deck[p] for p in PIECES):
            raise ValueError("Cards missing cannot contain negative card")
        if not all(missing_from_deck[p] <= DECK[p] for p in PIECES):
            raise ValueError("Cards missing more than total in deck")

        # Counter of remaining deck
        deck = DECK - missing_from_deck

        if not all(self[p] <= deck[p] for p in PIECES):
            return 0

        # Counter of all ways to draw
        ways_to_draw = math.prod(math.comb(deck[p], self[p]) for p in PIECES)

        return ways_to_draw / math.comb(deck.size(), self.size())


class PieceSet(Counter):

    def __eq__(self, other):
        return self.to_tuple == other.to_tuple

    def __hash__(self):
        return hash(self.to_tuple())

    def __str__(self):
        # for p in "QRNBP":
        #     print(p, self[p], p*self[p])
        return "".join(p * self[p] for p in PIECES)

    def queens(self):
        return self["Q"]

    def rooks(self):
        return self["R"]

    def bishops(self):
        return self["B"]

    def knights(self):
        return self["N"]

    def pawns(self):
        return self["P"]

    def to_tuple(self):
        return (self.queens(), self.rooks(), self.bishops(), self.knights(), self.pawns())

    def points(self):
        return 9 * self.queens() + 5 * self.rooks() + 3 * self.bishops() + 3 * self.knights() + self.pawns()

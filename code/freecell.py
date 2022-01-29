
import random
# import pydealer
import networkx as nx
import time

suits = "CDHS"
ranks = "A23456789TJQK"

cards = [r + s for r in ranks for s in suits]


def card_below(card):
    r, s = card
    if r == "A":
        return None
    return ranks[ranks.index(r) - 1] + s


def valid_build(card1, card2):
    r1, s1 = card1
    r2, s2 = card2

    c1 = s1 in "DH"
    c2 = s2 in "DH"

    return ranks.index(r1) + 1 == ranks.index(r2) and c1 != c2


assert card_below("TC") == "9C"


def shuffled_deck():
    deck = list(cards)
    random.shuffle(deck)

    return deck


class Position(object):

    def __init__(self, cascades=tuple(() for _ in range(8)), freecells=set()):
        """
        Initializes a new Position object,
        by default with empty cascades and freecells
        self.cascades is a tuple of 8 tuples of cards
        self.freecells is a set of cards
        The foundation is not tracked. Cards not in the cascades or in the
        freecells are considered to be in the foundation.
        """
        self.cascades = tuple(cascades)
        self.freecells = set(freecells)

    @classmethod
    def random(cls):
        deck = shuffled_deck()

        cascades = []

        for size in [7, 7, 7, 7, 6, 6, 6, 6]:
            cascades.append(tuple(deck[:size]))
            deck = deck[size:]

        return cls(cascades=tuple(cascades))

    def in_cascades(self, card):
        return any(card in cascade for cascade in self.cascades)

    def in_freecells(self, card):
        return card in self.freecells

    def in_foundation(self, card):
        return not self.in_cascades(card) and not self.in_freecells(card)

    def next_foundation(self, suit):
        """
        Returns the next card in the suit to go on the foundation
        """
        for rank in ranks:
            if not self.in_foundation(rank + suit):
                return rank + suit
        return None

    def last_foundation(self, suit):
        """
        Returns the next card in the suit to go on the foundation
        """
        if not self.in_foundation("A" + suit):
            return None

        return [rank + suit for rank in ranks if self.in_foundation(rank+suit)][-1]

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False

        return (self.freecells == other.freecells) and (self.cascades == other.cascades)

    def __hash__(self):
        return hash((self.cascades, frozenset(self.freecells)))

    def __str__(self):

        output = ""

        output += "+-----------------------+\n"
        output += "|" + " ".join(sorted(self.freecells)).ljust(11) + "|"
        for suit in suits:
            if self.last_foundation(suit):
                output += self.last_foundation(suit) + "|"
            else:
                output += "  |"
        output += "\n"
        output += "+-----------------------+\n"

        max_cascade_size = max(max(len(cascade)
                                   for cascade in self.cascades), 9)
        for i in range(max_cascade_size):
            card_row = [
                cascade[i] if len(cascade) > i else "  "
                for cascade in self.cascades]
            output += "|" + " ".join(card_row) + "|\n"
        output += "+-----------------------+\n"

        return output

    def get_moves(self):
        """
        Generator of all possible next positions.
        """

        cascades, freecells = self.cascades, self.freecells

        # Moving from cascade to foundation
        for i in range(len(cascades)):
            if not cascades[i]:
                continue

            card = cascades[i][-1]
            # Check if last card in pile is the lowest card of its suit
            if card == self.next_foundation(card[1]):
                new_cascades = list(cascades)
                new_cascades[i] = cascades[i][:-1]
                yield Position(new_cascades, freecells)

        # Moving from Free Cell to foundation
        for card in freecells:
            # Check if free cell card is lowest of its suit.
            if card == self.next_foundation(card[1]):
                yield Position(self.cascades, freecells - {card})

        # Moving from cascade i to cascade j
        for i in range(len(cascades)):
            for j in range(len(cascades)):
                if i == j:
                    continue
                if not cascades[i]:
                    continue

                card = cascades[i][-1]
                # Check if pile 2 is empty or if pile2's last card is parent is parent
                if not cascades[j] or valid_build(card, cascades[j][-1]):
                    # Yield this move
                    new_cascades = list(cascades)
                    new_cascades[i] = cascades[i][:-1]
                    new_cascades[j] = cascades[j]+(card,)
                    # new_cascades = new_cascades | {
                    #     cascades[i][:-1]} | {cascades[j] + (card,)}
                    yield Position(new_cascades, freecells)

        # Moving Free Cell to cascade
        for card in freecells:
            for i in range(len(cascades)):
                # Check if pile 2 is empty or if pile2's last card is parent is parent
                if not cascades[i] or valid_build(card, cascades[i][-1]):
                    # Yield this move
                    new_cascades = list(cascades)
                    new_cascades[i] = cascades[i] + (card,)
                    yield Position(new_cascades, freecells - {card})

        # Stock to Freecell
        if len(freecells) < 4:
            for i in range(len(cascades)):
                if cascades[i]:
                    card = cascades[i][-1]
                    new_cascade = list(cascades)
                    new_cascade[i] = cascades[i][:-1]
                    yield Position(new_cascade, freecells | {card})

    def cards_left(self):
        return sum(len(pile) for pile in self.cascades) + len(self.freecells)

    def upper_bound_to_completion(self):
        # Count number of cards left,
        # add number of cards on top of cards of the same suit, as such must
        # be moved at least once before going on the foundation
        total = self.cards_left()
        # For every card
        for pile in self.cascades:
            for i in range(len(pile)):
                # If the card is larger and on top of another of the same suit
                for j in range(i):
                    if pile[i][1] == pile[j][1] and ranks.index(pile[i][0]) > ranks.index(pile[j][0]):
                        total += 1
                        break
        return total

    def heuristic(self):
        # punish_cards_left = self.cards_left() * 10
        nonempty_piles = len(
            {pile for pile in self.cascades if len(pile) != 0})
        filled_freecells = 4 * len(self.freecells)
        deep_next_foundation = 0
        for suit in suits:
            next_card = self.next_foundation(suit)
            for pile in self.cascades:
                if next_card in pile:
                    deep_next_foundation += len(pile)

        # If there are many more red cards than black or vice versa,
        # it is hard to build
        uneven_foundation = 0
        cnext = ranks.index(self.next_foundation(
            "C")[0]) if self.next_foundation("C") else 15
        dnext = ranks.index(self.next_foundation(
            "D")[0]) if self.next_foundation("D") else 15
        hnext = ranks.index(self.next_foundation(
            "H")[0]) if self.next_foundation("H") else 15
        snext = ranks.index(self.next_foundation(
            "S")[0]) if self.next_foundation("S") else 15
        uneven_foundation += (max(cnext,
                                  snext) - max(dnext, hnext))**2
        uneven_foundation += (min(cnext,
                                  snext) - min(dnext, hnext))**2

        tableaux_length = 0
        for pile in self.cascades:
            if pile and pile[0] and pile[0][0] == "K":
                i = 0
                while i+1 < len(pile) and valid_build(pile[i+1], pile[i]):
                    i += 1
                tableaux_length += i + 1

        return self.cards_left() * 50 + nonempty_piles * 15 + filled_freecells * 10 + 1 * deep_next_foundation + 5 * uneven_foundation - tableaux_length * 20


class FreeCellGraph(nx.DiGraph):

    def __init__(self):
        self.counter = 0

    def __contains__(self, position):
        return True

    def __getitem__(self, position):
        self.counter += 1
        if self.counter % 1000 < 2:
            print(position, flush=True)
        return {next: {"weight": 1} for next in position.get_moves()}


for iter in range(100):
    position = Position.random()
    print(position)

    time.sleep(3)

    path = nx.astar_path(FreeCellGraph(), position, Position(),
                         heuristic=lambda x, y: x.heuristic())

    print(f"Found solution of length {len(path)}")
    time.sleep(3)
    for position in path:
        print(position)

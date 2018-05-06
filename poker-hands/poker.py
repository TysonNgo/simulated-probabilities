#-*-coding: utf-8-*-
from random import randint

class Card():
    def __init__(self, card, suit):
        self.card = str(card)
        self.suit = suit
        cards = {
            "2": [2],
            "3": [3],
            "4": [4],
            "5": [5],
            "6": [6],
            "7": [7],
            "8": [8],
            "9": [9],
            "10": [10],
            "J": [11],
            "Q": [12],
            "K": [13],
            "A": [1, 14]
        }
        self.values = cards[self.card]

    def __str__(self):
        return self.card+" "+self.suit

class Deck():
    def __init__(self, empty=False):
        self.cards = []
        
        if not empty:
            self.new_deck()

    def add(self, card):
        if isinstance(card, Card):
            self.cards.append(card)
        else:
            raise TypeError(str(card)+" is not a Card")

    def new_deck(self):
        self.cards[:] = []
        cards = [
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "J",
            "Q",
            "K",
            "A"
        ]
        suits = [
            "♠",
            "♥",
            "♦",
            "♣"
        ]
        for suit in suits:
            for card in cards:
                self.cards.append(Card(card, suit))

    def shuffle(self):
        for i in range(len(self)-1):
            j = randint(i+1, len(self)-1)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def draw(self):
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return "\n".join([str(c) for c in self.cards])

class Hand:
    """ Types of hands and their rankings
    1. Royal flush
    2. Straight flush
    3. Four of a kind
    4. Full house
    5. Flush
    6. Straight
    7. Three of a kind
    8. Two pair
    9. Pair
    10. High Card
    """
    def __init__(self, deck):
        self.cards = [deck.draw() for i in range(5)]
        self.card_count = {}

        for c in self.cards:
            if c.card in self.card_count:
                self.card_count[c.card] += 1
            else:
                self.card_count[c.card] = 1

        i = 0 if "2" in self else -1
        self.cards.sort(key=lambda c: c.values[i])

    @staticmethod
    def get_hand_types():
        return [
            "royal_flush",
            "straight_flush",
            "four_of_a_kind",
            "full_house",
            "flush",
            "straight",
            "three_of_a_kind",
            "two_pair",
            "pair",
            "high_card"
        ]

    def get_hand_type(self):
        if self.has_royal_flush():
            return "royal_flush"
        if self.has_straight_flush():
            return "straight_flush"
        if self.has_four_of_a_kind():
            return "four_of_a_kind"
        if self.has_full_house():
            return "full_house"
        if self.has_flush():
            return "flush"
        if self.has_straight():
            return "straight"
        if self.has_three_of_a_kind():
            return "three_of_a_kind"
        if self.has_two_pair():
            return "two_pair"
        if self.has_pair():
            return "pair"
        return "high_card"

    def has_royal_flush(self):
        return self.has_straight() and \
            self.has_flush() and \
            all(map(lambda c: c.values[-1] >= 10, self.cards))

    def has_straight_flush(self):
        return self.has_straight() and self.has_flush()

    def has_four_of_a_kind(self):
        return 4 in self.card_count.values()

    def has_full_house(self):
        vals = list(self.card_count.values())
        return vals.count(3) and vals.count(2)

    def has_flush(self):
        return len(set([c.suit for c in self.cards])) == 1

    def has_straight(self):
        i = 0 if "2" in self else -1
        for c in range(len(self.cards)-1):
            if self.cards[c+1].values[i]-self.cards[c].values[i] != 1:
                return False
        return True

    def has_three_of_a_kind(self):
        return 3 in self.card_count.values()

    def has_two_pair(self):
        return list(self.card_count.values()).count(2) == 2

    def has_pair(self):
        return 2 in self.card_count.values()

    def __str__(self):
        return ", ".join([str(c) for c in self.cards])

    def __contains__(self, card):
        return any([card == c.card for c in self.cards])

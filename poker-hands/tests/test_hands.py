#-*- coding: utf-8 -*-
import unittest
import poker

class TestHands(unittest.TestCase):
    def setUp(self):
        self.deck = poker.Deck(empty=True)

        def c(cards, suits):
            """args - [(x, y), ...] where
                x is the value of the card
                y is the suit of the card
            """
            suit = {
                0: "♠",
                1: "♥",
                2: "♦",
                3: "♣"
            }
            for c, s in zip(cards, suits):
                s = suit[s]
                self.deck.add(poker.Card(c, s))

        # flush
        c((10,7,4,2,3), #23
          ( 0 ,0,0,0,0))
        c((9,7,3,8,2), #22
          (0,0,0,0,0))
        c(("J",7,2,10,"Q"), #21
          ( 0 ,0,0, 0, 0 ))

        # lowest straight/straight flush
        c(("A",2,3,4,5), #20
          ( 0 ,0,0,0,0))
        c(("A",2,3,4,5), #19
          ( 0 ,1,0,3,1))
        c((2,3,4,5,"A"), #18
          (0,1,0,3, 1 ))
        c((3,2,"A",5,4), #17
          (0,0, 0 ,0,0))

        # highest straight
        c(( 10,"J","Q","K","A"), #16
          ( 0 , 1 , 1 , 0 , 0 ))

        # other straights
        c((8,6,7,5,4), #15
          (0,1,1,0,0))
        c((3,7,6,5,4), #14
          (0,1,1,0,0))
        c((10,6,9,8,7), #13
          (0,1,1,0,0))

        # royal flush
        c(( 10,"J","Q","K","A"), #12
          ( 0 , 0 , 0 , 0 , 0 ))
        c(("J", 10,"K","A","Q"), #11
          ( 1 , 1 , 1 , 1 , 1 ))
        c(("K","A","Q", 10,"J"), #10
          ( 2 , 2 , 2 , 2 , 2 ))
        c(( 10,"Q","J","A","K"), #9
          ( 3 , 3 , 3 , 3 , 3 ))

        # full house
        c(("A","A","A",2,2), #8
          ( 0 , 1 , 2 ,0,1))
        c((5,5,3,3,3), #7
          (0,1,2,0,1))
        c(("Q","K","Q","K","Q"), #6
          ( 0 , 0 , 1 , 1 , 3 ))

        # four of a kind
        c((2,2,2,2,5), #5
          (0,1,2,3,0))
        c((5,2,2,2,2), #4
          (0,1,2,3,0))

        # three of a kind
        c((7,7,7,"J","Q"), #3
          (0,1,2, 0 , 0 ))

        # two pair
        c((8,8,3,3,"A"), #2
          (0,1,2,3, 0 ))
      
        # single pair
        c((8,8,"A","K","J"), #1
          (0,1, 2 , 3 , 0 ))

        # nothing
        c((2,"A","K",5,3), #0
          (0, 0 , 0 ,0,1))

        self.royal_flush = [9, 10, 11, 12]
        self.straight_flush = [20, 17]
        self.four_of_a_kind = [4, 5]
        self.full_house = [6, 7, 8]
        self.flush = [21, 22, 23]
        self.straight = [13, 14, 15, 16, 18, 19]
        self.three_of_a_kind = [3]
        self.two_pair = [2]
        self.pair = [1]
    
    def t(self, has, hand_indexes):
        """
            has: method name of the type of hand to test
            hand_indexes: list of hands that contain the type of hand
        """
        hands = []
        for i in range(int(len(self.deck) / 5)):
            hand = poker.Hand(self.deck)
            if getattr(hand, has)():
                hands.append(hand)
                if i not in hand_indexes:
                    assert False, str(hand)+"\n"+str(i)        
        
        self.assertEqual(len(hands), len(hand_indexes))

    def test_has_royal_flush(self):
        self.t("has_royal_flush",
               self.royal_flush)

    def test_has_straight_flush(self):
        self.t("has_straight_flush",
               self.straight_flush+self.royal_flush)

    def test_has_four_of_a_kind(self):
        self.t("has_four_of_a_kind",
               self.four_of_a_kind)

    def test_has_full_house(self):
        self.t("has_full_house",
               self.full_house)

    def test_has_flush(self):
        self.t("has_flush",
               self.flush+self.royal_flush+self.straight_flush)

    def test_has_straight(self):
        self.t("has_straight",
               self.straight+self.royal_flush+self.straight_flush)

    def test_has_three_of_a_kind(self):
        self.t("has_three_of_a_kind",
               self.three_of_a_kind+self.full_house)

    def test_has_two_pair(self):
        self.t("has_two_pair",
               self.two_pair)

    def test_has_pair(self):
        self.t("has_pair",
               self.pair+self.two_pair+self.full_house)

    def test_get_hand_type(self):
        for i in range(int(len(self.deck) / 5)):
            hand = poker.Hand(self.deck)
            if i in self.royal_flush:
                self.assertEqual(hand.get_hand_type(), "royal_flush", msg=hand)
            if i in self.straight_flush:
                self.assertEqual(hand.get_hand_type(), "straight_flush", msg=hand)
            if i in self.four_of_a_kind:
                self.assertEqual(hand.get_hand_type(), "four_of_a_kind", msg=hand)
            if i in self.full_house:
                self.assertEqual(hand.get_hand_type(), "full_house", msg=hand)
            if i in self.flush:
                self.assertEqual(hand.get_hand_type(), "flush", msg=hand)
            if i in self.straight:
                self.assertEqual(hand.get_hand_type(), "straight", msg=hand)
            if i in self.three_of_a_kind:
                self.assertEqual(hand.get_hand_type(), "three_of_a_kind", msg=hand)
            if i in self.two_pair:
                self.assertEqual(hand.get_hand_type(), "two_pair", msg=hand)
            if i in self.pair:
                self.assertEqual(hand.get_hand_type(), "pair", msg=hand)
            if i == 0:
                self.assertEqual(hand.get_hand_type(), None, msg=hand)

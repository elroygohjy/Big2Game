import random

from big2.constants import FIVE_CARD_RANK
from big2.valid_cards_finder import ValidCardsFinder


class Board:
    def __init__(self, players_list):
        # turn is player object
        self.turn = None
        self.players_list = players_list
        self.current_player_idx = 0
        self.last_player = None

        # waiting for card to center
        self.waiting = False
        self.prev_suit = None
        self.prev_highest = None
        self.prev_type = None
        self.prev_no_played_cards = None
        self.played_cards = None
        self.is_first_turn = True

    def set_played_cards(self, prev_suit, prev_highest, prev_type, prev_no_played_cards, played_cards):
        self.prev_type = prev_type
        self.prev_suit = prev_suit
        self.prev_highest = prev_highest
        self.prev_no_played_cards = prev_no_played_cards
        self.played_cards = played_cards

    def passTurn(self, player) -> None:
        if player == self.turn:
            self.current_player_idx += 1
            self.current_player_idx %= 4
            self.turn = self.players_list[self.current_player_idx]

    def play_checker(self, player):
        if self.prev_no_played_cards is None:
            return True
        # check if cards are the same type
        if player.no_played_cards == self.prev_no_played_cards:
            # for 1,2,3,4 cards, we only check value, only 1 and 2 can have matching power/highest
            if player.no_played_cards in [1, 2, 3, 4]:
                if player.power > self.prev_highest:
                    return True
                # wont run for 3 of a kind or quads
                elif player.power == self.prev_highest:
                    return True if player.suit > self.prev_suit else False
                else:
                    return False
            else:
                rank_of_5 = FIVE_CARD_RANK.index(player.card_type)
                rank_of_prev_5 = FIVE_CARD_RANK.index(self.prev_type)
                if rank_of_5 > rank_of_prev_5:
                    return True
                elif rank_of_5 == rank_of_prev_5:

                    if player.card_type != 'color' and player.card_type != 'straight_flush':
                        return True if player.power > self.prev_highest else False
                    else:
                        if player.suit > self.prev_suit:
                            return True
                        elif player.suit == self.prev_suit:
                            return True if player.power > self.prev_highest else False
                        else:
                            return False
                else:
                    return False
        else:
            return False

    def play_card(self, player):
        if not self.waiting:
            if self.turn == player:
                player.check()
                if player.card_playable:
                    if self.play_checker(player) or (self.last_player == self.turn):

                        suit, card_type, power, no_of_cards, played_cards = \
                            player.play_card(player != self.players_list[0], self.current_player_idx)
                        # if user turn after pass, we need to make sure of played_cards dont reset
                        self.set_played_cards(suit, card_type, power, no_of_cards, played_cards)
                        self.waiting = True

    def check_waiting(self):
        is_card_to_centre = False
        if self.turn:
            for card in self.turn.selected_cards:
                if card.played:
                    is_card_to_centre = True
            if is_card_to_centre:
                self.waiting = False
                self.last_player = self.turn
                self.current_player_idx += 1
                self.current_player_idx %= 4
                self.turn = self.players_list[self.current_player_idx]

    # find who start first

    def start_up(self):
        if self.is_first_turn:
            self.turn = self.players_list[0]
            self.is_first_turn = False
            self.current_player_idx = 0

    # only supports one card
    def autoplay(self, player):
        index = [-1]
        player_cards = sorted(player.card_list, key=lambda x: (x.value, x.suit))
        if self.turn == player and not self.waiting and self.last_player != player:
            if self.prev_no_played_cards == 1:
                index = ValidCardsFinder.one_find(player_cards, self.prev_highest)
            elif self.prev_no_played_cards == 2:
                index = ValidCardsFinder.pair_find(player_cards, self.prev_highest, self.prev_suit)
            elif self.prev_no_played_cards == 3:
                index = ValidCardsFinder.triple_find(player_cards, self.prev_highest)
            elif self.prev_no_played_cards == 4:
                index = ValidCardsFinder.quad_find(player_cards, self.prev_highest)
            else:
                if self.prev_type == "straight":
                    index = ValidCardsFinder.straight_find(player_cards, self.prev_highest)
                    if -1 in index:
                        player_cards = sorted(player.card_list, key=lambda x: x.suit)
                        index = ValidCardsFinder.color_find(player_cards, -1, -1)
                        if -1 in index:
                            player_cards = sorted(player.card_list, key=lambda x: (x.value, x.suit))
                            index = ValidCardsFinder.full_house_find(player_cards, -1)
                            if -1 in index:
                                index = ValidCardsFinder.four_kind_find(player_cards, -1)
                elif self.prev_type == "color":
                    player_cards = sorted(player.card_list, key=lambda x: x.suit)
                    index = ValidCardsFinder.color_find(player_cards, self.prev_highest, self.prev_suit)
                    if -1 in index:
                        player_cards = sorted(player.card_list, key=lambda x: (x.value, x.suit))
                        index = ValidCardsFinder.full_house_find(player_cards, -1)
                        if -1 in index:
                            index = ValidCardsFinder.four_kind_find(player_cards, -1)
                elif self.prev_highest == "full_house":
                    index = ValidCardsFinder.full_house_find(player_cards, self.prev_highest)
                    if -1 in index:
                        index = ValidCardsFinder.four_kind_find(player_cards, -1)
                elif self.prev_highest == "four_of_a_kind":
                    index = ValidCardsFinder.four_kind_find(player_cards, self.prev_highest)

            if -1 not in index:
                for i in index:
                    player.select_card(player_cards[i])
                self.play_card(player)
            else:
                self.current_player_idx += 1
                self.current_player_idx %= 4
                self.turn = self.players_list[self.current_player_idx]
        elif self.turn == player and not self.waiting and self.last_player == player:
            type1 = ValidCardsFinder.one_find(player_cards, -1)
            type2 = ValidCardsFinder.pair_find(player_cards, -1, -1)
            type3 = ValidCardsFinder.straight_find(player_cards, -1)
            type4 = ValidCardsFinder.color_find(player_cards, -1, -1)
            type5 = ValidCardsFinder.full_house_find(player_cards, -1)
            type6 = ValidCardsFinder.four_kind_find(player_cards, -1)
            while True:
                played_type = random.choice([type1, type2, type3, type4, type5, type6])
                if -1 not in played_type:
                    for i in played_type:
                        player.select_card(player_cards[i])
                    self.play_card(player)
                    break


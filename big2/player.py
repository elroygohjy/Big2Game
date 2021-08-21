import time

import pygame.time

from big2.card_sprite import *

from big2.board import Board

from big2.constants import WIDTH, CARD_SIZE_PLUS_SP, \
    CARD_CENTER_X, CARD_CENTER_Y, BOTTOM_CARD_HEIGHT, PLAYER2_INIT_X, PLAYER3_INIT_Y, PLAYER4_INIT_X
from operator import attrgetter


class Player:
    def __init__(self):
        self.card_list: list[CardSprite] = []
        self.selected_cards: list[CardSprite] = []
        self.no_of_cards = 13
        self.card_playable = False
        self.to_reset_select = False
        self.ready = False

        # selected card power
        self.power = None
        self.card_type = None
        self.suit = None
        self.no_played_cards = None
        self.need_shuffle = False

    def add_card(self, card: CardSprite):
        self.card_list.append(card)
        if len(self.card_list) == 13:
            self.ready = True

    def select_card(self, card: CardSprite):
        self.selected_cards.append(card) if card not in self.selected_cards else self.selected_cards.remove(card)
        card.cardUp()

    def is_card_in_list(self, card):
        return card in self.card_list

    def reset_select(self):
        self.to_reset_select = True

    def is_ready(self):
        return self.ready

    @staticmethod
    def cal_loc_first_card(x, y, is_top):
        if is_top:
            first_x = (WIDTH - x * CARD_SIZE_PLUS_SP) / 2
            first_y = y
        else:
            first_x = x
            first_y = (WIDTH - y * CARD_SIZE_PLUS_SP) / 2
        return first_x, first_y

    def sort(self):
        self.card_list.sort(key=lambda x: (x.value, x.suit))
        # shift to center
        for card in self.card_list:
            card.change_coord(CARD_CENTER_X, BOTTOM_CARD_HEIGHT, False)
        self.selected_cards = []
        x, y = self.cal_loc_first_card(len(self.card_list), BOTTOM_CARD_HEIGHT, True)
        for card3 in self.card_list:
            card3.change_coord(x, y, False)
            x = x + CARD_SIZE_PLUS_SP

    def check_selected_card_same(self):
        # check if all values are the same
        return sum(card.value == self.selected_cards[0].value
                   for card in self.selected_cards) == len(self.selected_cards)

    def check_color(self):
        # check if all suits are the same
        return sum(card.suit == self.selected_cards[0].suit
                   for card in self.selected_cards) == len(self.selected_cards)

    def check_straight(self):
        lt: list[CardSprite] = sorted(self.selected_cards, key=lambda x: (x.value, x.suit))
        # check for A 2 3 4 5
        ace_straight = list(map(lambda x: cr.index(x), ['3', '4', '5', 'A', '2']))
        invalid_straight = list(map(lambda x: cr.index(x), ['J', 'Q', 'K', 'A', '2']))

        def check_for_edge_straight(straight):
            for i in range(len(lt)):
                if straight[0] != lt[0].value:
                    return False
            return True

        is_ace_st = check_for_edge_straight(ace_straight)
        is_invalid_st = check_for_edge_straight(invalid_straight)
        if is_ace_st:
            return True
        if is_invalid_st:
            return False
        for i in range(1, len(lt)):
            if lt[i].value - lt[i - 1].value != 1:
                return False
        return True

    def check_full_house_or_four(self):
        lt = sorted(self.selected_cards, key=lambda x: (x.value, x.suit))
        same_count = 0
        # 2, 2 to count as 2 cards
        offset = 1
        power = 0
        for i in range(1, len(lt)):
            if lt[i - 1].value == lt[i].value:
                same_count += offset
                if offset == 2 or offset == 3:
                    power = lt[i].value
                offset += 1
            else:
                offset = 1
        return same_count, power

    def set_playable_cards(self, suit=None, power=None, card_type=None, no_played_cards=None, playable=False):
        self.suit = suit
        self.power = power
        self.card_type = card_type
        self.card_playable = playable
        self.no_played_cards = no_played_cards

    def get_playable_cards(self):
        return self.suit, self.power, self.card_type, self.no_played_cards

    def check(self):
        no_of_cards = len(self.selected_cards)
        if no_of_cards == 1:
            self.set_playable_cards(self.selected_cards[0].suit, self.selected_cards[0].value,
                                    'single', 1, True)
        elif self.check_selected_card_same():
            if no_of_cards == 2:
                suit = max(self.selected_cards[0].suit, self.selected_cards[1].suit)
                self.set_playable_cards(suit, self.selected_cards[0].value,
                                        'pair', 2, True)
            elif no_of_cards == 3:
                # 4 is spade, for 3 of a kind, suit does not matter so default.
                self.set_playable_cards(4, self.selected_cards[0].value,
                                        'triple', 3, True)
            elif no_of_cards == 4:
                # 4 is spade, for 34of a kind, suit does not matter so default.
                self.set_playable_cards(4, self.selected_cards[0].value,
                                        'quad', 4, True)
            else:
                self.set_playable_cards()
        elif no_of_cards == 5:
            same_count, power_for_fh_four = self.check_full_house_or_four()
            is_color = self.check_color()
            is_straight = self.check_straight()
            if is_straight and is_color:
                power = max(self.selected_cards, key=attrgetter('value')).value
                self.set_playable_cards(self.selected_cards[0].suit, power,
                                        'straight_flush', 5, True)
            elif is_straight:
                power = max(self.selected_cards, key=attrgetter('value')).value
                self.set_playable_cards(self.selected_cards[0].suit, power,
                                        'straight', 5, True)
            elif is_color:
                power = max(self.selected_cards, key=attrgetter('value')).value
                self.set_playable_cards(self.selected_cards[0].suit, power,
                                        'color', 5, True)
            elif same_count == 4:  # is full-house
                self.set_playable_cards(4, power_for_fh_four, 'full_house', 5, True)
            elif same_count == 6:  # is four of a kind
                self.set_playable_cards(4, power_for_fh_four, 'four_of_a_kind', 5, True)
            else:
                self.set_playable_cards()
        else:
            self.set_playable_cards()

    # check with the board if card is playable
    def check_play(self, board: Board):
        board.play_card(self)

    def remove_card(self, card: CardSprite):
        self.card_list.remove(card)
        self.selected_cards.remove(card)

    def play_card(self, to_flip, player_type):
        x, y = self.cal_loc_first_card(len(self.selected_cards), CARD_CENTER_Y, True)
        if player_type % 2 != 0:
            x -= 36
        else:
            x -= 25
        self.selected_cards.sort(key=lambda x: (x.value, x.suit))
        for card in self.selected_cards:
            if to_flip:
                card.flip()
            card.update_layer()
            card.change_coord(x, CARD_CENTER_Y, True)
            if player_type % 2 == 0:
                x += CARD_SIZE_PLUS_SP
            else:
                y += CARD_SIZE_PLUS_SP
        return self.get_playable_cards()

    def shuffle(self, player_type):
        if player_type == 0:
            new_x, new_y = self.cal_loc_first_card(len(self.card_list), BOTTOM_CARD_HEIGHT, True)
        elif player_type == 1:
            new_x, new_y = self.cal_loc_first_card(PLAYER2_INIT_X, len(self.card_list), False)
        elif player_type == 2:
            new_x, new_y = self.cal_loc_first_card(len(self.card_list), PLAYER3_INIT_Y, True)
        else:
            new_x, new_y = self.cal_loc_first_card(PLAYER4_INIT_X, len(self.card_list), False)

        for card_in_list in self.card_list:
            card_in_list.change_coord(new_x, new_y, False)
            if player_type % 2 == 0:
                new_x += CARD_SIZE_PLUS_SP
            else:
                new_y += CARD_SIZE_PLUS_SP
        self.need_shuffle = False










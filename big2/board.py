from big2.constants import FIVE_CARD_RANK



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

        self.is_first_turn = True

    def set_played_cards(self, prev_suit, prev_highest, prev_type, prev_played_cards):
        self.prev_type = prev_type
        self.prev_suit = prev_suit
        self.prev_highest = prev_highest
        self.prev_no_played_cards = prev_played_cards

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
                        suit, card_type, power, no_of_cards = player.play_card(player != self.players_list[0],
                                                                               self.current_player_idx)
                        self.set_played_cards(suit, card_type, power, no_of_cards)
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

                print(self.current_player_idx)
                self.turn = self.players_list[self.current_player_idx]

    # find who start first

    def start_up(self):
        if self.is_first_turn:
            self.turn = self.players_list[0]
            self.is_first_turn = False
            self.current_player_idx = 0

    # only supports one card
    def autoplay(self, player):
        if self.turn == player and not self.waiting:
            player_list = sorted(player.card_list, key=lambda x: (x.value, x.suit))
            if self.prev_no_played_cards == 1:
                def one_check():
                    for idx, elem in enumerate(player_list):
                        if elem.value > self.prev_highest:
                            return idx
                    return -1

                index = one_check()
                if index != -1:
                    player.select_card(player_list[index])
                    self.play_card(player)
                else:
                    # fix this
                    print(self.current_player_idx)
                    self.current_player_idx += 1
                    self.current_player_idx %= 4
                    self.turn = self.players_list[self.current_player_idx]

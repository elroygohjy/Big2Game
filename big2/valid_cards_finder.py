from operator import attrgetter


class ValidCardsFinder:

    @staticmethod
    def one_find(player_cards, prev_highest: int):
        for idx, elem in enumerate(player_cards):
            if elem.value > prev_highest:
                return [idx]
        return [-1]

    @staticmethod
    def pair_find(player_cards, prev_highest, prev_suit):
        for i in range(1, len(player_cards)):
            if player_cards[i - 1].value == player_cards[i].value:
                if player_cards[i - 1].value > prev_highest:
                    return i - 1, i
                elif player_cards[i - 1].value == prev_highest:
                    suit = max(player_cards[i - 1].suit, player_cards[i].suit)
                    if suit > prev_suit:
                        return [i - 1, i]
        return [-1]

    @staticmethod
    def triple_find(player_cards, prev_highest):
        for i in range(2, len(player_cards)):
            if player_cards[i - 2].value == player_cards[i - 1].value == player_cards[i].value:
                if player_cards[i - 2].value > prev_highest:
                    return [i - 2, i - 1, i]
        return [-1]

    @staticmethod
    def quad_find(player_cards, prev_highest):
        for i in range(3, len(player_cards)):
            if player_cards[i - 3].value == player_cards[i - 2].value \
                    == player_cards[i - 1].value == player_cards[i].value:
                if player_cards[i - 2].value > prev_highest:
                    return [i - 3, i - 2, i - 1, i]
        return [-1]

    @staticmethod
    def color_find(suit_sorted_cards, prev_highest, prev_suit):
        for i in range(4, len(suit_sorted_cards)):
            if suit_sorted_cards[i - 4].suit == suit_sorted_cards[i - 3].suit \
                    == suit_sorted_cards[i - 2].suit == suit_sorted_cards[i - 1].suit \
                    == suit_sorted_cards[i].suit:
                power = 0
                for idx in range(i - 4, i + 1):
                    power = max(power, suit_sorted_cards[idx].value)
                if suit_sorted_cards[i].suit > prev_suit:
                    return [i - 4, i - 3, i - 2, i - 1, i]
                elif suit_sorted_cards[i].suit == prev_suit:
                    if power > prev_highest:
                        return [i - 4, i - 3, i - 2, i - 1, i]
        return [-1]

    @staticmethod
    def four_kind_find(player_cards, prev_highest):
        indexes = ValidCardsFinder.quad_find(player_cards, prev_highest)
        if -1 in indexes:
            return indexes
        else:
            for i in range(0, len(player_cards)):
                if i not in indexes:
                    indexes.insert(0, i)
                    return indexes

    @staticmethod
    def full_house_find(player_cards, prev_highest):
        indexes = ValidCardsFinder.triple_find(player_cards, prev_highest)
        if -1 in indexes:
            return indexes
        else:
            for i in range(1, len(player_cards)):
                if player_cards[i].value == player_cards[i - 1].value:
                    if i - 1 not in indexes and i not in indexes:
                        indexes.insert(0, i - 1)
                        indexes.insert(0, i)
                        return indexes

    @staticmethod
    def check_straight(five_cards):
        for i in range(0, len(five_cards) - 1):
            if five_cards[i].value + 1 != five_cards[i + 1].value:
                return False
        return True

    @staticmethod
    def straight_find(player_cards, prev_highest) -> list[int]:
        play_cards_wo_2 = [card for card in player_cards if card.value != 12]
        no_dupe_cards = play_cards_wo_2[:]
        for i in range(1, len(player_cards)):
            if player_cards[i - 1] == player_cards[i]:
                no_dupe_cards.remove(player_cards[i])
        for idx in range(4, len(no_dupe_cards)):
            straight = no_dupe_cards[idx - 4: idx + 1]
            if ValidCardsFinder.check_straight(straight):
                if no_dupe_cards[idx].value > prev_highest:
                    print(list(map(lambda x: player_cards.index(x), straight)))
                    return list(map(lambda x: player_cards.index(x), straight))
        return [-1]





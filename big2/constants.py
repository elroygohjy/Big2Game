import pygame

layer = 0

WIDTH, HEIGHT = 1000, 1000
FPS = 60
INITIAL_LOC_X = WIDTH / 2 - 25
INITIAL_LOC_Y = HEIGHT / 2 - 36
CARD_SIZE_PLUS_SP = 54
CARD_CENTER_Y = HEIGHT / 2 - 36
BOTTOM_CARD_HEIGHT = 1000 - 73
CARD_CENTER_X = 1000 / 2 - 25

PLAYER2_INIT_X = 1000 - 73
PLAYER2_INIT_Y = 149

PLAYER4_INIT_X = 0
PLAYER4_INIT_Y = 149

PLAYER3_INIT_X = 149
PLAYER3_INIT_Y = 0

DECK = ['AD', "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "XD", "JD", "QD", "KD",
        'AC', "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "XC", "JC", "QC", "KC",
        'AH', "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "XH", "JH", "QH", "KH",
        'AS', "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "XS", "JS", "QS", "KS"]

CARD_RANK = ('3', '4', '5', '6', '7', '8', '9', 'X', 'J', 'Q', 'K', 'A', '2')
SUIT_RANK = ('D', 'C', 'H', 'S')
SUIT_SYMBOL = ["♦", "♣", "♥", "♠"]

REVERSE_CARD_RANK = {0: '3', 1: '4', 2: '5', 3: '6', 4: '7', 5: '8', 6: '9', 7: '10', 8: 'J', 9: 'Q', 10: 'K', 11: 'A',
                     12: '2'}

FIVE_CARD_RANK = ('straight', 'color', 'full_house', 'four_of_a_kind', 'straight_flush')

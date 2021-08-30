import random

import pygame

from big2.board import Board
from big2.button import Button
from big2.card_sprite import CardSprite
from big2.constants import WIDTH, HEIGHT, FPS, DECK, CARD_SIZE_PLUS_SP, PLAYER2_INIT_X, PLAYER2_INIT_Y, \
    PLAYER3_INIT_X, PLAYER3_INIT_Y, PLAYER4_INIT_X, PLAYER4_INIT_Y, REVERSE_CARD_RANK as rcr, SUIT_SYMBOL as ss
from big2.player import Player

# WIN is window size
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Init font
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
font1 = pygame.font.SysFont('Arial', 25)
WINNING_FONT = pygame.font.SysFont('Comic Sans MS', 100)

# background and caption
pygame.display.set_caption("Big2")
bg = pygame.image.load("./asset/background.jpg").convert()
turn_box = pygame.image.load("./asset/turn_box.png")
card_box = pygame.image.load("./asset/card_box.png")
# buttons
pass_button_img = pygame.image.load("./asset/button_pass.png")
sort_button_img = pygame.image.load("./asset/button_sort.png")
play_button_img = pygame.image.load("./asset/button_play_go.png")
reset_button_img = pygame.image.load("./asset/button_reset-hand.png")
play_again_img = pygame.image.load("./asset/button_play-again.png")

play_button = Button(149, 825, play_button_img)
pass_button = Button(149 + 82 + 5, 825, pass_button_img)
sort_button = Button(149 + 82 + 84 + 10, 825, sort_button_img)
reset_button = Button(149 + 82 + 84 + 82 + 15, 825, reset_button_img)
play_again_button = Button((WIDTH - 255) / 2, (HEIGHT - 90) / 2 + 100, play_again_img)


def draw_window():
    WIN.blit(bg, (0, 0))
    WIN.blit(turn_box, (0, 1000 - 100))
    play_button.draw(WIN)
    pass_button.draw(WIN)
    sort_button.draw(WIN)
    reset_button.draw(WIN)


def main():
    pos_x = 149
    pos_y = 927

    pos2_x = PLAYER2_INIT_X
    pos2_y = PLAYER2_INIT_Y

    pos3_x = PLAYER3_INIT_X
    pos3_y = PLAYER3_INIT_Y

    pos4_x = PLAYER4_INIT_X
    pos4_y = PLAYER4_INIT_Y

    clock = pygame.time.Clock()
    deck = DECK[:]
    random.shuffle(deck)
    card_group = pygame.sprite.LayeredUpdates()
    player1 = Player(card_group)
    bot_player2 = Player(card_group)
    bot_player3 = Player(card_group)
    bot_player4 = Player(card_group)

    board = Board([player1, bot_player2, bot_player3, bot_player4])

    card = None
    card2 = None
    card3 = None
    card4 = None

    # bot_player2_card_grp = pygame.sprite.Group()
    # bot_player3_card_grp = pygame.sprite.Group()
    # bot_player4_card_grp = pygame.sprite.Group()

    # add card
    def check_and_add_card(cur_card: CardSprite, group: pygame.sprite.LayeredUpdates, player: Player):
        if cur_card not in group and cur_card:
            group.add(cur_card)
            player.add_card(cur_card)

    # move card to dest
    def move_card_(group: pygame.sprite.LayeredUpdates, player: Player,
                   coord_x, coord_y, cur_card: CardSprite, is_x, is_back, angle):
        if is_x:
            coord = coord_x
        else:
            coord = coord_y
        if not player.card_list and deck:
            return coord, CardSprite(deck.pop(0), coord_x, coord_y, angle, is_back)

        for this_card in player.card_list:
            if not this_card.at_dest:
                this_card.move_to_dest()
            else:
                # if card is already at dest, check if it is played card, if so set to shuffle true, and remove card
                # from player
                if this_card.played:
                    player.need_shuffle = True
                    player.remove_card(this_card)
                    group.add(this_card)
                    return coord, this_card
                # check if player is ready, meaning if he has 13 cards
                if not player.is_ready():
                    if is_x:
                        return coord_x + CARD_SIZE_PLUS_SP, \
                               CardSprite(deck.pop(0), coord_x + CARD_SIZE_PLUS_SP, coord_y, angle, is_back)
                    else:
                        return coord_y + CARD_SIZE_PLUS_SP, \
                               CardSprite(deck.pop(0), coord_x, coord_y + CARD_SIZE_PLUS_SP, angle, is_back)

        return coord, cur_card

    def draw_prev_cards(played_cards):
        # loc_x is the coordinate of button size + padding
        loc_x = 149 + 82 + 84 + 82 + 175
        WIN.blit(card_box, (loc_x, 775))
        if played_cards:
            for played_card in played_cards:
                text = rcr[played_card.value] + ss[played_card.suit]
                if played_card.suit % 2 == 0:
                    color = (255, 0, 0)
                else:
                    color = (0, 0, 0)
                text_sur = font1.render(text, True, color)
                loc_x += 40
                WIN.blit(text_sur, (loc_x, 820))
    game_end = False
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # card pressed
                for cur_card in player1.card_list:
                    if cur_card.rect.collidepoint(x, y):
                        player1.select_card(cur_card)

                # sort button pressed
                if sort_button.rect.collidepoint(x, y):
                    player1.sort()
                # play button pressed
                if play_button.rect.collidepoint(x, y):
                    player1.check_play(board)
                # reset selected card button pressed
                if reset_button.rect.collidepoint(x, y):
                    player1.reset_select()
                if pass_button.rect.collidepoint(x, y):
                    board.passTurn(player1)
                if play_again_button.rect.collidepoint(x, y):
                    main()

        # if not deck:
        check_and_add_card(card, card_group, player1)
        check_and_add_card(card2, card_group, bot_player2)
        check_and_add_card(card3, card_group, bot_player3)
        check_and_add_card(card4, card_group, bot_player4)

        pos_x, card = move_card_(card_group, player1, pos_x, pos_y, card, True, 0, False)
        pos2_y, card2 = move_card_(card_group, bot_player2, pos2_x, pos2_y, card2, False, True, 90)
        pos3_x, card3 = move_card_(card_group, bot_player3, pos3_x, pos3_y, card3, True, True, 0)
        pos4_y, card4 = move_card_(card_group, bot_player4, pos4_x, pos4_y, card4, False, True, 90)

        # check if card is done moving, and update to next player turn
        board.check_waiting()

        # if need shuffle and there is no card in selected cards, meaning space between
        if player1.need_shuffle and not player1.selected_cards:
            player1.shuffle(0)

        if bot_player2.need_shuffle and not bot_player2.selected_cards:
            bot_player2.shuffle(1)

        if bot_player3.need_shuffle and not bot_player3.selected_cards:
            bot_player3.shuffle(2)

        if bot_player4.need_shuffle and not bot_player4.selected_cards:
            bot_player4.shuffle(3)

        # if player press reset all button
        if player1.to_reset_select:
            if player1.selected_cards:
                player1.select_card(player1.selected_cards[0])
            else:
                player1.to_reset_select = False

        # print(len(player1.card_list), len(bot_player2.card_list),
        #       len(bot_player3.card_list), len(bot_player4.card_list))

        # for card5 in range(len(bot_player2.selected_cards)):
        #     print(bot_player2.selected_cards[card5].value)

        board.start_up()
        if board.turn != player1 and not game_end:
            for i in range(2):
                board.autoplay(bot_player2)
                board.autoplay(bot_player3)
                board.autoplay(bot_player4)

        draw_window()
        draw_prev_cards(board.played_cards)

        card_group.draw(WIN)
        if board.turn == player1:
            text_surface = font.render('My turn', True, (255, 255, 255))
            WIN.blit(text_surface, (25, 1000 - 65))
        elif board.turn == bot_player2:
            text_surface = font.render('P2 turn', True, (255, 255, 255))
            WIN.blit(text_surface, (25, 1000 - 65))
        elif board.turn == bot_player3:
            text_surface = font.render('P3 turn', True, (255, 255, 255))
            WIN.blit(text_surface, (25, 1000 - 65))
        else:
            text_surface = font.render('P4 turn', True, (255, 255, 255))
            WIN.blit(text_surface, (25, 1000 - 65))

        for player in board.players_list:
            text_surface = None
            # is_ready to make sure the game dont terminate when initially every card is 0
            if not player.card_list and player.is_ready():
                if player == player1:
                    text_surface = WINNING_FONT.render('You Win!', True, (0, 0, 0))
                elif player == bot_player2:
                    text_surface = WINNING_FONT.render('P2 Win!', True, (0, 0, 0))
                elif player == bot_player3:
                    text_surface = WINNING_FONT.render('P3 Win!', True, (0, 0, 0))
                else:
                    text_surface = WINNING_FONT.render('P4 Win!', True, (0, 0, 0))
                x, y = text_surface.get_size()
                print(x, y)
                WIN.blit(text_surface, ((WIDTH - x) / 2, (HEIGHT - y) / 2))
                play_again_button.draw(WIN)
                game_end = True

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()

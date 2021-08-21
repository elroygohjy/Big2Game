import math

import pygame
import pygame.sprite

from big2.constants import INITIAL_LOC_X, INITIAL_LOC_Y, CARD_RANK as cr, SUIT_RANK as sr, layer

import big2.constants



class CardSprite(pygame.sprite.Sprite):
    def __init__(self, card_name, dest_x, dest_y, angle, is_back):
        super().__init__()
        self.value = cr.index(card_name[0])
        self.suit = sr.index(card_name[1])
        self._layer = 0
        if not is_back:
            self.image = pygame.image.load("./asset/" + card_name + ".png")
            self.back = pygame.image.load("./asset/BG.png")
        else:
            self.image = pygame.image.load("./asset/BG.png")
            self.back = pygame.image.load("./asset/" + card_name + ".png")
        self.back = pygame.transform.rotate(self.back, angle)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.dest_x = dest_x
        self.dest_y = dest_y

        self.is_select = False
        self.at_dest = False

        self.rect.x = INITIAL_LOC_X
        self.rect.y = INITIAL_LOC_Y
        self.to_move_x = dest_x - INITIAL_LOC_X
        self.to_move_y = dest_y - INITIAL_LOC_Y

        self.going_played = False
        self.played = False

    def move_to_dest(self):
        def change_decimal_to_1(x):
            if abs(x) < 1:
                return 1 if x > 0 else -1
            else:
                return x

        # rect.x and rect.y can only update by integer
        if self.rect.x != self.dest_x or self.rect.y != self.dest_y:
            dist_to_move_x = change_decimal_to_1(self.to_move_x / 30)
            dist_to_move_y = change_decimal_to_1(self.to_move_y / 30)
            if abs(self.dest_x - self.rect.x) < abs(dist_to_move_x):
                self.rect.x = self.dest_x
            else:
                self.rect.x += dist_to_move_x
            if abs(self.dest_y - self.rect.y) < abs(dist_to_move_y):
                self.rect.y = self.dest_y
            else:
                self.rect.y += dist_to_move_y
        else:
            self.at_dest = True
            if self.going_played:
                self.played = True

    def flip(self):
        temp = self.image
        self.image = self.back
        self.back = temp

    def cardUp(self):
        if not self.played:
            if not self.is_select:
                self.rect.y -= 25
            else:
                self.rect.y += 25
            self.is_select = not self.is_select

    def change_coord(self, x, y, going_played):
        self.at_dest = False
        self.to_move_x = x - self.rect.x
        self.to_move_y = y - self.rect.y
        self.dest_x = x
        self.dest_y = y
        self.is_select = False
        self.going_played = going_played

    def update_layer(self):
        self._layer = big2.constants.layer
        big2.constants.layer += 1
        print(big2.constants.layer)




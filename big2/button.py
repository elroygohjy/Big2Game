
class Button:
    def __init__(self, x, y, image):
        self.img = image
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))

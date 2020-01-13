import pygame


class Camera:
    def __init__(self, w, h):
        from main import width, height
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = w
        self.height = h
        self.x = 0
        self.y = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        from main import width, height
        self.x = -target.rect.centerx + int(width / 2)
        self.y = -target.rect.centery + int(height / 2)

        self.x = min(0, self.x)
        self.y = min(0, self.y)
        self.x = max(-(self.width - width), self.x)
        self.y = max(-(self.height - height), self.y)

        self.camera = pygame.Rect(self.x, self.y, self.width, self.height)

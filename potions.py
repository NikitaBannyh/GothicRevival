import pygame

potion = [pygame.transform.scale(pygame.image.load('data/gui/potions.png'), (30, 30)),
          pygame.transform.scale(pygame.image.load('data/gui/potions 2.png'), (30, 55))]

potion_sound = pygame.mixer.Sound('sounds/potion_sound.ogg')


class Potion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        from main import potion_group, all_sprites
        super().__init__(potion_group, all_sprites)
        self.image = potion[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.idle_count = 0

    def update(self):
        from main import player_group, player
        if self.idle_count + 1 >= 40:
            self.idle_count = 0
        if self:
            self.image = potion[self.idle_count // 20]
            self.idle_count += 1
        if pygame.sprite.spritecollideany(self, player_group) is not None:
            player.get_hp()
            potion_sound.play()
            self.kill()

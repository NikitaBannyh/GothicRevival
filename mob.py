import pygame

from player import load_image

idle_ghost = [load_image(pygame.image.load('data/mobs/ghost/ghost-idle1.png')),
              load_image(pygame.image.load('data/mobs/ghost/ghost-idle2.png')),
              load_image(pygame.image.load('data/mobs/ghost/ghost-idle3.png')),
              load_image(pygame.image.load('data/mobs/ghost/ghost-idle4.png')),
              load_image(pygame.image.load('data/mobs/ghost/ghost-idle5.png')),
              load_image(pygame.image.load('data/mobs/ghost/ghost-idle6.png')),
              load_image(pygame.image.load('data/mobs/ghost/ghost-idle7.png'))
              ]

idle_slime = [pygame.transform.scale(pygame.image.load('data/mobs/slime/slime-idle-0.png'), (57, 45)),
              pygame.transform.scale(pygame.image.load('data/mobs/slime/slime-idle-1.png'), (57, 45)),
              pygame.transform.scale(pygame.image.load('data/mobs/slime/slime-idle-2.png'), (57, 45)),
              pygame.transform.scale(pygame.image.load('data/mobs/slime/slime-idle-3.png'), (57, 45))]

move_slime = [pygame.transform.scale(pygame.image.load('data/mobs/slime/slime-move-0.png'), (57, 45)),
              pygame.transform.scale(pygame.image.load('data/mobs/slime/slime-move-1.png'), (57, 45)),
              pygame.transform.scale(pygame.image.load('data/mobs/slime/slime-move-2.png'), (57, 45)),
              pygame.transform.scale(pygame.image.load('data/mobs/slime/slime-move-3.png'), (57, 45))]

attack_slime = [pygame.transform.scale(pygame.image.load('data/mobs/slime/slime-attack-0.png'), (57, 45)),
                pygame.transform.scale(pygame.image.load('data/mobs/slime/slime-attack-1.png'), (57, 45)),
                pygame.transform.scale(pygame.image.load('data/mobs/slime/slime-attack-2.png'), (57, 45)),
                pygame.transform.scale(pygame.image.load('data/mobs/slime/slime-attack-3.png'), (57, 45)),
                pygame.transform.scale(pygame.image.load('data/mobs/slime/slime-attack-4.png'), (57, 45))]

skeleton_rise = [load_image(pygame.image.load('data/mobs/skeleton/skeleton-rise-clothed-1.png')),
                 load_image(pygame.image.load('data/mobs/skeleton/skeleton-rise-clothed-2.png')),
                 load_image(pygame.image.load('data/mobs/skeleton/skeleton-rise-clothed-3.png')),
                 load_image(pygame.image.load('data/mobs/skeleton/skeleton-rise-clothed-4.png')),
                 load_image(pygame.image.load('data/mobs/skeleton/skeleton-rise-clothed-5.png')),
                 load_image(pygame.image.load('data/mobs/skeleton/skeleton-rise-clothed-6.png'))
                 ]
skeleton_walk = [load_image(pygame.image.load('data/mobs/skeleton/skeleton-clothed-1.png')),
                 load_image(pygame.image.load('data/mobs/skeleton/skeleton-clothed-2.png')),
                 load_image(pygame.image.load('data/mobs/skeleton/skeleton-clothed-3.png')),
                 load_image(pygame.image.load('data/mobs/skeleton/skeleton-clothed-4.png')),
                 load_image(pygame.image.load('data/mobs/skeleton/skeleton-clothed-5.png')),
                 load_image(pygame.image.load('data/mobs/skeleton/skeleton-clothed-6.png')),
                 load_image(pygame.image.load('data/mobs/skeleton/skeleton-clothed-7.png')),
                 load_image(pygame.image.load('data/mobs/skeleton/skeleton-clothed-8.png'))
                 ]
death = [load_image(pygame.image.load('data/mobs/death/enemy-death-1.png')),
         load_image(pygame.image.load('data/mobs/death/enemy-death-2.png')),
         load_image(pygame.image.load('data/mobs/death/enemy-death-3.png')),
         load_image(pygame.image.load('data/mobs/death/enemy-death-4.png')),
         load_image(pygame.image.load('data/mobs/death/enemy-death-5.png')),
         ]

rise_sound = pygame.mixer.Sound('sounds/rise.ogg')


class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        from main import mobs_group, all_sprites, ghost_image
        super().__init__(mobs_group, all_sprites)
        self.image = ghost_image
        self.image = load_image(self.image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.speed = 3
        self.idle_count = 0
        self.left = True
        self.right = False
        self.visible = False
        self.count_move = 0

    def update(self):
        from main import player_group, wall_group, stair_group, player, dead_line_group
        if pygame.sprite.spritecollideany(self, dead_line_group):
            self.kill()

        if pygame.sprite.spritecollideany(self, wall_group) is None and pygame.sprite.spritecollideany(self,
                                                                                                       stair_group) is not None:
            self.rect = self.rect.move(0, 6)
        elif pygame.sprite.spritecollideany(self, wall_group) is None and self.left is False:
            self.rect = self.rect.move(0, 6)

        elif pygame.sprite.spritecollideany(self, wall_group) is None and self.left is True:
            self.rect = self.rect.move(0, 6)
            self.image = pygame.transform.flip(self.image, True, False)

        if self.idle_count + 1 >= 49:
            self.idle_count = 0

        if player_group.sprites()[0].rect.colliderect(
                pygame.Rect(self.rect.x - 200, self.rect.y - 200, self.rect.width + 200, self.rect.height + 200)):
            self.visible = True
        from main import player_group, border_group_left, border_group_right
        if self.visible:
            if player_group.sprites()[0].rect.x < self.rect.x and pygame.sprite.spritecollideany(self,
                                                                                                 border_group_left) is None:
                self.rect = self.rect.move(-1, 0)
                self.image = idle_ghost[self.idle_count // 7]
                self.idle_count += 1
            elif player_group.sprites()[0].rect.x > self.rect.x and pygame.sprite.spritecollideany(self,
                                                                                                   border_group_right) is None:
                self.rect = self.rect.move(1, 0)
                self.image = pygame.transform.flip(idle_ghost[self.idle_count // 7], True, False)
                self.idle_count += 1
            else:
                self.image = idle_ghost[self.idle_count // 7]
                self.idle_count += 1

        if self.visible is False:
            if self.left:
                if self.count_move != 55 and pygame.sprite.spritecollideany(self, border_group_left) is None:
                    self.count_move += 1
                    self.rect = self.rect.move(-1, 0)
                    self.image = idle_ghost[self.idle_count // 7]
                    self.idle_count += 1
                else:
                    self.left = False
                    self.right = True
            elif self.right:
                if self.count_move != 0 and pygame.sprite.spritecollideany(self, border_group_right) is None:
                    self.count_move -= 1
                    self.rect = self.rect.move(1, 0)
                    self.image = pygame.transform.flip(idle_ghost[self.idle_count // 7], True, False)
                    self.idle_count += 1
                else:
                    self.left = True
                    self.right = False

        if pygame.sprite.collide_mask(self, player_group.sprites()[0]):
            player.get_damage()


class Slime(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        from main import mobs_group, all_sprites
        super().__init__(mobs_group, all_sprites)
        self.image = idle_slime[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.speed = 3
        self.idle_count = 0
        self.left = True
        self.right = False
        self.visible = False
        self.attack_count = 0
        self.health = 15

    def update(self):
        from main import player_group, wall_group, stair_group, player, dead_line_group
        if pygame.sprite.spritecollideany(self, dead_line_group):
            self.kill()

        if pygame.sprite.spritecollideany(self, wall_group) is None and pygame.sprite.spritecollideany(self,
                                                                                                       stair_group) is not None:
            self.rect = self.rect.move(0, 6)
        elif pygame.sprite.spritecollideany(self, wall_group) is None and self.left is False:
            self.rect = self.rect.move(0, 6)

        elif pygame.sprite.spritecollideany(self, wall_group) is None and self.left is True:
            self.rect = self.rect.move(0, 6)
            self.image = pygame.transform.flip(self.image, True, False)

        if self.idle_count + 1 >= 28:
            self.idle_count = 0
        if self.attack_count + 1 >= 40:
            self.attack_count = 0

        if player_group.sprites()[0].rect.colliderect(
                pygame.Rect(self.rect.x - 200, self.rect.y - 200, self.rect.width + 200, self.rect.height + 200)):
            self.visible = True
        from main import player_group, border_group_left, border_group_right
        if self.visible:
            if player_group.sprites()[0].rect.x < self.rect.x and pygame.sprite.spritecollideany(self,
                                                                                                 border_group_left) is None:
                self.rect = self.rect.move(-1, 0)
                self.image = move_slime[self.idle_count // 7]
                self.idle_count += 1
                self.left = True
                self.right = False
            elif player_group.sprites()[0].rect.x > self.rect.x and pygame.sprite.spritecollideany(self,
                                                                                                   border_group_right) is None:
                self.rect = self.rect.move(1, 0)
                self.image = pygame.transform.flip(move_slime[self.idle_count // 7], True, False)
                self.idle_count += 1
                self.left = False
                self.right = True
            else:
                self.image = move_slime[self.idle_count // 7]
                self.idle_count += 1
                self.right, self.left = False, False

        if self.visible is False:
            self.image = idle_slime[self.idle_count // 7]
            self.idle_count += 1
        if pygame.sprite.collide_mask(self, player_group.sprites()[0]):
            if self.right:
                self.image = pygame.transform.flip(attack_slime[self.attack_count // 8], True, False)
            elif self.left:
                self.image = attack_slime[self.attack_count // 8]
            else:
                self.image = attack_slime[self.attack_count // 8]

            self.attack_count += 1
            if self.attack_count in range(26, 32):
                player.get_damage()
                self.attack_count = 0


class Skeleton(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        from main import mobs_group, all_sprites
        super().__init__(mobs_group, all_sprites)
        self.image = skeleton_walk[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.speed = 3
        self.idle_count = 0
        self.left = True
        self.right = False
        self.visible = False
        self.rise_count = 0

    def update(self):
        from main import player_group, wall_group, stair_group, player, dead_line_group
        if self.health <= 0:
            self.kill()
        if pygame.sprite.spritecollideany(self, dead_line_group):
            self.kill()

        if pygame.sprite.spritecollideany(self, wall_group) is None and pygame.sprite.spritecollideany(self,
                                                                                                       stair_group) is not None:
            self.rect = self.rect.move(0, 6)
        elif pygame.sprite.spritecollideany(self, wall_group) is None and self.left is False:
            self.rect = self.rect.move(0, 6)
        elif pygame.sprite.spritecollideany(self, wall_group) is None and self.left is True:
            self.rect = self.rect.move(0, 6)
            self.image = pygame.transform.flip(self.image, True, False)

        if self.idle_count + 1 >= 42:
            self.idle_count = 0

        if player_group.sprites()[0].rect.colliderect(
                pygame.Rect(self.rect.x - 200, self.rect.y - 200, self.rect.width + 200,
                            self.rect.height + 200)) and self.visible is False:
            self.visible = True
            pygame.mixer.Sound.play(rise_sound)
        from main import player_group, border_group_left, border_group_right
        if self.visible:
            if self.rise_count < 36:
                self.image = skeleton_rise[self.rise_count // 6]
                self.rise_count += 1
            else:
                if player_group.sprites()[0].rect.x < self.rect.x and pygame.sprite.spritecollideany(self,
                                                                                                     border_group_left) is None:
                    self.rect = self.rect.move(-1, 0)
                    self.image = skeleton_walk[self.idle_count // 7]
                    self.idle_count += 1
                    self.left = True
                    self.right = False
                elif player_group.sprites()[0].rect.x > self.rect.x and pygame.sprite.spritecollideany(self,
                                                                                                       border_group_right) is None:
                    self.rect = self.rect.move(1, 0)
                    self.image = pygame.transform.flip(skeleton_walk[self.idle_count // 7], True, False)
                    self.idle_count += 1
                    self.left = False
                    self.right = True
                else:
                    if player_group.sprites()[0].rect.x < self.rect.x:
                        self.image = skeleton_walk[self.idle_count // 7]
                        self.idle_count += 1
                        self.right, self.left = False, False
                    else:
                        self.image = pygame.transform.flip(skeleton_walk[self.idle_count // 7], True, False)
                        self.idle_count += 1
                        self.right, self.left = False, False

        elif self.visible is False:
            self.image = skeleton_rise[0]
        if pygame.sprite.collide_mask(self, player_group.sprites()[0]) and self.idle_count in range(28, 35):
            player.get_damage()
            self.idle_count = 0

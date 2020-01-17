import pygame


def load_image(image):
    return pygame.transform.scale(image, (int(image.get_rect().width * 1.3), int(image.get_rect().height * 1.3)))


run = [load_image(pygame.image.load('data/character/left1.png')),
       load_image(pygame.image.load('data/character/left2.png')),
       load_image(pygame.image.load('data/character/left3.png')),
       load_image(pygame.image.load('data/character/left4.png')),
       load_image(pygame.image.load('data/character/left5.png')),
       load_image(pygame.image.load('data/character/left6.png')),
       load_image(pygame.image.load('data/character/left7.png')),
       load_image(pygame.image.load('data/character/left8.png')),
       load_image(pygame.image.load('data/character/left9.png')),
       load_image(pygame.image.load('data/character/left10.png')),
       load_image(pygame.image.load('data/character/left11.png')),
       load_image(pygame.image.load('data/character/left12.png'))]

attack = [load_image(pygame.image.load('data/character/attack1.png')),
          load_image(pygame.image.load('data/character/attack2.png')),
          load_image(pygame.image.load('data/character/attack3.png')),
          load_image(pygame.image.load('data/character/attack4.png')),
          load_image(pygame.image.load('data/character/attack5.png')),
          load_image(pygame.image.load('data/character/attack6.png'))
          ]

idle = [load_image(pygame.image.load('data/character/idle1.png')),
        load_image(pygame.image.load('data/character/idle2.png')),
        load_image(pygame.image.load('data/character/idle3.png')),
        load_image(pygame.image.load('data/character/idle4.png')), ]

fall = load_image(pygame.image.load('data/character/fall.png'))

jump = [load_image(pygame.image.load('data/character/jump2.png')),
        load_image(pygame.image.load('data/character/jump3.png')),
        load_image(pygame.image.load('data/character/jump4.png'))]

jump_attack = [pygame.image.load('data/character/jump-attack2.png'),
               pygame.image.load('data/character/jump-attack3.png'),
               pygame.image.load('data/character/jump-attack4.png'),
               pygame.image.load('data/character/jump-attack5.png'),
               pygame.image.load('data/character/jump-attack6.png')]

hurt = [
    load_image(pygame.image.load('data/character/gothic-hero-hurt2.png')),
    load_image(pygame.image.load('data/character/gothic-hero-hurt3.png'))]

dialog = pygame.transform.scale(pygame.image.load('data/character/dialog_window.png'), (200, 135))

health = pygame.transform.scale(pygame.image.load('data/gui/Health.png'), (150, 10))

stamina = pygame.transform.scale(pygame.image.load('data/gui/stamina.png'), (136, 10))

attack_sound = pygame.mixer.Sound('sounds/attack.ogg')
jump_sound = pygame.mixer.Sound('sounds/jump.ogg')
hurt_sound = pygame.mixer.Sound('sounds/hurt.ogg')
kill_enemy_sound = pygame.mixer.Sound('sounds/kill.ogg')


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        from main import player_group, all_sprites, player_image, hp
        super().__init__(player_group, all_sprites)
        self.image = load_image(player_image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.speed = 4
        self.hp = hp
        self.stamina = 150
        self.left = False
        self.right = False
        self.at = False
        self.jmp = False
        self.hrt = False
        self.fall = False
        self.at_count = 0
        self.walk_count = 0
        self.idle_count = 0
        self.jump_count = 0
        self.hp_bar = 0
        self.bounce = 2
        self.side = 0

    def update(self):
        from main import wall_group, game_over, dead_line_group, stair_group
        keys = pygame.key.get_pressed()
        self.move(keys)
        self.attack(keys)
        self.jump(keys)

        if self.hp <= 0 or pygame.sprite.spritecollideany(self, dead_line_group) is not None:
            game_over()

        if pygame.sprite.spritecollideany(self, wall_group) is None and pygame.sprite.spritecollideany(self,
                                                                                                       stair_group) is not None and self.jmp is False:
            self.rect = self.rect.move(0, 6)
        elif pygame.sprite.spritecollideany(self, wall_group) is None and self.left is False and self.jmp is False:
            self.rect = self.rect.move(0, 6)
            self.image = fall
            self.fall = True
        elif pygame.sprite.spritecollideany(self, wall_group) is None and self.left is True and self.jmp is False:
            self.rect = self.rect.move(0, 6)
            self.image = pygame.transform.flip(fall, True, False)
            self.fall = True

        else:
            self.fall = False

    def move(self, keys):
        from main import border_group_left, border_group_right

        if keys[pygame.K_a] and pygame.sprite.spritecollideany(self,
                                                               border_group_left) is None and self.hrt is False:

            if keys[pygame.K_LSHIFT] and self.stamina > 0:
                self.stamina -= 1
                self.rect = self.rect.move(-self.speed - 2, 0)
            else:
                self.rect = self.rect.move(-self.speed, 0)
                if self.stamina < 150:
                    self.stamina += 0.5
            self.left = True
            self.right = False
            self.side = 1

        elif keys[pygame.K_d] and pygame.sprite.spritecollideany(self,
                                                                 border_group_right) is None and self.hrt is False:

            if keys[pygame.K_LSHIFT] and self.stamina > 0:
                self.stamina -= 1
                self.rect = self.rect.move(self.speed + 2, 0)
            else:
                self.rect = self.rect.move(self.speed, 0)
                if self.stamina < 150:
                    self.stamina += 0.5
            self.left = False
            self.right = True
            self.side = 0

        else:
            self.left, self.right = False, False
            self.walk_count = 0
            if self.stamina < 170:
                self.stamina += 0.5

        if self.walk_count + 1 >= 60:
            self.walk_count = 0

        if self.idle_count + 1 >= 28:
            self.idle_count = 0

        if self.left:
            self.image = pygame.transform.flip(run[self.walk_count // 5], True, False)
            self.walk_count += 1
        elif self.right:
            self.image = run[self.walk_count // 5]
            self.walk_count += 1
        else:
            if self.side == 0:
                self.image = idle[self.idle_count // 7]
                self.idle_count += 1
            elif self.side == 1:
                self.image = pygame.transform.flip(idle[self.idle_count // 7], True, False)
                self.idle_count += 1

    def attack(self, keys):
        from main import mobs_group
        if keys[pygame.K_e]:

            self.at = True
        else:
            self.at = False

        if self.at_count + 1 >= 30:
            self.at_count = 0

        if self.at and self.side == 1:
            self.image = pygame.transform.flip(attack[self.at_count // 5], True, False)
            self.at_count += 1
        elif (self.at and self.left is False) or (self.at and self.side == 0):
            self.image = attack[self.at_count // 5]
            self.at_count += 1
        else:
            self.at_count = 0
        if self.at and self.at_count == 15:
            pygame.mixer.Sound.play(attack_sound)
        hit_rect_right = pygame.Rect(self.rect.x + 25, self.rect.y, self.rect.width, self.rect.height)
        hit_rect_left = pygame.Rect(self.rect.x - 25, self.rect.y, self.rect.width, self.rect.height)
        for i in mobs_group.sprites():
            if hit_rect_right.colliderect(i.rect) or hit_rect_left.colliderect(i.rect):
                if self.at and (self.at_count in range(11, 20)):
                    i.kill()
                    pygame.mixer.Sound.play(kill_enemy_sound)

    def jump(self, keys):
        from main import roof_group
        if self.jump_count + 1 > 14:
            self.jump_count = 1

        if keys[pygame.K_SPACE] and self.fall is False:
            self.jmp = True

            if self.bounce >= - 2:
                if self.bounce < 0 or pygame.sprite.spritecollideany(self, roof_group) is not None:

                    self.jmp = False
                else:
                    if self.jump_count == 0:
                        pygame.mixer.Sound.play(jump_sound)
                    if self.left is False:
                        self.image = jump[self.jump_count // 5]
                        self.rect = self.rect.move(0, -(self.bounce ** 2) / 8)
                        self.jump_count += 1
                    else:
                        self.image = pygame.transform.flip(jump[self.jump_count // 5], True, False)
                        self.rect = self.rect.move(0, -(self.bounce ** 2) / 8)
                        self.jump_count += 1
                self.bounce -= 0.5
        else:
            self.bounce = 10
            self.jmp = False
            self.jump_count = 0

    def draw_hp(self):
        from main import screen
        screen.blit(pygame.transform.chop(health, (0, 15, self.hp_bar, 15)), (48, 18))
        screen.blit(pygame.transform.chop(stamina, (8, 15, (150 - self.stamina), 15)), (58, 33))

    def get_hp(self):
        if self.hp < 10:
            self.hp += 2
            self.hp_bar -= 30

    def get_damage(self, damage):
        pygame.mixer.Sound.play(hurt_sound)
        if self.jmp is False and self.fall is False:
            self.hp -= damage
            self.hp_bar += damage * 15

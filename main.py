import pygame, sys, os

pygame.init()

fps = 60
size = width, height = 900, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
mobs_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
border_group_left = pygame.sprite.Group()
border_group_right = pygame.sprite.Group()
dead_line_group = pygame.sprite.Group()
roof_group = pygame.sprite.Group()
stair_group = pygame.sprite.Group()
end_level_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()

player_image = pygame.image.load('data/character/idle1.png')
enter = pygame.image.load('data/backgrounds and titles/press-enter-text.png')
title = pygame.image.load("data/backgrounds and titles/title.png")
ghost_image = pygame.image.load('data/mobs/ghost/ghost-idle1.png')
sword = pygame.transform.rotate(pygame.image.load('data/gui/sword.png'), -45)
fon = pygame.transform.scale(pygame.image.load('data/backgrounds and titles/background.png'), (width, height))
fon_2 = pygame.transform.scale(pygame.image.load('data/backgrounds and titles/background2.png'), (width, height))
health_bar = pygame.transform.scale(pygame.image.load('data/gui/HealthBar.png'), (200, 50))
stamina_bar = pygame.transform.scale(pygame.image.load('data/gui/staminabar.png'), (150, 15))
middle_ground = pygame.transform.scale(pygame.image.load('data/backgrounds and titles/middleground.png'),
                                       (width, height))
middle_ground_2 = pygame.transform.scale(pygame.image.load('data/backgrounds and titles/middleground2.png'),
                                         (width, height))
scroll = pygame.transform.scale(pygame.image.load('data/gui/scroll.png'), (350, 400))
conrols_image = pygame.transform.scale(pygame.image.load('data/backgrounds and titles/cntrls.png'), (width, height))

hp = 10
bg_pos = 0
mg_pos = 0


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global bg_pos, mg_pos
    while True:
        clock.tick(120)
        if bg_pos >= 900:
            bg_pos = 0
        elif mg_pos >= 900:
            mg_pos = 0
        screen.blit(fon, (bg_pos, 0))
        screen.blit(fon, (-width + bg_pos, 0))
        screen.blit(middle_ground, (mg_pos, 0))
        screen.blit(middle_ground, (-width + mg_pos, 0))
        bg_pos += 3
        mg_pos += 1
        screen.blit(pygame.transform.scale(title, (710, 100)), (115, 100))
        screen.blit(pygame.transform.scale(enter, (150, 30)), (350, 300))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return


def settings():
    global fon
    while True:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return


def menu():
    global fon, title, sword, bg_pos, mg_pos
    pos = 185
    while True:
        clock.tick(120)
        if bg_pos == 900:
            bg_pos = 0
        elif mg_pos == 900:
            mg_pos = 0
        screen.blit(fon, (bg_pos, 0))
        screen.blit(fon, (-width + bg_pos, 0))
        screen.blit(middle_ground, (mg_pos, 0))
        screen.blit(middle_ground, (-width + mg_pos, 0))
        bg_pos += 3
        mg_pos += 1
        screen.blit(title, (175, 75))
        screen.blit(sword, (310, pos))
        print_text('Start game', 360, 175)
        print_text(' Controls', 360, 225)
        print_text(' Settings', 360, 275)
        print_text('   Exit', 360, 325)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and pos <= 325:
                pos += 50
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and pos >= 225:
                pos -= 50
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if pos == 185:
                    return 'levels/map2.tmx'
                elif pos == 235:
                    controls()
                elif pos == 335:
                    terminate()

        pygame.display.flip()


def controls():
    screen.blit(conrols_image, (0, 0))
    print_text('Controls', 325, 90, font_type='shrift5.ttf', font_size=75, font_color=(217, 130, 30))
    print_text('Move: A and D', 325, 200, font_type='shrift5.ttf', font_size=50, font_color=(255, 255, 255))
    print_text(' Jump: SPACE', 325, 250, font_type='shrift5.ttf', font_size=50, font_color=(255, 255, 255))
    print_text('  Attack: E', 325, 300, font_type='shrift5.ttf', font_size=50, font_color=(255, 255, 255))
    print_text(' Run: SHIFT', 325, 350, font_type='shrift5.ttf', font_size=50, font_color=(255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                load_map(menu())
                return
        pygame.display.flip()
        clock.tick(fps)


def game_over():
    screen.fill((0, 0, 0))
    print_text('GAME OVER', 300, 105, font_type='shrift5.ttf', font_size=75)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                load_map(menu())
                return
        pygame.display.flip()
        clock.tick(fps)


def print_text(message, x, y, font_color=(255, 250, 250), font_type='shrift4.ttf', font_size=50):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def paused():
    pos = 180
    while True:
        clock.tick(120)
        screen.blit(scroll, (280, 50))
        print_text('Paused', 385, 90, font_size=70, font_color=(139, 0, 0))
        print_text('Continue', 390, 170, font_color=(0, 0, 0))
        print_text('Main menu', 380, 220, font_color=(0, 0, 0))
        screen.blit(sword, (330, pos))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and pos <= 180:
                pos += 50
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and pos >= 230:
                pos -= 50
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if pos == 230:
                    load_map(menu())
                    return
                elif pos == 180:
                    return
        pygame.display.flip()


def load_map(filename):
    global map, map_img, map_rect, player, ghost, cam, slime, skeleton
    from cam import Camera
    from player import Player
    from tiles import TiledMap, Obstacle
    from mob import Ghost, Slime, Skeleton
    from potions import Potion
    all_sprites.empty()
    player_group.empty()
    mobs_group.empty()
    wall_group.empty()
    border_group_left.empty()
    border_group_right.empty()
    dead_line_group.empty()
    roof_group.empty()
    stair_group.empty()
    end_level_group.empty()

    map = TiledMap(filename)
    map_img = map.make_map()
    map_rect = map_img.get_rect()

    cam = Camera(map.width, map.height)
    for tile_object in map.tmxdata.objects:
        if tile_object.name == 'wall':
            Obstacle(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height, wall_group)
        elif tile_object.name == 'player':
            player = Player(tile_object.x, tile_object.y)
        elif tile_object.name == 'border_left':
            Obstacle(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height, border_group_left)
        elif tile_object.name == 'border_right':
            Obstacle(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height, border_group_right)
        elif tile_object.name == 'ghost':
            ghost = Ghost(tile_object.x, tile_object.y)
        elif tile_object.name == 'dead_line':
            Obstacle(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height, dead_line_group)
        elif tile_object.name == 'roof':
            Obstacle(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height, roof_group)
        elif tile_object.name == 'stair':
            Obstacle(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height, stair_group)
        elif tile_object.name == 'end_level':
            Obstacle(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height, end_level_group)
        elif tile_object.name == 'potion':
            Potion(tile_object.x, tile_object.y)
        elif tile_object.name == 'slime':
            slime = Slime(tile_object.x, tile_object.y)
        elif tile_object.name == 'skeleton':
            skeleton = Skeleton(tile_object.x, tile_object.y)


def player_update():
    player.update()
    player.move()
    player.jump()
    player.attack()


player = None
ghost = None
slime = None
skeleton = None
map = None
map_img = None
map_rect = None
cam = None
load_map('levels/level2.tmx')
start_screen()
filename = menu()

load_map(filename)

while True:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            paused()

    all_sprites.update()
    cam.update(player)
    player_group.draw(screen)

    screen.blit(map_img, cam.apply_rect(map_rect))
    screen.blit(health_bar, (0, 0))
    screen.blit(stamina_bar, (47, 30))
    for sprite in all_sprites:
        screen.blit(sprite.image, cam.apply(sprite))
    player_update()
    pygame.display.flip()
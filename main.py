import pygame
import sys
import random

FPS = 60
size = WIDTH, HEIGHT = 1280, 720
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Osos Journey to Valhalla')


import sys

import pygame

file_name = 'data/levels/Svartalfheim.txt'
FPS = 60
pygame.init()
pygame.key.set_repeat(200, 70)

size = WIDTH, HEIGHT = 1280, 720
STEP = 16

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_level(filename):
    # filename = "data/" + filename
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except FileNotFoundError as f:
        print(f'Файл не найден')
        exit(-1)


def load_image(name, color_key=None):
    try:
        image = pygame.image.load(name).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


tile_images = {'wall': load_image('data/textures/blocks/obsidian.png'),
               'empty': load_image('data/textures/blocks/deepslate_tiles.png'),
               'portal': load_image('data/textures/blocks/portal.png')}
player_image = load_image('data/textures/mobs/osos.png', -1)
mob_images = {'scarecrow': load_image('data/textures/mobs/scarecrow.png', -1)}

tile_width = tile_height = 64
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall':
            self.add(wall_group)
        if tile_type == 'portal':
            self.add(portal_group)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 5)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, wall_group):
            self.rect.x -= dx
            self.rect.y -= dy
        if pygame.sprite.spritecollideany(self, portal_group):
            terminate()

class Mob(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, who):
        super().__init__(player_group, all_sprites)
        self.image = mob_images[who]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 16, tile_height * pos_y + 16)



class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'P':
                Tile('portal', x, y)
            elif level[y][x] == 'M':
                Tile('empty', x, y)
                new_mob = Mob(x,y, 'scarecrow')
            elif level[y][x] == 'G':
                Tile('empty', x, y)
                # new_mob = Mob(x,y)
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


player, level_x, level_y = generate_level(load_level(file_name))

camera = Camera()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.move(-STEP, 0)
            if event.key == pygame.K_d:
                player.move(STEP, 0)
            if event.key == pygame.K_w:
                player.move(0, -STEP)
            if event.key == pygame.K_s:
                player.move(0, STEP)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
    fon = pygame.transform.scale(load_image('data/textures/blocks/lava.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
terminate()

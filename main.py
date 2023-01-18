import sys
import os
import pygame
import random

file_name = 'data/levels/Midgard.txt'
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


def randomaiser(where):
    print(where)
    where = where.split('/')
    # print(where)
    # where.insert(3, file_name.split('/')[2].split('.')[0])
    # print(where)
    where = '\\'.join(where)
    print(where)
    for currentdir, dirs, files in os.walk('data'):
        if currentdir == where:
            print(where + '/' + random.choice(files))
            return load_image(where + '/' + random.choice(files), -1)


tile_images = {'leaves': load_image('data/textures/blocks/bamboo_large_leaves.png'),
               'empty': load_image('data/textures/blocks/grass.png'),
               'portal': load_image('data/textures/blocks/portal.png'),
               'waterH': load_image('data/textures/blocks/water_horizontal.png'),
               'waterV': load_image('data/textures/blocks/water_vertical.png'),
               'road': load_image('data/textures/blocks/cobblestone.png'),
               'mini': pygame.transform.scale(load_image('data/textures/houses/mini.png', -1),
                                              (117, 147)),
               'big': pygame.transform.scale(load_image('data/textures/houses/big.png', -1),
                                             (415, 345)),
               'storehouse': pygame.transform.scale(
                   load_image('data/textures/houses/storehouse.png', -1),
                   (268, 352)),
               'typeL': pygame.transform.flip(
                   pygame.transform.scale(load_image('data/textures/houses/typeL.png', -1),
                                          (207, 234)), True, False),
               'wood': pygame.transform.scale(load_image('data/textures/houses/wood.png', -1),
                                              (180, 162)),
               'tree': randomaiser('data/textures/blocks/trees')}
osos_images = {'right': load_image('data/textures/mobs/osos/right.png', -1),
               'left': load_image('data/textures/mobs/osos/left.png', -1)}

tile_width = tile_height = 64
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
house_group = pygame.sprite.Group()
tree_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type != 'tree':
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
        self.add(all_sprites)
        if tile_type in ['waterV', 'waterH', 'leaves']:
            self.add(wall_group)
        if tile_type == 'tree':
            self.add(tree_group)
            self.image = randomaiser('data/textures/blocks/trees')
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            # collide = True
            # while collide:
            #     if collide := pygame.sprite.spritecollideany(self, wall_group):
            #         self.rect.y -= 1
            #     collide = bool(collide)
            #     print(collide)
        if tile_type in ['mini', 'big', 'typeL', 'storehouse', 'wood']:
            self.add(house_group)
            if tile_type == 'mini':
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x - 25, tile_height * pos_y - 80)
            if tile_type == 'typeL':
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x - 13, tile_height * pos_y - 164)
            if tile_type == 'wood':
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x - 55, tile_height * pos_y - 90)
            if tile_type == 'big':
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x - 160, tile_height * pos_y - 80)
            if tile_type == 'storehouse':
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x - 70, tile_height * pos_y - 272)


class Osos(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = osos_images['right']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.health = 100
        self.inventory = []

    def move(self, dx, dy):
        global player, level_x, level_y
        self.rect.x += dx
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, wall_group) or \
                pygame.sprite.spritecollideany(self, tree_group) or \
                pygame.sprite.spritecollideany(self, house_group):
            self.rect.x -= dx
            self.rect.y -= dy

    def left_right(self, a):
        if a == 'left':
            self.image = osos_images['left']
        elif a == 'right':
            self.image = osos_images['right']


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
            if level[y][x] in [' ', '\t', '\n']:
                Tile('empty', x, y)
            elif level[y][x] == '.':
                Tile('empty', x, y)
                Tile('leaves', x, y)
            elif level[y][x] == 'w':
                Tile('waterH', x, y)
            elif level[y][x] == 'v':
                Tile('waterV', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Osos(x, y)
            elif level[y][x] == 'P':
                Tile('portal', x, y)
            elif level[y][x] == 'c':
                Tile('road', x, y)
            elif level[y][x] == 'm':
                Tile('empty', x, y)
                Tile('mini', x, y)
            elif level[y][x] == 'L':
                Tile('empty', x, y)
                Tile('typeL', x, y)
            elif level[y][x] == 'A':
                Tile('empty', x, y)
                Tile('storehouse', x, y)
            elif level[y][x] == 'B':
                Tile('empty', x, y)
                Tile('big', x, y)
            elif level[y][x] == 'W':
                Tile('empty', x, y)
                Tile('wood', x, y)
            elif level[y][x] == 'T':
                Tile('empty', x, y)
                Tile('tree', x, y)
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


player, level_x, level_y = generate_level(load_level(file_name))

pygame.mixer.init()
pygame.mixer.music.load('data/music/03_Midgard.flac')
pygame.mixer.music.play(loops=-1)

camera = Camera()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.move(-STEP, 0)
                player.left_right('left')
            if event.key == pygame.K_d:
                player.move(STEP, 0)
                player.left_right('right')
            if event.key == pygame.K_w:
                player.move(0, -STEP)
            if event.key == pygame.K_s:
                player.move(0, STEP)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
    # fon = pygame.transform.scale(load_image('data/textures/blocks/lava.png'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    house_group.draw(screen)
    tree_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
terminate()

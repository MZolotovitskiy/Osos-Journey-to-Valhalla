import sys
import os
import pygame
import random

file_name = 'data/levels/Midgard.txt'
keys = ['data/levels/Midgard.txt', 'data/levels/wood.txt', 'data/levels/typeL.txt',
        'data/levels/storehouse.txt', 'data/levels/big.txt', 'data/levels/normal.txt']
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
    # print(where)
    where = where.split('/')
    # print(where)
    # where.insert(3, file_name.split('/')[2].split('.')[0])
    # print(where)
    where = '\\'.join(where)
    # print(where)
    for currentdir, dirs, files in os.walk('data'):
        if currentdir == where:
            # print(where + '/' + random.choice(files))
            return load_image(where + '/' + random.choice(files))


tile_images = {'leaves': load_image('data/textures/blocks/bamboo_large_leaves.png'),
               'empty': pygame.transform.scale(load_image('data/textures/blocks/grass.png'),
                                               (64, 64)),
               'portal': load_image('data/textures/blocks/portal.png'),
               'water': pygame.transform.scale(load_image('data/textures/blocks/water.png'),
                                               (64, 64)),
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
               'normal': pygame.transform.scale(load_image('data/textures/houses/normal.png', -1),
                                                (180, 219)),
               'tree': load_image('data/textures/blocks/tree.png', -1),
               'planks': load_image('data/textures/blocks/jungle_planks.png'),
               'barrel': load_image('data/textures/blocks/barrel_side.png'),
               'quartz': load_image('data/textures/blocks/quartz_block_side.png'),
               'crafting_table': load_image('data/textures/blocks/crafting_table_top.png'),
               'furnace': load_image('data/textures/blocks/furnace_front.png'),
               'bed': load_image('data/textures/blocks/bed.png'),
               'log': load_image('data/textures/blocks/spruce_log.png'),
               'hay': load_image('data/textures/blocks/hay_block_side.png'),
               'sand': load_image('data/textures/blocks/sand.png'),
               'books': load_image('data/textures/blocks/bookshelf.png')}
item_images = {'key': load_image('data/textures/items/key.png', -1)}
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
item_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
portal_2ndLevel_back = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.tile_type = tile_type
        if tile_type not in ['berry', 'flower', 'portal_2ndLevel']:
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
        self.add(all_sprites)
        if tile_type in ['water', 'leaves', 'barrel', 'quartz', 'log', 'hay', 'furnace', 'crafting_table', 'books']:
            self.add(wall_group)
        if tile_type == 'flower':
            self.image = randomaiser('data/textures/plants/flower')
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'berry':
            self.image = randomaiser('data/textures/plants/sweet_berry_bush')
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'tree':
            self.add(tree_group)
        if tile_type in ['mini', 'big', 'typeL', 'storehouse', 'wood', 'normal']:
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
            if tile_type == 'normal':
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x - 55, tile_height * pos_y - 150)
        if tile_type == 'portal':
            self.add(portal_group)
        if tile_type == 'portal_2ndLevel':
            self.add(portal_2ndLevel_back)
            self.image = tile_images['portal']
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.tile_type = sheet
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.add(all_sprites)
        self.add(item_group)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Osos(pygame.sprite.Sprite):
    inventory = list()

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.tile_type = 'OSOSBATYA'
        self.image = osos_images['right']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.health = 100
        self.inventory = []

    def move(self, dx, dy):
        global player, level_x, level_y, file_name
        self.rect.x += dx
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, wall_group) or \
                pygame.sprite.spritecollideany(self, tree_group):
            self.rect.x -= dx
            self.rect.y -= dy
        if other := pygame.sprite.spritecollideany(self, item_group):
            Osos.inventory.append('KEY')
            other.kill()
            del keys[keys.index(file_name)]
        if pygame.sprite.spritecollideany(self, portal_2ndLevel_back):
            file_name = 'data/levels/Midgard.txt'
            player, level_x, level_y = generate_level(load_level('data/levels/Midgard.txt'))
        if other := pygame.sprite.spritecollideany(self, house_group):
            try:
                file_name = f'data/levels/{other.tile_type}.txt'
                player, level_x, level_y = generate_level(load_level(file_name))
            except Exception as e:
                print(e)
            self.rect.x -= dx
            self.rect.y -= dy
            print(Osos.inventory)
        if pygame.sprite.spritecollideany(self, portal_group):
            if len(Osos.inventory) == 6:
                terminate()
    def left_right(self, a):
        if a == 'left':
            self.image = osos_images['left']
        elif a == 'right':
            self.image = osos_images['right']
# остановка чтобы дослушать песню это так надо

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
    try:
        for i in all_sprites:
            # print(i.tile_type)
            i.kill()
    except Exception as e:
        print(e)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in [' ', '\t', '\n']:
                Tile('empty', x, y)
            elif level[y][x] == '.':
                if file_name == 'data/levels/storehouse.txt':
                    Tile('sand', x, y)
                else:
                    Tile('planks', x, y)
            elif level[y][x] == '#':
                if file_name == 'data/levels/wood.txt' or file_name == 'data/levels/storehouse.txt':
                    Tile('barrel', x, y)
                else:
                    Tile('quartz', x, y)
            elif level[y][x] == 'w':
                Tile('water', x, y)
            elif level[y][x] == 'f':
                Tile('empty', x, y)
                Tile('flower', x, y)
            elif level[y][x] == 'b':
                Tile('empty', x, y)
                Tile('berry', x, y)
            elif level[y][x] == '@':
                if file_name == 'data/levels/Midgard.txt':
                    Tile('empty', x, y)
                elif file_name == 'data/levels/storehouse.txt':
                    Tile('sand', x, y)
                else:
                    Tile('planks', x, y)
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
            elif level[y][x] == 'N':
                Tile('empty', x, y)
                Tile('normal', x, y)
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
            elif level[y][x] == 'z':
                Tile('portal_2ndLevel', x, y)
            elif level[y][x] == 'F':
                Tile('furnace', x, y)
            elif level[y][x] == 't':
                Tile('crafting_table', x, y)
            elif level[y][x] == 'e':
                Tile('bed', x, y)
            elif level[y][x] == 's':
                Tile('books', x, y)
            elif level[y][x] == 'l':
                Tile('log', x, y)
            elif level[y][x] == 'H':
                Tile('hay', x, y)
            elif level[y][x] == 'K':
                if file_name == 'data/levels/Midgard.txt':
                    Tile('empty', x, y)
                elif file_name == 'data/levels/storehouse.txt':
                    Tile('sand', x, y)
                else:
                    Tile('planks', x, y)
                if file_name in keys:
                    AnimatedSprite(item_images['key'], 16, 1, x, y)
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
    item_group.draw(screen)
    item_group.update()
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
terminate()

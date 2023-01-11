import sys
import os
import random
import pygame

files = ['data/levels/Muspelheim_1st.txt', 'data/levels/Muspelheim_2nd.txt']
files_DLC = ['data/levels/Muspelheim_3rd.txt']
k = 0
file_name = 'data/levels/Muspelheim_1st.txt'
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
            level_map = [line for line in mapFile]  # .strip
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
    where.insert(3, file_name.split('/')[2].split('.')[0])
    # print(where)
    where = '\\'.join(where)
    # print(where)
    for currentdir, dirs, files in os.walk('data'):
        if currentdir == where:
            # print(where + '/' + random.choice(files))
            return load_image(where + '/' + random.choice(files))


tile_images = {'wall': randomaiser('data/textures/blocks/wall'),
               'empty': randomaiser('data/textures/blocks/outside'),
               'floor': randomaiser('data/textures/blocks/floor'),
               'portal_next': load_image('data/textures/blocks/portal.png'),
               'portal_DLC': load_image('data/textures/blocks/portal.png'),
               'portal_back': load_image('data/textures/blocks/portal.png')}
osos_images = {'left': load_image('data/textures/mobs/osos/left.png', -1),
               'right': load_image('data/textures/mobs/osos/right.png', -1)}

tile_width = tile_height = 64
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
portal_next = pygame.sprite.Group()
portal_DLC = pygame.sprite.Group()
portal_back = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall':
            self.add(wall_group)
            self.image = randomaiser('data/textures/blocks/wall')
        elif tile_type == 'empty':
            self.add(all_sprites)
            self.image = randomaiser('data/textures/blocks/outside')
        elif tile_type == 'floor':
            self.add(all_sprites)
            self.image = randomaiser('data/textures/blocks/floor')
        elif tile_type in ['portal_next', 'portal_DLC', 'portal_back']:
            if tile_type == 'portal_next':
                self.add(portal_next)
            elif tile_type == 'portal_DLC':
                self.add(portal_DLC)
            else:
                self.add(portal_back)
            self.image = load_image('data/textures/blocks/portal.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Osos(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = osos_images['left']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.health = 100
        self.inventory = []

    def move(self, dx, dy):
        global player, level_x, level_y, k, files, files_DLC
        self.rect.x += dx
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, wall_group):
            self.rect.x -= dx
            self.rect.y -= dy
        if pygame.sprite.spritecollideany(self, portal_next):
            k += 1
            # player = None
            # level_x = None
            # level_y = None
            player, level_x, level_y = generate_level(load_level(files[k]))
        if pygame.sprite.spritecollideany(self, portal_DLC):
            player, level_x, level_y = generate_level(load_level(files_DLC))
        if pygame.sprite.spritecollideany(self, portal_back):
            k -= 1
            # player = None
            # level_x = None
            # level_y = None
            player, level_x, level_y = generate_level(load_level(files[k]))

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
    for i in all_sprites:
        i.kill()
    # load_fon = pygame.transform.scale(load_image('data/textures/fons/load.png'), (WIDTH, HEIGHT))
    # screen.blit(load_fon, (0, 0))
    # screen.fill((255, 255, 255))
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('floor', x, y)
            elif level[y][x] in [' ', '\t', '\n']:
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('floor', x, y)
                new_player = Osos(x, y)
            elif level[y][x] == 'P':
                Tile('portal_next', x, y)
            elif level[y][x] == 'p':
                Tile('portal_DLC', x, y)
            elif level[y][x] == 'L':
                Tile('portal_back', x, y)
            elif level[y][x] == 'M':
                Tile('floor', x, y)
                # new_mob = Mob(x,y, health)

    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


player, level_x, level_y = generate_level(load_level(file_name))

pygame.mixer.init()
pygame.mixer.music.load('data/music/05_Muspelheim.mp3')
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
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
terminate()

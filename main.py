import sys

import pygame

file_name = 'data/levels/Svartalfh3im.txt'
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
osos_images = {
    'up': pygame.transform.scale(load_image('data/textures/mobs/osos/up.png', -1), (256, 64)),
    'down': pygame.transform.scale(load_image('data/textures/mobs/osos/down.png', -1), (256, 64)),
    'left': pygame.transform.scale(load_image('data/textures/mobs/osos/left.png', -1), (256, 64)),
    'right': pygame.transform.scale(load_image('data/textures/mobs/osos/right.png', -1), (256, 64))}
mob_images = {
    'scarecrow': pygame.transform.scale(load_image('data/textures/mobs/scarecrow.png', -1),
                                        (64, 64)),
    'gid': pygame.transform.scale(load_image('data/textures/mobs/gid.png'), (54, 84))}
key_image = load_image('data/textures/items/key.png', -1)

tile_width = tile_height = 64
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
interface_group = pygame.sprite.Group()


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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
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


class Player(pygame.sprite.Sprite):
    inventory = list()

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames_left = self.cut_sheet(osos_images['left'], 4, 1)
        self.frames_right = self.cut_sheet(osos_images['right'], 4, 1)
        self.frames_up = self.cut_sheet(osos_images['up'], 4, 1)
        self.frames_down = self.cut_sheet(osos_images['down'], 4, 1)
        self.vector = 'left'
        self.cur_frame = 0
        # self.frames = list()
        self.update()
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.add(all_sprites)

    def cut_sheet(self, sheet, columns, rows):
        temp = list()
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                temp.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return temp

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, wall_group):
            self.rect.x -= dx
            self.rect.y -= dy
        if pygame.sprite.spritecollideany(self, portal_group):
            k = 0
            for i in self.inventory:
                if i == 'KEY':
                    k += 1
            if k == 2:
                terminate()
            self.rect.x -= dx
            self.rect.y -= dy
        if other := pygame.sprite.spritecollideany(self, item_group):
            self.inventory.append('KEY')
            other.kill()
        self.update()

    def update(self):
        if self.vector == 'left':
            self.frames = self.frames_left.copy()
        if self.vector == 'right':
            self.frames = self.frames_right.copy()
        if self.vector == 'up':
            self.frames = self.frames_up.copy()
        if self.vector == 'down':
            self.frames = self.frames_down.copy()
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Mob(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, who, health):
        super().__init__(player_group, all_sprites)
        self.image = mob_images[who]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.health = health


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
    global Key
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
                Mob(x, y, 'scarecrow', 5)
            elif level[y][x] == 'G':
                Tile('empty', x, y)
                Mob(x, y, 'gid', 100)
            elif level[y][x] == 'K':
                Tile('empty', x, y)
                Key = AnimatedSprite(key_image, 16, 1, x, y)
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def interface_init():
    pass


pygame.mixer.init()
pygame.mixer.music.load('data/music/02_Svartalfheim.mp3')
pygame.mixer.music.play(loops=-1)

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
                player.vector = 'left'
            if event.key == pygame.K_d:
                player.move(STEP, 0)
                player.vector = 'right'
            if event.key == pygame.K_w:
                player.move(0, -STEP)
                player.vector = 'up'
            if event.key == pygame.K_s:
                player.move(0, STEP)
                player.vector = 'down'
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
    # fon = pygame.transform.scale(load_image('data/textures/blocks/lava.png'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    item_group.update()
    item_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
terminate()

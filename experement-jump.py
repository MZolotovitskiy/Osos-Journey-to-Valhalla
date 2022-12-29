import os
import sys

import pygame

file_name = 'levels/alphatest.txt'
FPS = 60
pygame.init()
pygame.key.set_repeat(100, 100)

size = WIDTH, HEIGHT = 1280, 720
STEP = 25
V = 10

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_level(filename):
    filename = "data/tiles/" + filename
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except FileNotFoundError as f:
        print(f'Файл не найден')
        exit(-1)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
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


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')

tile_width = tile_height = 50
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall':
            self.add(wall_group)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, wall_group):
            self.rect.x -= dx
            self.rect.y -= dy


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
            if level[y][x] == '$':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


player, level_x, level_y = generate_level(load_level(file_name))

camera = Camera()

running = True
jump = False
disable_jump = False
h = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.move(-STEP, 0)
            if event.key == pygame.K_d:
                player.move(STEP, 0)
            if event.key == pygame.K_SPACE:
                if h <= 100 and not disable_jump:
                    player.move(0, -STEP)
                    jump = True
                    h += STEP // 2
                else:
                    h = 0
                    jump = False
                    disable_jump = True
            if event.key == pygame.K_s:
                player.move(0, STEP)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                h = 0
                jump = False
                disable_jump = False
    if not jump:
        player.move(0, STEP // 2)
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    fon = pygame.transform.scale(load_image('box.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    # screen.fill((0, 0, 0))

    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 50), 0)
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 50, 720), 0)
    pygame.draw.rect(screen, (0, 0, 0), (1230, 0, 50, 720), 0)
    pygame.draw.rect(screen, (0, 0, 0), (0, 620, 1280, 100), 0)
    pygame.display.flip()
    clock.tick(FPS)
terminate()

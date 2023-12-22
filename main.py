import sys
import pygame
import pytmx

file_name = 'data/levels/Svartalfheim/Svartalfheim.tmx'
FPS = 60
pygame.init()
pygame.key.set_repeat(200, 70)

size = WIDTH, HEIGHT = 1280, 720
STEP = 16

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
interface_group = pygame.sprite.Group()
mob_group = pygame.sprite.Group()


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

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, tile_width, tile_height):
        super().__init__(tiles_group, all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        # print(pos_x, pos_y)


# class AnimatedSprite(pygame.sprite.Sprite):
#     def __init__(self, sheet, columns, rows, x, y):
#         super().__init__(all_sprites)
#         self.frames = []
#         self.cut_sheet(sheet, columns, rows)
#         self.cur_frame = 0
#         self.image = self.frames[self.cur_frame]
#         self.rect = self.image.get_rect().move(
#             tile_width * x, tile_height * y)
#         self.add(all_sprites)
#         self.add(item_group)
#
#     def cut_sheet(self, sheet, columns, rows):
#         self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
#                                 sheet.get_height() // rows)
#         for j in range(rows):
#             for i in range(columns):
#                 frame_location = (self.rect.w * i, self.rect.h * j)
#                 self.frames.append(sheet.subsurface(pygame.Rect(
#                     frame_location, self.rect.size)))
#
#     def update(self):
#         self.cur_frame = (self.cur_frame + 1) % len(self.frames)
#         self.image = self.frames[self.cur_frame]


class Player(pygame.sprite.Sprite):
    inventory = list()

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames_left = self.cut_sheet(load_image('data/textures/png/osos_run_left.png', -1), 8, 1)
        self.frames_right = self.cut_sheet(load_image('data/textures/png/osos_run_right.png', -1), 8, 1)
        # self.frames_up = self.cut_sheet(osos_images['up'], 4, 1)
        # self.frames_down = self.cut_sheet(osos_images['down'], 4, 1)
        self.vector = 'left'
        self.cur_frame = 0
        # self.frames = list()
        self.update()
        self.rect = self.image.get_rect().move(pos_x, pos_y)

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
            terminate()
        if other := pygame.sprite.spritecollideany(self, item_group):
            self.inventory.append(other)
            other.kill()
        self.update()

    def update(self):
        if self.vector == 'left':
            self.frames = self.frames_left.copy()
        if self.vector == 'right':
            self.frames = self.frames_right.copy()
        # if self.vector == 'up':
        #     self.frames = self.frames_up.copy()
        # if self.vector == 'down':
        #     self.frames = self.frames_down.copy()
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


def generate_level(filename):
    try:
        map = pytmx.load_pygame(filename)
        tile_size = map.tilewidth
        osos = None
        for layer in range(6):
            for y in range(map.height):
                for x in range(map.width):
                    image = map.get_tile_image(x, y, layer)
                    if image:
                        temp = Tile(pygame.transform.scale2x(image), x * tile_size * 2, y * tile_size * 2, 16, 16)
                        if layer == 3:
                            osos = Player(x * 16 * 2, y * 16 * 2)
                        if layer == 1:
                            temp.add(wall_group)
                        if layer == 4:
                            temp.add(mob_group)
                        if layer == 5:
                            temp.add(portal_group)
                        temp.add(all_sprites)
        return osos
    except Exception as f:
        print(f)
        exit(-1)


def terminate():
    pygame.quit()
    sys.exit()


def interface_init():
    pass


pygame.mixer.init()
pygame.mixer.music.load('data/music/02_Svartalfheim.mp3')
pygame.mixer.music.play(loops=-1)

player = generate_level(file_name)

# camera = Camera()
#
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
            if event.key == pygame.K_SPACE:
                player.move(0, -STEP)

        # camera.update(player)
        # for sprite in all_sprites:
        #     camera.apply(sprite)
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

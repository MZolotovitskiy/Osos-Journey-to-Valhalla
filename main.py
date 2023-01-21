import sys
import os
import random
from os import environ
import pygame

file_name = 'data/levels/Svartalfh3im.txt'
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
files = ['data/levels/Svartalfh3im.txt', 'data/levels/Muspelheim_1st.txt',
         'data/levels/Muspelheim_2nd.txt']
k = 0
FPS = 60
pygame.init()
pygame.key.set_repeat(200, 70)
size = WIDTH, HEIGHT = 1280, 720
STEP = 16

l = 0
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
    where.insert(3, file_name.split('/')[2].split('.')[0])
    # print(where)
    where = '\\'.join(where)
    # print(where)
    for currentdir, dirs, files in os.walk('data'):
        if currentdir == where:
            print(where + '/' + random.choice(files))
            return load_image(where + '/' + random.choice(files))


osos_images = {'left': load_image('data/textures/mobs/osos/left.png', -1),
               'right': load_image('data/textures/mobs/osos/right.png', -1)}
tile_images = {'wall': load_image('data/textures/blocks/Svartalfheim/obsidian.png'),
               'empty': load_image('data/textures/blocks/Svartalfheim/deepslate_tiles.png'),
               'portal': load_image('data/textures/blocks/Svartalfheim/portal.png')}
item_images = {'key': load_image('data/textures/items/key.png', -1)}

mob_images = {
    'scarecrow': pygame.transform.scale(load_image('data/textures/mobs/scarecrow/standard.png', -1),
                                        (64, 64)),
    'gid': pygame.transform.scale(load_image('data/textures/mobs/gid.png'), (54, 84)),
    'fiend': load_image('data/textures/mobs/fiend/stay.png', -1),
    'fiend_attack': load_image('data/textures/mobs/fiend/attack.png', -1),
    'golem': load_image('data/textures/mobs/golem/stay.png')}
damaged_mob_images = {
    'scarecrow': pygame.transform.scale(load_image('data/textures/mobs/scarecrow/damage.png', -1),
                                        (64, 64)),
    'gid': pygame.transform.scale(load_image('data/textures/mobs/gid.png'), (54, 84))}
balticka3_images = {
    0: pygame.transform.rotozoom(load_image('data/textures/projectiles/balticka3/up.png', -1), 0,
                                 0.05),
    1: pygame.transform.rotozoom(load_image('data/textures/projectiles/balticka3/right.png', -1), 0,
                                 0.05),
    2: pygame.transform.rotozoom(load_image('data/textures/projectiles/balticka3/down.png', -1), 0,
                                 0.05),
    3: pygame.transform.rotozoom(load_image('data/textures/projectiles/balticka3/left.png', -1), 0,
                                 0.05)}

tile_width = tile_height = 64
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
interface_group = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
mob_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


def show_pos(pos):
    pass


def start_screen(screen):
    buttons = [pygame.Rect((60, 340), (307, 87)), pygame.Rect((60, 427), (307, 87)),
               pygame.Rect((60, 514), (307, 87)),
               pygame.Rect((60, 601), (307, 87))]
    write_intro(screen, buttons)
    pygame.display.flip()
    menu_running = True
    clock = pygame.time.Clock()
    is_drawn = False
    while menu_running:
        mouse_pos = pygame.mouse.get_pos()
        for i in range(len(buttons)):
            if buttons[i].collidepoint(mouse_pos):
                is_drawn = True
                screen.fill('black')
                write_intro(screen, buttons)
                s = pygame.Surface((buttons[i][2], buttons[i][3]), pygame.SRCALPHA)
                s.fill((190, 190, 190, 130))
                screen.blit(s, (buttons[i][0], buttons[i][1] - 10))
                break
            elif is_drawn:
                is_drawn = False
                screen.fill('black')
                write_intro(screen, buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if buttons[0].collidepoint(mouse_pos):
                    return
                if buttons[2].collidepoint(mouse_pos):
                    settings(screen)
                if buttons[3].collidepoint(mouse_pos):
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


def settings(screen):
    volume_bar_coord_x = (pygame.mixer.music.get_volume() * 720) + 60
    volume_bar = pygame.Rect((60, 437), (720, 10))
    sound_square = pygame.Rect((500, 482), (30, 30))
    return_buttton = pygame.Rect(60, 544, 481, 67)
    if pygame.mixer.music.get_busy():
        sound_enabled = True
    else:
        sound_enabled = False
    write_settings(screen, volume_bar, volume_bar_coord_x, sound_square, sound_enabled)
    pygame.display.flip()
    clock = pygame.time.Clock()
    settings_running = True
    while settings_running:
        write_settings(screen, volume_bar, volume_bar_coord_x, sound_square, sound_enabled)
        mouse_pos = pygame.mouse.get_pos()
        if return_buttton.collidepoint(mouse_pos):
            s = pygame.Surface((return_buttton[2], return_buttton[3]), pygame.SRCALPHA)
            s.fill((190, 190, 190, 130))
            screen.blit(s, (return_buttton[0], return_buttton[1]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if volume_bar.collidepoint(mouse_pos):
                    volume_bar_coord_x = mouse_pos[0]
                    pygame.mixer.music.set_volume(1 * (mouse_pos[0] - 60) / 720)
                if sound_square.collidepoint(mouse_pos):
                    sound_enabled = not sound_enabled
                    if not sound_enabled:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play()
                if return_buttton.collidepoint(mouse_pos):
                    return
        pygame.display.flip()
        clock.tick(FPS)


def write_intro(screen, buttons):
    text_coord = 330
    font = pygame.font.Font('C:/Windows/Fonts/times.ttf', 80)
    name_text = 'Путешествие Ососа в Вальгаллу'
    buttons_text = ['Новая игра', 'Сохранения', 'Настройки', 'Выход']
    intro_bground = load_image('data/Images/StartScreenBG.jpeg')
    screen.blit(intro_bground, (0, 0))
    name_rendered = font.render(name_text, True, pygame.Color('white'))
    intro_rect = name_rendered.get_rect()
    intro_rect.x += 40
    intro_rect.y += 30
    screen.blit(name_rendered, intro_rect)
    font = pygame.font.Font('C:/Windows/Fonts/times.ttf', 60)
    for line in buttons_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_size = string_rendered.get_rect()
        intro_rect = intro_size
        intro_rect.x = 60
        text_coord += 20
        intro_rect.top = text_coord
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def write_settings(screen, volume_bar, volume_bar_coord_x, sound_square, sound_enabled):
    screen.fill('black')
    intro_bground = load_image('data/Images/StartScreenBG.jpeg')
    screen.blit(intro_bground, (0, 0))
    text_coord = 330
    font = pygame.font.Font('C:/Windows/Fonts/times.ttf', 80)
    name_text = 'Путешествие Ососа в Вальгаллу'
    settings_text = 'Настройки'
    name_rendered = font.render(name_text, True, pygame.Color('white'))
    intro_rect = name_rendered.get_rect()
    intro_rect.x += 40
    intro_rect.y += 30
    screen.blit(name_rendered, intro_rect)
    name_rendered = font.render(settings_text, True, pygame.Color('white'))
    intro_rect = name_rendered.get_rect()
    intro_rect.x += 40
    intro_rect.y += 260
    screen.blit(name_rendered, intro_rect)
    font = pygame.font.Font('C:/Windows/Fonts/times.ttf', 60)
    volume_text = 'Громкость'
    string_rendered = font.render(volume_text, True, pygame.Color('white'))
    intro_size = string_rendered.get_rect()
    intro_rect = intro_size
    intro_rect.x = 60
    text_coord += 20
    intro_rect.top = text_coord
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    text_coord += 20
    pygame.draw.rect(screen, 'white', volume_bar)
    pygame.draw.circle(screen, (130, 130, 130), (volume_bar_coord_x, text_coord + 5), 10)
    string = 'Выключить звук'
    string_rendered = font.render(string, True, pygame.Color('white'))
    intro_size = string_rendered.get_rect()
    intro_rect = intro_size
    intro_rect.x = 60
    text_coord += 20
    intro_rect.top = text_coord
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    if sound_enabled:
        pygame.draw.rect(screen, 'white', sound_square, 1)
    else:
        pygame.draw.rect(screen, 'white', sound_square)
    string = 'Вернуться в меню'
    string_rendered = font.render(string, True, pygame.Color('white'))
    string_size = string_rendered.get_rect()
    string_rect = intro_size
    string_rect.x = 60
    text_coord += 20
    string_rect.top = text_coord
    screen.blit(string_rendered, string_rect)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, level):
        super().__init__(tiles_group, all_sprites)
        if level == 1:
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            if tile_type == 'wall':
                self.add(wall_group)
            if tile_type == 'portal':
                self.add(portal_group)
        elif level in [2, 3]:
            if tile_type == 'wall':
                self.image = randomaiser('data/textures/blocks/wall')
                self.add(wall_group)
            elif tile_type == 'empty':
                self.image = randomaiser('data/textures/blocks/outside')
                self.add(all_sprites)
            elif tile_type == 'floor':
                self.image = randomaiser('data/textures/blocks/floor')
                self.add(all_sprites)
            elif tile_type == 'portal':
                self.add(portal_group)
                self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)


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
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = osos_images['left']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 5)
        self.inventory = []
        self.damage = 3
        self.health = 200

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, wall_group) or \
                pygame.sprite.spritecollideany(self, mob_group):
            self.rect.x -= dx
            self.rect.y -= dy
        if pygame.sprite.spritecollideany(self, portal_group):
            global file_name, camera, player, level_x, level_y, l
            if l == 0:
                if len(self.inventory) == 2:
                    l += 1
                    file_name = files[l]
                    player, level_x, level_y = generate_level(load_level(files[l]))
            elif l == 1:
                l += 1
                file_name = files[l]
                print(l, file_name)
                player, level_x, level_y = generate_level(load_level(files[l]))
            set_song()
        if other := pygame.sprite.spritecollideany(self, item_group):
            self.inventory.append(other)
            other.kill()

    def left_right(self, a):
        if a == 'left':
            self.image = osos_images['left']
        elif a == 'right':
            self.image = osos_images['right']

    def attack(self, step):
        projectile = Projectile(self.rect.x, self.rect.y, step, self.damage, self)
        all_sprites.add(projectile)
        projectiles.add(projectile)

    def hp(self):
        s = pygame.Surface((210, 50), pygame.SRCALPHA)
        s.fill((190, 190, 190, 130))
        screen.blit(s, (15, 15))
        pygame.draw.rect(screen, 'red', (20, 50, abs(self.health), 10))
        name = 'OSOS'
        font = pygame.font.Font('C:/Windows/Fonts/times.ttf', 30)
        name_rendered = font.render(name, True, pygame.Color(255, 204, 0))
        rect = name_rendered.get_rect()
        rect.x += 16
        rect.y += 15
        screen.blit(name_rendered, rect)

    def dialog(self):
        for sprite in mob_group:
            rect = sprite.rect.copy()
            rect.width += 64
            rect.height += 64
            if rect.colliderect(player.rect):
                if sprite.who == 'gid':
                    global running
                    gid_word = [
                        'Привет, Осос! Как твои дела? А, точно ты же не разговариваешь...', 'В общем у меня есть '
                        'отличная идея! Я недавно прочитал про древнее существо,', 'хранящее потерянную реликвию. '
                        'Если ты победишь его, то точно станешь великим героем.']
                    room = 0
                    dialog_running = True
                    s = pygame.Surface((1280, 200), pygame.SRCALPHA)
                    s.fill((255, 255, 255, 130))
                    screen.blit(s, (0, 520))
                    pygame.display.flip()
                    for i in gid_word:
                        font = pygame.font.Font('C:/Windows/Fonts/times.ttf', 30)
                        name_rendered = font.render(i, True, pygame.Color(0, 0, 0))
                        trect = name_rendered.get_rect()
                        trect.x += 1
                        trect.y += 520 + room
                        screen.blit(name_rendered, trect)
                        room += 30
                        pygame.display.flip()
                    while dialog_running:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                dialog_running = False
                                running = False
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                dialog_running = False


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, step, damage, shooter):
        pygame.sprite.Sprite.__init__(self)
        self.image = balticka3_images[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.start_x = pos_x
        self.dx = 0
        self.step = step
        self.imnum = 0
        if self.step < 0:
            self.dn = -1
        else:
            self.dn = 1
        self.damage = 3
        self.shooter = shooter

    def update(self):
        self.imnum += self.dn
        center = self.rect.center
        if self.imnum > 3:
            self.imnum = 0
        elif self.imnum < 0:
            self.imnum = 3
        self.image = balticka3_images[self.imnum]
        self.rect = self.image.get_rect(center=center)
        self.rect.x += self.step
        self.dx += 8
        if self.dx >= 192:
            self.kill()
        if pygame.sprite.spritecollideany(self, wall_group):
            self.kill()
        if pygame.sprite.spritecollideany(self, mob_group) \
                and pygame.sprite.spritecollideany(self, mob_group) != self.shooter:
            pygame.sprite.spritecollideany(self, mob_group).health -= self.damage
            pygame.sprite.spritecollideany(self, mob_group).image = damaged_mob_images[
                pygame.sprite.spritecollideany(self, mob_group).who]
            self.kill()
        if self.rect.colliderect(player.rect) and player != self.shooter:
            player.hp(self.damage)
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, who, health, enemy=None, attack=None):
        super().__init__(player_group, all_sprites)
        self.who = who
        self.image = mob_images[self.who]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.health = health
        self.room = 0
        mob_group.add(self)

    def update(self):
        if self.health <= 0:
            self.kill()
        if self.room >= 15:
            self.image = mob_images[self.who]
            self.room = 0
        self.room += 1


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
    load_fon = pygame.transform.scale(load_image('data/textures/fons/load.png'),
                                      (WIDTH, HEIGHT))
    screen.blit(load_fon, (0, 0))
    pygame.display.flip()
    if level == load_level('data/levels/Svartalfh3im.txt'):
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y, 1)
                elif level[y][x] == '#':
                    Tile('wall', x, y, 1)
                elif level[y][x] == '@':
                    Tile('empty', x, y, 1)
                    new_player = Player(x, y)
                elif level[y][x] == 'P':
                    Tile('portal', x, y, 1)
                elif level[y][x] == 'M':
                    Tile('empty', x, y, 1)
                    Mob(x, y, 'scarecrow', 5)
                elif level[y][x] == 'G':
                    Tile('empty', x, y, 1)
                    Mob(x, y, 'gid', 100)
                elif level[y][x] == 'K':
                    Tile('empty', x, y, 1)
                    Key = AnimatedSprite(item_images['key'], 16, 1, x, y)
        return new_player, x, y
    elif level == load_level('data/levels/Muspelheim_1st.txt') or \
            level == load_level('data/levels/Muspelheim_2nd.txt'):
        for i in all_sprites:
            i.kill()
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('floor', x, y, 2)
                elif level[y][x] in [' ', '\t', '\n']:
                    Tile('empty', x, y, 2)
                elif level[y][x] == '#':
                    Tile('wall', x, y, 2)
                elif level[y][x] == '@':
                    Tile('floor', x, y, 2)
                    new_player = Player(x, y)
                elif level[y][x] == 'P':
                    Tile('portal', x, y, 2)
                elif level[y][x] == 'M':
                    Tile('floor', x, y, 2)
                    Mob(x, y, 'golem', 100)
                elif level[y][x] == 'm':
                    Tile('floor', x, y, 2)
                    Mob(x, y, 'fiend', 60)
                elif level[y][x] == 'K':
                    Tile('floor', x, y, 2)
                    AnimatedSprite(item_images['key'], 16, 1, x, y)
        return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def interface_init():
    pass


def set_song():
    if l == 0:
        pygame.mixer.music.load('data/music/02_Svartalfheim.mp3')
        pygame.mixer.music.play(loops=-1)
    if l == 1:
        pygame.mixer.music.load('data/music/05_Muspelheim.mp3')
        pygame.mixer.music.play(loops=-1)


pygame.mixer.init()
pygame.mixer.music.load('data/music/01_menuLoop.mp3')
pygame.mixer.music.play(loops=-1)
start_screen(screen)
set_song()

player, level_x, level_y = generate_level(load_level(file_name))

camera = Camera()
direction = True
running = True
room = 4
shot_room = 60
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.move(-STEP, 0)
                player.left_right('left')
                direction = True
            if event.key == pygame.K_d:
                player.move(STEP, 0)
                player.left_right('right')
                direction = False
            if event.key == pygame.K_w:
                player.move(0, -STEP)
            if event.key == pygame.K_s:
                player.move(0, STEP)
            if event.key == pygame.K_SPACE:
                if shot_room >= 60:
                    if direction:
                        player.attack(-8)
                    else:
                        player.attack(8)
                    shot_room = 0
            if event.key == pygame.K_e:
                player.dialog()
                q = 'aboba'
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    item_group.update()
    item_group.draw(screen)
    mob_group.update()
    player.hp()
    if room >= 3:
        projectiles.update()
        projectiles.draw(screen)
        room = 0
    room += 1
    shot_room += 1
    pygame.display.flip()
    clock.tick(FPS)
terminate()

from functions import start_screen
import sys
import pygame
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


FPS = 60
pygame.init()
pygame.key.set_repeat(200, 70)
size = WIDTH, HEIGHT = 1280, 720
STEP = 16
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

pygame.mixer.init()
osos_images = {'left': load_image('data/textures/mobs/osos/left.png', -1),
               'right': load_image('data/textures/mobs/osos/right.png', -1)}
tile_images = {'wall': load_image('data/textures/blocks/obsidian.png'),
               'empty': load_image('data/textures/blocks/deepslate_tiles.png'),
               'portal': load_image('data/textures/blocks/portal.png')}
mob_images = {
    'scarecrow': pygame.transform.scale(load_image('data/textures/mobs/scarecrow/standard.png', -1),
                                        (64, 64)),
    'gid': pygame.transform.scale(load_image('data/textures/mobs/gid.png'), (54, 84))}
damaged_mob_images = {
    'scarecrow': pygame.transform.scale(load_image('data/textures/mobs/scarecrow/damage.png', -1),
                                        (64, 64)),
    'gid': pygame.transform.scale(load_image('data/textures/mobs/gid.png'), (54, 84))}
key_image = load_image('data/textures/items/key.png', -1)
balticka3_images = {0: pygame.transform.rotozoom(load_image('data/textures/projectiles/balticka3/up.png', -1), 0, 0.05),
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
        intro_rect = name_rendered.get_rect()
        intro_rect.x += 16
        intro_rect.y += 15
        screen.blit(name_rendered, intro_rect)


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
    def __init__(self, pos_x, pos_y, who, health):
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


class Gid(Mob):
    def Protection(self):
        pass


class Dialog:
    def __init__(self):
        pass


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


music = pygame.mixer.Sound('data/music/menuLoop.mp3')
music.play()
pygame.mixer.init()
pygame.mixer.music.load('data/music/02_Svartalfheim.mp3')
pygame.mixer.music.play(loops=-1)

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
                pass
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


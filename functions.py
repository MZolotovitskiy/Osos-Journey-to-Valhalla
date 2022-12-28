import pygame
import sys
import os

FPS = 60


def load_image(name, color_key=None):
    fullname = os.path.join('Data', 'Images', name)
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


def terminate():
    pygame.quit()
    sys.exit()


def show_pos(pos):
    pass


def start_screen(screen):
    buttons = [pygame.Rect((60, 340), (307, 87)), pygame.Rect((60, 427), (307, 87)), pygame.Rect((60, 514), (307, 87)),
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
                if buttons[2].collidepoint(mouse_pos):
                    settings(screen)
                if buttons[3].collidepoint(mouse_pos):
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


def settings(screen):
    write_settings(screen)


def write_intro(screen, buttons):
    text_coord = 330
    font = pygame.font.Font('C:/Windows/Fonts/times.ttf', 80)
    name_text = 'Путешествие Ососа в Вальгаллу'
    buttons_text = ['Новая игра', 'Сохранения', 'Настройки', 'Выход']
    intro_bground = load_image('StartScreenBG.jpeg')
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


def write_settings(screen):
    screen.fill('black')
    intro_bground = load_image('StartScreenBG.jpeg')
    screen.blit(intro_bground, (0, 0))
    font = pygame.font.Font('C:/Windows/Fonts/times.ttf', 60)

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
    button_pos = []
    text_coord = 330
    font = pygame.font.Font(None, 90)
    name_text = 'Путешествие Ососа в Вальгаллу'
    buttons_text = ['Новая игра', 'Сохранения', 'Настройки', 'Выход']
    intro_bground = load_image('BGround.JPG')
    screen.blit(intro_bground, (0, 0))
    name_rendered = font.render(name_text, True, pygame.Color('white'))
    intro_rect = name_rendered.get_rect()
    intro_rect.x += 10
    intro_rect.y += 10
    screen.blit(name_rendered, intro_rect)
    font = pygame.font.Font(None, 60)
    for line in buttons_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_size = string_rendered.get_rect()
        intro_rect = intro_size
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 60
        text_coord += intro_rect.height
        button_pos.append(intro_size)
        screen.blit(string_rendered, intro_rect)
    pygame.display.flip()
    menu_running = True
    clock = pygame.time.Clock()
    is_drawn = False
    while menu_running:
        mouse_pos = pygame.mouse.get_pos()
        for i in range(len(button_pos)):
            if button_pos[i].collidepoint(mouse_pos):
                is_drawn = True
                text_coord = 330
                intro_rect = name_rendered.get_rect()
                intro_rect.x += 10
                intro_rect.y += 10
                screen.fill('black')
                screen.blit(intro_bground, (0, 0))
                screen.blit(name_rendered, intro_rect)
                font = pygame.font.Font(None, 60)
                for line in buttons_text:
                    string_rendered = font.render(line, True, pygame.Color('white'))
                    intro_size = string_rendered.get_rect()
                    intro_rect = intro_size
                    text_coord += 30
                    intro_rect.top = text_coord
                    intro_rect.x = 60
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)
                s = pygame.Surface((intro_rect[2] + 110, intro_rect[3] + 60), pygame.SRCALPHA)  # per-pixel alpha
                s.fill((190, 190, 190, 130))  # notice the alpha value in the color
                screen.blit(s, (button_pos[i][0], button_pos[i][1] - 30))
                break
            elif not is_drawn:
                is_drawn = False
                text_coord = 330
                intro_rect = name_rendered.get_rect()
                intro_rect.x += 10
                intro_rect.y += 10
                screen.fill('black')
                screen.blit(intro_bground, (0, 0))
                screen.blit(name_rendered, intro_rect)
                font = pygame.font.Font(None, 60)
                for line in buttons_text:
                    string_rendered = font.render(line, True, pygame.Color('white'))
                    intro_size = string_rendered.get_rect()
                    intro_rect = intro_size
                    text_coord += 30
                    intro_rect.top = text_coord
                    intro_rect.x = 60
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
        pygame.display.flip()
        clock.tick(FPS)

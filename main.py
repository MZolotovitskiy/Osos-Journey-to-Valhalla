import pygame
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'



pygame.init()
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)

pygame.mixer.init()
music = pygame.mixer.Sound('data/music/menuLoop.mp3')
music.play()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

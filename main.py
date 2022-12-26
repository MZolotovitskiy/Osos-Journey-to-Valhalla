import pygame
from functions import start_screen
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


FPS = 60
pygame.init()
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Osos Journey to Valhalla')
pygame.mixer.init()
music = pygame.mixer.Sound('data/music/menuLoop.mp3')
music.play()
start_screen(screen)
pygame.quit()

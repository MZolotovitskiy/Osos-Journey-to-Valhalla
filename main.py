from functions import start_screen
import pygame
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

FPS = 60
pygame.init()
pygame.mixer.init()
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Osos Journey to Valhalla')
pygame.mixer.music.load('Data/Music/menuLoop.mp3')
pygame.mixer.music.play(-1)
start_screen(screen)
pygame.quit()

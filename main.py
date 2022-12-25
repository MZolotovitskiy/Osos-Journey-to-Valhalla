import pygame
from functions import start_screen

FPS = 60
pygame.init()
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Osos Journey to Valhalla')
start_screen(screen)

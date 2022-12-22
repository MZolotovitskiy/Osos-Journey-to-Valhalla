import pygame

pygame.init()
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)

pygame.mixer.init()
music = pygame.mixer.Sound('data/menu.mp3')
music.play()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

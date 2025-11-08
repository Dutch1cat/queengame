import pygame
def draw_health_bar(screen, x, y, width, height, current, maximum, color):
    pygame.draw.rect(screen, (60, 60, 60), (x, y, width, height))  # sfondo
    ratio = current / maximum
    pygame.draw.rect(screen, color, (x, y, width * ratio, height))
def is_dead(c):
    if c.death:
        return True
    else:
        return False
def scale(img, dm:tuple):
    return pygame.transform.scale(img, dm)
def load(path):
    return pygame.image.load(path)
def now():
    return pygame.time.get_ticks()
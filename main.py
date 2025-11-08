import pygame
from player import Player
from enemy import Enemy
import functions as f
print("a")
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player = Player(400 - 64, 350)
enemy = Enemy(400 - 64, 100)

win_screen = f.scale(f.load("assets/end/win.png"), (800, 600))
lost_screen = f.scale(f.load("assets/end/gameover.png"), (800, 600))

running = True
end = False
end_time = None  # timer di fine partita

while running:
    screen.fill((30, 30, 30))

    # Barre della vita
    f.draw_health_bar(screen, 50, 50, 200, 20, player.health, player.max_health, (0, 200, 0))
    f.draw_health_bar(screen, 550, 50, 200, 20, enemy.health, enemy.max_health, (200, 0, 0))

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not end:
        if not f.is_dead(player) and not f.is_dead(enemy):
            player.handle_input(keys)
            player.update(enemy)
            enemy.update(player)
            enemy.draw(screen)
            player.draw(screen)
        else:
            end = True
            end_time = f.now()
            if f.is_dead(player):
                screen.blit(lost_screen, (0, 0))
            else:
                screen.blit(win_screen, (0, 0))
    else:
        # Mostra schermata finale per 5 secondi
        if f.is_dead(player):
            screen.blit(lost_screen, (0, 0))
        else:
            screen.blit(win_screen, (0, 0))
        if f.now() - end_time > 5000:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame
import random
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.base_y = y
        self.state = "idle"
        self.invulnerable = False
        self.attack_cooldown = random.randint(500,2500)  # ms
        self.attack_duration = 200   # ms
        self.prepare_duration = 400  # ms
        self.last_attack = pygame.time.get_ticks()
        self.action_timer = 0
        self.idle_frame = 0
        self.last_idle_switch = pygame.time.get_ticks()
        self.frame_duration = 400  # ms
        self.max_health = 600
        self.health = self.max_health
        self.just_attack = False
        self.death = False


        def load_scaled(path, size=(128, 192)):
            return pygame.transform.scale(pygame.image.load(path), size)

        self.images = {
            "idle": [load_scaled("assets/enemy1/idle1.png"),
                     load_scaled("assets/enemy1/idle2.png")],
            "prepare": load_scaled("assets/enemy1/prepare.png"),
            "attack": load_scaled("assets/enemy1/attack.png"),
            "hit": load_scaled("assets/enemy1/hit.png")
        }


    def update(self, player):
        now = pygame.time.get_ticks()

        if self.health <= 0:
            self.death = True

        # Gestione stato "hit" (non blocca il ciclo)
        if not self.death:
            if self.state == "hit":
                if now - self.action_timer > 400:
                    self.state = "idle"
                    self.invulnerable = False
                # Non return! Così può comunque entrare in prepare dopo

            # Idle animation
            if self.state == "idle":
                if now - self.last_idle_switch > self.frame_duration:
                    self.idle_frame = (self.idle_frame + 1) % 2
                    self.last_idle_switch = now
                if now - self.last_attack > self.attack_cooldown:
                    self.state = "prepare"
                    self.invulnerable = True
                    self.action_timer = now

            elif self.state == "prepare":
                if now - self.action_timer > self.prepare_duration:
                    self.state = "attack"
                    self.action_timer = now
                    self.just_attack = True

            elif self.state == "attack":
                self.y += 100
                if self.just_attack:
                    if player.state not in ["dodge_right", "dodge_left"]:
                        player.hit()
                        self.just_attack = False
                if now - self.action_timer > self.attack_duration:
                    self.y = self.base_y
                    self.state = "idle"
                    self.invulnerable = False
                    self.last_attack = now
                    self.attack_cooldown = random.randint(500, 2000)



    def draw(self, screen):
        if self.state == "idle":
            screen.blit(self.images["idle"][self.idle_frame], (self.x, self.y))
        else:
            screen.blit(self.images[self.state], (self.x, self.y))

    def receive_hit(self):
        if not self.invulnerable and self.state != "hit":
            print("Nemico colpito!")
            self.state = "hit"
            self.health = max(0, self.health - 15)
            self.action_timer = pygame.time.get_ticks()



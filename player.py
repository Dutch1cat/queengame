import pygame

class Player:
    def load_scaled(self, path, size=(128, 192)):
        return pygame.transform.scale(pygame.image.load(path), size)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.base_x = x
        self.base_y = y
        self.state = "idle"
        self.direction = None
        self.images = {
            "idle": [self.load_scaled("assets/player/idle1.png"),
                    self.load_scaled("assets/player/idle2.png")],
            "dodge_left": self.load_scaled("assets/player/dodge_left.png"),
            "dodge_right": self.load_scaled("assets/player/dodge_right.png"),
            "punch": self.load_scaled("assets/player/punch.png")
        }
        self.idle_frame = 0
        self.last_idle_switch = pygame.time.get_ticks()
        self.frame_duration = 400  # ms
        self.action_timer = 0
        self.action_duration = 450  # ms
        self.enemy_is_hit = False
        self.max_health = 100
        self.health = 100
        self.death = False

    def hit(self):
        self.state = "hit"
        self.action_timer = pygame.time.get_ticks()
        self.health = max(0, self.health - 10)
        self.images["hit"] = pygame.transform.scale(pygame.image.load("assets/player/hit.png"), (128, 192))
        self.x = self.base_x
        self.y = self.base_y


    def handle_input(self, keys):
        if not self.death:
            if self.state == "idle":
                if keys[pygame.K_LEFT]:
                    self.state = "dodge_left"
                    self.x -= 150
                    self.action_timer = pygame.time.get_ticks()
                elif keys[pygame.K_RIGHT]:
                    self.state = "dodge_right"
                    self.x += 150
                    self.action_timer = pygame.time.get_ticks()
                elif keys[pygame.K_z] or keys[pygame.K_RETURN]:
                    self.state = "punch"
                    self.enemy_is_hit = True
                    self.y -= 150
                    self.action_timer = pygame.time.get_ticks()

    def update(self, enemy):
        if self.health <= 0:
            self.death = True
        if not self.death:
            now = pygame.time.get_ticks()
            if self.enemy_is_hit:

                enemy.receive_hit()
                self.enemy_is_hit = False

            if self.state == "idle":
                if now - self.last_idle_switch > self.frame_duration:
                    self.idle_frame = (self.idle_frame + 1) % 2
                    self.last_idle_switch = now
            elif self.state == "hit":
                if pygame.time.get_ticks() - self.action_timer > 700:
                    self.state = "idle"


            elif now - self.action_timer > self.action_duration:
                self.x = self.base_x
                self.y = self.base_y
                self.state = "idle"

    def draw(self, screen):
        if self.state == "idle":
            screen.blit(self.images["idle"][self.idle_frame], (self.x, self.y))
        else:
            screen.blit(self.images[self.state], (self.x, self.y))

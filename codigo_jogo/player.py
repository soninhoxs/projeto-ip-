import pygame
from settings import *

# CLASSE DO JOGADOR
class Player:
    def __init__(self, x, y, img_left, img_right, img_front, width, height, speed=7):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_left = img_left
        self.image_right = img_right
        self.image_front = img_front
        self.image = self.image_front
        self.base_speed = speed
        self.speed = speed
        self.hitbox_offset_x = 20
        self.hitbox_offset_y = 20
        self.hitbox_width = self.width - 40
        self.hitbox_height = self.height - 30

        # Variáveis para o pulo
        self.is_jumping = False
        self.y_velocity = 0
        self.gravity = 1
        self.jump_strength = -20
        self.ground_y = y  # Posição inicial no chão

        # Variáveis para lentidão
        self.slowed_timer = 0
        self.SLOWED_DURATION = 300  # 5 segundos

        # Variáveis para o contador de hotdogs
        self.hotdogs_eaten = 0

    def update(self, keys):
        # Lógica para o timer de lentidão
        if self.slowed_timer > 0:
            self.slowed_timer -= 1
            if self.slowed_timer == 0:
                self.speed = self.base_speed  # Voltar a velocidade normal

        # Movimento horizontal
        moved = False
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.x = max(self.x, 0)
            self.image = self.image_left
            moved = True

        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.x = min(self.x, WIDTH - self.width)
            self.image = self.image_right
            moved = True

        # Se o jogador não se moveu horizontalmente, usa a imagem de frente
        if not moved:
            self.image = self.image_front

        # Lógica do pulo
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = self.jump_strength

        # Aplica gravidade se estiver pulando ou no ar
        if self.is_jumping or self.y < self.ground_y:
            self.y += self.y_velocity
            self.y_velocity += self.gravity

        # Checa se o personagem voltou para o chão principal
        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.is_jumping = False
            self.y_velocity = 0

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        if DEBUG_MODE:
            pygame.draw.rect(surface, RED, self.get_rect(), 2)

    def get_rect(self):
        return pygame.Rect(
            self.x + self.hitbox_offset_x,
            self.y + self.hitbox_offset_y,
            self.hitbox_width,
            self.hitbox_height
        )
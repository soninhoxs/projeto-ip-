import pygame
import random
from settings import *

# CLASSE DOS ITENS
class Item:
    def __init__(self, x, y, kind, images):
        self.x = x
        self.y = y
        self.kind = kind
        self.speed = random.randint(3, 6)

        # Associa a imagem correta
        self.image = images[kind]
        self.size = self.image.get_width()

        # Define a hitbox de acordo com o tipo de item
        hitbox_offsets = {
            "burger": (10, 10, self.size - 20, self.size - 20),
            "bomb": (30, 30, 60, 60),
            "hotdog": (10, 10, self.size - 20, self.size - 20),
            "donuts": (10, 10, self.size - 20, self.size - 20)
        }
        self.hitbox_offset_x, self.hitbox_offset_y, self.hitbox_width, self.hitbox_height = hitbox_offsets.get(kind, (
        0, 0, self.size, self.size))

    def fall(self):
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        if DEBUG_MODE:
            color = GREEN if self.kind in ["burger", "donuts"] else YELLOW if self.kind == "bomb" else RED
            pygame.draw.rect(surface, color, self.get_rect(), 2)

    def get_rect(self):
        return pygame.Rect(
            self.x + self.hitbox_offset_x,
            self.y + self.hitbox_offset_y,
            self.hitbox_width,
            self.hitbox_height
        )
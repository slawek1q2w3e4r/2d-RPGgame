import pygame as py
from src.img.images import rescale_image

class Enemy:
    def __init__(self, image_path, x, y, hp=100):
        self.image = rescale_image(image_path, 50, 50)
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp
        self.dead = False

    def draw(self, surface):
        if not self.dead:
            surface.blit(self.image, (self.x, self.y))
            self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        bar_width = 50
        bar_height = 5
        fill = (self.hp / self.max_hp) * bar_width
        outline_rect = py.Rect(self.x, self.y - 10, bar_width, bar_height)
        fill_rect = py.Rect(self.x, self.y - 10, fill, bar_height)

        py.draw.rect(surface, (255, 0, 0), fill_rect)
        py.draw.rect(surface, (255, 255, 255), outline_rect, 1)

    def Update(self):
        pass

    def take_damage(self, amount):
        if self.dead:
            return False  # już martwy

        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.dead = True
            return True
        return False

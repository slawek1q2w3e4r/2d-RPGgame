import pygame as py

class GUI:
    def __init__(self):
        self.font = py.font.SysFont("arial", 24)
        self.health = 100  # zdrowie gracza
        self.max_health = 100
        self.coins = 0     # ilość monet
        self.messages = []  # lista komunikatów (np. "Znalazłeś skrzynię!")

    def set_health(self, amount):
        self.health = max(0, min(self.max_health, amount))

    def add_coins(self, amount):
        self.coins += amount

    def add_message(self, text, duration=2000):
        # Dodaje wiadomość, która znika po czasie
        self.messages.append({
            "text": text,
            "start_time": py.time.get_ticks(),
            "duration": duration
        })

    def draw_health_bar(self, surface, x, y, width=200, height=20):
        health_ratio = self.health / self.max_health
        py.draw.rect(surface, (60, 60, 60), (x, y, width, height))
        py.draw.rect(surface, (255, 0, 0), (x, y, width * health_ratio, height))
        py.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)

    def draw_coins(self, surface, x, y):
        text = self.font.render(f"Monety: {self.coins}", True, (255, 255, 0))
        surface.blit(text, (x, y))

    def draw_messages(self, surface, x, y):
        now = py.time.get_ticks()
        offset = 0
        for msg in self.messages[:]:
            elapsed = now - msg["start_time"]
            if elapsed > msg["duration"]:
                self.messages.remove(msg)
                continue
            alpha = max(0, 255 - int((elapsed / msg["duration"]) * 255))
            text_surface = self.font.render(msg["text"], True, (255, 255, 255))
            text_surface.set_alpha(alpha)
            surface.blit(text_surface, (x, y + offset))
            offset += 30

    def draw(self, surface):
        self.draw_health_bar(surface, 20, 20)
        self.draw_coins(surface, 20, 50)
        self.draw_messages(surface, 20, 80)

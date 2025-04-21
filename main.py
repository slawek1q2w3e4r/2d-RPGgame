import pygame as py
from settings import *
from player import Player, Inventory
from enemy import Enemy
from menu import Menu
from gui import GUI
from map import TileMap
from src.item_db import ItemDatabase
from src.sfx import Sounds

class Game:
    def __init__(self):
        py.init()
        self.clock = py.time.Clock()
        self.window = py.display.set_mode((0, 0), py.FULLSCREEN)
        py.display.set_caption("RPG")
        self.running = True
        self.menu = Menu()
        self.gui = GUI()
        self.sfx = Sounds()
        self.item_db = ItemDatabase()  # Baza itemów (tekstury ładują się przy pobieraniu)

        self.tilemap = TileMap([
            "img/tiles/grass.png"
        ], self.window.get_width(), self.window.get_height())

        self.player = Player("img/player1.png",  400, 300, 100)
        self.inventory = Inventory(self.player)

        # Usuń domyślne equipowanie przedmiotu w __init__
        # jeśli chcesz wyposażyć item, zrób to w metodzie Start lub po kliknięciu w slot

        self.gui.set_health(self.player.hp)

        self.enemies = [
            Enemy("img/enemy1.png", 100, 100),
            Enemy("img/enemy1.png", 300, 200)
        ]

    def Draw(self):
        self.tilemap.draw(self.window)
        self.player.Draw(self.window)

        for enemy in self.enemies:
            if enemy.hp > 0:
                enemy.draw(self.window)

        self.gui.draw(self.window)
        self.inventory.draw(self.window)
        self.menu.draw(self.window)

        py.display.flip()  # aktualizacja ekranu

    def Update(self):
        self.player.Update(self.enemies, self.gui)

    def Handle_Events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False

            elif event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.menu.toggle()

            self.menu.handle_event(event)
            self.inventory.handle_event(event)

    def Start(self):
        self.inventory.add_item(self.item_db.get_item_by_id(1))
        self.sfx.Play_background()

    def Run(self):
        self.Start()
        while self.running:
            self.clock.tick(FPS)
            self.Handle_Events()
            self.Update()
            self.Draw()

        py.quit()

if __name__ == "__main__":
    App = Game()
    App.Run()

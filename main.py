import pygame as py
from settings import *
from player import Player, Inventory
from enemy import Enemy
from menu import Menu
from gui import GUI
from map import TileMap
from src.item_db import ItemDatabase
from game_manager import gameManager
from src.sfx import Sounds
import random

class Game:
    def __init__(self):
        py.init()
        self.clock = py.time.Clock()
        self.window = py.display.set_mode((0, 0), py.FULLSCREEN)
        py.display.set_caption("RPG")
        self.running = True
        self.sfx = Sounds()
        self.game_manager = gameManager()
        self.item_db = ItemDatabase()

        self.tilemap = TileMap([
            "img/tiles/grass.png"
        ], self.window.get_width(), self.window.get_height())

        self.player = Player("img/player1.png",  400, 300, 100)
        self.gui = GUI(self.player)
        self.inventory = Inventory(self.player)

        self.gui.set_health(self.player.hp)
        self.menu = Menu(self.gui, self.inventory, self.player, self.item_db)

        self.screen_width, self.screen_height = py.display.get_surface().get_size()
        self.enemy_count = random.randint(8, 15)
        self.enemies = []
        for _ in range(self.enemy_count):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            enemy = Enemy("img/enemy1.png", x, y)
            self.enemies.append(enemy)

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
        self.inventory.add_item(self.item_db.get_item_by_id(0))
        self.inventory.add_item(self.item_db.get_item_by_id(3))
        self.inventory.add_item(self.item_db.get_item_by_id(1))
        self.player.take_damage(20)
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

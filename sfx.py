import pygame as py

class Sounds:
    def __init__(self):
        py.init()
        py.mixer.init()

    def Play(self, path, name, volume):
        name = py.mixer.Sound(path)
        name.set_volume(volume)
        name.play()

    def Play_background(self):
        py.mixer.music.load("sounds/music.mp3")
        py.mixer.music.set_volume(0.5)  # głośność od 0.0 do 1.0
        py.mixer.music.play(-1)  # -1 = zapętlenie

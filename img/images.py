import pygame as py
import os

def rescale_image(path, target_x, target_y):
    image = py.image.load(path).convert_alpha()
    new_image = py.transform.smoothscale(image, (target_x, target_y))  # <- przypisanie jest kluczowe
    return new_image

class Animation:
    def __init__(self, folder_path, size=(50, 50), frame_delay=5):
        self.frames = []
        self.load_images(folder_path, size)
        self.frame_delay = frame_delay
        self.current_frame = 0
        self.timer = 0
        self.playing = False
        self.done = False

    def load_images(self, folder_path, size):
        files = sorted(os.listdir(folder_path))  # sortuje alfabetycznie
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):  # tylko obrazy
                full_path = os.path.join(folder_path, file)
                img = py.image.load(full_path).convert_alpha()
                img = py.transform.smoothscale(img, size)
                self.frames.append(img)

    def start(self):
        self.playing = True
        self.current_frame = 0
        self.timer = 0
        self.done = False

    def update(self):
        if self.playing:
            self.timer += 1
            if self.timer >= self.frame_delay:
                self.timer = 0
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    self.current_frame = len(self.frames) - 1
                    self.playing = False
                    self.done = True

    def draw(self, surface, pos, flip=False):
        if self.frames:
            image = self.frames[self.current_frame]
            if flip:
                image = py.transform.flip(image, True, False)
            rect = image.get_rect(center=pos)
            surface.blit(image, rect)

    def is_done(self):
        return self.done



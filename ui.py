# src/ui.py
import pygame as py

class ContextMenu:
    PADDING = 5

    def __init__(self):
        # Upewnij się, że fonty są zainicjowane
        if not py.font.get_init():
            py.font.init()
        # Tworzymy font dopiero teraz
        self.font = py.font.SysFont('arial', 18)

        self.options = []   # lista (tekst, callback)
        self.visible = False
        self.x = self.y = 0
        self.width = self.height = 0

    def show(self, x, y, options):
        self.options = options
        self.x, self.y = x, y
        sizes = [self.font.size(text) for text, _ in options]
        self.width  = max(w for w, h in sizes) + self.PADDING*2
        self.height = sum(h for w, h in sizes) + self.PADDING*(len(options)+1)
        self.visible = True

    def hide(self):
        self.visible = False

    def handle_event(self, event):
        if not self.visible:
            return
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            # klik wewnątrz menu?
            if self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height:
                offset = self.y + self.PADDING
                for text, callback in self.options:
                    text_w, text_h = self.font.size(text)
                    if offset <= my <= offset + text_h:
                        callback()
                        break
                    offset += text_h + self.PADDING
            # po kliknięciu chowamy menu
            self.hide()

    def draw(self, surface):
        if not self.visible:
            return
        # tło
        bg = py.Rect(self.x, self.y, self.width, self.height)
        py.draw.rect(surface, (50,50,50), bg)
        # tekst opcji
        offset = self.y + self.PADDING
        for text, _ in self.options:
            surface.blit(self.font.render(text, True, (255,255,255)), (self.x + self.PADDING, offset))
            offset += self.font.get_height() + self.PADDING

import pygame as py

class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = py.Rect(x, y, width, height)
        self.color = (50, 50, 50)
        self.hover_color = (70, 70, 70)
        self.text_color = (255, 255, 255)
        self.font = py.font.SysFont("arial", 24)
        self.callback = callback

    def draw(self, surface):
        mouse_pos = py.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        py.draw.rect(surface, self.hover_color if is_hovered else self.color, self.rect)
        py.draw.rect(surface, (200, 200, 200), self.rect, 2)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


class Menu:
    def __init__(self):
        self.active = False
        self.state = "main"  # może być 'main' albo 'settings'
        self.buttons = []

        self.create_main_buttons()

    def create_main_buttons(self):
        self.buttons = []
        start_y = 20
        button_height = 40
        spacing = 10

        def open_settings():
            self.state = "settings"
            self.create_settings_buttons()

        def exit_game():
            py.event.post(py.event.Event(py.QUIT))

        def close_menu():
            self.toggle()

        self.buttons = [
            Button("Ustawienia", 20, start_y + 0 * (button_height + spacing), 160, button_height, open_settings),
            Button("Wyjście",    20, start_y + 1 * (button_height + spacing), 160, button_height, exit_game),
            Button("Powrót",     20, start_y + 2 * (button_height + spacing), 160, button_height, close_menu)
        ]

    def create_settings_buttons(self):
        self.buttons = []
        start_y = 20
        button_height = 40
        spacing = 10

        def back_to_main():
            self.state = "main"
            self.create_main_buttons()

        def dummy_setting():
            print("Kliknięto opcję ustawień (np. dźwięk).")

        self.buttons = [
            Button("Opcja 1",  20, start_y + 0 * (button_height + spacing), 160, button_height, dummy_setting),
            Button("Opcja 2",  20, start_y + 1 * (button_height + spacing), 160, button_height, dummy_setting),
            Button("Powrót",   20, start_y + 2 * (button_height + spacing), 160, button_height, back_to_main)
        ]

    def toggle(self):
        self.active = not self.active
        if self.active:
            self.state = "main"
            self.create_main_buttons()

    def draw(self, surface):
        if not self.active:
            return

        menu_rect = py.Rect(10, 10, 180, len(self.buttons) * 50 + 20)
        py.draw.rect(surface, (30, 30, 30), menu_rect, border_radius=8)
        py.draw.rect(surface, (200, 200, 200), menu_rect, 2, border_radius=8)

        for button in self.buttons:
            button.draw(surface)

    def handle_event(self, event):
        if not self.active:
            return
        for button in self.buttons:
            button.handle_event(event)

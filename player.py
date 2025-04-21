import pygame as py
from src.img.images import rescale_image, Animation
from ui import ContextMenu
from settings import *
from sfx import Sounds


class Player:
    def __init__(self, image_dir, x, y, health):
        self.original_image = rescale_image(image_dir, 50, 50)
        self.image = self.original_image
        self.x = x
        self.y = y
        self.player_speed = 10
        self.max_speed = 4
        self.direction = py.Vector2(0, 0)
        self.sprinting = False
        self.hp = health
        self.equipped_item = None  # Brak domyślnego miecza
        self.sword_anim = None
        self.sfx = Sounds()

        self.attack_range = py.Rect(0, 0, 60, 60)
        self.attack_cooldown = 500  # ms
        self.last_attack_time = 0

        self.facing_right = True
        self.offsets = {
            "right": (26, 22),
            "left": (26, 22)
        }

    def equip_item(self, item):
        """
        Zakłada przedmiot na gracza.
        item: obiekt z atrybutem anim_folder_path i dmg, lub None żeby zdjąć
        """
        self.equipped_item = item

        if item and item.anim_folder_path:
            self.sword_anim = Animation(item.anim_folder_path, size=(50, 50))
        else:
            self.sword_anim = None

    def unequip_item(self):
        self.equip_item(None)

    def Move(self):
        keys = py.key.get_pressed()

        if keys[py.K_a]:
            self.x -= self.player_speed
            self.facing_right = False
        if keys[py.K_d]:
            self.x += self.player_speed
            self.facing_right = True
        if keys[py.K_w]:
            self.y -= self.player_speed
        if keys[py.K_s]:
            self.y += self.player_speed

        self.max_speed = 6 if keys[py.K_LSHIFT] else 4
        self.player_speed = self.max_speed

        self.image = self.original_image if self.facing_right else py.transform.flip(self.original_image, True, False)

    def Draw(self, surface):
        # Rysuj gracza
        surface.blit(self.image, (self.x, self.y))

        # Jeżeli mamy wyposażony przedmiot, rysujemy animację ataku
        if self.equipped_item and self.sword_anim:
            direction = "right" if self.facing_right else "left"
            offset_x, offset_y = self.offsets[direction]
            sword_pos = (self.x + offset_x, self.y + offset_y)

            if self.sword_anim.playing:
                # rysuj kolejną klatkę animacji
                self.sword_anim.draw(surface, sword_pos, flip=not self.facing_right)
            else:
                # pokaż statyczną pierwszą klatkę
                frame = self.sword_anim.frames[0]
                if not self.facing_right:
                    frame = py.transform.flip(frame, True, False)
                rect = frame.get_rect(center=sword_pos)
                surface.blit(frame, rect)

    def Update(self, enemies, gui):
        self.Move()
        if self.sword_anim:
            self.sword_anim.update()
        self.Attack(enemies, gui)

    def Attack(self, enemies, gui=None):
        if not (self.equipped_item and self.sword_anim):
            return  # nic się nie dzieje bez wyposażonego itemu

        current_time = py.time.get_ticks()
        if py.mouse.get_pressed()[
            0] and not self.sword_anim.playing and current_time - self.last_attack_time >= self.attack_cooldown:
            self.sword_anim.start()
            self.sfx.Play("sounds/sword-sound.mp3", "sword-sound", 0.25)
            self.last_attack_time = current_time

            width, height = 40, 40
            offset_y = 22

            if self.facing_right:
                attack_rect = py.Rect(self.x + 50, self.y + offset_y, width, height)
            else:
                attack_rect = py.Rect(self.x - width, self.y + offset_y, width, height)

            weapon_dmg = self.equipped_item.dmg

            for enemy in enemies:
                if enemy.dead:
                    continue
                enemy_rect = py.Rect(enemy.x, enemy.y, 50, 50)
                if attack_rect.colliderect(enemy_rect):
                    if enemy.take_damage(weapon_dmg):
                        self.sfx.Play("sounds/enemy-dead.mp3", "enemy-dead", 0.25)
                        if gui:
                            gui.add_coins(5)
                            gui.add_message("Zabiłeś przeciwnika! +5 monet")

    def get_hp(self):
        return self.hp


class Slot:
    def __init__(self, x, y, size=64):
        self.rect = py.Rect(x, y, size, size)
        self.item = None

    def draw(self, screen):
        py.draw.rect(screen, (100, 100, 100), self.rect, 2)
        if self.item and self.item.texture:
            screen.blit(self.item.texture, self.rect)


class Inventory:
    def __init__(self, player):
        self.player = player
        self.slots = []
        self.visible = False

        # Context menu do prawego‑kliku
        self.context_menu = ContextMenu()

        # Ustawienia siatki slotów
        slot_size = 64
        padding = 10
        cols, rows = 4, 3

        # Wyśrodkowanie na ekranie
        screen_w, screen_h = py.display.get_surface().get_size()
        total_w = cols * slot_size + (cols - 1) * padding
        total_h = rows * slot_size + (rows - 1) * padding
        start_x = (screen_w - total_w) // 2
        start_y = (screen_h - total_h) // 2

        # Stwórz puste sloty
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (slot_size + padding)
                y = start_y + row * (slot_size + padding)
                self.slots.append(Slot(x, y, slot_size))

    def add_item(self, item):
        """Dodaje przedmiot do pierwszego wolnego slotu."""
        for slot in self.slots:
            if slot.item is None:
                slot.item = item
                return True
        return False

    def handle_event(self, event):
        # przełącz widoczność inventarza (lewy przycisk)
        if event.type == py.KEYDOWN and event.key == py.K_i:
            self.visible = not self.visible
            self.context_menu.hide()

        # w Inventory.handle_event (poza left‑click equip) dodaj obsługę prawego:
        if self.visible and event.type == py.MOUSEBUTTONDOWN and event.button == 3:
            for slot in self.slots:
                if slot.rect.collidepoint(event.pos) and slot.item:
                    item = slot.item
                    opts = []
                    # jedzenie
                    if item.heal > 0:
                        def eat_it(slot=slot, item=item):
                            self.player.hp = min(self.player.hp + item.heal, MAX_HEALTH)
                            slot.item = None

                        opts.append((f"Zjedz (+{item.heal} HP)", eat_it))
                    # broń / dmg
                    if item.dmg > 0:
                        # jeśli już to w ręku → odłóż
                        if self.player.equipped_item == item:
                            opts.append(("Odłóż", self.player.unequip_item))
                        else:
                            def equip_it(item=item):
                                self.player.equip_item(item)

                            opts.append(("Wyposaż", equip_it))
                    # pokaż menu pod myszką
                    mx, my = event.pos
                    self.context_menu.show(mx, my, opts)
                    break

        # przekaż event do menu
        self.context_menu.handle_event(event)

    def draw(self, screen):
        if not self.visible:
            return
        for slot in self.slots:
            slot.draw(screen)
        # narysuj menu na wierzchu
        self.context_menu.draw(screen)

from src.img.images import rescale_image

class Item:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        texture_path: str = None,
        dmg: int = 0,
        heal: int = 0,
        feed: int = 0,
        anim_folder_path: str = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.texture_path = texture_path
        self.dmg = dmg
        self.heal = heal
        self.feed = feed
        self.anim_folder_path = anim_folder_path
        self.texture = None  # zostanie załadowane później

    def load_texture(self):
        """
        Ładuje i przeskalowuje teksturę, jeśli jeszcze nie została załadowana.
        Wywołuj po inicjalizacji pygame i utworzeniu okna.
        """
        if self.texture is None and self.texture_path:
            self.texture = rescale_image(self.texture_path, 64, 64)
        return self.texture

class ItemDatabase:
    """
    Baza przedmiotów. Inicjalizuje się po uruchomieniu pygame.
    """
    def __init__(self):
        # Przykładowe przedmioty tworzymy dopiero tutaj
        self.items = [
            Item(
                id=1,
                name="Iron Sword",
                description="Sharp iron blade",
                texture_path="img/sword_eq_1.png",
                dmg=10,
                heal=0,
                feed=0,
                anim_folder_path="img/animations/sword/",
            ),
            Item(
                id=2,
                name="Healing Potion",
                description="Restores health",
                texture_path="img/potion_heal.png",
                dmg=0,
                heal=20,
                feed=5,
                anim_folder_path=None,
            ),
            # ... kolejne przedmioty
        ]

    def get_item_by_id(self, item_id: int) -> Item:
        """
        Zwraca instancję Item o podanym ID lub None.
        """
        for item in self.items:
            if item.id == item_id:
                # upewnij się, że tekstura jest załadowana
                item.load_texture()
                return item
        return None

    def get_item_by_name(self, name: str) -> Item:
        """
        Zwraca instancję Item o podanej nazwie (małe/duże litery ignorowane) lub None.
        """
        for item in self.items:
            if item.name.lower() == name.lower():
                item.load_texture()
                return item
        return None

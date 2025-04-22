from src.img.images import rescale_image

class Item:
    def __init__(
        self,
        id: int,
        name: str,
        rarity: str,
        description: str,
        texture_path: str = None,
        dmg: int = 0,
        heal: int = 0,
        feed: int = 0,
        anim_folder_path: str = None,
        price: int = 0,
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
        self.price = price

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
                0,
                "Iron Sword",
                "Uncommon",
                "Sharp iron blade",
                "img/sword_eq_1.png",
                10,
                0,
                0,
                "img/animations/sword/",
                10,
            ),
            Item(
                1,
                "Healing Potion",
                "rare",
                "Restores health",
                None,
                0,
                20,
                5,
                None,
                10,
            ),
            Item(
                2,
                "bread",
                "common",
                "dry but nutritious bread",
                None,
                0,
                5,
                20,
                None,
                2,
            ),
            Item(
                3,
                "Golem Sword",
                "Legendary",
                "Very Sharp Sword from Golems",
                "img/sword_eq_1.png",
                30,
                0,
                0,
                "img/animations/sword/",
                100,
            ),
            Item(
                4,
                "Flame Dagger",
                "Epic",
                "A dagger imbued with eternal flame.",
                None,
                20,  # dmg
                0,  # heal
                0,  # feed
                None,
                80,
            ),

            Item(
                5,
                "Guardian Shield",
                "Rare",
                "A sturdy shield made by mountain guardians.",
                None,
                0,
                0,
                0,
                None,
                50,
            ),

            Item(
                6,
                "Healing Staff",
                "Uncommon",
                "A staff that heals its wielder.",
                None,
                5,
                20,
                0,
                None,
                40,
            ),

            Item(
                7,
                "Thunder Axe",
                "Legendary",
                "An axe crackling with the power of storms.",
                None,
                35,
                0,
                0,
                None,
                150,
            ),

            Item(
                8,
                "Shadow Cloak",
                "Epic",
                "Makes the wearer harder to hit. (20% chance to hti)",
                None,
                0,
                0,
                0,
                None,
                200,
            ),

            Item(
                9,
                "Vampire Fang",
                "Rare",
                "Steals a bit of enemy life on hit.",
                None,
                15,
                5,
                0,
                None,
                150,
            ),

            Item(
                10,
                "Frozen Lance",
                "Epic",
                "A weapon forged in the coldest peaks.",
                None,
                25,
                0,
                0,
                None,
                100,
            ),

            Item(
                11,
                "Crystal Helm",
                "Uncommon",
                "A helm made of pure enchanted crystal.",
                None,
                0,
                0,
                0,
                None,
                150,
            ),

            Item(
                12,
                "Phoenix Feather",
                "Legendary",
                "Revives the user once after death.",
                None,
                0,
                50,
                0,
                None,
                300,
            ),
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

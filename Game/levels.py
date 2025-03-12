"""
    Jhon Oliver Castillo Caraballo
    22-SISN-2-063
"""

from enum import Enum
from Utils.assets import ASSETS


class TileType(Enum):
    """
    Enumeración de los tipos de bloques en el juego.
    """
    EMPTY = 0      # Espacio vacío (aire)
    BRICK = 1      # Bloques de plataforma sólida
    LADDER = 2     # Para subir/bajar
    GOLD = 3       # Objetos coleccionables
    EXIT = 4       # Salida del nivel (inicialmente cerrada)
    EXIT_OPEN = 5  # Salida abierta (cuando todo el oro es recolectado)
    DIGGABLE = 6   # Bloques que se pueden cavar temporalmente
    BASE = 7  # Plataforma base


class Level:
    """
    Clase que representa un nivel del juego.
    """

    def __init__(self, level):
        self.level_number = level
        self.map = []
        self.gold = 0  # This is initialized to 0 but should be explicitly reset before counting
        self.exit = (0, 0)  # Default value
        self.player = None
        self.enemies = []
        self.ladders = []
        self.ropes = []
        self.diggables = []
        self.brick = []
        self.base = []
        self.load_level()

    # Mapeo de los elementos del nivel
    TILE_ASSETS = {
        TileType.EMPTY: None,
        TileType.BRICK: ASSETS.TILE.value,
        TileType.LADDER: ASSETS.LADDER.value,
        TileType.GOLD: ASSETS.COIN.value,
        TileType.EXIT: ASSETS.CLOSED_DOOR.value,
        TileType.EXIT_OPEN: ASSETS.EXIT.value,
        TileType.DIGGABLE: ASSETS.TILE.value,
        TileType.BASE: ASSETS.BASE._value_,
    }

    def load_level(self):
        # Nivel 1
        GRID_BASE = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 1, 1, 1, 1, 3, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 6, 6, 6, 1, 2, 1, 6, 6, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 0, 0, 0],
            [0, 0, 1, 2, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 0],
            [0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 2, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
        ]

        self.map = GRID_BASE

        # Reset counters before processing the map
        self.gold = 0
        self.ladders = []
        self.ropes = []
        self.diggables = []
        self.brick = []

        # Procesa el mapa para obtener las posiciones de los elementos
        for row_idx, row in enumerate(self.map):
            for col_idx, tile in enumerate(row):
                position = (col_idx, row_idx)  # Se guarda la posición actual
                if tile == TileType.EMPTY.value:
                    continue
                if tile == TileType.BRICK.value:
                    self.brick.append(position)
                elif tile == TileType.LADDER.value:
                    self.ladders.append(position)
                elif tile == TileType.GOLD.value:
                    self.gold += 1
                elif tile == TileType.EXIT.value:
                    self.exit = position
                elif tile == TileType.DIGGABLE.value:
                    self.diggables.append(position)
                elif tile == TileType.BASE.value:
                    self.base.append(position)

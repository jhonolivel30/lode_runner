"""
    Jhon Oliver Castillo Caraballo
    22-SISN-2-063
"""

import pygame as pg
from Utils.constants import CONSTANTS
from Utils.assets import ASSETS
from Game.levels import Level, TileType


class Map:
    def __init__(self, level_number=1):
        self.tile_size = CONSTANTS.TILE_SIZE.value
        # Cálculo de dimensiones del grid basado en las constantes de ventana
        self.grid_width = CONSTANTS.WINDOW_SIZE.value[0] // self.tile_size
        self.grid_height = CONSTANTS.WINDOW_SIZE.value[1] // self.tile_size

        # Add width and height properties for Enemy class to use
        self.width = self.grid_width
        self.height = self.grid_height

        self.scale = CONSTANTS.WINDOW_SCALE.value
        self.grid = []
        self.total_gold = 0
        self.collected_gold = 0
        self.exit_pos = (0, 0)
        # Rastrea bloques cavados temporalmente {(x,y): temporizador}
        self.digging_blocks = {}
        # Añadir propiedad para controlar si la salida está abierta
        self.exit_open = False

        # Cargar el fondo del juego
        try:
            self.background = pg.image.load(str(ASSETS.GAME_BACKGROUND.value))
            self.background = pg.transform.scale(
                self.background, CONSTANTS.WINDOW_SIZE.value)
        except Exception as e:
            print(f"Error al cargar el fondo: {e}")
            self.background = None

        # Cargar imágenes para los tiles
        self.tile_images = self.load_tile_images()

        # Cargar nivel desde la clase Level
        self.current_level = Level(level_number)
        self.load_from_level(self.current_level)

    def load_tile_images(self):
        """Cargar y escalar las imágenes de los tiles"""
        scaled_size = int(self.tile_size * self.scale)
        tile_images = {}

        for tile_type, asset_path in Level.TILE_ASSETS.items():
            if asset_path is not None:  # Skip empty tile
                try:
                    # Load the image from the path
                    image = pg.image.load(str(asset_path))
                    # Scale the image to match our tile size
                    image = pg.transform.scale(
                        image, (scaled_size, scaled_size))
                    tile_images[tile_type] = image
                except Exception as e:
                    print(f"Error loading image {asset_path}: {e}")
                    # Use a colored rectangle as fallback
                    tile_images[tile_type] = None
            else:
                tile_images[tile_type] = None

        return tile_images

    def load_from_level(self, level):
        """Cargar datos del mapa desde un objeto Level"""
        self.grid = []
        self.total_gold = level.gold
        self.collected_gold = 0
        self.exit_pos = level.exit

        # Add debug information to verify gold count
        gold_positions = []
        for row_idx, row in enumerate(level.map):
            for col_idx, tile in enumerate(row):
                if tile == TileType.GOLD.value:
                    gold_positions.append((col_idx, row_idx))

        # Convertir el mapa del nivel a nuestro formato de grid con valores enum de TileType apropiados
        for row in level.map:
            grid_row = []
            for tile_value in row:
                grid_row.append(TileType(tile_value))
            self.grid.append(grid_row)

        # Update width and height based on the actual grid dimensions
        if self.grid:
            self.height = len(self.grid)
            self.width = len(self.grid[0]) if self.grid[0] else 0

    def load_level(self, level_number):
        """Cargar un nuevo nivel por su número"""
        self.current_level = Level(level_number)
        self.load_from_level(self.current_level)

    def get_tile(self, x, y):
        """Obtener tipo de casilla en coordenadas de grid"""
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            return self.grid[y][x]
        return TileType.EMPTY  # Devolver vacío para posiciones fuera de límites

    def set_tile(self, x, y, tile_type):
        """Establecer tipo de casilla en coordenadas de grid"""
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            self.grid[y][x] = tile_type

    def collect_gold(self, x, y):
        """Intentar recoger oro en la posición especificada"""
        if self.get_tile(x, y) == TileType.GOLD:
            self.set_tile(x, y, TileType.EMPTY)
            self.collected_gold += 1

            # Si todo el oro ha sido recogido, abrir la salida
            if self.collected_gold >= self.total_gold:
                self.open_exit()

            return True
        return False

    def open_exit(self):
        """Abrir la salida cuando todo el oro ha sido recogido"""
        x, y = self.exit_pos
        self.set_tile(x, y, TileType.EXIT_OPEN)
        self.exit_open = True  # Actualizar la propiedad exit_open
        print("Exit opened at position:", self.exit_pos)  # Para depurar

    def dig(self, x, y):
        """Cavar en la posición especificada si es un bloque excavable"""
        if self.get_tile(x, y) == TileType.DIGGABLE:
            self.set_tile(x, y, TileType.EMPTY)
            self.digging_blocks[(x, y)] = 100  # Temporizador para 100 frames
            return True
        return False

    def update(self):
        """Actualizar estado del mapa (restaurar bloques cavados, etc.)"""
        keys_to_remove = []

        for pos, timer in self.digging_blocks.items():
            if timer <= 0:
                x, y = pos
                self.set_tile(x, y, TileType.DIGGABLE)
                keys_to_remove.append(pos)
            else:
                self.digging_blocks[pos] -= 1

        for key in keys_to_remove:
            del self.digging_blocks[key]

    def draw(self, surface):
        """Dibujar el mapa en la superficie proporcionada"""
        scaled_tile_size = int(self.tile_size * self.scale)

        # Dibujar el fondo primero
        if self.background:
            surface.blit(self.background, (0, 0))

        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile != TileType.EMPTY:
                    rect = pg.Rect(
                        int(x * scaled_tile_size),
                        int(y * scaled_tile_size),
                        scaled_tile_size,
                        scaled_tile_size
                    )

                    # If we have an image for this tile type, use it
                    if self.tile_images.get(tile) is not None:
                        surface.blit(self.tile_images[tile], rect)
                    else:
                        # Fallback to colored rectangles if image is missing
                        if tile == TileType.BRICK:
                            pg.draw.rect(
                                surface, CONSTANTS.COLOR_BROWN.value, rect)
                        elif tile == TileType.LADDER:
                            pg.draw.rect(
                                surface, CONSTANTS.COLOR_RED.value, rect)
                        elif tile == TileType.GOLD:
                            pg.draw.rect(
                                surface, CONSTANTS.COLOR_YELLOW.value, rect)
                        elif tile == TileType.EXIT or tile == TileType.EXIT_OPEN:
                            pg.draw.rect(
                                surface, CONSTANTS.COLOR_GREEN.value, rect)
                        elif tile == TileType.DIGGABLE:
                            pg.draw.rect(
                                surface, CONSTANTS.COLOR_GRAY.value, rect)

    def is_solid(self, x, y):
        """Comprobar si la casilla en (x,y) es sólida (no se puede atravesar)"""
        tile = self.get_tile(x, y)
        return tile in (TileType.BRICK, TileType.DIGGABLE, TileType.BRICK)

    def can_stand_on(self, x, y):
        """Comprobar si un personaje puede pararse en esta casilla"""
        # Verificar límites del mapa
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        # Si estamos en una escalera, podemos pararnos
        if self.get_tile(x, y) == TileType.LADDER:
            return True

        # Verificar si hay soporte debajo
        if y + 1 >= self.height:
            return True  # Base del mapa

        tile_below = self.get_tile(x, y + 1)
        return tile_below in (TileType.BRICK, TileType.DIGGABLE, TileType.BASE)

    def can_climb(self, x, y, direction=0):
        """
        Comprobar si un personaje puede escalar en esta posición
        direction: 0 para mantener posición, 1 para subir, -1 para bajar
        """
        # Verificar límites del mapa
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        current_tile = self.get_tile(x, y)

        # Si estamos en una escalera, podemos escalar
        if current_tile == TileType.LADDER:
            # Si estamos intentando bajar, verificar si hay un bloque sólido debajo
            if direction < 0:  # Intentando bajar
                tile_below = self.get_tile(x, y + 1)
                if tile_below in (TileType.BASE, TileType.DIGGABLE, TileType.BRICK):
                    # Hay un bloque sólido debajo, no podemos seguir bajando
                    return False
            return True

        return False

    def is_exit_open(self):
        """Comprobar si la salida está abierta"""
        x, y = self.exit_pos
        return self.get_tile(x, y) == TileType.EXIT_OPEN and self.exit_open

    def is_player_at_exit(self, player_pos):
        """Comprobar si el jugador está en la posición de la salida"""
        x, y = player_pos
        return (x, y) == self.exit_pos and self.is_exit_open()

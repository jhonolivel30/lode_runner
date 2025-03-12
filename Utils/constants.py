"""
    Jhon Oliver Castillo Caraballo
    22-SISN-2-063
"""

from enum import Enum
import pygame as pg
from pathlib import Path
import pygame_menu as pg_menu

# Ruta raíz
ROOT_PATH = Path(__file__).parent.parent
ROOT_STR_PATH = str(Path(__file__).parent.parent)

# Inicializar pygame
pg.display.init()
INFO = pg.display.Info()


class Direction(Enum):
    FRONT = 1
    BACK = 2
    LEFT = 3
    RIGHT = 4


class CONSTANTS(Enum):

    WINDOW_SCALE = 1.00
    TILE_SIZE = int(INFO.current_h * 0.06)
    WINDOW_SIZE = (20 * TILE_SIZE, 14 * TILE_SIZE)
    FPS = 60
    # Usado para mantener la relación de aspecto
    ASPECT_RATIO = WINDOW_SIZE[0] / WINDOW_SIZE[1]

    # Colores
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_GOLD = (255, 215, 0)  # Color temático para Lode Runner
    COLOR_BROWN = (139, 69, 19)  # Color secundario
    COLOR_RED = (220, 20, 60)    # Color para destacados
    COLOR_ORANGE = (255, 140, 0)  # Color para elementos interactivos
    TRANSPARENT_COLOR = (0, 0, 0, 0)
    COLOR_YELLOW = (255, 255, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (0, 0, 255)
    COLOR_GRAY = (128, 128, 128)
    COLOR_LIGHT_GRAY = (200, 200, 200)
    COLOR_DARK_GRAY = (100, 100, 100)
    COLOR_PURPLE = (128, 0, 128)
    COLOR_CYAN = (0, 255, 255)
    COLOR_PINK = (255, 192, 203)
    COLOR_LIME = (0, 255, 0)
    COLOR_MAGENTA = (255, 0, 255)
    COLOR_TEAL = (0, 128, 128)
    COLOR_NAVY = (0, 0, 128)

    # Configuración de fuentes
    # Fuente retro tipo pixel
    MENU_FONT = pg_menu.font.FONT_FIRACODE
    MENU_FONT_SIZE = 20  # Aumentado para mejor legibilidad
    TITLE_FONT_SIZE = 36  # Aumentado para mayor impacto visual
    SUBTITLE_FONT_SIZE = 24  # Aumentado para jerarquía visual

    # Efectos visuales
    MENU_SHADOW_OFFSET = 2
    BUTTON_PADDING = 25  # Aumentado para botones más cómodos
    BUTTON_BORDER_RADIUS = 8  # Ajustado para un estilo más uniforme

    # * Extras
    ASSETS_PATH = ROOT_PATH / 'assets'

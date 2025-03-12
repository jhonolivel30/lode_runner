"""
    Jhon Oliver Castillo Caraballo
    22-SISN-2-063
"""

from enum import Enum
from pathlib import Path
from Utils.constants import CONSTANTS


class ASSETS(Enum):
    '''
    Todas las constantes de los assets utilizados en el juego
    '''

    # Referencia al directorio de assets
    ASSETS_DIR = CONSTANTS.ASSETS_PATH.value

    # Images
    MENU_BACKGROUND = ASSETS_DIR / "Graphics" / "screenshot3.jpg"

    GAME_BACKGROUND = ASSETS_DIR / "Graphics" / "world1" / "world1_0.bmp"
    TILE = ASSETS_DIR / "Graphics" / "world1" / "block1_0.bmp"
    BRICK = ASSETS_DIR / "Graphics" / "world1" / "block2_0.bmp"
    STEEL = ASSETS_DIR / "Graphics" / "world1" / "block3_0.bmp"
    COIN = ASSETS_DIR / "Graphics" / "block8_0.bmp"
    LADDER = ASSETS_DIR / "Graphics" / "world1" / "block10_0.bmp"
    CLOSED_DOOR = ASSETS_DIR / "Graphics" / "world1" / "block5_0.bmp"
    EXIT = ASSETS_DIR / "Graphics" / "world1" / "block6_0.bmp"
    BASE = ASSETS_DIR / "Graphics" / "world1" / "block2_0.bmp"

    escaleras1 = ASSETS_DIR / "Graphics" / "world1" / "block9_0.bmp"
    escaleras2 = ASSETS_DIR / "Graphics" / "world1" / "block10_0.bmp"

    # Player movements with paths
    PLAYER_LEFT_1 = ASSETS_DIR / "Graphics" / "block29_11.bmp"
    PLAYER_LEFT_2 = ASSETS_DIR / "Graphics" / "block29_12.bmp"
    PLAYER_LEFT_3 = ASSETS_DIR / "Graphics" / "block29_13.bmp"
    PLAYER_LEFT_4 = ASSETS_DIR / "Graphics" / "block29_14.bmp"
    PLAYER_LEFT_5 = ASSETS_DIR / "Graphics" / "block29_15.bmp"
    PLAYER_LEFT_6 = ASSETS_DIR / "Graphics" / "block29_16.bmp"

    PLAYER_UP_FRENTE_1 = ASSETS_DIR / "Graphics" / "block29_21.bmp"
    PLAYER_UP_FRENTE_2 = ASSETS_DIR / "Graphics" / "block29_22.bmp"
    PLAYER_UP_FRENTE_3 = ASSETS_DIR / "Graphics" / "block29_23.bmp"

    PLAYER_DOWN_ESPALDA_1 = ASSETS_DIR / "Graphics" / "block29_24.bmp"
    PLAYER_DOWN_ESPALDA_2 = ASSETS_DIR / "Graphics" / "block29_25.bmp"
    PLAYER_DOWN_ESPALDA_3 = ASSETS_DIR / "Graphics" / "block29_26.bmp"

    PLAYER_RIGHT_1 = ASSETS_DIR / "Graphics" / "block29_1.bmp"
    PLAYER_RIGHT_2 = ASSETS_DIR / "Graphics" / "block29_2.bmp"
    PLAYER_RIGHT_3 = ASSETS_DIR / "Graphics" / "block29_3.bmp"
    PLAYER_RIGHT_4 = ASSETS_DIR / "Graphics" / "block29_4.bmp"
    PLAYER_RIGHT_5 = ASSETS_DIR / "Graphics" / "block29_5.bmp"
    PLAYER_RIGHT_6 = ASSETS_DIR / "Graphics" / "block29_6.bmp"

    # Enemy movements with paths
    ENEMY_LEFT_1 = ASSETS_DIR / "Graphics" / "block31_7.bmp"
    ENEMY_LEFT_2 = ASSETS_DIR / "Graphics" / "block31_8.bmp"
    ENEMY_LEFT_3 = ASSETS_DIR / "Graphics" / "block31_9.bmp"
    ENEMY_LEFT_4 = ASSETS_DIR / "Graphics" / "block31_10.bmp"

    ENEMY_RIGHT_1 = ASSETS_DIR / "Graphics" / "block31_0.bmp"
    ENEMY_RIGHT_2 = ASSETS_DIR / "Graphics" / "block31_1.bmp"
    ENEMY_RIGHT_3 = ASSETS_DIR / "Graphics" / "block31_2.bmp"
    ENEMY_RIGHT_4 = ASSETS_DIR / "Graphics" / "block31_3.bmp"
    ENEMY_RIGHT_5 = ASSETS_DIR / "Graphics" / "block31_4.bmp"
    ENEMY_RIGHT_6 = ASSETS_DIR / "Graphics" / "block31_5.bmp"
    ENEMY_RIGHT_7 = ASSETS_DIR / "Graphics" / "block31_6.bmp"

    ENEMY_UP_ESPALDA_1 = ASSETS_DIR / "Graphics" / "block31_14.bmp"
    ENEMY_UP_ESPALDA_2 = ASSETS_DIR / "Graphics" / "block31_15.bmp"
    ENEMY_UP_ESPALDA_3 = ASSETS_DIR / "Graphics" / "block31_16.bmp"
    ENEMY_UP_ESPALDA_4 = ASSETS_DIR / "Graphics" / "block31_17.bmp"
    ENEMY_UP_ESPALDA_5 = ASSETS_DIR / "Graphics" / "block31_18.bmp"
    ENEMY_UP_ESPALDA_6 = ASSETS_DIR / "Graphics" / "block31_19.bmp"
    ENEMY_UP_ESPALDA_7 = ASSETS_DIR / "Graphics" / "block31_20.bmp"

    ENEMY_DOWN_FRENTE_1 = ASSETS_DIR / "Graphics" / "block31_21.bmp"
    ENEMY_DOWN_FRENTE_2 = ASSETS_DIR / "Graphics" / "block31_22.bmp"
    ENEMY_DOWN_FRENTE_3 = ASSETS_DIR / "Graphics" / "block31_23.bmp"
    ENEMY_DOWN_FRENTE_4 = ASSETS_DIR / "Graphics" / "block31_24.bmp"
    ENEMY_DOWN_FRENTE_5 = ASSETS_DIR / "Graphics" / "block31_25.bmp"
    ENEMY_DOWN_FRENTE_6 = ASSETS_DIR / "Graphics" / "block31_26.bmp"

    # Sounds
    BACKGROUND_MUSIC = ASSETS_DIR / "music" / "01_Title_Screen.mp3"
    STAGE_START_SOUND = ASSETS_DIR / "music" / "02_Stage_Start.mp3"
    MAIN_BACKGROUND_MUSIC = ASSETS_DIR / "music" / "03_Main_BGM.mp3"
    ALL_GOLD_COLLECTED_SOUND = ASSETS_DIR / "music" / "04_All_Gold_Collected.mp3"
    STAGE_CLEAR_SOUND = ASSETS_DIR / "music" / "05_Stage_Clear.mp3"
    STAGE_MISS_SOUND = ASSETS_DIR / "music" / "06_Miss.mp3"
    GAME_OVER_SOUND = ASSETS_DIR / "music" / "07_Game_Over.mp3"
    # SELECTION_SOUND = ASSETS_DIR / "music" / "selection.wav"
    # CLICK_SOUND = ASSETS_DIR / "music" / "click.wav"

"""
    Jhon Oliver Castillo Caraballo
    22-SISN-2-063
"""

from enum import Enum


class STRINGS(Enum):
    GAME_TITLE = "Lode Runner"
    START_BUTTON = "Iniciar Juego"
    BRIEFING_BUTTON = "Instrucciones"
    RETREAT_BUTTON = "Salir"
    RETURN_BUTTON = "Volver"

    BRIEFING_TITLE = "Cómo Jugar"
    CONTROLS_HEADER = "Controles"
    MOVEMENT_CONTROLS = "Flechas: Mover y trepar"
    FIRE_CONTROLS = "Z/X: Cavar izquierda/derecha"

    # Nuevos textos para enriquecer el menú
    GAME_SUBTITLE = "¡Recoge todo el oro y escapa!"
    ABOUT_GAME = "Un clásico juego de plataformas y estrategia"
    AUTHOR = "Por: Jhon Oliver Castillo"
    VERSION = "Versión 1.0"
    DIFFICULTY_EASY = "Fácil"
    DIFFICULTY_MEDIUM = "Normal"
    DIFFICULTY_HARD = "Difícil"
    DIFFICULTY_SELECT = "Selecciona dificultad:"

    # Textos para el menú de pausa
    PAUSE_TITLE = "Juego Pausado"
    RESUME_BUTTON = "Continuar"
    QUIT_TO_MENU_BUTTON = "Menú Principal"

    # Textos para el menú de victoria
    VICTORY_TITLE = "¡Victoria!"
    VICTORY_MESSAGE = "¡Has completado el juego!"
    PLAY_AGAIN_BUTTON = "Jugar de Nuevo"

    # Textos para el menú de derrota
    DEFEAT_TITLE = "Game Over"
    DEFEAT_MESSAGE = "Has perdido todas tus vidas"
    RETRY_BUTTON = "Reintentar"
    

    # Estadísticas del juego
    LIVES_TEXT = "Vidas: {}"
    GOLD_TEXT = "Oro: {}/{}"

"""
    Jhon Oliver Castillo Caraballo
    22-SISN-2-063
"""

from pathlib import Path
from typing import List, Tuple, Dict, Optional, Any, cast, TypedDict, Union
import os
from Utils.assets import ASSETS
import pygame as pg


class AxisMapping(TypedDict):
    negative: str
    positive: str


class JoystickMapping(TypedDict):
    axis: Dict[int, AxisMapping]
    buttons: Dict[int, str]
    deadzone: float


class Setup:
    COLORS = {
        'INFO': '\033[38;5;46m',      # Verde Retro
        'SUCCESS': '\033[38;5;226m',   # Amarillo Retro
        'ERROR': '\033[38;5;202m',     # Naranja Retro
        'RESET': '\033[0m'
    }

    # Control activo (None significa ningún joystick conectado)
    active_joystick: Optional[Any] = None

    # Mapeo de controles del joystick
    JOYSTICK_MAPPING: JoystickMapping = {
        'axis': {
            # Eje horizontal (izquierda/derecha)
            0: {'negative': 'LEFT', 'positive': 'RIGHT'},
            # Eje vertical (arriba/abajo)
            1: {'negative': 'UP', 'positive': 'DOWN'},
        },
        'buttons': {
            0: 'DIG_LEFT',    # Típicamente botón A/X (cavar a la izquierda)
            1: 'DIG_RIGHT',   # Típicamente botón B/O (cavar a la derecha)
            2: 'SELECT',      # Para seleccionar opciones en menú
            7: 'PAUSE',       # Típicamente botón Start/Options (pausar juego)
            6: 'MENU'         # Típicamente botón Select/Share (volver al menú)
        },
        'deadzone': 0.5       # Umbral para ignorar pequeños movimientos del stick
    }

    # Variable para rastrear estados de botones anteriores (para detectar pulsaciones)
    previous_button_states: Dict[str, bool] = {}

    @staticmethod
    def validate_assets() -> bool:
        """
        Valida todos los recursos requeridos del juego.

        Realiza una validación completa de los recursos del juego incluyendo:
        - Existencia del archivo
        - Permisos del archivo
        - Integridad básica del archivo

        Returns:
            bool: True si todos los recursos son válidos, False en caso contrario
        """
        missing_assets: List[Tuple[str, str, str]
                             ] = []  # (nombre, ruta, razón)
        total_assets = len(
            [asset for asset in ASSETS if asset.name != 'ASSETS_DIR'])
        validated = 0

        print(
            f"\n{Setup.COLORS['INFO']}[SCAN] Iniciando escaneo de recursos...{Setup.COLORS['RESET']}")

        for asset_enum in ASSETS:
            if asset_enum.name == 'ASSETS_DIR':
                continue

            asset_path = asset_enum.value
            validated += 1
            print(
                f"\r[DATA] Progreso: {Setup.COLORS['SUCCESS']}{validated}/{total_assets}{Setup.COLORS['RESET']} archivos procesados", end="")

            if not isinstance(asset_path, Path):
                missing_assets.append((
                    asset_enum.name,
                    str(asset_path),
                    "Tipo de ruta inválido"
                ))
                continue

            if not asset_path.exists():
                missing_assets.append((
                    asset_enum.name,
                    str(asset_path),
                    "Archivo no encontrado"
                ))
                continue

            if not os.access(asset_path, os.R_OK):
                missing_assets.append((
                    asset_enum.name,
                    str(asset_path),
                    "Archivo no legible"
                ))
                continue

            if asset_path.stat().st_size == 0:
                missing_assets.append((
                    asset_enum.name,
                    str(asset_path),
                    "Archivo está vacío"
                ))

        print()  # Nueva línea después del progreso

        if missing_assets:
            print(
                f"\n{Setup.COLORS['ERROR']}[ERROR] VALIDACIÓN FALLIDA{Setup.COLORS['RESET']}")
            print(
                f"{Setup.COLORS['INFO']}[WARNING] Problemas detectados:{Setup.COLORS['RESET']}")
            for name, path, reason in missing_assets:
                print(f"\n<{name}>:")
                print(f"  PATH: {path}")
                print(f"  FAIL: {reason}")
            print(
                f"\n{Setup.COLORS['INFO']}[SYSTEM] Repare los errores para continuar{Setup.COLORS['RESET']}")
            return False

        print(
            f"\n{Setup.COLORS['SUCCESS']}[OK] VALIDACIÓN COMPLETA{Setup.COLORS['RESET']}")
        print(
            f"{Setup.COLORS['INFO']}[LOAD] CARGANDO LODE RUNNER...{Setup.COLORS['RESET']}")
        return True

    @staticmethod
    def initialize_controllers() -> bool:
        """
        Inicializa el sistema de joystick y detecta controladores conectados.

        Returns:
            bool: True si hay al menos un joystick conectado, False en caso contrario
        """
        pg.joystick.init()
        joystick_count = pg.joystick.get_count()

        # Inicializar estado previo de botones
        Setup.previous_button_states = {
            'LEFT': False, 'RIGHT': False, 'UP': False, 'DOWN': False,
            'DIG_LEFT': False, 'DIG_RIGHT': False, 'PAUSE': False,
            'MENU': False, 'SELECT': False
        }

        if joystick_count > 0:
            print(
                f"{Setup.COLORS['INFO']}[JOYSTICK] Detectado(s) {joystick_count} controlador(es){Setup.COLORS['RESET']}")
            for i in range(joystick_count):
                joystick = pg.joystick.Joystick(i)
                joystick.init()
                print(
                    f"{Setup.COLORS['SUCCESS']}[JOYSTICK] #{i}: {joystick.get_name()}{Setup.COLORS['RESET']}")

                # Activar el primer joystick encontrado
                if i == 0:
                    Setup.active_joystick = joystick
                    print(
                        f"{Setup.COLORS['INFO']}[JOYSTICK] Usando: {joystick.get_name()}{Setup.COLORS['RESET']}")

                    # Mostrar información del joystick
                    num_axes = joystick.get_numaxes()
                    num_buttons = joystick.get_numbuttons()
                    print(
                        f"{Setup.COLORS['INFO']}[JOYSTICK] Ejes: {num_axes}, Botones: {num_buttons}{Setup.COLORS['RESET']}")
            return True
        else:
            print(
                f"{Setup.COLORS['INFO']}[JOYSTICK] No se detectaron controladores{Setup.COLORS['RESET']}")
            return False

    @staticmethod
    def get_joystick() -> Optional[Any]:
        """
        Obtiene el joystick activo.

        Returns:
            Optional[Any]: El joystick activo o None si no hay ninguno
        """
        return Setup.active_joystick

    @staticmethod
    def has_joystick() -> bool:
        """
        Verifica si hay un joystick activo.

        Returns:
            bool: True si hay un joystick activo, False en caso contrario
        """
        return Setup.active_joystick is not None

    @staticmethod
    def get_joystick_actions() -> Dict[str, bool]:
        """
        Procesa la entrada del joystick y devuelve las acciones activas.

        Returns:
            Dict[str, bool]: Diccionario con las acciones activas (True si están activadas)
        """
        actions = {
            'LEFT': False, 'RIGHT': False, 'UP': False, 'DOWN': False,
            'DIG_LEFT': False, 'DIG_RIGHT': False, 'PAUSE': False,
            'MENU': False, 'SELECT': False
        }

        joystick = Setup.get_joystick()
        if not joystick:
            return actions

        try:
            # Procesar ejes (controles analógicos)
            axis_mapping = cast(Dict[int, AxisMapping],
                                Setup.JOYSTICK_MAPPING.get('axis', {}))
            for axis_id, axis_map in axis_mapping.items():
                if axis_id < joystick.get_numaxes():
                    value = joystick.get_axis(axis_id)
                    deadzone = float(
                        Setup.JOYSTICK_MAPPING.get('deadzone', 0.5))

                    if value < -deadzone:  # Umbral negativo
                        actions[axis_map['negative']] = True
                    elif value > deadzone:  # Umbral positivo
                        actions[axis_map['positive']] = True

            # Procesar botones
            button_mapping = cast(
                Dict[int, str], Setup.JOYSTICK_MAPPING.get('buttons', {}))
            for button_id, action in button_mapping.items():
                if button_id < joystick.get_numbuttons() and joystick.get_button(button_id):
                    actions[action] = True

        except (AttributeError, pg.error) as e:
            print(
                f"{Setup.COLORS['ERROR']}[JOYSTICK] Error al leer entrada: {e}{Setup.COLORS['RESET']}")
        except KeyError as e:
            print(
                f"{Setup.COLORS['ERROR']}[JOYSTICK] Error al acceder a una acción: {e}{Setup.COLORS['RESET']}")

        return actions

    @staticmethod
    def is_joystick_button_pressed(action: str) -> bool:
        """
        Verifica si una acción específica del joystick está activa.

        Args:
            action: Nombre de la acción a verificar

        Returns:
            bool: True si la acción está activa, False en caso contrario
        """
        actions = Setup.get_joystick_actions()
        return actions.get(action, False)

    @staticmethod
    def get_button_pressed_events() -> Dict[str, bool]:
        """
        Detecta eventos de pulsación de botones (solo cuando cambian de no pulsados a pulsados).

        Returns:
            Dict[str, bool]: Diccionario con eventos de pulsación
        """
        current_actions = Setup.get_joystick_actions()
        pressed_events = {}

        for action, state in current_actions.items():
            # Evento de pulsación: botón ahora presionado que antes no lo estaba
            pressed_events[action] = state and not Setup.previous_button_states.get(
                action, False)

        # Actualizar estados anteriores para la próxima verificación
        Setup.previous_button_states = current_actions.copy()

        return pressed_events

    @staticmethod
    def get_joystick_info() -> Dict[str, Any]:
        """
        Obtiene información detallada sobre el joystick activo.

        Returns:
            Dict[str, Any]: Diccionario con información del joystick
        """
        info = {
            'connected': False,
            'name': 'None',
            'axes': 0,
            'buttons': 0,
            'mapping': Setup.JOYSTICK_MAPPING
        }

        joystick = Setup.get_joystick()
        if joystick is not None:
            try:
                info.update({
                    'connected': True,
                    'name': joystick.get_name(),
                    'axes': joystick.get_numaxes(),
                    'buttons': joystick.get_numbuttons()
                })
            except (AttributeError, pg.error) as e:
                print(
                    f"{Setup.COLORS['ERROR']}[JOYSTICK] Error al obtener información: {e}{Setup.COLORS['RESET']}")

        return info

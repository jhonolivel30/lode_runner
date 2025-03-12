"""
    Jhon Oliver Castillo Caraballo
    22-SISN-2-063
"""

import pygame as pg
import pygame_menu as pg_menu
from Utils.constants import CONSTANTS
from Utils.strings import STRINGS
from Utils.assets import ASSETS
from Utils.setup import Setup
import os.path


class Theme:
    surface = None
    menu_background_image = None
    current_menu = None  # Almacena referencia al menú activo
    custom_font = None   # Fuente personalizada para el menú

    @classmethod
    def initialize(cls):
        pg.display.init()
        # Se elimina la bandera pg.RESIZABLE para mantener tamaño fijo
        cls.surface = pg.display.set_mode(CONSTANTS.WINDOW_SIZE.value)
        # Inicializar fuentes personalizadas
        pg.font.init()

        # Cargar fuente personalizada si existe, sino usar la predeterminada
        if os.path.exists(CONSTANTS.MENU_FONT.value):
            cls.custom_font = CONSTANTS.MENU_FONT.value
        else:
            cls.custom_font = None
            print(
                "Aviso: Fuente personalizada no encontrada, usando fuente predeterminada.")

        # Cargar la imagen de fondo del menú
        cls.menu_background_image = pg.Surface(CONSTANTS.WINDOW_SIZE.value)
        cls.menu_background_image.fill(CONSTANTS.COLOR_BLACK.value)
        # Intentar cargar una imagen si está disponible
        try:
            bg_image = pg.image.load(ASSETS.MENU_BACKGROUND.value)
            cls.menu_background_image = pg.transform.scale(
                bg_image, CONSTANTS.WINDOW_SIZE.value)
        except (AttributeError, FileNotFoundError):
            # Continuar con fondo plano si la imagen no se encuentra
            print("Aviso: Imagen de fondo no encontrada, usando fondo predeterminado.")
            pass
        return cls.surface

    @classmethod
    def main_background(cls):
        """
        Dibuja el fondo del menú cubriendo toda la ventana sin preservar proporciones
        """
        # Obtener dimensiones actuales de la superficie
        window_width, window_height = cls.surface.get_size()

        # Limpiar superficie
        cls.surface.fill(CONSTANTS.COLOR_BLACK.value)

        # Estirar la imagen para cubrir toda la ventana sin preservar proporciones
        if cls.menu_background_image:
            # Simplemente estirar la imagen para cubrir toda la ventana
            scaled_image = pg.transform.scale(
                cls.menu_background_image, (window_width, window_height))
            cls.surface.blit(scaled_image, (0, 0))

            # Añadir un degradado oscuro para mejorar la visibilidad del texto
            overlay = pg.Surface((window_width, window_height), pg.SRCALPHA)
            # Negro semi-transparente (aumentado a 150)
            overlay.fill((0, 0, 0, 150))
            cls.surface.blit(overlay, (0, 0))

    @staticmethod
    def get_loderunner_theme():
        """
        Crea un tema personalizado para el juego Lode Runner con estética retro
        """
        theme = pg_menu.Theme()

        # Configurar colores y estilo
        theme.background_color = CONSTANTS.TRANSPARENT_COLOR.value
        theme.title_background_color = CONSTANTS.TRANSPARENT_COLOR.value
        theme.title_font_color = CONSTANTS.COLOR_GOLD.value
        theme.widget_font_color = CONSTANTS.COLOR_WHITE.value
        theme.selection_color = CONSTANTS.COLOR_ORANGE.value

        # Configurar fuentes
        if os.path.exists(CONSTANTS.MENU_FONT.value):
            theme.title_font = CONSTANTS.MENU_FONT.value
            theme.title_font_size = CONSTANTS.TITLE_FONT_SIZE.value
            theme.widget_font = CONSTANTS.MENU_FONT.value
            theme.widget_font_size = CONSTANTS.MENU_FONT_SIZE.value
        else:
            theme.title_font = pg_menu.font.FONT_8BIT
            theme.title_font_size = CONSTANTS.TITLE_FONT_SIZE.value
            theme.widget_font = pg_menu.font.FONT_8BIT
            theme.widget_font_size = CONSTANTS.MENU_FONT_SIZE.value

        # Configurar espaciado y estilo
        theme.widget_margin = (0, 15)  # Margen aumentado para mejor separación
        theme.widget_padding = CONSTANTS.BUTTON_PADDING.value  # Botones más grandes
        theme.widget_border_width = 2  # Añadir borde a los widgets
        theme.widget_border_color = CONSTANTS.COLOR_GOLD.value  # Borde dorado
        theme.widget_border_radius = CONSTANTS.BUTTON_BORDER_RADIUS.value

        # Efectos de decoración
        theme.widget_shadow = True
        theme.widget_shadow_offset = CONSTANTS.MENU_SHADOW_OFFSET.value

        # Alineación general
        theme.widget_alignment = pg_menu.locals.ALIGN_CENTER

        return theme

    @staticmethod
    def style_button(button, color=None):
        """
        Aplica un estilo consistente a los botones
        """
        if color is None:
            color = CONSTANTS.COLOR_BROWN.value

        button.set_background_color(color)
        button.set_border(2, CONSTANTS.COLOR_GOLD.value)
        button.set_alignment(pg_menu.locals.ALIGN_CENTER)
        # Asegurar que el padding sea consistente
        button.update_font({'padding': CONSTANTS.BUTTON_PADDING.value})
        return button

    @staticmethod
    def style_label(label, is_title=False, color=None):
        """
        Aplica un estilo consistente a las etiquetas
        """
        if color is None:
            color = CONSTANTS.COLOR_GOLD.value if is_title else CONSTANTS.COLOR_WHITE.value

        font_size = CONSTANTS.SUBTITLE_FONT_SIZE.value if is_title else CONSTANTS.MENU_FONT_SIZE.value
        label._font_color = color
        label.update_font({'size': font_size})
        label.set_alignment(pg_menu.locals.ALIGN_CENTER)
        return label

    @staticmethod
    def create_menu_base(width, height, title, center_content=True):
        """
        Crea una base de menú con configuración consistente
        """
        theme = Theme.get_loderunner_theme()
        menu = pg_menu.Menu(
            theme=theme,
            height=height,
            width=width,
            title=title,
            center_content=center_content,
            joystick_enabled=True,  # Habilitar soporte de joystick
            mouse_enabled=True,
            mouse_visible=True
        )
        # Configure joystick separately if available
        if Setup.has_joystick():
            try:
                # Try to update joystick - this works in newer pygame_menu versions
                menu.update_joystick(0)
            except (AttributeError, TypeError):
                # Fallback for different pygame_menu versions
                pass

        return menu

    @classmethod
    def create_about_menu(cls, window_width: int, window_height: int):
        """
        Crea el menú de instrucciones con estilo mejorado y menos cargado
        """
        about_menu = cls.create_menu_base(
            window_width,
            window_height,
            STRINGS.BRIEFING_TITLE.value
        )

        # Añadir contenido con estilo más limpio
        about_menu.add.vertical_margin(30)

        controls_header = about_menu.add.label(STRINGS.CONTROLS_HEADER.value)
        cls.style_label(controls_header, is_title=True)

        about_menu.add.vertical_margin(15)

        # Usar fuente más pequeña para las instrucciones
        movement_label = about_menu.add.label(
            STRINGS.MOVEMENT_CONTROLS.value, margin=(20, 0))
        cls.style_label(movement_label, is_title=False)
        movement_label.update_font(
            {'size': int(CONSTANTS.MENU_FONT_SIZE.value * 0.85)})

        fire_label = about_menu.add.label(
            STRINGS.FIRE_CONTROLS.value, margin=(20, 0))
        cls.style_label(fire_label, is_title=False)
        fire_label.update_font(
            {'size': int(CONSTANTS.MENU_FONT_SIZE.value * 0.85)})

        about_menu.add.vertical_margin(40)

        # Información del juego con menos énfasis
        about_menu.add.vertical_margin(10)

        author_label = about_menu.add.label(STRINGS.AUTHOR.value)
        cls.style_label(author_label, is_title=False)
        author_label.update_font(
            {'size': int(CONSTANTS.MENU_FONT_SIZE.value * 0.85)})

        version_label = about_menu.add.label(STRINGS.VERSION.value)
        cls.style_label(version_label, is_title=False)
        version_label.update_font(
            {'size': int(CONSTANTS.MENU_FONT_SIZE.value * 0.85)})

        about_menu.add.vertical_margin(40)

        # Botón de regreso con estilo mejorado
        return_btn = about_menu.add.button(
            STRINGS.RETURN_BUTTON.value, pg_menu.events.BACK)
        cls.style_button(return_btn)

        return about_menu

    @classmethod
    def create_pause_menu(cls, window_width: int, window_height: int, resume_action, restart_action, quit_action):
        """
        Crea el menú de pausa
        """
        pause_menu = cls.create_menu_base(
            window_width // 2,  # Más pequeño que el menú principal
            window_height // 2,
            STRINGS.PAUSE_TITLE.value
        )

        pause_menu.add.vertical_margin(20)
        resume_btn = pause_menu.add.button(
            STRINGS.RESUME_BUTTON.value, resume_action)
        cls.style_button(resume_btn)

        pause_menu.add.vertical_margin(10)

        restart_btn = pause_menu.add.button(
            STRINGS.RETRY_BUTTON.value, restart_action)
        cls.style_button(restart_btn)

        pause_menu.add.vertical_margin(10)

        quit_btn = pause_menu.add.button(
            STRINGS.QUIT_TO_MENU_BUTTON.value, quit_action)
        cls.style_button(quit_btn)

        return pause_menu

    @classmethod
    def create_victory_menu(cls, window_width: int, window_height: int, play_again_action, quit_action):
        """
        Crea el menú de victoria para un juego de un solo nivel
        """
        victory_menu = cls.create_menu_base(
            window_width // 1.5,
            window_height // 1.5,
            STRINGS.VICTORY_TITLE.value
        )

        victory_menu.add.vertical_margin(20)

        victory_msg = victory_menu.add.label(STRINGS.VICTORY_MESSAGE.value)
        cls.style_label(victory_msg, is_title=True,
                        color=CONSTANTS.COLOR_GOLD.value)

        victory_menu.add.vertical_margin(30)

        again_btn = victory_menu.add.button(
            STRINGS.PLAY_AGAIN_BUTTON.value, play_again_action)
        cls.style_button(again_btn)

        victory_menu.add.vertical_margin(10)

        menu_btn = victory_menu.add.button(
            STRINGS.QUIT_TO_MENU_BUTTON.value, quit_action)
        cls.style_button(menu_btn)

        return victory_menu

    @classmethod
    def create_defeat_menu(cls, window_width: int, window_height: int, retry_action, quit_action):
        """
        Crea el menú de derrota
        """
        defeat_menu = cls.create_menu_base(
            window_width // 1.5,
            window_height // 1.5,
            STRINGS.DEFEAT_TITLE.value
        )

        defeat_menu.add.vertical_margin(20)

        defeat_msg = defeat_menu.add.label(STRINGS.DEFEAT_MESSAGE.value)
        cls.style_label(defeat_msg, is_title=True,
                        color=CONSTANTS.COLOR_RED.value)

        defeat_menu.add.vertical_margin(30)

        retry_btn = defeat_menu.add.button(
            STRINGS.RETRY_BUTTON.value, retry_action)
        cls.style_button(retry_btn)

        defeat_menu.add.vertical_margin(10)

        menu_btn = defeat_menu.add.button(
            STRINGS.QUIT_TO_MENU_BUTTON.value, quit_action)
        cls.style_button(menu_btn)

        return defeat_menu

    @classmethod
    def menu_loop(cls, run_game):
        """
        Bucle principal para el menú del juego
        """
        pg.init()
        pg.mixer.init()

        # Inicializar controladores de juego
        Setup.initialize_controllers()

        # Cargar música de fondo si está disponible
        try:
            pg.mixer.music.load(ASSETS.BACKGROUND_MUSIC.value)
            pg.mixer.music.play(-1)
        except (AttributeError, FileNotFoundError):
            print("Aviso: Archivo de música no encontrado.")

        pg.display.set_caption(STRINGS.GAME_TITLE.value)
        clock = pg.time.Clock()

        # Configurar sonidos del menú
        menu_sound = pg_menu.sound.Sound()
        try:
            menu_sound.set_sound(
                pg_menu.sound.SOUND_TYPE_WIDGET_SELECTION, ASSETS.STAGE_START_SOUND.value)
            menu_sound.set_sound(
                pg_menu.sound.SOUND_TYPE_CLICK_MOUSE, ASSETS.ALL_GOLD_COLLECTED_SOUND.value)
            # Añadir sonido para navegación con joystick
            menu_sound.set_sound(
                pg_menu.sound.SOUND_TYPE_KEY_ADDITION, ASSETS.STAGE_START_SOUND.value)
        except (AttributeError, FileNotFoundError):
            # Continuar sin sonidos personalizados si no están disponibles
            print("Aviso: Archivos de sonido no encontrados.")

        window_height = int(
            CONSTANTS.WINDOW_SIZE.value[1] * CONSTANTS.WINDOW_SCALE.value)
        window_width = int(
            CONSTANTS.WINDOW_SIZE.value[0] * CONSTANTS.WINDOW_SCALE.value)

        about_menu = cls.create_about_menu(window_width, window_height)

        # Crear el menú principal usando la función base
        main_menu = cls.create_menu_base(
            window_width,
            window_height,
            STRINGS.GAME_TITLE.value
        )
        main_menu.set_onclose(pg_menu.events.EXIT)

        # Guardar referencia al menú principal
        cls.current_menu = main_menu

        # Añadir subtítulo del juego
        subtitle = main_menu.add.label(STRINGS.GAME_SUBTITLE.value)
        cls.style_label(subtitle, is_title=True)

        main_menu.add.vertical_margin(30)

        # Crear botones con estilo mejorado
        start_btn = main_menu.add.button(STRINGS.START_BUTTON.value, run_game)
        cls.style_button(start_btn)

        main_menu.add.vertical_margin(15)

        briefing_btn = main_menu.add.button(
            STRINGS.BRIEFING_BUTTON.value, about_menu)
        cls.style_button(briefing_btn)

        main_menu.add.vertical_margin(15)

        exit_btn = main_menu.add.button(
            STRINGS.RETREAT_BUTTON.value, pg_menu.events.EXIT)
        cls.style_button(exit_btn)

        # Configurar sonidos
        main_menu.set_sound(menu_sound)
        about_menu.set_sound(menu_sound)

        # Añadir un controlador de cambio de estado del menú para rastrear el menú activo actual
        def update_menu_positions():
            """Actualizar todas las posiciones del menú para asegurar que estén centradas"""
            window_width, window_height = cls.surface.get_size()

            for menu in [main_menu, about_menu]:
                menu_width, menu_height = menu.get_size()
                x = (window_width - menu_width) // 2
                y = (window_height - menu_height) // 2
                menu.translate(x, y)

        # Actualizar el controlador de cambio de menú para asegurar el posicionamiento adecuado
        def on_menu_change(current, new):
            cls.current_menu = new
            update_menu_positions()
            # Asegurar que el joystick esté habilitado en el nuevo menú
            if Setup.has_joystick():
                new.update_joystick(0)  # Actualizar referencia al joystick

        main_menu.set_onbeforeopen(on_menu_change)
        about_menu.set_onbeforeopen(on_menu_change)

        # Actualización inicial de posición
        cls.current_menu = main_menu
        update_menu_positions()

        running = True
        while running:
            clock.tick(CONSTANTS.FPS.value)
            cls.main_background()

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    running = False

            if main_menu.is_enabled():
                main_menu.mainloop(cls.surface, cls.main_background,
                                   disable_loop=False, fps_limit=CONSTANTS.FPS.value)

            pg.display.flip()

        exit()

    @staticmethod
    def load_game_background(tile_size):
        """Cargar y escalar la imagen de fondo del juego"""
        try:
            background_image = pg.image.load(
                ASSETS.GAME_BACKGROUND.value).convert()
            return pg.transform.scale(background_image, (tile_size, tile_size))
        except (AttributeError, FileNotFoundError):
            # Crear un fondo simple si no se encuentra la imagen
            background = pg.Surface((tile_size, tile_size))
            background.fill(CONSTANTS.COLOR_BLACK.value)
            return background

    @staticmethod
    def draw_background(surface, background_image, tile_size, window_size):
        """Dibujar el fondo como baldosas a través de la superficie del juego"""
        for y in range(0, window_size[1], tile_size):
            for x in range(0, window_size[0], tile_size):
                surface.blit(background_image, (x, y))

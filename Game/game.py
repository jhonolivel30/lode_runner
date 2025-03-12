"""
    Jhon Oliver Castillo Caraballo
    22-SISN-2-063
"""

import pygame as pg
from Utils.constants import CONSTANTS
from Utils.assets import ASSETS
from Utils.setup import Setup
from Game.map import Map
from Entities.Player import Player
from Entities.Enemy import Enemy
from Utils.theme import Theme
import pygame_menu as pg_menu


class Game:
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.running = True
        self.clock = pg.time.Clock()
        self.map = Map()
        # Inicializar jugador
        # Puedes ajustar la posición inicial
        self.player = Player(self.map, start_pos=(1, 1))
        # Inicializar enemigos
        self.enemies = []
        self.spawn_enemies()

        # Debug mode for pathfinding visualization
        self.debug_mode = False

        # Estados del juego
        self.game_state = "playing"  # Estados: "playing", "paused", "victory", "defeat"

        # Inicializar música y sonidos
        pg.mixer.init()
        self.sound_effects = {}
        self.load_music()
        self.load_sound_effects()

        # Crear menús
        self.init_menus()

        # Cargar iconos para la UI (con manejo de errores)
        self.life_icon = self.create_ui_icon(
            'heart', (255, 0, 0))  # Icono rojo para vidas
        self.gold_icon = self.create_ui_icon(
            'coin', (255, 215, 0))  # Icono dorado para monedas

        # Fuente personalizada para UI
        self.ui_font = pg.font.Font(None, 28)

        # Control de reproducción de sonidos
        self.last_coin_time = 0
        self.coin_sound_cooldown = 500  # milisegundos

    def load_music(self):
        """Carga la música del juego"""
        try:
            pg.mixer.music.load(ASSETS.MAIN_BACKGROUND_MUSIC.value)
            # Volumen más bajo para la música de fondo
            pg.mixer.music.set_volume(0.5)
            pg.mixer.music.play(-1)
        except (AttributeError, FileNotFoundError):
            print("Aviso: Archivo de música principal no encontrado.")

    def load_sound_effects(self):
        """Carga todos los efectos de sonido del juego"""
        sound_assets = {
            'stage_start': ASSETS.STAGE_START_SOUND.value,
            'all_gold': ASSETS.ALL_GOLD_COLLECTED_SOUND.value,
            'stage_clear': ASSETS.STAGE_CLEAR_SOUND.value,
            'miss': ASSETS.STAGE_MISS_SOUND.value,
            'game_over': ASSETS.GAME_OVER_SOUND.value
        }

        for name, path in sound_assets.items():
            self.sound_effects[name] = self.load_sound(path)

        # Reproducir sonido de inicio de nivel
        self.play_sound('stage_start')

    def play_sound(self, sound_name):
        """Reproduce un efecto de sonido por su nombre"""
        if sound_name in self.sound_effects and self.sound_effects[sound_name]:
            self.sound_effects[sound_name].play()

    def load_sound(self, sound_path):
        """Carga un efecto de sonido"""
        try:
            sound = pg.mixer.Sound(sound_path)
            # Ajustar volumen para que no sea demasiado alto
            sound.set_volume(0.7)
            return sound
        except (AttributeError, FileNotFoundError):
            print(f"Aviso: Archivo de sonido no encontrado: {sound_path}")
            return None

    def load_image(self, path, size=None):
        """Carga una imagen y la redimensiona si es necesario"""
        try:
            img = pg.image.load(path).convert_alpha()
            if size:
                img = pg.transform.scale(img, size)
            return img
        except (FileNotFoundError, pg.error):
            print(f"Error: No se pudo cargar la imagen: {path}")
            # Crear una superficie de color como respaldo
            fallback = pg.Surface(size if size else (32, 32), pg.SRCALPHA)
            fallback.fill((255, 0, 255))  # Color magenta para indicar error
            return fallback

    def init_menus(self):
        """Inicializa los menús del juego"""
        width, height = self.screen.get_size()

        # Menú de pausa
        self.pause_menu = Theme.create_pause_menu(
            width, height,
            self.resume_game,
            self.restart_level,
            self.quit_to_main_menu
        )
        # Configurar joystick para los menús
        if Setup.has_joystick():
            self.pause_menu.enable_joystick(0)  # Usar joystick 0

        # Menú de victoria
        self.victory_menu = Theme.create_victory_menu(
            width, height,
            self.restart_level,
            self.quit_to_main_menu
        )
        if Setup.has_joystick():
            self.victory_menu.enable_joystick(0)

        # Menú de derrota
        self.defeat_menu = Theme.create_defeat_menu(
            width, height,
            self.restart_level,
            self.quit_to_main_menu
        )
        if Setup.has_joystick():
            self.defeat_menu.enable_joystick(0)

    def spawn_enemies(self):
        """Crea tres enemigos en diferentes posiciones del mapa"""
        # Define las posiciones iniciales para los enemigos
        enemy_positions = [
            (3, 3),   # Enemigo 1
            (10, 5),  # Enemigo 2
            (15, 7)   # Enemigo 3
        ]

        # Crear los enemigos
        for position in enemy_positions:
            enemy = Enemy(self.map, self.player, start_pos=position)
            self.enemies.append(enemy)

    def handle_events(self):
        """Maneja los eventos de pygame"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.game_state == "playing":
                        self.pause_game()
                    elif self.game_state == "paused":
                        self.resume_game()
                # Toggle debug mode with 'D' key
                elif event.key == pg.K_d:
                    self.debug_mode = not self.debug_mode
                    # Apply debug mode to all enemies
                    for enemy in self.enemies:
                        enemy.debug = self.debug_mode
                    print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")

                    # Print current enemy states in debug mode
                    if self.debug_mode:
                        for i, enemy in enumerate(self.enemies):
                            print(
                                f"Enemy {i}: Position ({enemy.x}, {enemy.y}), State: {'CHASING' if enemy.is_chasing else 'PATROL'}")
                            if enemy.current_path:
                                print(f"  Current path: {enemy.current_path}")
            # Procesar eventos de joystick
            elif event.type == pg.JOYBUTTONDOWN:
                if self.game_state == "playing":
                    # Aquí solo manejamos el botón de pausa, el resto se maneja en handle_input
                    if Setup.has_joystick() and Setup.is_joystick_button_pressed('PAUSE'):
                        self.pause_game()
                elif self.game_state == "paused":
                    if Setup.has_joystick() and Setup.is_joystick_button_pressed('PAUSE'):
                        self.resume_game()

        # Procesar acciones del joystick (para pausar/reanudar)
        if Setup.has_joystick():
            joystick_actions = Setup.get_joystick_actions()

            # Pausar con botón START del joystick
            if joystick_actions.get('PAUSE'):
                if self.game_state == "playing":
                    self.pause_game()
                elif self.game_state == "paused":
                    self.resume_game()

            # Salir al menú con botón SELECT/SHARE del joystick
            if joystick_actions.get('MENU') and self.game_state != "playing":
                self.quit_to_main_menu()

    def pause_game(self):
        """Pausa el juego y muestra el menú de pausa"""
        self.game_state = "paused"
        pg.mixer.music.pause()

    def resume_game(self):
        """Reanuda el juego desde el menú de pausa"""
        self.game_state = "playing"
        pg.mixer.music.unpause()

    def show_victory(self):
        """Muestra el menú de victoria"""
        if self.game_state != "victory":
            self.game_state = "victory"
            pg.mixer.music.stop()
            self.play_sound('stage_clear')

    def show_defeat(self):
        """Muestra el menú de derrota"""
        if self.game_state != "defeat":
            self.game_state = "defeat"
            pg.mixer.music.stop()
            self.play_sound('game_over')

    def restart_level(self):
        """Reinicia el nivel"""
        # Reiniciar el mapa, jugador y enemigos
        self.map = Map()
        self.player = Player(self.map, start_pos=(1, 1))
        self.enemies = []
        self.spawn_enemies()

        # Reanudar música y estado de juego
        self.game_state = "playing"
        try:
            pg.mixer.music.load(ASSETS.MAIN_BACKGROUND_MUSIC.value)
            pg.mixer.music.play(-1)
            # Reproducir sonido de inicio de nivel
            self.play_sound('stage_start')
        except (AttributeError, FileNotFoundError):
            print("Aviso: Archivo de música principal no encontrado.")

    def quit_to_main_menu(self):
        """Sale del juego y vuelve al menú principal"""
        self.running = False

    def check_game_conditions(self):
        """Verifica condiciones de victoria o derrota"""
        # Condición de victoria: recoger todo el oro y llegar a la salida
        if self.player.gold_collected >= self.map.total_gold:
            # Si la puerta está abierta y el jugador está en la posición de la puerta
            if self.map.is_exit_open() and self.map.is_player_at_exit((self.player.x, self.player.y)):
                self.show_victory()

        # Condición de derrota: perder todas las vidas
        if self.player.lives <= 0:
            self.show_defeat()

    def update(self, delta_time):
        """Actualiza la lógica del juego"""
        if self.game_state != "playing":
            return

        self.map.update()

        # Guardar el oro anterior para detectar cuándo se recoge uno nuevo
        previous_gold = self.player.gold_collected

        self.player.update(delta_time)

        # Verificar si se ha recogido una moneda
        if self.player.gold_collected > previous_gold:
            # Añadir cooldown para evitar que el sonido se reproduzca demasiado seguido
            current_time = pg.time.get_ticks()
            if current_time - self.last_coin_time > self.coin_sound_cooldown:
                self.play_sound('all_gold')
                self.last_coin_time = current_time

        for enemy in self.enemies:
            enemy.update(delta_time)

            # Verificar colisión con enemigos
            if self.player.check_enemy_collision(enemy):
                self.play_sound('miss')

        # Comprobar si se recogió todo el oro y la salida aún no está abierta
        if self.player.gold_collected >= self.map.total_gold and not self.map.exit_open:
            self.map.open_exit()
            self.play_sound('all_gold')

        # Verificar condiciones de victoria/derrota
        self.check_game_conditions()

    def draw(self):
        """Dibuja los elementos del juego"""
        self.screen.fill(CONSTANTS.COLOR_BLACK.value)
        self.map.draw(self.screen)
        self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.draw_stats()

    def draw_stats(self):
        """Muestra estadísticas del juego como vidas y oro recogido con mejor UI"""
        # Panel para la UI
        panel_width = 200
        panel_height = 80
        panel_margin = 10

        # Crear un panel semitransparente
        ui_panel = pg.Surface((panel_width, panel_height), pg.SRCALPHA)
        ui_panel.fill((0, 0, 0, 160))  # Negro semitransparente

        # Posición del panel (esquina superior izquierda)
        panel_pos = (panel_margin, panel_margin)

        # Dibujar el panel
        self.screen.blit(ui_panel, panel_pos)

        # Agregar bordes al panel
        pg.draw.rect(self.screen, CONSTANTS.COLOR_WHITE.value,
                     (panel_pos[0], panel_pos[1], panel_width, panel_height), 2)

        # Mejorar espaciado entre iconos y valores
        icon_margin = 15
        text_offset = 50  # Aumentado de 35 a 50 para mayor separación

        # Centrado vertical para cada línea
        line1_y = 15
        line2_y = 45

        # Vidas
        self.screen.blit(
            self.life_icon, (panel_pos[0] + icon_margin, panel_pos[1] + line1_y))

        # Usar el texto desde STRINGS para mayor consistencia
        lives_text = self.ui_font.render(
            f"x {self.player.lives}", True, CONSTANTS.COLOR_WHITE.value)
        self.screen.blit(
            lives_text, (panel_pos[0] + text_offset, panel_pos[1] + line1_y))

        # Oro recogido
        self.screen.blit(
            self.gold_icon, (panel_pos[0] + icon_margin, panel_pos[1] + line2_y))

        gold_text = self.ui_font.render(
            f"x {self.player.gold_collected}/{self.map.total_gold}", True, CONSTANTS.COLOR_GOLD.value)
        self.screen.blit(
            gold_text, (panel_pos[0] + text_offset, panel_pos[1] + line2_y))

    def create_ui_icon(self, icon_type, color):
        """Crea un icono para la UI"""
        size = (24, 24)
        icon = pg.Surface(size, pg.SRCALPHA)

        if icon_type == 'heart':
            # Dibujar un corazón simple
            radius = 8
            pg.draw.circle(icon, color, (radius, radius + 4),
                           radius)  # Círculo izquierdo
            # Círculo derecho
            pg.draw.circle(icon, color, (size[0] - radius, radius + 4), radius)
            # Triángulo para la parte inferior del corazón
            points = [
                (0, radius),
                (size[0] // 2, size[1]),
                (size[0], radius)
            ]
            pg.draw.polygon(icon, color, points)

        elif icon_type == 'coin':
            # Dibujar una moneda/círculo
            radius = min(size) // 2 - 2
            pg.draw.circle(icon, color, (size[0] // 2, size[1] // 2), radius)
            # Interior más oscuro
            pg.draw.circle(icon, (200, 150, 0),
                           (size[0] // 2, size[1] // 2), radius - 3)

            # Añadir un brillo
            pg.draw.circle(icon, (255, 255, 200),
                           (size[0] // 2 - 3, size[1] // 2 - 3), 2)

        return icon

    def run(self):
        """Main game loop"""
        while self.running:
            delta_time = self.clock.tick(CONSTANTS.FPS.value) / 1000.0

            # Manejo de eventos
            self.handle_events()

            # Actualizar y dibujar según el estado del juego
            if self.game_state == "playing":
                self.update(delta_time)
                self.draw()
            elif self.game_state == "paused":
                self.draw()  # Mostrar el juego congelado detrás del menú
                # Pasar eventos a los menús (incluidos eventos de joystick)
                self.pause_menu.update(pg.event.get())
                self.pause_menu.mainloop(self.screen, disable_loop=True)
            elif self.game_state == "victory":
                self.draw()  # Mostrar el juego congelado detrás del menú
                self.victory_menu.update(pg.event.get())
                self.victory_menu.mainloop(self.screen, disable_loop=True)
            elif self.game_state == "defeat":
                self.draw()  # Mostrar el juego congelado detrás del menú
                self.defeat_menu.update(pg.event.get())
                self.defeat_menu.mainloop(self.screen, disable_loop=True)

            pg.display.flip()

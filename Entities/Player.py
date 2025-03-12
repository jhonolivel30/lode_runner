"""
    Jhon Oliver Castillo Caraballo
    22-SISN-2-063
"""

import pygame as pg
from Utils.constants import CONSTANTS, Direction
from Utils.assets import ASSETS
from Utils.setup import Setup


class Player:
    def __init__(self, map_obj, start_pos=(1, 1)):
        self.map = map_obj
        self.x, self.y = start_pos  # Posición en el grid
        # Reducir la velocidad del jugador
        self.speed = 0.15  # Velocidad de movimiento (menor valor = más lento)
        self.move_cooldown = 0  # Tiempo de espera entre movimientos
        self.direction = Direction.FRONT
        self.previous_direction = self.direction  # Add tracking of previous direction
        self.is_moving = False
        self.is_climbing = False
        self.is_falling = False
        self.is_digging = False

        # Control de tiempo para cavar
        self.dig_cooldown = 0
        self.dig_cooldown_time = 20  # Frames de espera entre excavaciones

        # Cargar imágenes para animación
        self.sprite_size = CONSTANTS.TILE_SIZE.value
        self.load_animations()

        # Variables de animación
        self.current_frame = 0
        self.animation_speed = 0.15
        self.animation_time = 0

        # Rectangle para colisiones y dibujo
        self.rect = pg.Rect(
            self.x * self.sprite_size,
            self.y * self.sprite_size,
            self.sprite_size,
            self.sprite_size
        )

        # Contadores y estados
        self.gold_collected = 0
        self.lives = 10
        self.invincible = False
        self.invincible_time = 0

    def load_animations(self):
        """Cargar todas las animaciones del jugador"""
        # Crear diccionario para las animaciones
        self.animations = {
            Direction.RIGHT: [],
            Direction.LEFT: [],
            Direction.FRONT: [],  # Para subir escaleras
            Direction.BACK: []    # Para bajar escaleras
        }

        # Cargar los frames para cada dirección
        # RIGHT
        right_assets = [
            ASSETS.PLAYER_RIGHT_1.value, ASSETS.PLAYER_RIGHT_2.value,
            ASSETS.PLAYER_RIGHT_3.value, ASSETS.PLAYER_RIGHT_4.value,
            ASSETS.PLAYER_RIGHT_5.value, ASSETS.PLAYER_RIGHT_6.value
        ]

        # LEFT
        left_assets = [
            ASSETS.PLAYER_LEFT_1.value, ASSETS.PLAYER_LEFT_2.value,
            ASSETS.PLAYER_LEFT_3.value, ASSETS.PLAYER_LEFT_4.value,
            ASSETS.PLAYER_LEFT_5.value, ASSETS.PLAYER_LEFT_6.value
        ]

        # FRONT (subiendo)
        front_assets = [
            ASSETS.PLAYER_UP_FRENTE_1.value, ASSETS.PLAYER_UP_FRENTE_2.value,
            ASSETS.PLAYER_UP_FRENTE_3.value
        ]

        # BACK (bajando)
        back_assets = [
            ASSETS.PLAYER_DOWN_ESPALDA_1.value, ASSETS.PLAYER_DOWN_ESPALDA_2.value,
            ASSETS.PLAYER_DOWN_ESPALDA_3.value
        ]

        # Función para cargar y escalar imágenes
        def load_image(path):
            try:
                img = pg.image.load(str(path))
                img = pg.transform.scale(
                    img, (self.sprite_size, self.sprite_size))
                # Establecer transparencia si es necesario
                if img.get_at((0, 0)) == (0, 0, 0):
                    img.set_colorkey((0, 0, 0))
                return img
            except Exception as e:
                print(f"Error cargando imagen {path}: {e}")
                # Crear un rectángulo de color como respaldo
                surface = pg.Surface((self.sprite_size, self.sprite_size))
                surface.fill(CONSTANTS.COLOR_RED.value)
                return surface

        # Cargar todas las imágenes
        for asset in right_assets:
            self.animations[Direction.RIGHT].append(load_image(asset))

        for asset in left_assets:
            self.animations[Direction.LEFT].append(load_image(asset))

        for asset in front_assets:
            self.animations[Direction.FRONT].append(load_image(asset))

        for asset in back_assets:
            self.animations[Direction.BACK].append(load_image(asset))

        # Imagen actual
        self.current_image = self.animations[self.direction][0]

    def animate(self, delta_time):
        """Actualiza la animación basada en el estado del jugador"""
        if self.direction != self.previous_direction:
            self.current_frame = 0
            self.previous_direction = self.direction

        if not self.is_moving and not self.is_climbing and not self.is_falling:
            # Si no se está moviendo, mantener el primer frame de la animación
            self.current_frame = 0
        else:
            # Actualizar tiempo de animación
            self.animation_time += delta_time
            if self.animation_time >= self.animation_speed:
                self.animation_time = 0

                # Avanzar al siguiente frame
                direction_frames = self.animations[self.direction]
                # Ensure we don't go out of bounds
                self.current_frame = (
                    self.current_frame + 1) % len(direction_frames)

        # Safety check to ensure current_frame is always valid
        direction_frames = self.animations[self.direction]
        if self.current_frame >= len(direction_frames):
            self.current_frame = 0

        # Actualizar la imagen actual
        self.current_image = self.animations[self.direction][self.current_frame]

    def move(self, dx, dy):
        """Intenta mover al jugador en la dirección especificada"""
        new_x = self.x + dx
        new_y = self.y + dy

        # Verificar límites del mapa
        if not (0 <= new_x < len(self.map.grid[0]) and 0 <= new_y < len(self.map.grid)):
            return False

        # Si estamos en una escalera o queremos bajar mientras estamos encima de una
        if self.is_climbing or (dy > 0 and self.map.can_climb(self.x, self.y)):
            if self.map.can_climb(new_x, new_y):
                self.x, self.y = new_x, new_y
                return True

        # Movimiento horizontal normal o caída
        if not self.map.is_solid(new_x, new_y):
            self.x, self.y = new_x, new_y
            return True

        return False

    def update_position(self):
        """Actualiza la posición del rectángulo basado en coordenadas del grid"""
        self.rect.x = int(self.x * self.sprite_size)
        self.rect.y = int(self.y * self.sprite_size)

    def check_falling(self):
        """Verifica si el jugador debería estar cayendo"""
        # Si ya está en una escalera, no debería caer
        if self.is_climbing:
            return

        # Verificar si hay soporte debajo
        has_support = self.map.can_stand_on(self.x, self.y)

        if not has_support:
            self.is_falling = True
            self.move(0, 1)  # Mover hacia abajo
        else:
            self.is_falling = False

    def collect_gold(self):
        """Intenta recoger oro en la posición actual"""
        if self.map.collect_gold(self.x, self.y):
            self.gold_collected += 1
            return True
        return False

    def dig(self, direction):
        """Intenta cavar en la dirección especificada"""
        if self.dig_cooldown > 0:
            return False

        # Solo podemos cavar cuando estamos parados en algo sólido
        if not self.map.can_stand_on(self.x, self.y) and not self.is_climbing:
            return False

        dig_x = self.x
        dig_y = self.y + 1  # Siempre cavamos debajo de nosotros

        if direction == Direction.LEFT:
            dig_x -= 1
        elif direction == Direction.RIGHT:
            dig_x += 1

        # Intentar cavar
        if self.map.dig(dig_x, dig_y):
            self.is_digging = True
            self.dig_cooldown = self.dig_cooldown_time
            return True

        return False

    def handle_input(self):
        """Procesa la entrada del teclado y joystick para mover al jugador"""
        keys = pg.key.get_pressed()

        # Obtener acciones del joystick
        joystick_actions = {}
        if Setup.has_joystick():
            joystick_actions = Setup.get_joystick_actions()

        # Store previous direction before processing input
        self.previous_direction = self.direction

        # No procesar input si estamos cayendo
        if self.is_falling:
            return

        # Reducir cooldown de excavación si está activo
        if self.dig_cooldown > 0:
            self.dig_cooldown -= 1

        # Gestionar el cooldown del movimiento
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return  # No procesar movimientos hasta que el cooldown termine

        moved = False

        # Movimiento horizontal
        if keys[pg.K_LEFT] or joystick_actions.get('LEFT', False):
            self.direction = Direction.LEFT
            if self.move(-1, 0):
                moved = True
                # Establecer cooldown basado en velocidad
                self.move_cooldown = int(1 / self.speed)
        elif keys[pg.K_RIGHT] or joystick_actions.get('RIGHT', False):
            self.direction = Direction.RIGHT
            if self.move(1, 0):
                moved = True
                # Establecer cooldown basado en velocidad
                self.move_cooldown = int(1 / self.speed)

        # Movimiento vertical (escaleras)
        if self.map.can_climb(self.x, self.y):
            if keys[pg.K_UP] or joystick_actions.get('UP', False):
                self.direction = Direction.FRONT
                self.is_climbing = True
                if self.move(0, -1):
                    moved = True
                    # Establecer cooldown basado en velocidad
                    self.move_cooldown = int(1 / self.speed)
            elif keys[pg.K_DOWN] or joystick_actions.get('DOWN', False):
                self.direction = Direction.BACK
                self.is_climbing = True
                if self.move(0, 1):
                    moved = True
                    # Establecer cooldown basado en velocidad
                    self.move_cooldown = int(1 / self.speed)
            else:
                # Si no estamos presionando teclas de movimiento vertical,
                # seguimos en la escalera pero no nos movemos
                self.is_climbing = True
        else:
            self.is_climbing = False

        # Excavar bloques - con teclado o joystick
        if keys[pg.K_z] or joystick_actions.get('DIG_LEFT', False):
            self.dig(Direction.LEFT)
        elif keys[pg.K_x] or joystick_actions.get('DIG_RIGHT', False):
            self.dig(Direction.RIGHT)

        self.is_moving = moved

    def update(self, delta_time=1/60):
        """Actualiza el estado del jugador"""
        # Procesar input
        self.handle_input()

        # Verificar caída
        self.check_falling()

        # Actualizar invulnerabilidad
        if self.invincible:
            self.invincible_time -= 1
            if self.invincible_time <= 0:
                self.invincible = False

        # Recoger oro si está en la posición actual
        self.collect_gold()

        # Actualizar animación
        self.animate(delta_time)

        # Actualizar posición del rectángulo
        self.update_position()

        # Actualizar estado de invulnerabilidad
        if hasattr(self, 'invulnerable') and self.invulnerable:
            self.invulnerable_timer += delta_time
            if self.invulnerable_timer >= self.invulnerable_duration:
                self.invulnerable = False

    def draw(self, surface):
        """Dibuja al jugador en la superficie proporcionada"""
        # Si es invulnerable, parpadear
        if self.invincible and self.invincible_time % 6 >= 3:
            return  # No dibujar cada pocos frames para crear efecto de parpadeo

        surface.blit(self.current_image, self.rect)

    def hit(self):
        """Cuando el jugador es golpeado por un enemigo"""
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            # Invulnerable por 90 frames (1.5 segundos a 60 FPS)
            self.invincible_time = 90
            return True
        return False

    def is_at_exit(self):
        """Verificar si el jugador está en la salida abierta"""
        return (self.x, self.y) == self.map.exit_pos and self.map.is_exit_open()

    def check_enemy_collision(self, enemy):
        """Detecta si hay colisión entre el jugador y un enemigo"""
        # Definir el área de colisión (puede ajustarse según el tamaño del sprite)
        player_rect = pg.Rect(self.x * self.sprite_size, self.y * self.sprite_size,
                              self.sprite_size, self.sprite_size)
        enemy_rect = pg.Rect(enemy.x * enemy.sprite_size, enemy.y * enemy.sprite_size,
                             enemy.sprite_size, enemy.sprite_size)

        # Verificar colisión
        if player_rect.colliderect(enemy_rect):
            # Solo registrar una colisión si no estamos en período de invulnerabilidad
            if not self.invincible:
                return self.hit()  # Use the hit method which already handles invincibility
        return False

"""
    Jhon Oliver Castillo Caraballo
    22-SISN-2-063
"""

import pygame as pg
import random
import math
from Utils.constants import Direction, CONSTANTS
from Utils.assets import ASSETS
from IA.a_star import AStar


class EnemyState:
    IDLE = 0
    PATROLLING = 1
    PURSUING = 2


class Enemy:
    def __init__(self, map_obj, player, start_pos=(1, 1)):
        self.map = map_obj  # Objeto del mapa
        self.player = player  # Referencia al jugador
        self.x, self.y = start_pos  # Posición en el grid
        self.sprite_size = CONSTANTS.TILE_SIZE.value  # Tamaño del sprite

        # AÑADIR: Posición precisa en píxeles para movimiento suave
        self.pixel_x = self.x * self.sprite_size
        self.pixel_y = self.y * self.sprite_size

        # Guardar la posición inicial para patrullaje
        self.initial_position = start_pos
        self.patrol_radius = 3  # Reducido de 5 a 3 para patrullas más concentradas

        # Variables de movimiento y comportamiento
        self.speed = 0.05  # Reducido de 0.07 a 0.05
        self.pixel_speed = 0.8  # Reducido de 2.0 a 0.8 para movimiento más lento
        self.move_cooldown = 0  # Tiempo entre movimientos
        self.vision_range = 3  # Reducido de 5 a 3 para dar mejor oportunidad de escape
        self.direction = Direction.RIGHT  # Dirección inicial
        self.is_moving = False
        self.is_climbing = False
        self.is_falling = False
        self.is_chasing = False  # Indica si está persiguiendo al jugador

        # Control de patrulla
        self.patrol_direction = self._get_random_direction()
        self.patrol_timer = 0
        self.patrol_duration = 120  # Aumentado de 60 a 120 para patrullas más lentas

        # AÑADIR: Puntos de patrulla para mantener a los enemigos en su zona
        self.patrol_points = self._generate_patrol_points()
        self.current_patrol_point = 0
        self.patrol_wait_timer = 0
        self.patrol_wait_duration = 40  # Esperar un tiempo antes de cambiar de punto

        # Camino para persecución (A*)
        self.pathfinder = AStar(self.map)
        self.current_path = []
        self.path_index = 0
        self.path_update_timer = 0
        # Aumentado de 45 a 60 para actualizar rutas con menos frecuencia
        self.path_update_interval = 60

        # AÑADIR: Target pixel position para movimiento suave
        self.target_pixel_x = self.pixel_x
        self.target_pixel_y = self.pixel_y
        self.reached_target = True  # Flag para controlar si se alcanzó la posición objetivo

        # Estado de persecución
        self.chase_duration = 60  # Reducido de 80 a 60 frames
        self.chase_timer = 0
        self.last_seen_pos = None
        # Reducir velocidad durante persecución (era 1.0 implícitamente)
        self.chase_speed_multiplier = 0.7

        # Animación - hacer más lenta para mejor sincronización con movimiento
        self.load_animations()
        self.current_frame = 0
        self.animation_speed = 0.25  # Aumentado de 0.2 a 0.25 para animación más lenta
        self.animation_time = 0
        self.previous_direction = self.direction
        self.frame_skip_counter = 0  # Contador para evitar saltos en la animación

        # Rectángulo para colisiones y dibujo
        self.rect = pg.Rect(
            self.pixel_x,
            self.pixel_y,
            self.sprite_size,
            self.sprite_size
        )

        # Debug
        self.debug = False
        # Color para ruta de depuración
        self.path_color = (255, 100, 100)  # Rojo para la ruta

    def load_animations(self):
        """Cargar todas las animaciones del enemigo"""
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
            ASSETS.ENEMY_RIGHT_1.value, ASSETS.ENEMY_RIGHT_2.value,
            ASSETS.ENEMY_RIGHT_3.value, ASSETS.ENEMY_RIGHT_4.value
        ]

        # LEFT
        left_assets = [
            ASSETS.ENEMY_LEFT_1.value, ASSETS.ENEMY_LEFT_2.value,
            ASSETS.ENEMY_LEFT_3.value, ASSETS.ENEMY_LEFT_4.value
        ]

        # FRONT (bajando)
        front_assets = [
            ASSETS.ENEMY_DOWN_FRENTE_1.value, ASSETS.ENEMY_DOWN_FRENTE_2.value,
            ASSETS.ENEMY_DOWN_FRENTE_3.value
        ]

        # BACK (subiendo)
        back_assets = [
            ASSETS.ENEMY_UP_ESPALDA_1.value, ASSETS.ENEMY_UP_ESPALDA_2.value,
            ASSETS.ENEMY_UP_ESPALDA_3.value
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

    def _get_random_direction(self):
        """Retorna una dirección aleatoria para patrulla"""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        return random.choice(directions)

    def _generate_patrol_points(self):
        """Genera puntos de patrulla alrededor de la posición inicial"""
        points = []
        x, y = self.initial_position

        # Generar varios puntos de patrulla en un rango alrededor de la posición inicial
        for _ in range(4):
            # Generar un punto aleatorio dentro del radio de patrulla
            dx = random.randint(-self.patrol_radius, self.patrol_radius)
            dy = random.randint(-self.patrol_radius, self.patrol_radius)

            patrol_x = max(0, min(self.map.width - 1, x + dx))
            patrol_y = max(0, min(self.map.height - 1, y + dy))

            # Verificar que el punto sea válido (no es un muro)
            if not self.map.is_solid(patrol_x, patrol_y):
                points.append((patrol_x, patrol_y))

        # Si no se generaron puntos válidos, usar la posición inicial
        if not points:
            points = [(x, y)]

        return points

    def animate(self, delta_time):
        """Actualiza la animación basada en el estado del enemigo"""
        if self.direction != self.previous_direction:
            self.current_frame = 0
            self.previous_direction = self.direction

        # Solo animar si estamos en movimiento
        if self.is_moving or self.is_climbing or self.is_falling:
            # Actualizar tiempo de animación con interpolación más suave
            self.animation_time += delta_time * 0.6  # Factor más lento
            if self.animation_time >= self.animation_speed:
                self.animation_time = 0

                # Avanzar al siguiente frame solo si estamos en movimiento
                # para evitar animaciones durante pausas
                direction_frames = self.animations[self.direction]
                if self.is_moving:
                    self.frame_skip_counter += 1
                    if self.frame_skip_counter >= 2:  # Solo avanzar cada 2 actualizaciones
                        self.current_frame = (
                            self.current_frame + 1) % len(direction_frames)
                        self.frame_skip_counter = 0
        else:
            # Si no está en movimiento, mantener el primer frame
            self.current_frame = 0

        # Verificar que current_frame sea válido
        direction_frames = self.animations[self.direction]
        if self.current_frame >= len(direction_frames):
            self.current_frame = 0

        # Actualizar la imagen actual
        self.current_image = self.animations[self.direction][self.current_frame]

    def move(self, dx, dy):
        """Intenta mover al enemigo en la dirección especificada"""
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

    def move_smooth(self, target_x, target_y):
        """Mueve al enemigo suavemente hacia el objetivo, en píxeles"""
        # Calcular la dirección hacia el objetivo
        dx = target_x - self.pixel_x
        dy = target_y - self.pixel_y

        # Normalizar el vector de dirección
        distance = math.sqrt(dx*dx + dy*dy)

        # Aplicar velocidad adecuada basada en estado
        actual_speed = self.pixel_speed
        if self.is_chasing:
            actual_speed *= self.chase_speed_multiplier

        # Velocidad extra cuando está en escalera para evitar que se atasque
        if self.is_climbing:
            actual_speed *= 1.2

        if distance < actual_speed:
            # Si estamos muy cerca del objetivo, ir directamente a él
            self.pixel_x = target_x
            self.pixel_y = target_y
            self.is_moving = False
            self.reached_target = True
            return True
        else:
            # Avanzar en la dirección calculada
            self.is_moving = True
            self.reached_target = False
            factor = actual_speed / distance
            self.pixel_x += dx * factor
            self.pixel_y += dy * factor

            # Actualizar las coordenadas del grid basándonos en la posición en píxeles
            grid_x = int(self.pixel_x / self.sprite_size)
            grid_y = int(self.pixel_y / self.sprite_size)

            # Solo actualizar coordenadas del grid cuando realmente cambiamos de celda
            if grid_x != self.x or grid_y != self.y:
                self.x = grid_x
                self.y = grid_y

            # Actualizar la dirección para animación
            if self.is_climbing:
                # Si estamos en una escalera, mantener la dirección adecuada
                if dy > 0:
                    self.direction = Direction.FRONT  # Bajando
                else:
                    self.direction = Direction.BACK   # Subiendo
            else:
                # Si no estamos en escalera, actualizar dirección horizontal
                if abs(dx) > abs(dy):
                    self.direction = Direction.RIGHT if dx > 0 else Direction.LEFT

            return False

    def update_position(self):
        """Actualiza la posición del rectángulo basado en coordenadas en píxeles"""
        self.rect.x = int(self.pixel_x)
        self.rect.y = int(self.pixel_y)

    def check_falling(self):
        """Verifica si el enemigo debería estar cayendo"""
        # Si ya está en una escalera, no debería caer
        if self.is_climbing:
            return

        # Verificar si hay soporte debajo
        has_support = self.map.can_stand_on(self.x, self.y)

        if not has_support:
            self.is_falling = True
            # Calcular centro del próximo tile
            target_y = (self.y + 1) * self.sprite_size
            self.target_pixel_y = target_y

            # Mover suavemente hacia abajo
            if self.move_smooth(self.pixel_x, self.target_pixel_y):
                self.y += 1  # Actualizar posición en la grid
        else:
            self.is_falling = False

    def is_player_visible(self):
        """Verifica si el jugador está dentro del rango de visión"""
        # Obtener posiciones
        player_x, player_y = self.player.x, self.player.y

        # Calcular distancia Manhattan
        distance = abs(self.x - player_x) + abs(self.y - player_y)

        # Si está fuera del rango, no es visible
        if distance > self.vision_range:
            return False

        # Verificar línea de visión usando A*
        path = self.pathfinder.find_path(
            (self.x, self.y), (player_x, player_y))

        # Si hay un camino corto, consideramos que hay línea de visión
        return len(path) <= self.vision_range + 2

    def update_path_to_player(self):
        """Actualiza el camino hacia el jugador usando A*"""
        player_x, player_y = self.player.x, self.player.y

        # Si el enemigo está en una escalera, asegurarse de que termina el movimiento en la escalera
        # antes de recalcular la ruta para evitar quedarse atascado a mitad de subida/bajada
        if self.is_climbing and not self.reached_target and self.current_path:
            return

        self.current_path = self.pathfinder.find_path(
            (self.x, self.y), (player_x, player_y))
        self.path_index = 0
        self.last_seen_pos = (player_x, player_y)

    def patrol(self):
        """Comportamiento de patrulla más inteligente usando puntos predefinidos"""
        # Si no tenemos puntos de patrulla o estamos esperando
        if len(self.patrol_points) == 0:
            self.patrol_points = self._generate_patrol_points()
            return

        # Si hemos llegado al destino actual, esperar un poco antes de moverse de nuevo
        if self.reached_target and self.path_index >= len(self.current_path):
            self.patrol_wait_timer += 1
            if self.patrol_wait_timer < self.patrol_wait_duration:
                self.is_moving = False  # Asegurarse de que no se mueve durante la espera
                return

            # Reiniciar el temporizador y seleccionar el siguiente punto
            self.patrol_wait_timer = 0
            self.current_patrol_point = (
                self.current_patrol_point + 1) % len(self.patrol_points)
            target = self.patrol_points[self.current_patrol_point]

            # Buscar camino hacia el punto usando A*
            self.current_path = self.pathfinder.find_path(
                (self.x, self.y), target)
            self.path_index = 0

        # Seguir el camino actual si tenemos uno
        if self.current_path and self.path_index < len(self.current_path):
            self.follow_path()
        else:
            # Si no hay camino válido, generar nuevos puntos de patrulla
            self.patrol_points = self._generate_patrol_points()

    def follow_path(self):
        """Sigue el camino actual punto por punto con movimiento suave"""
        # Asegurarse de que tenemos un camino válido
        if not self.current_path or self.path_index >= len(self.current_path):
            self.reached_target = True
            return

        # Obtener el siguiente punto del camino
        next_pos = self.current_path[self.path_index]

        # Calcular posición objetivo en píxeles (centro del tile)
        target_pixel_x = next_pos[0] * self.sprite_size
        target_pixel_y = next_pos[1] * self.sprite_size

        # Comprobar si el siguiente movimiento implica usar una escalera
        if self.path_index > 0 and self.path_index < len(self.current_path):
            current_x, current_y = self.x, self.y
            next_x, next_y = next_pos

            # Detectar movimiento vertical (escalera)
            if next_y != current_y:
                if self.map.can_climb(current_x, current_y) and self.map.can_climb(next_x, next_y):
                    self.is_climbing = True
                    # Ajustar dirección para animación
                    self.direction = Direction.BACK if next_y < current_y else Direction.FRONT
                else:
                    self.is_climbing = False
            else:
                # Mantener estado de escalera si estamos en una
                self.is_climbing = self.map.can_climb(current_x, current_y)

        # Mover suavemente hacia el objetivo
        if self.move_smooth(target_pixel_x, target_pixel_y):
            # Si llegamos al punto objetivo, avanzar al siguiente
            self.path_index += 1

    def chase_player(self):
        """Persigue al jugador usando A* y movimiento suave"""
        # Si no hay un camino o es momento de actualizarlo
        self.path_update_timer += 1
        if not self.current_path or self.path_update_timer >= self.path_update_interval:
            self.update_path_to_player()
            self.path_update_timer = 0

        # Seguir el camino calculado
        self.follow_path()

    def update(self, delta_time=1/60):
        """Actualiza el estado del enemigo"""
        # Reducir cooldown de movimiento
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

        # Verificar caída
        self.check_falling()

        # Si está cayendo, no procesar otros comportamientos
        if self.is_falling:
            # Ajustar dirección para animación de caída
            self.direction = Direction.BACK
            self.is_moving = True
        else:
            # Verificar si el jugador es visible
            player_visible = self.is_player_visible()

            # Establecer/mantener estado de persecución
            if player_visible:
                self.is_chasing = True
                self.chase_timer = self.chase_duration
            elif self.is_chasing:
                self.chase_timer -= 1
                if self.chase_timer <= 0:
                    self.is_chasing = False

            # Comportamiento basado en estado
            if self.is_chasing:
                self.chase_player()
            else:
                self.patrol()

        # Actualizar animación
        self.animate(delta_time)

        # Actualizar posición del rectángulo basado en posición en píxeles
        self.update_position()

    def draw(self, surface):
        """Dibuja al enemigo en la superficie proporcionada"""
        surface.blit(self.current_image, self.rect)

        # Para debug: dibujar el camino actual como líneas conectadas
        if self.debug and self.current_path and len(self.current_path) > 1:
            # Dibujar puntos y líneas entre ellos
            for i in range(len(self.current_path) - 1):
                start_pos = self.current_path[i]
                end_pos = self.current_path[i + 1]

                # Convertir coordenadas de grid a píxeles (centrando en el bloque)
                start_x = start_pos[0] * \
                    self.sprite_size + self.sprite_size // 2
                start_y = start_pos[1] * \
                    self.sprite_size + self.sprite_size // 2
                end_x = end_pos[0] * self.sprite_size + self.sprite_size // 2
                end_y = end_pos[1] * self.sprite_size + self.sprite_size // 2

                # Dibujar línea entre puntos
                pg.draw.line(surface, self.path_color, (start_x, start_y),
                             (end_x, end_y), 2)

                # Dibujar pequeños círculos en los puntos de la ruta
                pg.draw.circle(surface, self.path_color, (start_x, start_y), 3)

            # Dibujar el último punto
            if self.current_path:
                last_pos = self.current_path[-1]
                last_x = last_pos[0] * self.sprite_size + self.sprite_size // 2
                last_y = last_pos[1] * self.sprite_size + self.sprite_size // 2
                # Punto final en amarillo
                pg.draw.circle(surface, (255, 255, 0), (last_x, last_y), 4)

            # Marcar posición actual en la ruta
            if 0 <= self.path_index < len(self.current_path):
                current_target = self.current_path[self.path_index]
                target_x = current_target[0] * \
                    self.sprite_size + self.sprite_size // 2
                target_y = current_target[1] * \
                    self.sprite_size + self.sprite_size // 2
                # Punto actual en verde
                pg.draw.circle(surface, (0, 255, 0), (target_x, target_y), 5)

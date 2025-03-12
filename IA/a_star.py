"""
    Jhon Oliver Castillo Caraballo
    22-SISN-2-063
"""
import heapq


class AStar:
    def __init__(self, game_map):
        self.map = game_map
        # Reducir distancia máxima de búsqueda para rutas más cortas
        self.max_search_distance = 25  # Reducido de 40 a 25
        self.cache = {}  # Cache para almacenar caminos frecuentes
        # Store map dimensions for easy access
        self.width = len(game_map.grid[0]) if game_map.grid else 0
        self.height = len(game_map.grid) if game_map.grid else 0

        # Add property to map object for easy access
        game_map.width = self.width
        game_map.height = self.height

    def heuristic(self, a, b):
        # Usar distancia Manhattan para la heurística
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos):
        x, y = pos
        # Priorizar movimiento vertical cuando estamos en escaleras
        if self.map.can_climb(x, y):
            # Primero arriba/abajo, luego laterales
            directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        else:
            # Priorizar movimiento lateral y caída
            directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        neighbors = []

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            # Verificar límites del mapa
            if not (0 <= new_x < self.width and 0 <= new_y < self.height):
                continue

            # Evaluar si podemos movernos a esta nueva posición
            if self.is_walkable(new_x, new_y, x, y):
                neighbors.append((new_x, new_y))

        return neighbors

    def is_walkable(self, x, y, from_x=None, from_y=None):
        """Determina si una posición es caminable desde la posición actual"""
        # Si no tenemos una posición de origen, consideramos accesibilidad general
        if from_x is None or from_y is None:
            # Una posición es caminable si:
            # 1. No es sólida (no es un muro) o
            # 2. Es una escalera (se puede escalar)
            return (not self.map.is_solid(x, y) or
                    self.map.can_climb(x, y))

        # Casos específicos basados en dirección del movimiento
        moving_up = from_y > y
        moving_down = from_y < y
        moving_horizontal = from_y == y

        # Si nos movemos hacia abajo, necesitamos una escalera o caer sobre algo sólido
        if moving_down:
            # Bajando por una escalera
            if self.map.can_climb(x, y):
                return True
            # Cayendo sobre un bloque
            if not self.map.is_solid(x, y) and self.map.can_stand_on(x, y):
                return True
            return False

        # Si nos movemos hacia arriba, necesitamos estar en una escalera
        elif moving_up:
            # Solo podemos subir si hay una escalera en la posición actual y la siguiente
            return self.map.can_climb(from_x, from_y) and self.map.can_climb(x, y)

        # Si nos movemos horizontalmente
        elif moving_horizontal:
            # Podemos movernos horizontalmente si:
            # 1. El destino no es sólido y
            # 2. Podemos pararnos en él (tiene soporte) o es una escalera
            return (not self.map.is_solid(x, y) and
                    (self.map.can_stand_on(x, y) or self.map.can_climb(x, y)))

        # Por defecto, aplicar la regla general
        return (not self.map.is_solid(x, y) or
                self.map.can_climb(x, y))

    def find_path(self, start, goal):
        # Si el inicio y fin son iguales, devolver un camino con un solo punto
        if start == goal:
            return [start]

        # Verificar el caché primero
        cache_key = (start, goal)
        if cache_key in self.cache:
            return self.cache[cache_key].copy()

        # Si la distancia es demasiado grande, usar un camino aproximado
        if self.heuristic(start, goal) > self.max_search_distance:
            return self.find_approximate_path(start, goal)

        # Implementación estándar A*
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                break

            # Optimización: si la distancia es excesiva, abortar
            if cost_so_far[current] > self.max_search_distance * 1.5:
                break

            for next_pos in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    # Aumentar peso de la heurística para caminos más directos
                    priority = new_cost + self.heuristic(goal, next_pos) * 1.2
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        if goal not in came_from:
            # Si no hay camino al objetivo, buscar el punto más cercano alcanzable
            closest = min(came_from.keys(), key=lambda pos: self.heuristic(
                pos, goal), default=start)
            if closest == start:
                return []
            goal = closest

        # Reconstruir el camino
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()

        # Simplificar el camino eliminando puntos innecesarios
        if len(path) > 2:
            path = self.simplify_path(path)

        # Guardar en caché para uso futuro (solo si no es demasiado largo)
        if len(path) <= 15:  # Reducido de 20 a 15
            self.cache[cache_key] = path.copy()

        return path

    def simplify_path(self, path):
        """Simplifica el camino eliminando puntos innecesarios en línea recta"""
        if len(path) < 3:
            return path

        simplified = [path[0]]  # Siempre incluir el primer punto

        i = 0
        while i < len(path) - 1:
            # Comprobar si podemos eliminar puntos intermedios
            current = path[i]

            # Buscar el punto más lejano que se puede alcanzar en línea recta
            furthest = i + 1
            for j in range(i + 2, len(path)):
                # Verificar si hay línea recta entre current y path[j]
                if self.is_straight_line_clear(current, path[j]):
                    furthest = j
                else:
                    break

            simplified.append(path[furthest])
            i = furthest

        return simplified

    def is_straight_line_clear(self, start, end):
        """Verifica si hay un camino en línea recta entre start y end"""
        # Implementación básica de Bresenham para líneas rectas
        x0, y0 = start
        x1, y1 = end

        # Si son el mismo punto o adyacentes, la línea está despejada
        if abs(x1-x0) <= 1 and abs(y1-y0) <= 1:
            return True

        # Caso especial: línea horizontal
        if y0 == y1:
            min_x, max_x = min(x0, x1), max(x0, x1)
            for x in range(min_x + 1, max_x):
                if not self.is_walkable(x, y0):
                    return False
            return True

        # Caso especial: línea vertical
        if x0 == x1:
            min_y, max_y = min(y0, y1), max(y0, y1)
            for y in range(min_y + 1, max_y):
                if not self.is_walkable(x0, y):
                    return False
            return True

        # Para caminos diagonales u otros más complejos, siempre retornar False
        # para evitar atravesar paredes o hacer movimientos imposibles
        return False

    def find_approximate_path(self, start, goal):
        """Encuentra un camino aproximado cuando el objetivo está muy lejos"""
        # Dirección general hacia el objetivo
        path = [start]
        current_x, current_y = start
        goal_x, goal_y = goal

        # Calcular una trayectoria en línea recta hasta el límite de búsqueda
        steps = min(self.max_search_distance, self.heuristic(start, goal))
        for _ in range(steps):
            # Determinar dirección principal
            if abs(current_x - goal_x) > abs(current_y - goal_y):
                dx = 1 if current_x < goal_x else -1
                dy = 0
            else:
                dx = 0
                dy = 1 if current_y < goal_y else -1

            # Verificar si la nueva posición es válida
            new_x, new_y = current_x + dx, current_y + dy
            if (0 <= new_x < self.width and
                0 <= new_y < self.height and
                    self.is_walkable(new_x, new_y)):
                current_x, current_y = new_x, new_y
                path.append((current_x, current_y))
            else:
                # Intentar otra dirección
                if dx != 0:  # Si estábamos moviéndonos horizontalmente
                    dy = 1 if current_y < goal_y else -1
                    dx = 0
                else:  # Si estábamos moviéndonos verticalmente
                    dx = 1 if current_x < goal_x else -1
                    dy = 0

                # Verificar la nueva dirección
                new_x, new_y = current_x + dx, current_y + dy
                if (0 <= new_x < self.width and
                    0 <= new_y < self.height and
                        self.is_walkable(new_x, new_y)):
                    current_x, current_y = new_x, new_y
                    path.append((current_x, current_y))

        return path

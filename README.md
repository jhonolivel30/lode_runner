# Proyecto de Juego Lode Runner

## Introducción

Lode Runner es una recreación de un juego de plataformas clásico desarrollado en Python utilizando la biblioteca Pygame. Este proyecto implementa las mecánicas principales del juego original de 1983 donde los jugadores navegan a través de niveles, recolectando oro mientras evitan enemigos. El juego presenta navegación por plataformas, escalada de escaleras y la característica mecánica de excavación que permite a los jugadores crear hoyos temporalmente para atrapar enemigos.

## Descripción del Juego

En Lode Runner, controlas un personaje que debe recolectar todas las piezas de oro en un nivel antes de escapar a través de una salida que se abre una vez que todo el oro es recolectado. Los enemigos patrullan el nivel y perseguirán al jugador cuando estén cerca. Los jugadores pueden cavar hoyos a ambos lados para atrapar temporalmente a los enemigos y crear nuevos caminos.

## Características

- Mecánicas de juego clásicas: Correr, subir escaleras, cavar hoyos
- IA de enemigos con capacidades de búsqueda de rutas
- Sistema de progresión basado en niveles
- Gráficos y efectos de sonido de estilo retro
- Soporte para controladores (gamepad y teclado)
- Sistema de menús con función de pausa del juego
- Pantallas de victoria y derrota
- Modo de depuración para visualizar la búsqueda de rutas de enemigos

## Estructura del Proyecto

```
LodeRunner/
│
├── lode_runner.py           # Punto de entrada principal
│
├── Game/                    # Lógica principal del juego
│   ├── game.py              # Bucle principal y gestión de estados
│   ├── levels.py            # Definiciones y carga de niveles
│   └── map.py               # Renderizado de mapas y detección de colisiones
│
├── Entities/                # Entidades del juego
│   ├── Player.py            # Lógica del personaje del jugador
│   └── Enemy.py             # IA y comportamiento de enemigos
│
├── IA/                      # Inteligencia artificial
│   ├── a_star.py            # Implementación de búsqueda de rutas A*
│   └── node.py              # Nodos de árbol de comportamiento para toma de decisiones de IA
│
├── Utils/                   # Módulos de utilidad
│   ├── assets.py            # Rutas y gestión de recursos
│   ├── constants.py         # Constantes y configuración del juego
│   ├── setup.py             # Inicialización del juego y configuración del controlador
│   ├── strings.py           # Cadenas de texto utilizadas en el juego
│   └── theme.py             # Tematización de UI y creación de menús
│
└── assets/                  # Recursos del juego (imágenes, sonidos, música)
    ├── Graphics/            # Imágenes de sprites y fondos
    └── music/               # Efectos de sonido y música de fondo
```

## Instalación

### Requisitos

- Python 3.x
- Pygame
- Pygame_menu

### Instrucciones de Configuración

1. Clona el repositorio o descarga el código fuente
2. Instala los paquetes requeridos:
   ```
   pip install -r requirements.txt
   ```
3. Ejecuta el juego:
   ```
   python lode_runner.py
   ```

## Cómo Jugar

### Controles

- **Teclas de Flecha**: Mover el personaje jugador (izquierda, derecha, arriba, abajo)
- **Arriba/Abajo**: Subir y bajar escaleras
- **Tecla Z**: Cavar un hoyo a la izquierda
- **Tecla X**: Cavar un hoyo a la derecha
- **ESC**: Pausar el juego
- **D**: Alternar modo de depuración (muestra la búsqueda de rutas de enemigos)

### Soporte para Controladores

El juego soporta gamepads con el siguiente mapeo predeterminado:

- **D-Pad/Joystick Izquierdo**: Mover el personaje jugador
- **Botón A/X**: Cavar un hoyo a la izquierda
- **Botón B/O**: Cavar un hoyo a la derecha
- **Botón Start**: Pausar/Reanudar juego
- **Botón Select/Share**: Volver al menú principal

## Mecánicas del Juego

### Movimiento

- El jugador puede moverse izquierda y derecha en plataformas
- Subir y bajar escaleras
- Caer si no hay plataforma debajo

### Excavación

- Los jugadores pueden cavar hoyos en plataformas perforables a la izquierda o derecha
- Los hoyos permanecen abiertos temporalmente y luego se rellenan
- Los enemigos pueden caer en los hoyos, quedando atrapados temporalmente

### Colección de Oro

- Todas las piezas de oro deben ser recolectadas para abrir la salida
- La salida aparece como una escalera una vez que todo el oro es recolectado
- Alcanza la salida para completar el nivel

### Sistema de Vidas

- El jugador comienza con múltiples vidas
- Chocar con un enemigo resulta en la pérdida de una vida
- Después de perder una vida, el jugador se vuelve temporalmente invulnerable
- El juego termina cuando se pierden todas las vidas

## Implementación Técnica

### Sistema Basado en Casillas

El juego utiliza un sistema de cuadrícula basado en casillas para el diseño del nivel y la detección de colisiones. Cada casilla puede representar:

- Espacio vacío
- Plataformas de ladrillo (sólidas)
- Terreno excavable
- Escaleras para movimiento vertical
- Coleccionables de oro
- Puntos de salida

### IA de Enemigos

Los enemigos usan una combinación de árboles de comportamiento y búsqueda de rutas A*:

- **Árbol de Comportamiento**: Gestiona la toma de decisiones (patrullar, perseguir, atacar)
- **Búsqueda de Rutas A***: Calcula rutas óptimas para alcanzar al jugador
- **Seguimiento de Ruta**: Permite a los enemigos navegar por la estructura compleja del nivel
- **Detección del Jugador**: Los enemigos detectan al jugador dentro de cierto rango

### Gestión de Estados

El juego implementa diferentes estados:

- Menú principal
- Jugabilidad
- Pausado
- Victoria
- Derrota

Cada estado tiene su propia lógica de actualización y renderizado, con transiciones suaves entre estados.

## Desarrollo

### Modo de Depuración

Presiona 'D' durante el juego para habilitar el modo de depuración, que muestra:

- Rutas de búsqueda de enemigos
- Radio de detección de enemigos
- Estado actual del enemigo (patrullar/perseguir)

### Ampliación del Juego

Para añadir nuevos niveles:

1. Modifica el método `load_level` en `levels.py`
2. Crea nuevos diseños de cuadrícula usando los valores de tipo de casilla
3. Ajusta las posiciones de aparición de enemigos en `Game/game.py`

## Créditos

- **Desarrollador**: Jhon Oliver Castillo Caraballo (22-SISN-2-063)
- **Juego Original**: Lode Runner por Douglas E. Smith (1983)
- **Bibliotecas Utilizadas**: Pygame, Pygame_menu

## Licencia

Este proyecto es una implementación educativa y no para uso comercial. Todos los recursos y conceptos originales del juego pertenecen a sus respectivos propietarios.

---

_"Lode Runner es un juego de plataformas clásico donde la estrategia se encuentra con la acción. ¡Navega por los niveles, recoge todo el oro y escapa mientras burlas a tus perseguidores!"_

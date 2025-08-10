import pygame
import random
import sys
import math

# Inicializar pygame
pygame.init()

# Colores mejorados
BLACK = (15, 15, 23)
WHITE = (255, 255, 255)
RED = (231, 76, 60)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)
ORANGE = (230, 126, 34)
DARK_GREEN = (39, 174, 96)
LIGHT_GRAY = (189, 195, 199)
DARK_GRAY = (44, 62, 80)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (77, 166, 255)
OBSTACLE_COLOR = (127, 140, 141)
OBSTACLE_GLOW = (236, 240, 241)
LASER_COLOR = (255, 0, 255)
POWER_COLOR = (255, 215, 0)

# Configuración de la pantalla
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
UI_HEIGHT = 80  # Altura reservada para la UI
CELL_SIZE = 25
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = (WINDOW_HEIGHT - UI_HEIGHT) // CELL_SIZE

# Configuración del juego por dificultad
DIFFICULTY_SETTINGS = {
    "facil": {"fps": 8, "obstacles": False, "moving_obstacles": False, "num_obstacles": 0},
    "medio": {"fps": 12, "obstacles": True, "moving_obstacles": False, "num_obstacles": (8, 14)},
    "dificil": {"fps": 16, "obstacles": True, "moving_obstacles": True, "num_obstacles": (12, 18)}
}

class Laser:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.trail = []
        self.life = 15  # Duración del láser
        
    def update(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:
            self.trail.pop(0)
            
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.life -= 1
        
        # Wrap around
        self.x = self.x % GRID_WIDTH
        self.y = self.y % GRID_HEIGHT
        
    def is_alive(self):
        return self.life > 0
        
    def draw(self, screen):
        # Dibujar rastro del láser
        for i, (x, y) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail))) if self.trail else 255
            size = max(1, int(CELL_SIZE * 0.3 * (i / len(self.trail)))) if self.trail else CELL_SIZE // 3
            laser_color = (LASER_COLOR[0], LASER_COLOR[1], LASER_COLOR[2])
            pygame.draw.circle(screen, laser_color, 
                             (x * CELL_SIZE + CELL_SIZE // 2, 
                              y * CELL_SIZE + CELL_SIZE // 2 + UI_HEIGHT), size)
        
        # Dibujar cabeza del láser
        pygame.draw.circle(screen, (255, 255, 255),
                         (self.x * CELL_SIZE + CELL_SIZE // 2,
                          self.y * CELL_SIZE + CELL_SIZE // 2 + UI_HEIGHT), CELL_SIZE // 2)
        pygame.draw.circle(screen, LASER_COLOR,
                         (self.x * CELL_SIZE + CELL_SIZE // 2,
                          self.y * CELL_SIZE + CELL_SIZE // 2 + UI_HEIGHT), CELL_SIZE // 3)

class Obstacle:
    def __init__(self, x, y, shape="square"):
        self.x = x
        self.y = y
        self.shape = shape
        self.visible = True
        self.blink_timer = random.randint(30, 180)  # Timer aleatorio inicial
        self.blink_speed = random.randint(40, 120)  # Velocidad aleatoria de parpadeo
        self.positions = self.generate_shape()
    
    def generate_shape(self):
        positions = [(self.x, self.y)]
        
        if self.shape == "L":
            positions.extend([
                (self.x, self.y + 1),
                (self.x, self.y + 2),
                (self.x + 1, self.y + 2)
            ])
        elif self.shape == "T":
            positions.extend([
                (self.x - 1, self.y),
                (self.x + 1, self.y),
                (self.x, self.y + 1)
            ])
        elif self.shape == "line":
            positions.extend([
                (self.x, self.y + 1),
                (self.x, self.y + 2)
            ])
        elif self.shape == "block":
            positions.extend([
                (self.x + 1, self.y),
                (self.x, self.y + 1),
                (self.x + 1, self.y + 1)
            ])
        elif self.shape == "cross":
            positions.extend([
                (self.x - 1, self.y),
                (self.x + 1, self.y),
                (self.x, self.y - 1),
                (self.x, self.y + 1)
            ])
        elif self.shape == "diagonal":
            positions.extend([
                (self.x + 1, self.y + 1),
                (self.x + 2, self.y + 2)
            ])
        elif self.shape == "zigzag":
            positions.extend([
                (self.x + 1, self.y),
                (self.x + 1, self.y + 1),
                (self.x + 2, self.y + 1)
            ])
        elif self.shape == "big_block":
            positions.extend([
                (self.x + 1, self.y),
                (self.x + 2, self.y),
                (self.x, self.y + 1),
                (self.x + 1, self.y + 1),
                (self.x + 2, self.y + 1),
                (self.x, self.y + 2),
                (self.x + 1, self.y + 2),
                (self.x + 2, self.y + 2)
            ])
        elif self.shape == "reverse_L":
            positions.extend([
                (self.x + 1, self.y),
                (self.x + 1, self.y + 1),
                (self.x + 1, self.y + 2),
                (self.x, self.y + 2)
            ])
        elif self.shape == "small_cross":
            positions.extend([
                (self.x - 1, self.y),
                (self.x + 1, self.y),
                (self.x, self.y + 1)
            ])
        elif self.shape == "corner":
            positions.extend([
                (self.x + 1, self.y),
                (self.x, self.y + 1)
            ])
        elif self.shape == "long_line":
            positions.extend([
                (self.x, self.y + 1),
                (self.x, self.y + 2),
                (self.x, self.y + 3)
            ])
        elif self.shape == "step":
            positions.extend([
                (self.x + 1, self.y),
                (self.x + 1, self.y + 1),
                (self.x + 2, self.y + 1),
                (self.x + 2, self.y + 2)
            ])
        elif self.shape == "U_shape":
            positions.extend([
                (self.x, self.y + 1),
                (self.x, self.y + 2),
                (self.x + 1, self.y + 2),
                (self.x + 2, self.y + 2),
                (self.x + 2, self.y + 1)
            ])
        elif self.shape == "triangle":
            positions.extend([
                (self.x, self.y + 1),
                (self.x - 1, self.y + 2),
                (self.x + 1, self.y + 2)
            ])
        elif self.shape == "diamond":
            positions.extend([
                (self.x, self.y - 1),
                (self.x - 1, self.y),
                (self.x + 1, self.y),
                (self.x, self.y + 1)
            ])
        elif self.shape == "snake_shape":
            positions.extend([
                (self.x + 1, self.y),
                (self.x + 2, self.y),
                (self.x + 2, self.y + 1),
                (self.x + 3, self.y + 1),
                (self.x + 3, self.y + 2)
            ])
        
        # Filtrar posiciones fuera de los límites
        return [(x, y) for x, y in positions if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT]
    
    def update(self, moving_obstacles=False):
        if moving_obstacles:
            self.blink_timer -= 1
            if self.blink_timer <= 0:
                self.visible = not self.visible
                self.blink_timer = self.blink_speed
                
                # 20% probabilidad de cambiar de posición cuando desaparece
                if not self.visible and random.random() < 0.2:
                    self.x = random.randint(2, GRID_WIDTH - 4)
                    self.y = random.randint(2, GRID_HEIGHT - 4)
                    self.positions = self.generate_shape()
    
    def remove_position(self, pos):
        """Elimina una posición específica del obstáculo"""
        if pos in self.positions:
            self.positions.remove(pos)
        return len(self.positions) == 0  # Retorna True si el obstáculo está completamente destruido
    
    def draw(self, screen):
        if self.visible and self.positions:
            for pos in self.positions:
                x, y = pos
                # Efecto de brillo
                pygame.draw.rect(screen, OBSTACLE_GLOW,
                               (x * CELL_SIZE - 1, y * CELL_SIZE - 1 + UI_HEIGHT, CELL_SIZE + 2, CELL_SIZE + 2))
                pygame.draw.rect(screen, OBSTACLE_COLOR,
                               (x * CELL_SIZE, y * CELL_SIZE + UI_HEIGHT, CELL_SIZE, CELL_SIZE))
                # Detalles internos
                pygame.draw.rect(screen, (100, 100, 100),
                               (x * CELL_SIZE + 2, y * CELL_SIZE + 2 + UI_HEIGHT, CELL_SIZE - 4, CELL_SIZE - 4))

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False
        self.trail = []
        self.laser_mode = False
        self.laser_timer = 0
        self.laser_shots_remaining = 0
        self.laser_shoot_cooldown = 0
        
    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head_x = head_x + dir_x
        new_head_y = head_y + dir_y
        
        # Wrap-around
        new_head_x = new_head_x % GRID_WIDTH
        new_head_y = new_head_y % GRID_HEIGHT
        
        new_head = (new_head_x, new_head_y)
        
        # Guardar posición anterior para efecto de rastro
        if len(self.body) > 0:
            self.trail.append(self.body[0])
            if len(self.trail) > 5:
                self.trail.pop(0)
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            
        # Actualizar modo láser
        if self.laser_timer > 0:
            self.laser_timer -= 1
            if self.laser_timer == 0:
                self.laser_mode = False
                self.laser_shots_remaining = 0
                
        # Actualizar cooldown de disparo
        if self.laser_shoot_cooldown > 0:
            self.laser_shoot_cooldown -= 1
    
    def change_direction(self, direction):
        # Evitar que la serpiente se mueva en dirección opuesta
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def check_self_collision(self):
        head_x, head_y = self.body[0]
        return (head_x, head_y) in self.body[1:]
    
    def check_obstacle_collision(self, obstacles):
        head_pos = self.body[0]
        for obstacle in obstacles:
            if obstacle.visible and head_pos in obstacle.positions:
                return True
        return False
    
    def eat_food(self, food_pos):
        return self.body[0] == food_pos
    
    def grow_snake(self):
        self.grow = True
        
    def activate_laser(self):
        self.laser_mode = True
        self.laser_timer = 300  # 5 segundos a 60 FPS
        self.laser_shots_remaining = 5
        self.laser_shoot_cooldown = 0  # Primer disparo inmediato
        
    def can_shoot_laser(self):
        return self.laser_mode and self.laser_shots_remaining > 0 and self.laser_shoot_cooldown == 0
        
    def shoot_laser(self):
        if self.can_shoot_laser():
            self.laser_shots_remaining -= 1
            self.laser_shoot_cooldown = 60  # 1 segundo entre disparos
            return Laser(self.body[0][0], self.body[0][1], self.direction)
        return None

class Food:
    def __init__(self, snake_body, obstacles=None):
        self.position = self.generate_position(snake_body, obstacles)
        self.pulse = 0
        self.type = "normal"  # normal, bonus, power
        self.bonus_timer = 0
    
    def generate_position(self, snake_body, obstacles=None):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            # Verificar que no esté en la serpiente
            if (x, y) in snake_body:
                continue
                
            # Verificar que no esté en obstáculos
            if obstacles:
                obstacle_collision = False
                for obstacle in obstacles:
                    if obstacle.visible and (x, y) in obstacle.positions:
                        obstacle_collision = True
                        break
                if obstacle_collision:
                    continue
            
            return (x, y)
    
    def respawn(self, snake_body, obstacles=None):
        self.position = self.generate_position(snake_body, obstacles)
        # Probabilidades: 70% normal, 20% bonus, 10% power
        rand = random.random()
        if rand < 0.1:
            self.type = "power"
            self.bonus_timer = 300
        elif rand < 0.3:
            self.type = "bonus"
            self.bonus_timer = 200
        else:
            self.type = "normal"
            self.bonus_timer = 0
    
    def update(self):
        self.pulse += 0.2
        if self.bonus_timer > 0:
            self.bonus_timer -= 1
            if self.bonus_timer <= 0:
                self.type = "normal"

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.color = color
        self.life = 30
        self.max_life = 30
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vy += 0.1
    
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            size = int(3 * (self.life / self.max_life))
            if size > 0:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class Game:
    def __init__(self):
        # Hacer la ventana redimensionable
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("🐍 Snake Game Mejorado")
        self.clock = pygame.time.Clock()
        
        # Fuentes mejoradas
        self.big_font = pygame.font.Font(None, 48)
        self.medium_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 64)
        
        self.score = 0
        self.high_score = self.load_high_score()
        self.particles = []
        self.screen_shake = 0
        self.combo = 0
        self.combo_timer = 0
        self.lasers = []
        
        # Estados del juego
        self.game_state = "menu"
        self.difficulty = "medio"
        self.selected_option = 1
        
        self.obstacles = []
        self.fps = DIFFICULTY_SETTINGS[self.difficulty]["fps"]
        
    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as f:
                return int(f.read())
        except:
            return 0
    
    def save_high_score(self):
        try:
            with open("high_score.txt", "w") as f:
                f.write(str(self.high_score))
        except:
            pass
    
    def generate_obstacles(self):
        self.obstacles = []
        if not DIFFICULTY_SETTINGS[self.difficulty]["obstacles"]:
            return
            
        # Formas más variadas para el modo medio y difícil
        basic_shapes = ["square", "L", "T", "line", "block", "cross", "corner", "small_cross"]
        medium_shapes = ["reverse_L", "long_line", "step", "triangle", "diamond", "diagonal", "zigzag"]
        advanced_shapes = ["big_block", "U_shape", "snake_shape"]
        
        if self.difficulty == "medio":
            available_shapes = basic_shapes + medium_shapes
        else:  # difícil
            available_shapes = basic_shapes + medium_shapes + advanced_shapes
            
        min_obs, max_obs = DIFFICULTY_SETTINGS[self.difficulty]["num_obstacles"]
        num_obstacles = random.randint(min_obs, max_obs)
        
        for _ in range(num_obstacles):
            attempts = 0
            while attempts < 50:
                x = random.randint(4, GRID_WIDTH - 5)
                y = random.randint(4, GRID_HEIGHT - 5)
                shape = random.choice(available_shapes)
                
                # Verificar que no esté cerca del centro (spawn de la serpiente)
                center_x, center_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
                if abs(x - center_x) > 5 or abs(y - center_y) > 5:
                    obstacle = Obstacle(x, y, shape)
                    # Verificar que el obstáculo no esté fuera de límites
                    if obstacle.positions:  # Solo agregar si tiene posiciones válidas
                        self.obstacles.append(obstacle)
                        break
                attempts += 1
    
    def reset_game(self):
        self.snake = Snake()
        self.generate_obstacles()
        self.food = Food(self.snake.body, self.obstacles)
        self.score = 0
        self.game_state = "playing"
        self.particles = []
        self.screen_shake = 0
        self.combo = 0
        self.combo_timer = 0
        self.fps = DIFFICULTY_SETTINGS[self.difficulty]["fps"]
        self.lasers = []
    
    def add_particles(self, x, y, color, count=8):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def screen_shake_effect(self, intensity):
        self.screen_shake = intensity
    
    def handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % 3
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % 3
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                difficulties = ["facil", "medio", "dificil"]
                self.difficulty = difficulties[self.selected_option]
                self.reset_game()
            elif event.key == pygame.K_ESCAPE:
                return False
        elif event.type == pygame.VIDEORESIZE:
            # Manejar redimensionamiento de ventana
            global WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT
            WINDOW_WIDTH = max(800, event.w)
            WINDOW_HEIGHT = max(600, event.h)
            GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
            GRID_HEIGHT = (WINDOW_HEIGHT - UI_HEIGHT) // CELL_SIZE
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        return True
    
    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.snake.change_direction((0, -1))
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.snake.change_direction((0, 1))
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.snake.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.snake.change_direction((1, 0))
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"
        elif event.type == pygame.VIDEORESIZE:
            # Manejar redimensionamiento durante el juego
            global WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT
            WINDOW_WIDTH = max(800, event.w)
            WINDOW_HEIGHT = max(600, event.h)
            GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
            GRID_HEIGHT = (WINDOW_HEIGHT - UI_HEIGHT) // CELL_SIZE
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        return True
    
    def handle_game_over_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.reset_game()
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"
            elif event.key == pygame.K_m:
                self.game_state = "menu"
        elif event.type == pygame.VIDEORESIZE:
            global WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT
            WINDOW_WIDTH = max(800, event.w)
            WINDOW_HEIGHT = max(600, event.h)
            GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
            GRID_HEIGHT = (WINDOW_HEIGHT - UI_HEIGHT) // CELL_SIZE
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        return True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_high_score()
                return False
            
            if self.game_state == "menu":
                if not self.handle_menu_events(event):
                    return False
            elif self.game_state == "playing":
                if not self.handle_game_events(event):
                    return False
            elif self.game_state == "game_over":
                if not self.handle_game_over_events(event):
                    return False
        
        return True
    
    def update(self):
        if self.game_state == "playing":
            self.snake.move()
            
            # Verificar colisión con el cuerpo
            if self.snake.check_self_collision():
                self.game_state = "game_over"
                self.screen_shake_effect(10)
                if self.score > self.high_score:
                    self.high_score = self.score
                head_x, head_y = self.snake.body[0]
                screen_x = head_x * CELL_SIZE + CELL_SIZE // 2
                screen_y = head_y * CELL_SIZE + CELL_SIZE // 2 + UI_HEIGHT
                self.add_particles(screen_x, screen_y, RED, 15)
            
            # Verificar colisión con obstáculos
            if self.snake.check_obstacle_collision(self.obstacles):
                self.game_state = "game_over"
                self.screen_shake_effect(10)
                if self.score > self.high_score:
                    self.high_score = self.score
                head_x, head_y = self.snake.body[0]
                screen_x = head_x * CELL_SIZE + CELL_SIZE // 2
                screen_y = head_y * CELL_SIZE + CELL_SIZE // 2 + UI_HEIGHT
                self.add_particles(screen_x, screen_y, PURPLE, 15)
            
            # Verificar si comió la comida
            if self.snake.eat_food(self.food.position):
                self.snake.grow_snake()
                
                # Puntuación según tipo de comida
                if self.food.type == "power":
                    points = 50
                    self.combo += 2
                    self.snake.activate_laser()
                elif self.food.type == "bonus":
                    points = 25
                    self.combo += 1
                else:
                    points = 10
                    self.combo = max(0, self.combo - 1)
                
                # Bonus por combo
                if self.combo > 0:
                    points += self.combo * 5
                    self.combo_timer = 120
                
                self.score += points
                
                # Efectos visuales
                food_x, food_y = self.food.position
                screen_x = food_x * CELL_SIZE + CELL_SIZE // 2
                screen_y = food_y * CELL_SIZE + CELL_SIZE // 2 + UI_HEIGHT
                if self.food.type == "power":
                    color = POWER_COLOR
                elif self.food.type == "bonus":
                    color = ORANGE
                else:
                    color = NEON_GREEN
                self.add_particles(screen_x, screen_y, color, 12)
                self.screen_shake_effect(3)
                
                self.food.respawn(self.snake.body, self.obstacles)
            
            # Sistema de disparo láser mejorado
            if self.snake.can_shoot_laser():
                new_laser = self.snake.shoot_laser()
                if new_laser:
                    self.lasers.append(new_laser)
            
            # Actualizar láseres
            for laser in self.lasers[:]:
                laser.update()
                if not laser.is_alive():
                    self.lasers.remove(laser)
                    continue
                
                # Verificar colisión de láser con obstáculos
                laser_pos = (laser.x, laser.y)
                for obstacle in self.obstacles[:]:
                    if obstacle.visible and laser_pos in obstacle.positions:
                        # Eliminar solo la posición específica del obstáculo
                        if obstacle.remove_position(laser_pos):
                            # Si el obstáculo está completamente destruido, eliminarlo
                            self.obstacles.remove(obstacle)
                        # Eliminar el láser
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        # Efectos de destrucción
                        screen_x = laser_pos[0] * CELL_SIZE + CELL_SIZE // 2
                        screen_y = laser_pos[1] * CELL_SIZE + CELL_SIZE // 2 + UI_HEIGHT
                        self.add_particles(screen_x, screen_y, LASER_COLOR, 8)
                        self.screen_shake_effect(2)
                        break
            
            # Actualizar comida
            self.food.update()
            
            # Actualizar obstáculos
            for obstacle in self.obstacles:
                obstacle.update(DIFFICULTY_SETTINGS[self.difficulty]["moving_obstacles"])
            
            # Actualizar combo timer
            if self.combo_timer > 0:
                self.combo_timer -= 1
            else:
                self.combo = max(0, self.combo - 1)
        
        # Actualizar partículas
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
        
        # Reducir screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
    
    def draw_menu(self):
        # Fondo del menú
        self.draw_background()
        
        # Título
        title_text = self.title_font.render("🐍 SNAKE GAME", True, NEON_GREEN)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.medium_font.render("Selecciona tu nivel de dificultad", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 180))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Opciones de dificultad mejoradas
        options = [
            ("FÁCIL", "Velocidad lenta, sin obstáculos", GREEN),
            ("MEDIO", "Velocidad normal, obstáculos fijos", YELLOW),
            ("DIFÍCIL", "Velocidad rápida, obstáculos dinámicos", RED)
        ]
        
        start_y = 250
        option_height = 90
        box_width = 600
        box_height = 75
        
        for i, (title, desc, color) in enumerate(options):
            y_pos = start_y + i * option_height
            
            # Calcular posición de la caja
            box_x = WINDOW_WIDTH // 2 - box_width // 2
            box_y = y_pos - box_height // 2 + 15
            
            # Resaltar opción seleccionada
            if i == self.selected_option:
                # Fondo de selección con borde
                pygame.draw.rect(self.screen, (40, 40, 40), 
                               (box_x, box_y, box_width, box_height))
                pygame.draw.rect(self.screen, color, 
                               (box_x, box_y, box_width, box_height), 3)
                
                # Indicador de selección
                arrow_text = self.big_font.render("►", True, color)
                self.screen.blit(arrow_text, (box_x - 40, y_pos - 10))
            else:
                # Fondo normal
                pygame.draw.rect(self.screen, (25, 25, 25), 
                               (box_x, box_y, box_width, box_height))
                pygame.draw.rect(self.screen, LIGHT_GRAY, 
                               (box_x, box_y, box_width, box_height), 1)
            
            # Texto de la opción
            option_text = self.big_font.render(title, True, color if i == self.selected_option else WHITE)
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, y_pos))
            self.screen.blit(option_text, option_rect)
            
            # Descripción
            desc_text = self.small_font.render(desc, True, LIGHT_GRAY)
            desc_rect = desc_text.get_rect(center=(WINDOW_WIDTH // 2, y_pos + 25))
            self.screen.blit(desc_text, desc_rect)
        
        # Instrucciones
        instructions = [
            "↑↓ o W/S para navegar",
            "ENTER o ESPACIO para seleccionar",
            "ESC para salir"
        ]
        
        inst_y = WINDOW_HEIGHT - 120
        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, (150, 150, 150))
            inst_rect = inst_text.get_rect(center=(WINDOW_WIDTH // 2, inst_y + i * 25))
            self.screen.blit(inst_text, inst_rect)
    
    def draw_background(self):
        # Fondo con degradado sutil
        for y in range(0, WINDOW_HEIGHT, 4):
            color_intensity = int(15 + (y / WINDOW_HEIGHT) * 10)
            color = (color_intensity, color_intensity, color_intensity + 8)
            pygame.draw.rect(self.screen, color, (0, y, WINDOW_WIDTH, 4))
    
    def draw_grid(self):
        # Grilla solo en el área de juego
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (35, 35, 45), (x, UI_HEIGHT), (x, WINDOW_HEIGHT), 1)
        for y in range(UI_HEIGHT, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (35, 35, 45), (0, y), (WINDOW_WIDTH, y), 1)
    
    def draw_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
    
    def draw_snake(self):
        # Dibujar rastro primero
        for i, pos in enumerate(self.snake.trail):
            x, y = pos
            alpha = int(50 * (i / len(self.snake.trail))) if self.snake.trail else 0
            size = CELL_SIZE - 8
            pygame.draw.rect(self.screen, (0, 100, 150, alpha),
                           (x * CELL_SIZE + 4, y * CELL_SIZE + 4 + UI_HEIGHT, size, size))
        
        # Dibujar serpiente con efectos
        for i, segment in enumerate(self.snake.body):
            x, y = segment
            
            if i == 0:  # Cabeza
                # Efecto especial si está en modo láser
                if self.snake.laser_mode:
                    glow_size = CELL_SIZE + 6
                    pygame.draw.rect(self.screen, POWER_COLOR,
                                   (x * CELL_SIZE - 3, y * CELL_SIZE - 3 + UI_HEIGHT, glow_size, glow_size))
                
                # Efecto de brillo en la cabeza
                glow_size = CELL_SIZE + 4
                pygame.draw.rect(self.screen, NEON_GREEN,
                               (x * CELL_SIZE - 2, y * CELL_SIZE - 2 + UI_HEIGHT, glow_size, glow_size))
                pygame.draw.rect(self.screen, GREEN,
                               (x * CELL_SIZE, y * CELL_SIZE + UI_HEIGHT, CELL_SIZE, CELL_SIZE))
                
                # Ojos
                eye_size = 3
                pygame.draw.circle(self.screen, WHITE,
                                 (x * CELL_SIZE + 6, y * CELL_SIZE + 6 + UI_HEIGHT), eye_size)
                pygame.draw.circle(self.screen, WHITE,
                                 (x * CELL_SIZE + CELL_SIZE - 6, y * CELL_SIZE + 6 + UI_HEIGHT), eye_size)
                pygame.draw.circle(self.screen, BLACK,
                                 (x * CELL_SIZE + 6, y * CELL_SIZE + 6 + UI_HEIGHT), 1)
                pygame.draw.circle(self.screen, BLACK,
                                 (x * CELL_SIZE + CELL_SIZE - 6, y * CELL_SIZE + 6 + UI_HEIGHT), 1)
            else:  # Cuerpo
                # Degradado del cuerpo
                intensity = max(0.3, 1 - (i / len(self.snake.body)))
                body_color = (int(BLUE[0] * intensity), int(BLUE[1] * intensity), int(BLUE[2] * intensity))
                pygame.draw.rect(self.screen, body_color,
                               (x * CELL_SIZE + 1, y * CELL_SIZE + 1 + UI_HEIGHT, CELL_SIZE - 2, CELL_SIZE - 2))
                # Borde sutil
                pygame.draw.rect(self.screen, NEON_BLUE,
                               (x * CELL_SIZE + 1, y * CELL_SIZE + 1 + UI_HEIGHT, CELL_SIZE - 2, CELL_SIZE - 2), 1)
    
    def draw_food(self):
        x, y = self.food.position
        center_x = x * CELL_SIZE + CELL_SIZE // 2
        center_y = y * CELL_SIZE + CELL_SIZE // 2 + UI_HEIGHT
        
        if self.food.type == "power":
            # Comida de poder con efecto especial
            pulse_size = int(4 + math.sin(self.food.pulse) * 3)
            # Efecto de brillo dorado
            pygame.draw.circle(self.screen, (255, 255, 150), (center_x, center_y), CELL_SIZE // 2 + pulse_size)
            pygame.draw.circle(self.screen, POWER_COLOR, (center_x, center_y), CELL_SIZE // 2)
            # Dibujar rayo
            ray_points = []
            for i in range(8):
                angle = i * math.pi / 4 + self.food.pulse * 0.1
                inner_radius = CELL_SIZE // 4
                outer_radius = CELL_SIZE // 2
                # Punto interno
                inner_x = center_x + math.cos(angle) * inner_radius
                inner_y = center_y + math.sin(angle) * inner_radius
                # Punto externo
                outer_x = center_x + math.cos(angle) * outer_radius
                outer_y = center_y + math.sin(angle) * outer_radius
                ray_points.extend([(inner_x, inner_y), (outer_x, outer_y)])
            
            # Dibujar líneas de rayo
            for i in range(0, len(ray_points), 2):
                if i + 1 < len(ray_points):
                    pygame.draw.line(self.screen, WHITE, ray_points[i], ray_points[i+1], 2)
                    
        elif self.food.type == "bonus":
            # Comida bonus con efecto de estrella pulsante
            pulse_size = int(3 + math.sin(self.food.pulse) * 2)
            star_color = ORANGE
            # Efecto de brillo
            pygame.draw.circle(self.screen, (255, 200, 100), (center_x, center_y), CELL_SIZE // 2 + pulse_size)
            pygame.draw.circle(self.screen, star_color, (center_x, center_y), CELL_SIZE // 2)
            # Dibujar estrella
            points = []
            for i in range(10):
                angle = i * math.pi / 5
                if i % 2 == 0:
                    radius = CELL_SIZE // 3
                else:
                    radius = CELL_SIZE // 6
                point_x = center_x + math.cos(angle) * radius
                point_y = center_y + math.sin(angle) * radius
                points.append((point_x, point_y))
            pygame.draw.polygon(self.screen, YELLOW, points)
        else:
            # Comida normal con efecto de pulsación
            pulse_size = int(2 + math.sin(self.food.pulse) * 1)
            pygame.draw.circle(self.screen, (255, 100, 100), (center_x, center_y), CELL_SIZE // 2 + pulse_size)
            pygame.draw.circle(self.screen, RED, (center_x, center_y), CELL_SIZE // 2)
            pygame.draw.circle(self.screen, (255, 150, 150), (center_x, center_y), CELL_SIZE // 3)
    
    def draw_lasers(self):
        for laser in self.lasers:
            laser.draw(self.screen)
    
    def draw_particles(self):
        for particle in self.particles:
            particle.draw(self.screen)
    
    def draw_ui(self):
        # Panel de información fijo en la parte superior
        ui_surface = pygame.Surface((WINDOW_WIDTH, UI_HEIGHT))
        ui_surface.set_alpha(240)
        ui_surface.fill(DARK_GRAY)
        self.screen.blit(ui_surface, (0, 0))
        
        # Línea separadora
        pygame.draw.line(self.screen, NEON_BLUE, (0, UI_HEIGHT), (WINDOW_WIDTH, UI_HEIGHT), 2)
        
        # Columna izquierda - Puntuación
        score_text = self.medium_font.render(f"Puntuación: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 15))
        
        high_score_text = self.small_font.render(f"Mejor: {self.high_score}", True, LIGHT_GRAY)
        self.screen.blit(high_score_text, (20, 45))
        
        # Columna central - Información del juego
        difficulty_text = self.small_font.render(f"Dificultad: {self.difficulty.upper()}", True, YELLOW)
        self.screen.blit(difficulty_text, (WINDOW_WIDTH // 2 - 100, 15))
        
        length_text = self.small_font.render(f"Longitud: {len(self.snake.body)}", True, LIGHT_GRAY)
        self.screen.blit(length_text, (WINDOW_WIDTH // 2 - 100, 35))
        
        # Modo láser
        if hasattr(self.snake, 'laser_mode') and self.snake.laser_mode:
            shots_left = self.snake.laser_shots_remaining
            time_left = self.snake.laser_timer // 60 + 1
            laser_text = self.small_font.render(f"LÁSER: {shots_left} disparos | {time_left}s", True, LASER_COLOR)
            self.screen.blit(laser_text, (WINDOW_WIDTH // 2 - 100, 55))
        
        # Columna derecha - Combo y controles
        if self.combo > 0:
            combo_text = self.medium_font.render(f"Combo x{self.combo}!", True, ORANGE)
            self.screen.blit(combo_text, (WINDOW_WIDTH - 200, 15))
        
        controls_text = self.small_font.render("Flechas/WASD: mover | ESC: menú", True, (150, 150, 150))
        self.screen.blit(controls_text, (WINDOW_WIDTH - 250, 50))
    
    def draw_game_over(self):
        # Overlay de Game Over
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Textos de Game Over
        game_over_text = self.big_font.render("¡GAME OVER!", True, RED)
        final_score_text = self.medium_font.render(f"Puntuación Final: {self.score}", True, WHITE)
        difficulty_text = self.medium_font.render(f"Dificultad: {self.difficulty.upper()}", True, YELLOW)
        restart_text = self.medium_font.render("ESPACIO: Reiniciar | M/ESC: Menú", True, NEON_GREEN)
        
        # Centrar los textos
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        difficulty_rect = difficulty_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(final_score_text, final_score_rect)
        self.screen.blit(difficulty_text, difficulty_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        # Screen shake effect
        shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        
        if self.game_state == "menu":
            self.draw_menu()
        else:
            # Crear superficie temporal para el shake
            temp_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)) if self.screen_shake > 0 else None
            
            self.draw_background()
            self.draw_ui()  # UI primero para que no tape el juego
            self.draw_grid()
            self.draw_obstacles()
            self.draw_snake()
            self.draw_food()
            self.draw_lasers()
            self.draw_particles()
            
            if self.game_state == "game_over":
                self.draw_game_over()
            
            # Aplicar shake si es necesario
            if self.screen_shake > 0:
                temp_surface.blit(self.screen, (0, 0))
                self.screen.fill(BLACK)
                self.screen.blit(temp_surface, (shake_x, shake_y))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps if self.game_state == "playing" else 60)
        
        self.save_high_score()
        pygame.quit()
        sys.exit()

# Ejecutar el juego
if __name__ == "__main__":
    game = Game()
    game.run()
from src.particle_system.schemas import Particle, ParticleSystem
import random
import math
import pygame
import time
from collections import deque


PARTICLE_COLORS = [
    (66, 135, 245), (0, 191, 255),      # Azul
    (50, 205, 50), (0, 255, 128),       # Verde
    (255, 255, 0), (255, 215, 0),       # Amarelo
    (255, 105, 180), (255, 20, 147),    # Rosa
    (138, 43, 226), (186, 85, 211),     # Roxo
    (255, 0, 0), (220, 20, 60),         # Vermelho
    (255, 140, 0), (255, 69, 0),        # Laranja
]


class Slider:
    def __init__(self, x: int, y: int, width: int, height: int, min_val: float, max_val: float, initial_val: float, label: str = "", step: float = 1.0):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.step = step
        self.dragging = False
        self.handle_rect = pygame.Rect(x, y, 20, height)
        self.label = label
        self.update_handle_position()

    def update_handle_position(self):
        # Atualiza a posição do handle baseado no valor atual
        percentage = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.handle_rect.x = self.rect.x + (self.rect.width - self.handle_rect.width) * percentage

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Calcula o novo valor baseado na posição do mouse
            rel_x = event.pos[0] - self.rect.x
            percentage = max(0, min(1, rel_x / self.rect.width))
            raw_value = self.min_val + (self.max_val - self.min_val) * percentage
            # Arredonda para o step mais próximo
            self.value = round(raw_value / self.step) * self.step
            self.update_handle_position()

    def draw(self, screen):
        # Desenha o label
        font = pygame.font.Font(None, 24)
        label_text = font.render(f"{self.label}: {self.value:.1f}", True, (255, 255, 255))
        screen.blit(label_text, (self.rect.x, self.rect.y - 25))
        
        # Desenha a barra do slider
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        # Desenha o handle
        pygame.draw.rect(screen, (200, 200, 200), self.handle_rect)


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.is_active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_active = not self.is_active
                return True
        return False

    def draw(self, screen):
        # Desenha o botão
        pygame.draw.rect(screen, self.color if self.is_active else (100, 100, 100), self.rect)
        # Desenha a borda
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        # Desenha o texto
        font = pygame.font.Font(None, 24)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


class ParticleGenerator:
    def __init__(self, position: tuple[int, int], radius: float = 50.0, spawn_interval: float = 1.0):
        self.position = position
        self.radius = radius
        self.spawn_interval = spawn_interval
        self.last_spawn_time = 0
        self.current_particles = 0
        self.rgb_mode = False
        self.bloom_effect = False
        self.bloom_intensity = 1.0  # Novo atributo para controlar a intensidade do bloom
        self.trails_enabled = True  # Novo atributo para controlar as trails

    def can_spawn(self, current_time: float) -> bool:
        return current_time - self.last_spawn_time >= self.spawn_interval

    def spawn_particle(self, particle_system: ParticleSystem, max_particles: int, particle_speed: float = 100.0):
        # Determinar quantas partículas serão geradas (1 a 4)
        num_particles = random.randint(1, 4)
        
        # Verificar se há espaço suficiente para todas as partículas
        if self.current_particles + num_particles > max_particles:
            return

        for _ in range(num_particles):
            # Gerar ângulo aleatório
            angle = random.uniform(0, 2 * math.pi)
            
            # Calcular velocidade baseada no ângulo
            speed = random.uniform(particle_speed * 0.5, particle_speed)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # Gerar cor
            if self.rgb_mode:
                color = random.choice(PARTICLE_COLORS)
            else:
                color = (255, 255, 255)  # Branco por padrão
            
            # Criar partícula
            particle = Particle(
                position=self.position,  # Agora sempre spawna do centro
                velocity=(vx, vy),
                acceleration=(0, 98.1),  # Gravidade
                rotation=0,
                size=random.uniform(2, 4),
                color=color,
                alpha=255.0,
                lifespan=random.uniform(2, 4)
            )
            
            particle_system.particles.append(particle)
            self.current_particles += 1
        
        self.last_spawn_time = pygame.time.get_ticks() / 1000.0

    def draw(self, screen: pygame.Surface):
        # Desenhar círculo do gerador
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)
        
        # Desenhar informações
        font = pygame.font.Font(None, 24)
        info_text = [
            f"Partículas: {self.current_particles}",
            f"Raio: {self.radius:.1f}",
            f"Intervalo: {self.spawn_interval:.1f}s",
            f"RGB: {'Ativado' if self.rgb_mode else 'Desativado'}",
            f"Bloom: {'Ativado' if self.bloom_effect else 'Desativado'}",
            f"Tamanho: {self.bloom_intensity:.1f}x",
            f"Trails: {'Ativado' if self.trails_enabled else 'Desativado'}"
        ]
        
        for i, text in enumerate(info_text):
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10 + i * 25))


def create_particle(
    position: tuple[float, float],
    velocity: tuple[float, float],
    acceleration: tuple[float, float],
    rotation: float,
    size: float,
    color: tuple[int, int, int],
    alpha: float,
    lifespan: float,
    trail: deque = None
) -> Particle:
    return Particle(
        position=position,
        velocity=velocity,
        acceleration=acceleration,
        rotation=rotation,
        size=size,
        color=color,
        alpha=alpha,
        lifespan=lifespan,
        trail=trail or deque(maxlen=30)
    )


def create_particle_system(particles: list[Particle]) -> ParticleSystem:
    return ParticleSystem(particles=particles)


def generate_particles(
    screen_width: int,
    screen_height: int,
    count: int,
    speed_range: tuple[float, float],
    size_range: tuple[float, float],
    color: tuple[int, int, int],
    lifespan_range: tuple[float, float],
) -> list[Particle]:
    particles = []
    for _ in range(count):
        # Gerar posição aleatória na tela
        x = random.uniform(0, screen_width)
        y = random.uniform(0, screen_height)
        
        # Gerar velocidade aleatória em uma direção
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(speed_range[0], speed_range[1])
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        
        # Gerar tamanho aleatório
        size = random.uniform(size_range[0], size_range[1])
        
        # Gerar tempo de vida aleatório
        lifespan = random.uniform(lifespan_range[0], lifespan_range[1])
        
        # Criar partícula
        particle = create_particle(
            position=(x, y),
            velocity=(vx, vy),
            acceleration=(0, 98.1),  # gravidade
            rotation=random.uniform(0, 360),
            size=size,
            color=color,
            alpha=255,
            lifespan=lifespan,
        )
        particles.append(particle)
    
    return particles


def update_particle_system(particle_system: ParticleSystem, dt: float, generator: ParticleGenerator):
    # Atualiza as partículas e conta quantas morreram
    dead_particles = 0
    initial_count = len(particle_system.particles)
    
    # Verificar se o botão direito está pressionado
    mouse_pos = pygame.mouse.get_pos()
    is_magnetic = pygame.mouse.get_pressed()[2]  # Botão direito
    
    for particle in particle_system.particles[:]:
        # Verificar se a partícula saiu do raio do gerador
        dx = particle.position[0] - generator.position[0]
        dy = particle.position[1] - generator.position[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > generator.radius:
            particle_system.particles.remove(particle)
            dead_particles += 1
            continue
        
        # Atualizar partícula e remover se morreu
        if not particle.update(dt, mouse_pos if is_magnetic else None, is_magnetic):
            particle_system.particles.remove(particle)
            dead_particles += 1
    
    # Atualiza o contador do gerador considerando todas as partículas que morreram
    final_count = len(particle_system.particles)
    generator.current_particles = final_count


def render_particle_system(particle_system: ParticleSystem, screen, generator: ParticleGenerator):
    for particle in particle_system.particles:
        # Renderizar trilha (sempre com a cor original da partícula)
        if generator.trails_enabled and len(particle.trail) > 1:
            points = list(particle.trail)
            # Desenhar trilha normal com a cor da partícula
            pygame.draw.lines(screen, particle.color, False, points, 2)

        # Calcular tamanho base da partícula
        base_size = particle.size * generator.bloom_intensity

        # Renderizar partícula
        if generator.bloom_effect:
            # Efeito de bloom
            for i in range(8):  # Aumentado para 8 camadas para mais blur
                size = base_size * (1 + i * 1.2)  # Aumentado o incremento para mais blur
                alpha = int(particle.alpha * (1 - i * 0.15))  # Reduzido a perda de alpha para mais blur
                alpha = min(max(alpha, 0), 255)
                
                # Camada de brilho branco
                surf = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
                white_alpha = min(max(alpha // 3, 0), 255)
                pygame.draw.circle(
                    surf,
                    (255, 255, 255, white_alpha),
                    (int(size), int(size)),
                    int(size)
                )
                screen.blit(surf, (particle.position[0] - size, particle.position[1] - size))
                
                # Camada com cor da partícula
                surf = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
                pygame.draw.circle(
                    surf,
                    (*[int(c) for c in particle.color], alpha),
                    (int(size), int(size)),
                    int(size)
                )
                screen.blit(surf, (particle.position[0] - size, particle.position[1] - size))
        else:
            # Partícula normal
            surf = pygame.Surface((int(base_size * 2), int(base_size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(
                surf,
                (*[int(c) for c in particle.color], int(min(max(particle.alpha, 0), 255))),
                (int(base_size), int(base_size)),
                int(base_size)
            )
            screen.blit(surf, (particle.position[0] - base_size, particle.position[1] - base_size))


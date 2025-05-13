from pydantic import BaseModel
import pygame
from collections import deque
from typing import Optional
import math


class Particle(BaseModel):
    position: tuple[float, float]
    velocity: tuple[float, float]
    acceleration: tuple[float, float]
    rotation: float  # in degrees
    size: float
    color: tuple[int, int, int]  # RGB
    alpha: float = 255.0
    lifespan: float = 1.0
    age: float = 0.0
    trail: Optional[deque] = None
    magnetic_strength: float = 500.0  # Força da atração magnética

    def __init__(self, **data):
        super().__init__(**data)
        if self.trail is None:
            self.trail = deque(maxlen=30)

    def update(self, dt: float, mouse_pos: Optional[tuple[int, int]] = None, is_magnetic: bool = False):
        self.age += dt
        if self.age >= self.lifespan:
            return False
        
        # Atualizar posição baseada na velocidade
        x, y = self.position
        vx, vy = self.velocity
        ax, ay = self.acceleration
        
        # Se estiver no modo magnético e o mouse estiver pressionado
        if is_magnetic and mouse_pos:
            # Calcular direção para o mouse
            dx = mouse_pos[0] - x
            dy = mouse_pos[1] - y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance > 0:  # Evitar divisão por zero
                # Normalizar e aplicar força magnética
                dx /= distance
                dy /= distance
                vx += dx * self.magnetic_strength * dt
                vy += dy * self.magnetic_strength * dt
        else:
            # Aplicar gravidade normalmente
            vx += ax * dt
            vy += ay * dt
        
        new_x = x + vx * dt
        new_y = y + vy * dt
        
        # Atualizar trilha
        self.trail.append((x, y))
        
        self.position = (new_x, new_y)
        self.velocity = (vx, vy)
        return True

    def render(self, screen: pygame.Surface, bloom_effect: bool = False, bloom_intensity: float = 1.0):
        # Renderizar trilha
        if len(self.trail) > 1:
            points = list(self.trail)
            if bloom_effect:
                # Desenhar trilha com efeito de bloom (usando a cor da partícula)
                for i in range(len(points) - 1):
                    alpha = int(255 * (i / len(points)) * bloom_intensity)
                    alpha = min(max(alpha, 0), 255)
                    # Trilha principal com cor da partícula
                    pygame.draw.line(screen, (*[int(c) for c in self.color], alpha), points[i], points[i + 1], 3)
                    # Trilha com brilho branco suave
                    white_alpha = min(max(alpha // 3, 0), 255)
                    pygame.draw.line(screen, (255, 255, 255, white_alpha), points[i], points[i + 1], 4)
            else:
                # Desenhar trilha normal com a cor da partícula
                pygame.draw.lines(screen, self.color, False, points, 2)

        # Renderizar partícula
        if bloom_effect:
            # Efeito de bloom
            for i in range(8):  # Aumentado para 8 camadas para mais blur
                size = self.size * (1 + i * 1.2 * bloom_intensity)  # Aumentado o incremento para mais blur
                alpha = int(self.alpha * (1 - i * 0.15) * bloom_intensity)  # Reduzido a perda de alpha para mais blur
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
                screen.blit(surf, (self.position[0] - size, self.position[1] - size))
                
                # Camada com cor da partícula
                surf = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
                pygame.draw.circle(
                    surf,
                    (*[int(c) for c in self.color], alpha),
                    (int(size), int(size)),
                    int(size)
                )
                screen.blit(surf, (self.position[0] - size, self.position[1] - size))
        else:
            # Partícula normal
            surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(
                surf,
                (*[int(c) for c in self.color], int(min(max(self.alpha, 0), 255))),
                (int(self.size), int(self.size)),
                int(self.size)
            )
            screen.blit(surf, (self.position[0] - self.size, self.position[1] - self.size))


class ParticleSystem(BaseModel):
    particles: list[Particle]

    def update(self, dt: float):
        for particle in self.particles[:]:
            if not particle.update(dt):
                self.particles.remove(particle)

    def render(self, screen: pygame.Surface, bloom_effect: bool = False, bloom_intensity: float = 1.0):
        for particle in self.particles:
            particle.render(screen, bloom_effect, bloom_intensity)

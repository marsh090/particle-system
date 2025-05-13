import pygame
from src.particle_system.schemas import Particle, ParticleSystem
from src.pygame.helper import *

# Constantes de layout
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MARGIN = 20
SLIDER_WIDTH = 200
SLIDER_HEIGHT = 20
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30
SLIDER_SPACING = 50
BUTTON_SPACING = 110
INFO_SPACING = 25

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
clock = pygame.time.Clock()
running = True
last_time = pygame.time.get_ticks() / 1000.0

# Criar sliders
particle_limit_slider = Slider(
    x=MARGIN,
    y=MARGIN + SLIDER_SPACING * 4,
    width=SLIDER_WIDTH,
    height=SLIDER_HEIGHT,
    min_val=10,
    max_val=1000,
    initial_val=315,
    label="Limite de Partículas"
)

generator_radius_slider = Slider(
    x=MARGIN,
    y=MARGIN + SLIDER_SPACING * 5,
    width=SLIDER_WIDTH,
    height=SLIDER_HEIGHT,
    min_val=10,
    max_val=350,
    initial_val=110,
    label="Raio do Gerador"
)

spawn_interval_slider = Slider(
    x=MARGIN,
    y=MARGIN + SLIDER_SPACING * 6,
    width=SLIDER_WIDTH,
    height=SLIDER_HEIGHT,
    min_val=0,
    max_val=5,
    initial_val=1.5,
    label="Intervalo de Geração",
    step=0.5
)

speed_slider = Slider(
    x=MARGIN,
    y=MARGIN + SLIDER_SPACING * 7,
    width=SLIDER_WIDTH,
    height=SLIDER_HEIGHT,
    min_val=50,
    max_val=500,
    initial_val=185,
    label="Velocidade"
)

bloom_intensity_slider = Slider(
    x=MARGIN,
    y=MARGIN + SLIDER_SPACING * 8,
    width=SLIDER_WIDTH,
    height=SLIDER_HEIGHT,
    min_val=1,
    max_val=3.0,
    initial_val=1.0,
    label="Tamanho"
)

# Criar botões
rgb_button = Button(
    x=MARGIN,
    y=MARGIN + SLIDER_SPACING * 9,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    text="RGB",
    color=(255, 0, 0)
)

bloom_button = Button(
    x=MARGIN + BUTTON_SPACING,
    y=MARGIN + SLIDER_SPACING * 9,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    text="Bloom",
    color=(0, 255, 0)
)

trails_button = Button(
    x=MARGIN + BUTTON_SPACING * 2,
    y=MARGIN + SLIDER_SPACING * 9,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    text="Trails",
    color=(0, 0, 255)
)

exit_button = Button(
    x=MARGIN,
    y=MARGIN + SLIDER_SPACING * 10,
    width=SLIDER_WIDTH,
    height=BUTTON_HEIGHT,
    text="Sair",
    color=(255, 0, 0)
)

# Inicializar gerador de partículas
generator = ParticleGenerator(
    position=(screen.get_width() // 2 + 100, screen.get_height() // 2),
    radius=generator_radius_slider.value,
    spawn_interval=spawn_interval_slider.value
)

# Criar sistema de partículas vazio
particle_system = create_particle_system([])

while running:
    current_time = pygame.time.get_ticks() / 1000.0
    dt = current_time - last_time
    last_time = current_time

    # Processar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Atualizar sliders
        particle_limit_slider.handle_event(event)
        generator_radius_slider.handle_event(event)
        spawn_interval_slider.handle_event(event)
        speed_slider.handle_event(event)
        bloom_intensity_slider.handle_event(event)
        
        # Atualizar botões
        rgb_button.handle_event(event)
        bloom_button.handle_event(event)
        trails_button.handle_event(event)
        if exit_button.handle_event(event):
            running = False
        
        # Atualizar gerador
        generator.radius = generator_radius_slider.value
        generator.spawn_interval = spawn_interval_slider.value
        generator.rgb_mode = rgb_button.is_active
        generator.bloom_effect = bloom_button.is_active
        generator.bloom_intensity = bloom_intensity_slider.value
        generator.trails_enabled = trails_button.is_active

    # Limpar tela
    screen.fill((0, 0, 0))

    # Atualizar sistema de partículas
    update_particle_system(particle_system, dt, generator)

    # Gerar novas partículas
    if generator.can_spawn(current_time):
        generator.spawn_particle(particle_system, particle_limit_slider.value, speed_slider.value)

    # Renderizar sistema de partículas
    render_particle_system(particle_system, screen, generator)

    # Renderizar gerador
    generator.draw(screen)

    # Renderizar controles
    particle_limit_slider.draw(screen)
    generator_radius_slider.draw(screen)
    spawn_interval_slider.draw(screen)
    speed_slider.draw(screen)
    bloom_intensity_slider.draw(screen)
    rgb_button.draw(screen)
    bloom_button.draw(screen)
    trails_button.draw(screen)
    exit_button.draw(screen)

    # Atualizar tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

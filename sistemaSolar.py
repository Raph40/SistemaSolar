# Importar a biblioteca Pygame para criação de jogos e aplicações multimédia
import pygame
# Importar a biblioteca Math para operações matemáticas
import math
# Importar a biblioteca Random para geração de números aleatórios
import random

# Inicializar todos os módulos do Pygame
pygame.init()

# Definir constantes para as dimensões da janela
# Largura da janela em pixels
WIDTH = 1280
# Altura da janela em pixels
HEIGHT = 720
# Altura do painel de menu no topo da janela
MENU_HEIGHT = 70

# Criar a janela principal com as dimensões especificadas
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Definir o título da janela
pygame.display.set_caption("Sistema Solar")

# Definir cores usando valores RGB (Red, Green, Blue)
# Cor preta
BLACK = (0, 0, 0)
# Cor branca
WHITE = (255, 255, 255)
# Cinza escuro para fundos
DARK_GRAY = (30, 30, 30)
# Azul claro para realces
HIGHLIGHT = (100, 150, 255)
# Cor normal para botões
BUTTON_COLOR = (70, 70, 70)
# Cor para quando o rato está sobre um botão
BUTTON_HOVER_COLOR = (100, 100, 100)
# Cor do texto nos botões
BUTTON_TEXT_COLOR = WHITE

# Tentar carregar e reproduzir música de fundo
try:
    # Carregar o ficheiro de música
    pygame.mixer.music.load("space_music.ogg")
    # Reproduzir a música em loop infinito
    pygame.mixer.music.play(-1)
except Exception:
    # Continuar sem música se houver erro
    pass

# Tentar carregar o som de clique
try:
    # Carregar o ficheiro de som
    click_sound = pygame.mixer.Sound("click.wav")
except Exception:
    # Definir como None se não conseguir carregar
    click_sound = None

# Tentar carregar a textura do Sol
try:
    # Carregar a imagem do Sol
    sun_texture = pygame.image.load("texturas/sun.jpg")
    # Redimensionar a textura para 200x200 pixels
    sun_texture = pygame.transform.scale(sun_texture, (200, 200))
except:
    # Usar None se não conseguir carregar a textura
    sun_texture = None
    # Mostrar mensagem de aviso
    print("Could not load sun texture, using solid color instead")

# Definir o número de estrelas no fundo
NUM_STARS = 150
# Criar lista de estrelas com propriedades aleatórias
stars = [{
    "x": random.randint(0, WIDTH),  # Posição X aleatória
    "y": random.randint(0, HEIGHT),  # Posição Y aleatória
    "brightness": random.randint(100, 255),  # Brilho inicial aleatório
    "dir": random.choice([-1, 1])  # Direção do brilho (aumentar ou diminuir)
} for _ in range(NUM_STARS)]

# Definir fatores de escala para o sistema solar
# Escala para converter distâncias reais para pixels
DISTANCE_SCALE = 0.9  # milhões de km para pixels
# Escala para converter tamanhos reais para pixels
RADIUS_SCALE = 0.0005  # km para pixels

# Configurações de tempo da simulação
# Número de frames por segundo
FPS = 60
# Dias simulados avançados em cada frame
DAYS_PER_FRAME = 0.8  # Controla a velocidade da simulação

# Dados reais dos planetas do sistema solar
# Cada planeta tem um dicionário com suas propriedades
PLANETS_RAW = [
    # Mercúrio
    {
        "name": "Mercury", 
        "radius_km": 2440, 
        "distance_mkm": 57.9, 
        "orbital_period_days": 88, 
        "color": (200, 200, 200),
        "temperature_c": 167, 
        "moons": 0, 
        "composition": "Rochoso", 
        "description": "O planeta mais próximo do Sol."
    },
    # Vénus
    {
        "name": "Venus", 
        "radius_km": 6052, 
        "distance_mkm": 108.2, 
        "orbital_period_days": 224.7, 
        "color": (255, 165, 0),
        "temperature_c": 464, 
        "moons": 0, 
        "composition": "Rochoso", 
        "description": "Conhecido como planeta irmão da Terra."
    },
    # Terra
    {
        "name": "Earth", 
        "radius_km": 6371, 
        "distance_mkm": 149.6, 
        "orbital_period_days": 365.2, 
        "color": (0, 100, 255),
        "temperature_c": 15, 
        "moons": 1, 
        "composition": "Rochoso", 
        "description": "O planeta azul."
    },
    # Marte
    {
        "name": "Mars", 
        "radius_km": 3390, 
        "distance_mkm": 227.9, 
        "orbital_period_days": 687, 
        "color": (255, 0, 0),
        "temperature_c": -65, 
        "moons": 2, 
        "composition": "Rochoso", 
        "description": "O planeta vermelho."
    },
    # Júpiter
    {
        "name": "Jupiter", 
        "radius_km": 69911, 
        "distance_mkm": 778.5, 
        "orbital_period_days": 4331, 
        "color": (255, 200, 100),
        "temperature_c": -110, 
        "moons": 79, 
        "composition": "Gasoso", 
        "description": "O maior planeta do sistema solar."
    },
    # Saturno (com anéis)
    {
        "name": "Saturn", 
        "radius_km": 58232, 
        "distance_mkm": 1434, 
        "orbital_period_days": 10747, 
        "color": (210, 180, 140),
        "temperature_c": -140, 
        "moons": 82, 
        "composition": "Gasoso", 
        "description": "Famoso pelos seus anéis.",
        "has_rings": True, 
        "ring_color": (200, 200, 180), 
        "ring_inner_radius": 1.5, 
        "ring_outer_radius": 2.3
    },
    # Úrano
    {
        "name": "Uranus", 
        "radius_km": 25362, 
        "distance_mkm": 2871, 
        "orbital_period_days": 30589, 
        "color": (100, 255, 255),
        "temperature_c": -195, 
        "moons": 27, 
        "composition": "Gasoso", 
        "description": "Planeta com eixo inclinado."
    },
    # Neptuno
    {
        "name": "Neptune", 
        "radius_km": 24622, 
        "distance_mkm": 4495, 
        "orbital_period_days": 59800, 
        "color": (0, 0, 255),
        "temperature_c": -200, 
        "moons": 14, 
        "composition": "Gasoso", 
        "description": "O planeta mais distante."
    },
]

# Configurações do Cinturão de Asteroides
# Distância interna em Unidades Astronómicas (UA)
ASTEROID_BELT_INNER = 2.2
# Distância externa em UA
ASTEROID_BELT_OUTER = 3.2
# Número de asteroides a criar
ASTEROID_COUNT = 200
# Cores possíveis para os asteroides
ASTEROID_COLORS = [(150, 150, 150), (180, 180, 180), (200, 200, 200)]
# Lista para armazenar os asteroides
asteroids = []

# Fator de conversão de UA para milhões de km
# 1 UA ≈ 149.6 milhões de km
AU_TO_MKM = 149.6

# Criar os asteroides do cinturão
for _ in range(ASTEROID_COUNT):
    # Distância aleatória dentro do cinturão (em UA)
    distance_au = random.uniform(ASTEROID_BELT_INNER, ASTEROID_BELT_OUTER)
    # Converter para milhões de km
    distance_mkm = distance_au * AU_TO_MKM
    
    # Ângulo orbital aleatório (0 a 2π)
    angle = random.uniform(0, 2 * math.pi)
    
    # Tamanho aleatório entre 1km e 500km
    radius_km = random.uniform(1, 500)
    # Converter raio para pixels (mínimo de 1 pixel)
    radius_px = max(1, int(radius_km * RADIUS_SCALE))
    
    # Escolher cor aleatória da lista
    color = random.choice(ASTEROID_COLORS)
    
    # Calcular velocidade orbital usando a 3ª Lei de Kepler
    # Período orbital em anos: T² = a³ (a em UA)
    period_years = math.sqrt(distance_au ** 3)
    # Converter período para dias
    period_days = period_years * 365.25
    # Calcular frames necessários para uma órbita completa
    frames_per_orbit = period_days / DAYS_PER_FRAME
    # Calcular velocidade angular (radianos por frame)
    speed = 2 * math.pi / frames_per_orbit
    
    # Adicionar asteroide à lista com todas suas propriedades
    asteroids.append({
        "distance_mkm": distance_mkm,  # Distância em milhões de km
        "distance": distance_mkm * DISTANCE_SCALE,  # Distância em pixels
        "angle": angle,  # Ângulo atual na órbita
        "speed": speed,  # Velocidade angular
        "radius": radius_px,  # Raio em pixels
        "color": color,  # Cor do asteroide
        "radius_km": radius_km  # Raio real em km
    })

# Lista para armazenar os planetas processados
PLANETS = []
# Processar cada planeta dos dados brutos
for p in PLANETS_RAW:
    # Converter distância para pixels
    distance_px = p["distance_mkm"] * DISTANCE_SCALE
    # Converter raio para pixels (mínimo de 2 pixels)
    radius_px = max(2, int(p["radius_km"] * RADIUS_SCALE))
    # Calcular frames por órbita completa
    frames_per_orbit = p["orbital_period_days"] / DAYS_PER_FRAME
    # Calcular velocidade angular
    speed = 2 * math.pi / frames_per_orbit
    
    # Criar dicionário com dados do planeta
    planet_data = {
        "name": p["name"],  # Nome do planeta
        "radius": radius_px,  # Raio em pixels
        "distance": distance_px,  # Distância em pixels
        "speed": speed,  # Velocidade orbital
        "color": p["color"],  # Cor do planeta
        "angle": 0,  # Ângulo inicial na órbita
        "rotation": 0,  # Rotação do planeta
        "trail": [],  # Lista para armazenar posições anteriores
        "radius_km": p["radius_km"],  # Raio real em km
        "distance_mkm": p["distance_mkm"],  # Distância real em milhões de km
        "orbital_period_days": p["orbital_period_days"],  # Período orbital em dias
        "temperature_c": p["temperature_c"],  # Temperatura média
        "moons": p["moons"],  # Número de luas
        "composition": p["composition"],  # Composição principal
        "description": p["description"],  # Descrição do planeta
    }
    
    # Adicionar dados dos anéis se o planeta tiver
    if "has_rings" in p:
        planet_data["has_rings"] = p["has_rings"]
        planet_data["ring_color"] = p["ring_color"]
        planet_data["ring_inner_radius"] = p["ring_inner_radius"]
        planet_data["ring_outer_radius"] = p["ring_outer_radius"]
    
    # Adicionar planeta à lista
    PLANETS.append(planet_data)

# Configurar fontes para texto
# Fonte padrão com tamanho 20
font = pygame.font.SysFont(None, 20)
# Fonte para mostrar FPS com tamanho 24
fps_font = pygame.font.SysFont(None, 24)
# Fonte para informações com tamanho 18
info_font = pygame.font.SysFont(None, 18)

# Variáveis para controlar a visualização
# Fator de zoom inicial
zoom = 1.0
# Deslocamento da câmara em X e Y
offset_x, offset_y = 0, 0
# Flag para indicar se está arrastando a vista
dragging = False
# Última posição do rato durante arrasto
last_mouse_pos = None

# Variáveis para seleção de planetas
# Planeta atualmente selecionado
selected_planet = None
# Alvo para deslocamento da câmara em X
target_offset_x = 0
# Alvo para deslocamento da câmara em Y
target_offset_y = 0
# Flag para indicar se a câmara está seguindo um planeta
camera_following = False
# Flag para pausar a simulação
paused = False

# Retângulo para o botão de pausa/retomar
button_rect = pygame.Rect(WIDTH - 140, 10, 120, 30)

def draw_starry_background():
    """
    Desenha o fundo estrelado com estrelas que mudam de brilho aleatoriamente
    """
    # Para cada estrela na lista
    for star in stars:
        # Alterar o brilho conforme a direção
        star["brightness"] += star["dir"] * random.randint(1, 3)
        
        # Limitar brilho máximo
        if star["brightness"] >= 255:
            star["brightness"] = 255
            # Inverter direção (começar a escurecer)
            star["dir"] = -1
        # Limitar brilho mínimo
        elif star["brightness"] <= 100:
            star["brightness"] = 100
            # Inverter direção (começar a clarear)
            star["dir"] = 1
        
        # Criar cor com o valor de brilho atual (tons de cinza)
        color = (star["brightness"],) * 3
        # Desenhar estrela na posição com a cor calculada
        screen.set_at((star["x"], star["y"]), color)

def transform_pos(center, x, y):
    """
    Transforma coordenadas considerando zoom e deslocamento da câmara
    """
    # Aplicar zoom e deslocamento à coordenada X
    tx = (x - center[0]) * zoom + center[0] + offset_x
    # Aplicar zoom e deslocamento à coordenada Y
    ty = (y - center[1]) * zoom + center[1] + offset_y
    # Retornar coordenadas como inteiros
    return int(tx), int(ty)

def draw_planet_orbit(center, planet):
    """
    Desenha a órbita de um planeta como um círculo branco
    """
    # Calcular raio da órbita considerando o zoom
    radius = int(planet["distance"] * zoom)
    # Desenhar apenas se o raio for positivo
    if radius > 0:
        # Desenhar círculo branco fina (1 pixel de largura)
        pygame.draw.circle(screen, WHITE, transform_pos(center, center[0], center[1]), radius, 1)

def draw_asteroid_belt(center):
    """
    Desenha o cinturão de asteroides entre Marte e Júpiter
    """
    # Calcular raios interno e externo considerando zoom
    inner_radius = ASTEROID_BELT_INNER * AU_TO_MKM * DISTANCE_SCALE * zoom
    outer_radius = ASTEROID_BELT_OUTER * AU_TO_MKM * DISTANCE_SCALE * zoom
    
    # Criar superfície translúcida para o cinturão
    belt_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    # Desenhar o raio externo com cor semi-transparente
    pygame.draw.circle(belt_surface, (100, 100, 100, 30), 
                      transform_pos(center, center[0], center[1]), outer_radius)
    # "Cortar" o centro para criar um anel
    pygame.draw.circle(belt_surface, (0, 0, 0, 0), 
                      transform_pos(center, center[0], center[1]), inner_radius)
    # Desenhar a superfície na tela
    screen.blit(belt_surface, (0, 0))
    
    # Desenhar cada asteroide individualmente
    for asteroid in asteroids:
        # Calcular posição usando ângulo e distância
        x = center[0] + math.cos(asteroid["angle"]) * asteroid["distance"]
        y = center[1] + math.sin(asteroid["angle"]) * asteroid["distance"]
        # Transformar posição considerando zoom e deslocamento
        tx, ty = transform_pos(center, x, y)
        # Calcular raio considerando zoom (mínimo 1 pixel)
        radius = max(1, int(asteroid["radius"] * zoom))
        
        # Verificar se o asteroide está visível na tela
        if (tx > -50 and tx < WIDTH + 50 and ty > -50 and ty < HEIGHT + 50):
            # Desenhar asteroide como círculo
            pygame.draw.circle(screen, asteroid["color"], (tx, ty), radius)

def draw_planet_rings(center, planet, tx, ty):
    """
    Desenha os anéis de um planeta (se tiver)
    """
    # Verificar se o planeta tem anéis
    if not planet.get("has_rings", False):
        return  # Sair se não tiver anéis
    
    # Calcular raios dos anéis considerando zoom
    inner_radius = planet["radius"] * planet["ring_inner_radius"] * zoom
    outer_radius = planet["radius"] * planet["ring_outer_radius"] * zoom
    
    # Criar superfície para os anéis com transparência
    ring_surface = pygame.Surface((outer_radius * 2, outer_radius * 2), pygame.SRCALPHA)
    # Desenhar parte externa dos anéis
    pygame.draw.circle(ring_surface, (*planet["ring_color"], 150), 
                      (outer_radius, outer_radius), outer_radius)
    # "Cortar" o centro para criar o anel
    pygame.draw.circle(ring_surface, (0, 0, 0, 0), 
                      (outer_radius, outer_radius), inner_radius)
    
    # Calcular ângulo de rotação dos anéis
    angle = planet["rotation"] * 2
    # Rodar a superfície dos anéis
    rotated_ring = pygame.transform.rotate(ring_surface, angle * 180/math.pi)
    # Obter retângulo para posicionar os anéis
    ring_rect = rotated_ring.get_rect(center=(tx, ty))
    # Desenhar anéis na tela
    screen.blit(rotated_ring, ring_rect)

def draw_sun(center):
    """
    Desenha o Sol no centro do sistema solar
    """
    # Calcular posição do Sol considerando zoom e deslocamento
    sun_x, sun_y = transform_pos(center, center[0], center[1])
    # Calcular raio do Sol considerando zoom (mínimo 5 pixels)
    sun_radius = max(5, int(20 * zoom))
    
    # Verificar se existe textura do Sol
    if sun_texture:
        # Tamanho da textura
        texture_size = sun_radius
        # Criar superfície para o Sol texturizado
        textured_sun = pygame.Surface((texture_size*2, texture_size*2), pygame.SRCALPHA)
        # Redimensionar textura para o tamanho atual
        scaled_texture = pygame.transform.scale(sun_texture, (texture_size*2, texture_size*2))
        # Aplicar textura
        textured_sun.blit(scaled_texture, (0, 0))
        # Criar máscara circular para a textura
        mask = pygame.Surface((texture_size*2, texture_size*2), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (texture_size, texture_size), texture_size)
        # Aplicar máscara para manter apenas a parte circular
        textured_sun.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        # Obter retângulo para posicionar o Sol
        sun_rect = textured_sun.get_rect(center=(sun_x, sun_y))
        # Desenhar Sol na tela
        screen.blit(textured_sun, sun_rect)

def draw_planet(center, planet):
    """
    Desenha um planeta na sua posição atual com seu rastro
    """
    # Calcular posição usando ângulo e distância
    x = center[0] + math.cos(planet["angle"]) * planet["distance"]
    y = center[1] + math.sin(planet["angle"]) * planet["distance"]
    # Transformar posição considerando zoom e deslocamento
    tx, ty = transform_pos(center, x, y)
    # Calcular raio considerando zoom (mínimo 1 pixel)
    radius = max(1, int(planet["radius"] * zoom))

    # Desenhar anéis primeiro (para ficarem atrás do planeta)
    draw_planet_rings(center, planet, tx, ty)

    # Desenhar sombra do planeta (deslocada 3 pixels)
    pygame.draw.circle(screen, (30, 30, 30), (tx+3, ty+3), radius+2)
    # Desenhar planeta com sua cor
    pygame.draw.circle(screen, planet["color"], (tx, ty), radius)

    # Desenhar indicador de rotação do planeta
    rot_len = radius  # Comprimento da linha
    rot_x = tx + math.cos(planet["rotation"]) * rot_len  # Ponto final X
    rot_y = ty + math.sin(planet["rotation"]) * rot_len  # Ponto final Y
    # Desenhar linha branca do centro até o ponto calculado
    pygame.draw.line(screen, WHITE, (tx, ty), (rot_x, rot_y), 2)

    # Criar texto com nome do planeta
    label = font.render(planet["name"], True, WHITE)
    # Posicionar texto acima do planeta
    label_rect = label.get_rect(center=(tx, ty - radius - 10))
    # Desenhar texto na tela
    screen.blit(label, label_rect)

    # Adicionar posição atual ao rastro
    planet["trail"].append((tx, ty))
    # Limitar tamanho do rastro a 50 pontos
    if len(planet["trail"]) > 50:
        planet["trail"].pop(0)

    # Desenhar rastro se tiver pelo menos 2 pontos
    if len(planet["trail"]) > 1:
        # Criar superfície para o rastro com transparência
        trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # Desenhar linhas entre pontos consecutivos do rastro
        for i in range(1, len(planet["trail"])):
            # Calcular transparência (mais transparente para pontos mais antigos)
            alpha = int(255 * (i / len(planet["trail"])))
            # Criar cor com transparência
            color = (*planet["color"], alpha)
            # Desenhar linha entre pontos do rastro
            pygame.draw.line(trail_surface, color, planet["trail"][i - 1], planet["trail"][i], 2)
        # Desenhar superfície do rastro na tela
        screen.blit(trail_surface, (0, 0))

def draw_info_panel(planet):
    """
    Desenha um painel com informações detalhadas sobre o planeta selecionado
    """
    # Dimensões do painel
    panel_w, panel_h = 320, 210
    # Margem das bordas
    margin = 20
    # Posição X (canto direito com margem)
    panel_x = WIDTH - panel_w - margin
    # Posição Y (canto inferior com margem)
    panel_y = HEIGHT - panel_h - margin
    
    # Desenhar fundo do painel (cinza escuro)
    pygame.draw.rect(screen, DARK_GRAY, (panel_x, panel_y, panel_w, panel_h))
    # Desenhar borda branca ao redor do painel
    pygame.draw.rect(screen, WHITE, (panel_x, panel_y, panel_w, panel_h), 2)

    # Lista de linhas de informação a mostrar
    lines = [
        f"Nome: {planet['name']}",
        f"Raio: {planet['radius_km']} km",
        f"Distância: {planet['distance_mkm']} milhões km",
        f"Período orbital: {planet['orbital_period_days']} dias",
        f"Temperatura média: {planet.get('temperature_c', 'N/A')} °C",
        f"Número de luas: {planet.get('moons', 0)}",
        f"Composição: {planet.get('composition', 'Desconhecida')}",
        f"Velocidade angular: {planet['speed']:.6f} rad/frame",
        f"Rotação: {planet['rotation']:.2f} rad",
        f"Descrição: {planet.get('description', '')}",
    ]

    # Desenhar cada linha de informação
    for i, line in enumerate(lines):
        # Renderizar texto
        txt = info_font.render(line, True, WHITE)
        # Posicionar texto com espaçamento vertical
        screen.blit(txt, (panel_x + 10, panel_y + 10 + i * 20))

def draw_menu():
    """
    Desenha o menu superior com botões e nomes dos planetas
    """
    # Desenhar fundo do menu (cinza escuro)
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, MENU_HEIGHT))

    # Obter posição do rato
    mx, my = pygame.mouse.get_pos()
    # Verificar se o rato está sobre o botão
    if button_rect.collidepoint(mx, my):
        # Usar cor de destaque
        color = BUTTON_HOVER_COLOR
    else:
        # Usar cor normal
        color = BUTTON_COLOR

    # Desenhar botão de pausa/retomar
    pygame.draw.rect(screen, color, button_rect)
    # Texto do botão muda conforme estado da simulação
    btn_text = font.render("Retomar" if paused else "Pausar", True, BUTTON_TEXT_COLOR)
    # Centralizar texto no botão
    btn_text_rect = btn_text.get_rect(center=button_rect.center)
    # Desenhar texto do botão
    screen.blit(btn_text, btn_text_rect)

    # Desenhar título do menu
    title = font.render("Selecione um Planeta", True, WHITE)
    screen.blit(title, (10, 8))

    # Desenhar nomes dos planetas no menu
    for i, planet in enumerate(PLANETS):
        # Calcular posição X (distribuídos horizontalmente)
        x = 20 + i * 120
        # Posição Y fixa
        y = 37
        # Usar cor de destaque se for o planeta selecionado
        color = HIGHLIGHT if planet == selected_planet else WHITE
        # Renderizar nome do planeta
        text = font.render(planet["name"], True, color)
        # Desenhar nome na posição calculada
        screen.blit(text, (x, y))

def check_menu_click(pos):
    """
    Verifica se houve clique em algum nome de planeta no menu
    Retorna o planeta clicado ou None
    """
    x, y = pos
    # Verificar se o clique foi dentro da área do menu
    if y < MENU_HEIGHT:
        # Verificar cada planeta no menu
        for i, planet in enumerate(PLANETS):
            # Calcular posição do nome do planeta
            px = 20 + i * 120
            py = 37
            # Criar retângulo para área clicável
            planet_rect = pygame.Rect(px, py, 110, 25)
            # Verificar se o clique foi nesta área
            if planet_rect.collidepoint(x, y):
                # Retornar planeta correspondente
                return PLANETS[i]
    # Retornar None se não clicou em nenhum planeta
    return None

def main():
    """
    Função principal que controla o loop do jogo
    """
    # Calcular centro do sistema (considerando altura do menu)
    center = (WIDTH // 2, (HEIGHT + MENU_HEIGHT) // 2)

    # Dias simulados acumulados
    simulated_days = 0

    # Declarar variáveis globais que serão modificadas
    global zoom, offset_x, offset_y, dragging, last_mouse_pos
    global selected_planet, paused, camera_following

    def lerp(a, b, t):
        """
        Interpolação linear entre a e b com fator t
        Usado para transições suaves de zoom e movimento
        """
        return a + (b - a) * t

    # Configurar relógio para controlar FPS
    clock = pygame.time.Clock()
    # Flag para controlar o loop principal
    running = True

    # Loop principal do jogo
    while running:
        # Obter tempo desde o último frame
        dt = clock.tick(FPS)
        # Atualizar dias simulados (se não estiver pausado)
        if not paused:
            simulated_days += DAYS_PER_FRAME
        
        # Obter estado das teclas
        teclas = pygame.key.get_pressed()

        # Processar eventos
        for event in pygame.event.get():
            # Evento de fechar a janela
            if event.type == pygame.QUIT:
                running = False

            # Evento de clique do rato
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Botão esquerdo do rato
                if event.button == 1:
                    # Verificar se clicou no botão de pausa
                    if button_rect.collidepoint(event.pos):
                        # Alternar estado de pausa
                        paused = not paused
                        # Tocar som se existir
                        if click_sound:
                            click_sound.play()
                    else:
                        # Obter posição do clique
                        mx, my = event.pos
                        # Verificar se clicou em algum nome de planeta no menu
                        clicked_planet = check_menu_click(event.pos)
                        if clicked_planet:
                            # Definir planeta selecionado
                            selected_planet = clicked_planet
                            # Tocar som se existir
                            if click_sound:
                                click_sound.play()

                            # Calcular posição atual do planeta
                            planet_x = center[0] + math.cos(selected_planet["angle"]) * selected_planet["distance"]
                            planet_y = center[1] + math.sin(selected_planet["angle"]) * selected_planet["distance"]

                            # Transformar para coordenadas de tela
                            tx, ty = transform_pos(center, planet_x, planet_y)

                            # Calcular deslocamento necessário para centralizar o planeta
                            target_offset_x = WIDTH // 2 - tx
                            target_offset_y = HEIGHT//2 - ty
                            # Ativar modo de seguir planeta
                            camera_following = True
                        else:
                            # Verificar se clicou diretamente em um planeta (do mais próximo para o mais distante)
                            for planet in reversed(PLANETS):
                                # Calcular posição do planeta
                                px = center[0] + math.cos(planet["angle"]) * planet["distance"]
                                py = center[1] + math.sin(planet["angle"]) * planet["distance"]
                                # Transformar para coordenadas de tela
                                tx, ty = transform_pos(center, px, py)
                                # Calcular raio em pixels
                                radius = max(1, int(planet["radius"] * zoom))
                                # Calcular distância do clique ao centro do planeta
                                dist = math.hypot(tx - mx, ty - my)
                                # Verificar se clique foi dentro do planeta
                                if dist <= radius:
                                    # Selecionar planeta
                                    selected_planet = planet
                                    # Tocar som se existir
                                    if click_sound:
                                        click_sound.play()
                                    break
                            else:
                                # Nenhum planeta foi clicado
                                selected_planet = None

                            # Começar a arrastar a vista
                            dragging = True
                            # Guardar posição inicial do arrasto
                            last_mouse_pos = event.pos

                # Roda do rato para cima - zoom in
                elif event.button == 4:
                    zoom = min(5, zoom * 1.1)
                # Roda do rato para baixo - zoom out
                elif event.button == 5:
                    zoom = max(0.07, zoom / 1.1)

            # Evento de soltar botão do rato
            elif event.type == pygame.MOUSEBUTTONUP:
                # Botão esquerdo
                if event.button == 1:
                    # Parar de arrastar
                    dragging = False

            # Evento de movimento do rato
            elif event.type == pygame.MOUSEMOTION:
                # Se estiver arrastando
                if dragging:
                    # Obter posição atual
                    mx, my = event.pos
                    # Obter última posição
                    lx, ly = last_mouse_pos
                    # Atualizar deslocamento da câmara
                    offset_x += mx - lx
                    offset_y += my - ly
                    # Atualizar última posição
                    last_mouse_pos = (mx, my)
                    # Desativar modo de seguir planeta
                    camera_following = False

        # Lógica para seguir o planeta selecionado
        if camera_following and selected_planet:
            # Calcular posição atual do planeta
            planet_x = center[0] + math.cos(selected_planet["angle"]) * selected_planet["distance"]
            planet_y = center[1] + math.sin(selected_planet["angle"]) * selected_planet["distance"]

            # Configurações de zoom para diferentes planetas
            min_zoom = 0.4  # Zoom mínimo
            max_zoom = 2.5  # Zoom máximo
            max_distance = max(p["distance"] for p in PLANETS)  # Maior distância
            
            # Distâncias de referência para ajuste de zoom
            zoom_planet_jupiter = 3500
            zoom_planet_saturn = 4000
            zoom_planet_urano = 4400
            zoom_planet_neptune = 4550

            # Escolher distância de referência conforme o planeta selecionado
            if selected_planet["name"] in ["Jupiter"]:
                distance_for_zoom = zoom_planet_jupiter
            elif selected_planet["name"] in ["Saturn"]:
                distance_for_zoom = zoom_planet_saturn
            elif selected_planet["name"] in ["Uranus"]:
                distance_for_zoom = zoom_planet_urano
            elif selected_planet["name"] in ["Neptune"]:
                distance_for_zoom = zoom_planet_neptune
            else:
                distance_for_zoom = selected_planet["distance"]

            # Calcular zoom desejado baseado na distância
            desired_zoom = max_zoom - (distance_for_zoom / max_distance) * (max_zoom - min_zoom)

            # Aplicar interpolação suave para o zoom
            zoom = lerp(zoom, desired_zoom, 0.15)

            # Transformar posição do planeta para coordenadas de tela
            tx, ty = transform_pos(center, planet_x, planet_y)

            # Calcular deslocamento necessário para centralizar o planeta
            target_offset_x = WIDTH // 2 - tx
            target_offset_y = HEIGHT // 2 - ty

            # Aplicar interpolação suave para o deslocamento
            offset_x = lerp(offset_x, target_offset_x, 0.1)
            offset_y = lerp(offset_y, target_offset_y, 0.1)

        # Limpar a tela com fundo preto
        screen.fill(BLACK)
        # Desenhar fundo estrelado
        draw_starry_background()

        # Desenhar o Sol no centro
        draw_sun(center)

        # Desenhar órbitas e planetas
        for planet in PLANETS:
            # Atualizar posição e rotação se não estiver pausado
            if not paused:
                planet["angle"] += planet["speed"]
                planet["rotation"] += 0.1

            # Desenhar órbita do planeta
            draw_planet_orbit(center, planet)
            # Desenhar planeta
            draw_planet(center, planet)

        # Atualizar posição dos asteroides se não estiver pausado
        if not paused:
            for asteroid in asteroids:
                asteroid["angle"] += asteroid["speed"]
        
        # Desenhar cinturão de asteroides
        draw_asteroid_belt(center)

        # Desenhar menu superior
        draw_menu()

        # Desenhar painel de informações se houver planeta selecionado
        if selected_planet:
            draw_info_panel(selected_planet)

        # Mostrar FPS atual
        fps = clock.get_fps()
        fps_text = fps_font.render(f"FPS: {int(fps)}", True, WHITE)
        screen.blit(fps_text, (10, HEIGHT - fps_text.get_height() - 10))

        # Mostrar tempo simulado acumulado
        time_text = fps_font.render(f"Tempo simulado: {int(simulated_days):,} dias", True, WHITE)
        screen.blit(time_text, (10, HEIGHT - fps_text.get_height() - 35))

        # Atualizar a tela
        pygame.display.flip()
        # Manter taxa de frames constante
        clock.tick(FPS)

    # Encerrar o Pygame ao sair do loop
    pygame.quit()

# Verificar se este script está sendo executado diretamente
if __name__ == "__main__":
    # Iniciar a função principal
    main()
import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 1280, 720
MENU_HEIGHT = 70
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sistema Solar")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (30, 30, 30)
HIGHLIGHT = (100, 150, 255)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = WHITE

try:
    pygame.mixer.music.load("space_music.ogg")
    pygame.mixer.music.play(-1)
except Exception:
    pass

try:
    click_sound = pygame.mixer.Sound("click.wav")
except Exception:
    click_sound = None

NUM_STARS = 150
stars = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT), "brightness": random.randint(100, 255), "dir": random.choice([-1, 1])} for _ in range(NUM_STARS)]

# Escalas para caber na tela visualmente
DISTANCE_SCALE = 0.5  # escala de distância (milhões km para pixels)
RADIUS_SCALE = 0.0005  # escala de raio (km para pixels)

# Frames por segundo e dias por frame (ajustar a velocidade da simulação)
FPS = 60
DAYS_PER_FRAME = 0.8  # Ajustado para desacelerar ainda mais

# Dados reais dos planetas:
# raio em km, distância média ao sol em milhões de km, período orbital em dias, cor
PLANETS_RAW = [
    {"name": "Mercury", "radius_km": 2440, "distance_mkm": 57.9, "orbital_period_days": 88, "color": (200, 200, 200),
     "temperature_c": 167, "moons": 0, "composition": "Rochoso", "description": "O planeta mais próximo do Sol."},

    {"name": "Venus", "radius_km": 6052, "distance_mkm": 108.2, "orbital_period_days": 224.7, "color": (255, 165, 0),
     "temperature_c": 464, "moons": 0, "composition": "Rochoso", "description": "Conhecido como planeta irmão da Terra."},

    {"name": "Earth", "radius_km": 6371, "distance_mkm": 149.6, "orbital_period_days": 365.2, "color": (0, 100, 255),
     "temperature_c": 15, "moons": 1, "composition": "Rochoso", "description": "O planeta azul."},

    {"name": "Mars", "radius_km": 3390, "distance_mkm": 227.9, "orbital_period_days": 687, "color": (255, 0, 0),
     "temperature_c": -65, "moons": 2, "composition": "Rochoso", "description": "O planeta vermelho."},

    {"name": "Jupiter", "radius_km": 69911, "distance_mkm": 778.5, "orbital_period_days": 4331, "color": (255, 200, 100),
     "temperature_c": -110, "moons": 79, "composition": "Gasoso", "description": "O maior planeta do sistema solar."},

    {"name": "Saturn", "radius_km": 58232, "distance_mkm": 1434, "orbital_period_days": 10747, "color": (210, 180, 140),
     "temperature_c": -140, "moons": 82, "composition": "Gasoso", "description": "Famoso pelos seus anéis."},

    {"name": "Uranus", "radius_km": 25362, "distance_mkm": 2871, "orbital_period_days": 30589, "color": (100, 255, 255),
     "temperature_c": -195, "moons": 27, "composition": "Gasoso", "description": "Planeta com eixo inclinado."},

    {"name": "Neptune", "radius_km": 24622, "distance_mkm": 4495, "orbital_period_days": 59800, "color": (0, 0, 255),
     "temperature_c": -200, "moons": 14, "composition": "Gasoso", "description": "O planeta mais distante."},
]

PLANETS = []
for p in PLANETS_RAW:
    distance_px = p["distance_mkm"] * DISTANCE_SCALE
    radius_px = max(2, int(p["radius_km"] * RADIUS_SCALE))
    frames_per_orbit = p["orbital_period_days"] / DAYS_PER_FRAME
    speed = 2 * math.pi / frames_per_orbit
    PLANETS.append({
        "name": p["name"],
        "radius": radius_px,
        "distance": distance_px,
        "speed": speed,
        "color": p["color"],
        "angle": 0,
        "rotation": 0,
        "trail": [],
        "radius_km": p["radius_km"],
        "distance_mkm": p["distance_mkm"],
        "orbital_period_days": p["orbital_period_days"],
        "temperature_c": p["temperature_c"],
        "moons": p["moons"],
        "composition": p["composition"],
        "description": p["description"],
    })

font = pygame.font.SysFont(None, 20)
fps_font = pygame.font.SysFont(None, 24)
info_font = pygame.font.SysFont(None, 18)

zoom = 1.0
offset_x, offset_y = 0, 0
dragging = False
last_mouse_pos = None

selected_planet = None
target_offset_x = 0
target_offset_y = 0
camera_following = False
paused = False

# Botão Pausar/Retomar
button_rect = pygame.Rect(WIDTH - 140, 10, 120, 30)

def draw_starry_background():
    for star in stars:
        star["brightness"] += star["dir"] * random.randint(1, 3)
        if star["brightness"] >= 255:
            star["brightness"] = 255
            star["dir"] = -1
        elif star["brightness"] <= 100:
            star["brightness"] = 100
            star["dir"] = 1
        color = (star["brightness"],) * 3
        screen.set_at((star["x"], star["y"]), color)

def transform_pos(center, x, y):
    tx = (x - center[0]) * zoom + center[0] + offset_x
    ty = (y - center[1]) * zoom + center[1] + offset_y
    return int(tx), int(ty)

def draw_planet_orbit(center, planet):
    radius = int(planet["distance"] * zoom)
    if radius > 0:
        pygame.draw.circle(screen, WHITE, transform_pos(center, center[0], center[1]), radius, 1)

def draw_planet(center, planet):
    x = center[0] + math.cos(planet["angle"]) * planet["distance"]
    y = center[1] + math.sin(planet["angle"]) * planet["distance"]
    tx, ty = transform_pos(center, x, y)
    radius = max(1, int(planet["radius"] * zoom))

    pygame.draw.circle(screen, (30, 30, 30), (tx+3, ty+3), radius+2)
    pygame.draw.circle(screen, planet["color"], (tx, ty), radius)

    rot_len = radius
    rot_x = tx + math.cos(planet["rotation"]) * rot_len
    rot_y = ty + math.sin(planet["rotation"]) * rot_len
    pygame.draw.line(screen, WHITE, (tx, ty), (rot_x, rot_y), 2)

    label = font.render(planet["name"], True, WHITE)
    label_rect = label.get_rect(center=(tx, ty - radius - 10))
    screen.blit(label, label_rect)

    planet["trail"].append((tx, ty))
    if len(planet["trail"]) > 50:
        planet["trail"].pop(0)

    if len(planet["trail"]) > 1:
        trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for i in range(1, len(planet["trail"])):
            alpha = int(255 * (i / len(planet["trail"])))
            color = (*planet["color"], alpha)
            pygame.draw.line(trail_surface, color, planet["trail"][i - 1], planet["trail"][i], 2)
        screen.blit(trail_surface, (0, 0))

def draw_info_panel(planet):
    panel_w, panel_h = 320, 210
    margin = 20
    panel_x = WIDTH - panel_w - margin
    panel_y = HEIGHT - panel_h - margin
    pygame.draw.rect(screen, DARK_GRAY, (panel_x, panel_y, panel_w, panel_h))
    pygame.draw.rect(screen, WHITE, (panel_x, panel_y, panel_w, panel_h), 2)

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

    for i, line in enumerate(lines):
        txt = info_font.render(line, True, WHITE)
        screen.blit(txt, (panel_x + 10, panel_y + 10 + i * 20))

def draw_menu():
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, MENU_HEIGHT))

    # Botão Pausar/Retomar
    mx, my = pygame.mouse.get_pos()
    if button_rect.collidepoint(mx, my):
        color = BUTTON_HOVER_COLOR
    else:
        color = BUTTON_COLOR

    pygame.draw.rect(screen, color, button_rect)
    btn_text = font.render("Retomar" if paused else "Pausar", True, BUTTON_TEXT_COLOR)
    btn_text_rect = btn_text.get_rect(center=button_rect.center)
    screen.blit(btn_text, btn_text_rect)

    title = font.render("Selecione um Planeta", True, WHITE)
    screen.blit(title, (10, 8))

    for i, planet in enumerate(PLANETS):
        x = 20 + i * 120  # coloca todos em uma única linha
        y = 37            # mantém todos na mesma altura
        color = HIGHLIGHT if planet == selected_planet else WHITE
        text = font.render(planet["name"], True, color)
        screen.blit(text, (x, y))


def check_menu_click(pos):
    x, y = pos
    if y < MENU_HEIGHT:
        for i, planet in enumerate(PLANETS):
            px = 20 + i * 120
            py = 37
            planet_rect = pygame.Rect(px, py, 110, 25)
            if planet_rect.collidepoint(x, y):
                return PLANETS[i]
    return None

def main():

    center = (WIDTH // 2, (HEIGHT + MENU_HEIGHT) // 2)

    simulated_days = 0

    global zoom, offset_x, offset_y, dragging, last_mouse_pos, selected_planet, paused, camera_following

    def lerp(a, b, t):
        return a + (b - a) * t

    clock = pygame.time.Clock()
    running = True
    center = (WIDTH // 2, (HEIGHT + MENU_HEIGHT) // 2)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_rect.collidepoint(event.pos):
                        paused = not paused
                        if click_sound:
                            click_sound.play()
                    else:
                        mx, my = event.pos
                        clicked_planet = check_menu_click(event.pos)
                        if clicked_planet:
                            selected_planet = clicked_planet
                            if click_sound:
                                click_sound.play()

                            # Calcular posição do planeta e ajustar offset para centralizá-lo
                            planet_x = center[0] + math.cos(selected_planet["angle"]) * selected_planet["distance"]
                            planet_y = center[1] + math.sin(selected_planet["angle"]) * selected_planet["distance"]

                            tx, ty = transform_pos(center, planet_x, planet_y)

                            target_offset_x = WIDTH // 2 - tx
                            target_offset_y = HEIGHT//2 - ty
                            camera_following = True
                        else:
                            for planet in reversed(PLANETS):
                                px = center[0] + math.cos(planet["angle"]) * planet["distance"]
                                py = center[1] + math.sin(planet["angle"]) * planet["distance"]
                                tx, ty = transform_pos(center, px, py)
                                radius = max(1, int(planet["radius"] * zoom))
                                dist = math.hypot(tx - mx, ty - my)
                                if dist <= radius:
                                    selected_planet = planet
                                    if click_sound:
                                        click_sound.play()
                                    break
                            else:
                                selected_planet = None

                            dragging = True
                            last_mouse_pos = event.pos

                elif event.button == 4:
                    zoom = min(5, zoom * 1.1)
                elif event.button == 5:
                    zoom = max(0.1, zoom / 1.1)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mx, my = event.pos
                    lx, ly = last_mouse_pos
                    offset_x += mx - lx
                    offset_y += my - ly
                    last_mouse_pos = (mx, my)
                    camera_following = False

        if camera_following and selected_planet:
            planet_x = center[0] + math.cos(selected_planet["angle"]) * selected_planet["distance"]
            planet_y = center[1] + math.sin(selected_planet["angle"]) * selected_planet["distance"]

            min_zoom = 0.4
            max_zoom = 2.5
            max_distance = max(p["distance"] for p in PLANETS)
            neptune = next(p for p in PLANETS if p["name"] == "Neptune")

            if selected_planet["name"] in ["Jupiter", "Saturn", "Uranus"]:
                distance_for_zoom = neptune["distance"]
            else:
                distance_for_zoom = selected_planet["distance"]

            desired_zoom = max_zoom - (distance_for_zoom / max_distance) * (max_zoom - min_zoom)

            # Se for Netuno, garante zoom mínimo para ele ficar visível
            if selected_planet["name"] == "Neptune":
                desired_zoom = max(desired_zoom, 0.7)  # força pelo menos 0.7 de zoom no Netuno

            zoom = lerp(zoom, desired_zoom, 0.15)

            tx, ty = transform_pos(center, planet_x, planet_y)

            # Ajuste para centralizar o planeta na área visível (considerando MENU_WIDTH)
            target_offset_x = WIDTH // 2 - tx
            target_offset_y = HEIGHT // 2 - ty

            offset_x = lerp(offset_x, target_offset_x, 0.1)
            offset_y = lerp(offset_y, target_offset_y, 0.1)

        screen.fill(BLACK)
        draw_starry_background()

        sun_x, sun_y = transform_pos(center, center[0], center[1])
        pygame.draw.circle(screen, (255, 255, 0), (sun_x, sun_y), max(5, int(20 * zoom)))

        for planet in PLANETS:
            if not paused:
                planet["angle"] += planet["speed"]
                planet["rotation"] += 0.1

            draw_planet_orbit(center, planet)
            draw_planet(center, planet)

        draw_menu()

        if selected_planet:
            draw_info_panel(selected_planet)

        fps = clock.get_fps()
        if not paused:
            simulated_days += DAYS_PER_FRAME
        fps_text = fps_font.render(f"FPS: {int(fps)}", True, WHITE)
        screen.blit(fps_text, (10, HEIGHT - fps_text.get_height() - 10))

        # Mostra o tempo simulado
        time_text = fps_font.render(f"Tempo simulado: {int(simulated_days):,} dias", True, WHITE)
        screen.blit(time_text, (10, HEIGHT - fps_text.get_height() - 35))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

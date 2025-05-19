import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 1280, 720
MENU_WIDTH = 220
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

PLANETS = [
    {"name": "Mercury", "radius": 4, "distance": 50, "speed": 0.05, "color": (200, 200, 200), "angle": 0, "rotation": 0, "trail": []},
    {"name": "Venus", "radius": 6, "distance": 80, "speed": 0.035, "color": (255, 165, 0), "angle": 0, "rotation": 0, "trail": []},
    {"name": "Earth", "radius": 7, "distance": 110, "speed": 0.03, "color": (0, 100, 255), "angle": 0, "rotation": 0, "trail": []},
    {"name": "Mars", "radius": 6, "distance": 140, "speed": 0.025, "color": (255, 0, 0), "angle": 0, "rotation": 0, "trail": []},
    {"name": "Jupiter", "radius": 12, "distance": 180, "speed": 0.02, "color": (255, 200, 100), "angle": 0, "rotation": 0, "trail": []},
    {"name": "Saturn", "radius": 10, "distance": 230, "speed": 0.017, "color": (210, 180, 140), "angle": 0, "rotation": 0, "trail": []},
    {"name": "Uranus", "radius": 9, "distance": 270, "speed": 0.014, "color": (100, 255, 255), "angle": 0, "rotation": 0, "trail": []},
    {"name": "Neptune", "radius": 9, "distance": 310, "speed": 0.012, "color": (0, 0, 255), "angle": 0, "rotation": 0, "trail": []},
]

font = pygame.font.SysFont(None, 20)
fps_font = pygame.font.SysFont(None, 24)
info_font = pygame.font.SysFont(None, 18)

zoom = 1.0
offset_x, offset_y = 0, 0
dragging = False
last_mouse_pos = None

selected_planet = None
paused = False

# Botão Pausar/Retomar
button_rect = pygame.Rect(WIDTH - MENU_WIDTH + 20, 10, MENU_WIDTH - 40, 30)

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
    panel_w, panel_h = MENU_WIDTH - 20, 140
    panel_x = WIDTH - MENU_WIDTH + 10
    panel_y = HEIGHT - panel_h - 20
    pygame.draw.rect(screen, DARK_GRAY, (panel_x, panel_y, panel_w, panel_h))
    pygame.draw.rect(screen, WHITE, (panel_x, panel_y, panel_w, panel_h), 2)

    lines = [
        f"Nome: {planet['name']}",
        f"Raio: {planet['radius']} px",
        f"Distância: {planet['distance']} px",
        f"Velocidade: {planet['speed']:.4f} rad/frame",
        f"Rotação: {planet['rotation']:.2f} rad",
    ]

    for i, line in enumerate(lines):
        txt = info_font.render(line, True, WHITE)
        screen.blit(txt, (panel_x + 10, panel_y + 10 + i * 25))

def draw_menu():
    pygame.draw.rect(screen, DARK_GRAY, (WIDTH - MENU_WIDTH, 0, MENU_WIDTH, HEIGHT))

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

    title = font.render("Planetas", True, WHITE)
    screen.blit(title, (WIDTH - MENU_WIDTH + 10, 50))

    for i, planet in enumerate(PLANETS):
        y = 80 + i * 30
        color = HIGHLIGHT if planet == selected_planet else WHITE
        text = font.render(planet["name"], True, color)
        screen.blit(text, (WIDTH - MENU_WIDTH + 20, y))

def check_menu_click(pos):
    x, y = pos
    if x < WIDTH - MENU_WIDTH:
        return None
    idx = (y - 80) // 30
    if 0 <= idx < len(PLANETS):
        return PLANETS[idx]
    return None

def main():
    global zoom, offset_x, offset_y, dragging, last_mouse_pos, selected_planet, paused

    clock = pygame.time.Clock()
    running = True
    center = (WIDTH // 2 - MENU_WIDTH//2, HEIGHT // 2)

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
                        else:
                            for planet in PLANETS:
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
        fps_text = fps_font.render(f"FPS: {int(fps)}", True, WHITE)
        screen.blit(fps_text, (10, HEIGHT - fps_text.get_height() - 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

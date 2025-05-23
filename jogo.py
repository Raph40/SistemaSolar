import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Chicken Invaders")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Fonte
fonte = pygame.font.SysFont("Arial", 28)
titulo_fonte = pygame.font.SysFont("Arial", 48, bold=True)

# Carregamento de imagens
nave_img = pygame.image.load("./texturas/Nave.png").convert_alpha()
inimigo_img = pygame.image.load("./texturas/Asteroide.png").convert_alpha()
tiro_img = pygame.Surface((5, 15))
tiro_img.fill((255, 255, 0))

# Carregamento de sons
pygame.mixer.init()
tiro_som = pygame.mixer.Sound("./musicas/som_tiro.wav")
explosao_som = pygame.mixer.Sound("./musicas/som_explosao.wav")
colisao_som = pygame.mixer.Sound("./musicas/som_colisao.wav")
fundo_som = pygame.mixer.Sound("space_music.ogg")
fundo_som.set_volume(0.3)

# Ajuste do volume dos efeitos sonoros
tiro_som.set_volume(0.03)
explosao_som.set_volume(0.1)
colisao_som.set_volume(0.3)

# Classes
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(nave_img, (50, 50))
        self.rect = self.image.get_rect(center=(LARGURA // 2, ALTURA - 60))
        self.vel = 5
        self.vidas = 3

    def update(self, teclas):
        if teclas[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.vel
        if teclas[pygame.K_d] and self.rect.right < LARGURA:
            self.rect.x += self.vel
        if teclas[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.vel
        if teclas[pygame.K_s] and self.rect.bottom < ALTURA:
            self.rect.y += self.vel

class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = tiro_img
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.vel = -8

    def update(self, *args):
        self.rect.y += self.vel
        if self.rect.bottom < 0:
            self.kill()

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, velocidade_extra=0):
        super().__init__()
        self.image = pygame.transform.scale(inimigo_img, (40, 40))
        self.rect = self.image.get_rect(center=(random.randint(40, LARGURA-40), -40))
        self.velx = random.choice([-2, -1, 1, 2])
        self.vely = random.randint(1, 3) + velocidade_extra

    def update(self, *args):
        self.rect.x += self.velx
        self.rect.y += self.vely
        if self.rect.left < 0 or self.rect.right > LARGURA:
            self.velx *= -1
        if self.rect.top > ALTURA:
            self.kill()

# Funções
def desenhar_texto_centralizado(texto, rect):
    img = fonte.render(texto, True, BRANCO)
    img_rect = img.get_rect(center=rect.center)
    tela.blit(img, img_rect)

def menu_inicial():
    botao_jogar = pygame.Rect(LARGURA//2 - 100, ALTURA//2 - 25, 200, 50)
    botao_sair = pygame.Rect(LARGURA//2 - 100, ALTURA//2 + 50, 200, 50)
    esperando = True
    while esperando:
        tela.fill(PRETO)
        # Título do menu
        titulo = titulo_fonte.render("Chicken Invaders", True, BRANCO)
        titulo_rect = titulo.get_rect(center=(LARGURA//2, ALTURA//2 - 100))
        tela.blit(titulo, titulo_rect)

        # Botão "Começar Jogo" com fundo preto e borda branca
        pygame.draw.rect(tela, PRETO, botao_jogar, border_radius=10)
        pygame.draw.rect(tela, BRANCO, botao_jogar, width=2, border_radius=10)
        desenhar_texto_centralizado("Começar Jogo", botao_jogar)
        # Botão "Sair" com fundo preto e borda branca
        pygame.draw.rect(tela, PRETO, botao_sair, border_radius=10)
        pygame.draw.rect(tela, BRANCO, botao_sair, width=2, border_radius=10)
        desenhar_texto_centralizado("Sair", botao_sair)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    esperando = False
                elif botao_sair.collidepoint(evento.pos):
                    pygame.quit()
                    exit()

def mostrar_tela_fim(score):
    botao = pygame.Rect(LARGURA//2 - 100, ALTURA//2 + 40, 200, 50)
    esperando = True
    while esperando:
        tela.fill(PRETO)
        desenhar_texto_centralizado("Game Over", pygame.Rect(LARGURA//2 - 100, ALTURA//2 - 60, 200, 30))
        desenhar_texto_centralizado(f"Score Final: {score}", pygame.Rect(LARGURA//2 - 100, ALTURA//2 - 20, 200, 30))
        # Botão "Voltar ao Menu" com fundo preto e borda branca
        pygame.draw.rect(tela, PRETO, botao, border_radius=10)
        pygame.draw.rect(tela, BRANCO, botao, width=2, border_radius=10)
        desenhar_texto_centralizado("Voltar ao Menu", botao)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao.collidepoint(evento.pos):
                    esperando = False
                    menu_inicial()
                    iniciar_jogo()

# Inicialização
def iniciar_jogo():
    fundo_som.play(-1)
    todos_sprites = pygame.sprite.Group()
    tiros = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    nave = Nave()
    todos_sprites.add(nave)
    score = 0
    tempo_jogo = 0
    velocidade_extra_inimigo = 0

    clock = pygame.time.Clock()
    rodando = True
    SPAWN_INIMIGO = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_INIMIGO, 1000)

    while rodando:
        dt = clock.tick(60)
        tempo_jogo += dt
        teclas = pygame.key.get_pressed()

        if tempo_jogo // 10000 > velocidade_extra_inimigo:
            velocidade_extra_inimigo += 1
            nave.vel += 0.5

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    tiro = Tiro(nave.rect.centerx, nave.rect.top)
                    todos_sprites.add(tiro)
                    tiros.add(tiro)
                    tiro_som.play()
            if evento.type == SPAWN_INIMIGO:
                for _ in range(1 + velocidade_extra_inimigo):
                    inimigo = Inimigo(velocidade_extra_inimigo)
                    todos_sprites.add(inimigo)
                    inimigos.add(inimigo)

        todos_sprites.update(teclas)

        # Colisões
        for inimigo in inimigos:
            if nave.rect.colliderect(inimigo.rect):
                inimigo.kill()
                nave.vidas -= 1
                colisao_som.play()
                if nave.vidas <= 0:
                    fundo_som.stop()
                    rodando = False

        for tiro in tiros:
            hits = pygame.sprite.spritecollide(tiro, inimigos, True)
            if hits:
                tiro.kill()
                score += 10
                explosao_som.play()

        # Desenho
        tela.fill(PRETO)
        todos_sprites.draw(tela)
        desenhar_texto_centralizado(f"Score: {score}", pygame.Rect(10, 10, 200, 30))
        desenhar_texto_centralizado(f"Vidas: {nave.vidas}", pygame.Rect(10, 40, 200, 30))
        pygame.display.flip()

    mostrar_tela_fim(score)

menu_inicial()
iniciar_jogo()

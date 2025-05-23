# Importar a biblioteca pygame para criar o jogo
import pygame
# Importar a biblioteca random para gerar números aleatórios
import random

# Inicializar todos os módulos da biblioteca pygame
pygame.init()

# Configurações da janela do jogo
LARGURA, ALTURA = 800, 600  # Definir largura e altura da janela
tela = pygame.display.set_mode((LARGURA, ALTURA))  # Criar a janela do jogo
pygame.display.set_caption("Star Ship")  # Definir o título da janela

# Definir cores em formato RGB (Red, Green, Blue)
BRANCO = (255, 255, 255)  # Cor branca
PRETO = (0, 0, 0)  # Cor preta
VERMELHO = (255, 0, 0)  # Cor vermelha
CINZA = (100, 100, 100, 128)  # Cor cinza semi-transparente para o menu de pausa

# Configurar as fontes de texto
fonte = pygame.font.SysFont("Arial", 28)  # Fonte normal tamanho 28
titulo_fonte = pygame.font.SysFont("Arial", 48, bold=True)  # Fonte em negrito tamanho 48

# Carregar imagens para o jogo
nave_img = pygame.image.load("./texturas/Nave.png").convert_alpha()  # Imagem da nave do jogador
inimigo_img = pygame.image.load("./texturas/Asteroide.png").convert_alpha()  # Imagem dos inimigos/asteroides
tiro_img = pygame.Surface((5, 15))  # Criar superfície para os tiros
tiro_img.fill((255, 255, 0))  # Pintar os tiros de amarelo

# Inicializar o sistema de som do pygame
pygame.mixer.init()
# Carregar os efeitos sonoros
tiro_som = pygame.mixer.Sound("./musicas/som_tiro.wav")  # Som do tiro
explosao_som = pygame.mixer.Sound("./musicas/som_explosao.wav")  # Som da explosão
colisao_som = pygame.mixer.Sound("./musicas/som_colisao.wav")  # Som da colisão
fundo_som = pygame.mixer.Sound("space_music.ogg")  # Música de fundo
fundo_som.set_volume(0.3)  # Definir volume da música de fundo

# Ajustar os volumes dos efeitos sonoros
tiro_som.set_volume(0.03)  # Volume baixo para o som do tiro
explosao_som.set_volume(0.1)  # Volume médio para o som da explosão
colisao_som.set_volume(0.3)  # Volume mais alto para o som da colisão

# Configurar o fundo estrelado
stars = []  # Lista para guardar as estrelas
for _ in range(200):  # Criar 200 estrelas
    # Posição aleatória para cada estrela
    x = random.randint(0, LARGURA - 1)
    y = random.randint(0, ALTURA - 1)
    # Brilho inicial aleatório entre 100 e 255
    brightness = random.randint(100, 255)
    # Adicionar estrela à lista com suas propriedades
    stars.append({"x": x, "y": y, "brightness": brightness, "dir": random.choice([-1, 1])})

def draw_starry_background():
    """Função para desenhar o fundo estrelado com estrelas que piscam"""
    for star in stars:  # Para cada estrela na lista
        # Alterar o brilho da estrela
        star["brightness"] += star["dir"] * random.randint(1, 3)
        # Limitar o brilho máximo
        if star["brightness"] >= 255:
            star["brightness"] = 255
            star["dir"] = -1  # Começar a diminuir o brilho
        # Limitar o brilho mínimo
        elif star["brightness"] <= 100:
            star["brightness"] = 100
            star["dir"] = 1  # Começar a aumentar o brilho
        # Definir a cor com base no brilho (tons de cinza)
        color = (star["brightness"],) * 3
        # Desenhar a estrela na tela
        tela.set_at((star["x"], star["y"]), color)

# Classe para a nave do jogador
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Inicializar a classe base Sprite
        # Redimensionar a imagem da nave
        self.image = pygame.transform.scale(nave_img, (50, 50))
        # Posicionar a nave no centro na parte inferior da tela
        self.rect = self.image.get_rect(center=(LARGURA // 2, ALTURA - 60))
        self.vel = 5  # Velocidade de movimento
        self.vidas = 3  # Número de vidas

    def update(self, teclas):
        """Atualizar a posição da nave com base nas teclas pressionadas"""
        # Mover para a esquerda (tecla A)
        if teclas[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.vel
        # Mover para a direita (tecla D)
        if teclas[pygame.K_d] and self.rect.right < LARGURA:
            self.rect.x += self.vel
        # Mover para cima (tecla W)
        if teclas[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.vel
        # Mover para baixo (tecla S)
        if teclas[pygame.K_s] and self.rect.bottom < ALTURA:
            self.rect.y += self.vel

# Classe para os tiros da nave
class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Inicializar a classe base Sprite
        self.image = tiro_img  # Usar a superfície do tiro
        # Posicionar o tiro na posição dada
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.vel = -8  # Velocidade do tiro (para cima)

    def update(self, *args):
        """Atualizar a posição do tiro"""
        self.rect.y += self.vel  # Mover o tiro
        # Se o tiro sair da tela, removê-lo
        if self.rect.bottom < 0:
            self.kill()

# Classe para os inimigos/asteroides
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, velocidade_extra=0):
        super().__init__()  # Inicializar a classe base Sprite
        # Redimensionar a imagem do inimigo
        self.image = pygame.transform.scale(inimigo_img, (40, 40))
        # Posicionar aleatoriamente no topo da tela
        self.rect = self.image.get_rect(center=(random.randint(40, LARGURA-40), -40))
        # Velocidade horizontal aleatória
        self.velx = random.choice([-2, -1, 1, 2])
        # Velocidade vertical aleatória com possível aumento de dificuldade
        self.vely = random.randint(1, 3) + velocidade_extra

    def update(self, *args):
        """Atualizar a posição do inimigo"""
        self.rect.x += self.velx  # Mover horizontalmente
        self.rect.y += self.vely  # Mover verticalmente
        # Inverter direção se bater nas bordas laterais
        if self.rect.left < 0 or self.rect.right > LARGURA:
            self.velx *= -1
        # Remover se sair pela parte inferior da tela
        if self.rect.top > ALTURA:
            self.kill()

def desenhar_texto_centralizado(texto, rect):
    """Função para desenhar texto centralizado num retângulo"""
    img = fonte.render(texto, True, BRANCO)  # Renderizar o texto
    img_rect = img.get_rect(center=rect.center)  # Centralizar o texto
    tela.blit(img, img_rect)  # Desenhar o texto na tela

def menu_pausa():
    """Função para mostrar o menu de pausa"""
    # Pausar a música de fundo
    pygame.mixer.pause()
    
    # Criar uma superfície semi-transparente para o overlay
    s = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    s.fill((0, 0, 0, 128))  # Preto semi-transparente
    tela.blit(s, (0, 0))  # Desenhar o overlay
    
    # Texto principal do menu de pausa
    texto_pausa = titulo_fonte.render("JOGO PAUSADO", True, BRANCO)
    texto_rect = texto_pausa.get_rect(center=(LARGURA//2, ALTURA//2 - 50))
    tela.blit(texto_pausa, texto_rect)
    
    # Instruções para continuar
    instrucao = fonte.render("Pressione ESC para continuar", True, BRANCO)
    instrucao_rect = instrucao.get_rect(center=(LARGURA//2, ALTURA//2 + 50))
    tela.blit(instrucao, instrucao_rect)
    
    # Atualizar a tela
    pygame.display.flip()
    
    # Loop do menu de pausa
    pausado = True
    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Se clicar para fechar
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:  # Se pressionar uma tecla
                if evento.key == pygame.K_ESCAPE:  # Tecla ESC - continuar
                    pausado = False
                    pygame.mixer.unpause()  # Retomar a música
                    return True  # Continuar o jogo
                elif evento.key == pygame.K_m:  # Tecla M - voltar ao menu
                    pygame.mixer.unpause()
                    return False  # Voltar ao menu
    
    pygame.mixer.unpause()
    return True

def menu_inicial():
    """Função para mostrar o menu principal"""
    fundo_som.stop()  # Garantir que a música está parada
    
    # Criar retângulos para os botões
    botao_jogar = pygame.Rect(LARGURA//2 - 100, ALTURA//2 - 25, 200, 50)
    botao_sair = pygame.Rect(LARGURA//2 - 100, ALTURA//2 + 50, 200, 50)
    esperando = True
    
    while esperando:
        # Desenhar o fundo
        tela.fill(PRETO)
        draw_starry_background()
        
        # Desenhar o título do jogo
        titulo = titulo_fonte.render("Star Ship", True, BRANCO)
        titulo_rect = titulo.get_rect(center=(LARGURA//2, ALTURA//2 - 100))
        tela.blit(titulo, titulo_rect)

        # Desenhar o botão "Começar Jogo"
        pygame.draw.rect(tela, PRETO, botao_jogar, border_radius=10)
        pygame.draw.rect(tela, BRANCO, botao_jogar, width=2, border_radius=10)
        desenhar_texto_centralizado("Começar Jogo", botao_jogar)
        
        # Desenhar o botão "Sair"
        pygame.draw.rect(tela, PRETO, botao_sair, border_radius=10)
        pygame.draw.rect(tela, BRANCO, botao_sair, width=2, border_radius=10)
        desenhar_texto_centralizado("Sair", botao_sair)
        
        pygame.display.flip()

        # Processar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Fechar a janela
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:  # Clique do rato
                if botao_jogar.collidepoint(evento.pos):  # Clicou em "Começar Jogo"
                    esperando = False
                    iniciar_jogo()
                elif botao_sair.collidepoint(evento.pos):  # Clicou em "Sair"
                    pygame.quit()
                    exit()

def mostrar_tela_fim(score):
    """Função para mostrar a tela de fim de jogo"""
    fundo_som.stop()  # Parar a música
    
    # Criar o botão para voltar ao menu
    botao = pygame.Rect(LARGURA//2 - 100, ALTURA//2 + 40, 200, 50)
    esperando = True
    
    while esperando:
        # Desenhar o fundo
        tela.fill(PRETO)
        draw_starry_background()
        
        # Mostrar texto "Game Over" e pontuação
        desenhar_texto_centralizado("Game Over", pygame.Rect(LARGURA//2 - 100, ALTURA//2 - 60, 200, 30))
        desenhar_texto_centralizado(f"Score Final: {score}", pygame.Rect(LARGURA//2 - 100, ALTURA//2 - 20, 200, 30))
        
        # Desenhar o botão "Voltar ao Menu"
        pygame.draw.rect(tela, PRETO, botao, border_radius=10)
        pygame.draw.rect(tela, BRANCO, botao, width=2, border_radius=10)
        desenhar_texto_centralizado("Voltar ao Menu", botao)
        
        pygame.display.flip()

        # Processar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Fechar a janela
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:  # Clique do rato
                if botao.collidepoint(evento.pos):  # Clicou no botão
                    esperando = False
                    menu_inicial()  # Voltar ao menu

def iniciar_jogo():
    """Função principal do jogo"""
    fundo_som.play(-1)  # Iniciar música de fundo em loop
    
    # Criar grupos de sprites
    todos_sprites = pygame.sprite.Group()  # Todos os elementos do jogo
    tiros = pygame.sprite.Group()  # Grupo dos tiros
    inimigos = pygame.sprite.Group()  # Grupo dos inimigos
    
    # Criar a nave do jogador e adicionar ao grupo
    nave = Nave()
    todos_sprites.add(nave)
    
    # Variáveis do jogo
    score = 0  # Pontuação
    tempo_jogo = 0  # Tempo decorrido
    velocidade_extra_inimigo = 0  # Dificuldade progressiva
    
    # Configurar o relógio para controlar o FPS
    clock = pygame.time.Clock()
    rodando = True
    
    # Configurar evento para spawn de inimigos
    SPAWN_INIMIGO = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_INIMIGO, 1000)  # A cada 1 segundo

    # Loop principal do jogo
    while rodando:
        dt = clock.tick(60)  # Limitar a 60 FPS
        tempo_jogo += dt  # Atualizar tempo decorrido
        
        # Obter estado das teclas
        teclas = pygame.key.get_pressed()

        # Aumentar dificuldade com o tempo
        if tempo_jogo // 10000 > velocidade_extra_inimigo:
            velocidade_extra_inimigo += 1
            nave.vel += 0.5  # Aumentar velocidade da nave

        # Processar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Fechar a janela
                rodando = False
            if evento.type == pygame.KEYDOWN:  # Tecla pressionada
                if evento.key == pygame.K_SPACE:  # Tecla ESPAÇO - disparar
                    tiro = Tiro(nave.rect.centerx, nave.rect.top)
                    todos_sprites.add(tiro)
                    tiros.add(tiro)
                    tiro_som.play()  # Tocar som do tiro
                elif evento.key == pygame.K_ESCAPE:  # Tecla ESC - pausar
                    if not menu_pausa():  # Se escolher voltar ao menu
                        fundo_som.stop()
                        return
            if evento.type == SPAWN_INIMIGO:  # Evento de spawn de inimigos
                for _ in range(1 + velocidade_extra_inimigo):  # Aumentar quantidade com dificuldade
                    inimigo = Inimigo(velocidade_extra_inimigo)
                    todos_sprites.add(inimigo)
                    inimigos.add(inimigo)

        # Atualizar todos os sprites
        todos_sprites.update(teclas)

        # Verificar colisões
        for inimigo in inimigos:
            if nave.rect.colliderect(inimigo.rect):  # Colisão nave-inimigo
                inimigo.kill()
                nave.vidas -= 1
                colisao_som.play()
                if nave.vidas <= 0:  # Sem vidas - fim de jogo
                    rodando = False

        for tiro in tiros:
            hits = pygame.sprite.spritecollide(tiro, inimigos, True)  # Colisão tiro-inimigo
            if hits:
                tiro.kill()
                score += 10  # Aumentar pontuação
                explosao_som.play()  # Tocar som de explosão

        # Desenhar tudo
        tela.fill(PRETO)  # Limpar a tela
        draw_starry_background()  # Desenhar fundo estrelado
        todos_sprites.draw(tela)  # Desenhar todos os sprites
        
        # Desenhar painel de informação
        s = pygame.Surface((200, 70), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))  # Fundo semi-transparente
        tela.blit(s, (5, 5))
        
        # Mostrar pontuação e vidas
        desenhar_texto_centralizado(f"Score: {score}", pygame.Rect(10, 10, 200, 30))
        desenhar_texto_centralizado(f"Vidas: {nave.vidas}", pygame.Rect(10, 40, 200, 30))
        
        pygame.display.flip()  # Atualizar a tela

    # Fim do jogo - mostrar tela de game over
    mostrar_tela_fim(score)

# Iniciar o jogo pelo menu principal
menu_inicial()
import pgzrun
import random

WIDTH = 800
HEIGHT = 600

# Estados do jogo
estado_jogo = "menu"  # menu, jogando, vitoria, derrota

# Sprites
jogador = Actor("guardiao", (WIDTH // 2, HEIGHT - 60))
estrelas = []
cometas = []

# Variáveis
pontuacao = 0
vidas = 3
TOTAL_ESTRELAS = 5

# Função personalizada com parâmetro numérico
def criar_cometa(velocidade):
    x = random.randint(50, WIDTH - 50)
    cometa = Actor("cometa", (x, -40))
    cometa.vel = velocidade
    cometas.append(cometa)

# Função para criar clones de estrelas
def criar_estrelas():
    estrelas.clear()
    for _ in range(TOTAL_ESTRELAS):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(100, 400)
        estrela = Actor("estrela", (x, y))
        estrelas.append(estrela)

def draw():
    screen.clear()
    
    if estado_jogo == "menu":
        screen.draw.text("GUARDIÃO DAS ESTRELAS", center=(WIDTH//2, 100), fontsize=50, color="orange")
        screen.draw.text("Controles: Use as setas (cima, baixo, esquerda, direita) para mover", center=(WIDTH//2, 200), fontsize=30, color="white")
        screen.draw.text("Objetivo: Colete todas as estrelas e evite os cometas!", center=(WIDTH//2, 240), fontsize=28, color="white")
        screen.draw.text("Pressione ENTER para começar", center=(WIDTH//2, 320), fontsize=30, color="green")
    
    elif estado_jogo == "jogando":
        jogador.draw()
        for estrela in estrelas:
            estrela.draw()
        for cometa in cometas:
            cometa.draw()
        
        screen.draw.text(f"Estrelas: {pontuacao}/{TOTAL_ESTRELAS}", (10, 10), fontsize=30, color="yellow")
        screen.draw.text(f"Vidas: {vidas}", (10, 50), fontsize=30, color="red")

    elif estado_jogo == "vitoria":
        screen.draw.text("VOCÊ VENCEU!", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="gold")
        screen.draw.text("Pressione ENTER para jogar novamente", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=30, color="white")

    elif estado_jogo == "derrota":
        screen.draw.text("GAME OVER!", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="red")
        screen.draw.text("Pressione ENTER para tentar novamente", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=30, color="white")

def update():
    global pontuacao, vidas, estado_jogo

    if estado_jogo != "jogando":
        return

    # Movimento livre da nave
    if keyboard.left:
        jogador.x -= 5
    if keyboard.right:
        jogador.x += 5
    if keyboard.up:
        jogador.y -= 5
    if keyboard.down:
        jogador.y += 5

    # Limitar movimento dentro da tela
    jogador.x = max(30, min(WIDTH - 30, jogador.x))
    jogador.y = max(30, min(HEIGHT - 30, jogador.y))

    # Coleta de estrelas
    for estrela in estrelas[:]:
        if jogador.colliderect(estrela):
            estrelas.remove(estrela)
            pontuacao += 1

    # Movimento dos cometas
    for cometa in cometas[:]:
        cometa.y += cometa.vel
        if cometa.y > HEIGHT:
            cometas.remove(cometa)
        elif jogador.colliderect(cometa):
            cometas.remove(cometa)
            vidas -= 1

    # Verificação de vitória
    if pontuacao >= TOTAL_ESTRELAS:
        estado_jogo = "vitoria"

    # Verificação de derrota
    if vidas <= 0:
        estado_jogo = "derrota"


def on_key_down(key):
    global estado_jogo, pontuacao, vidas, cometas

    if key == keys.RETURN:
        if estado_jogo in ["menu", "vitoria", "derrota"]:
            pontuacao = 0
            vidas = 3
            criar_estrelas()
            cometas.clear()
            estado_jogo = "jogando"

# Criação contínua de clones de cometas
def spawn_cometa():
    if estado_jogo == "jogando":
        velocidade = random.uniform(2, 5)
        criar_cometa(velocidade)

clock.schedule_interval(spawn_cometa, 2.0)

pgzrun.go()

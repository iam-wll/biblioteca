import sys
import random
import pygame

# 1. Inicialização
pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coletor de Moedas - Pygame")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22, bold=True)

# 2. Configuração dos Elementos
player = pygame.Rect(285, 185, 30, 30)  # Posição x, y, largura, altura
coin = pygame.Rect(random.randint(20, WIDTH - 40), random.randint(20, HEIGHT - 40), 20, 20)

speed = 5
score = 0
time_left = 15.0  # Segundos de jogo

# 3. Loop Principal
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Tempo decorrido por quadro (em segundos)

    # Captura eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and time_left <= 0:
            if event.key == pygame.K_r:  # Reiniciar o jogo
                score = 0
                time_left = 15.0
                player.x, player.y = 285, 185

    if time_left > 0:
        time_left -= dt

        # Movimentação do Jogador
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.left > 0:
            player.x -= speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.right < WIDTH:
            player.x += speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.top > 0:
            player.y -= speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.bottom < HEIGHT:
            player.y += speed

        # Colisão com a moeda
        if player.colliderect(coin):
            score += 1
            coin.x = random.randint(20, WIDTH - 40)
            coin.y = random.randint(20, HEIGHT - 40)

    # --- Desenhar na Tela ---
    screen.fill((25, 25, 35))  # Fundo escuro

    if time_left > 0:
        pygame.draw.ellipse(screen, (255, 215, 0), coin)     # Moeda Dourada
        pygame.draw.rect(screen, (0, 180, 255), player)       # Jogador Azul

        # Exibir HUD
        score_txt = font.render(f"Moedas: {score}", True, (255, 255, 255))
        timer_txt = font.render(f"Tempo: {max(0.0, time_left):.1f}s", True, (255, 255, 255))
        screen.blit(score_txt, (15, 15))
        screen.blit(timer_txt, (WIDTH - 150, 15))
    else:
        # Tela de Game Over
        over_txt = font.render(f"Fim de Jogo! Pontuação Final: {score}", True, (255, 100, 100))
        restart_txt = font.render("Pressione 'R' para jogar novamente", True, (200, 200, 200))
        
        screen.blit(over_txt, (WIDTH // 2 - over_txt.get_width() // 2, HEIGHT // 2 - 30))
        screen.blit(restart_txt, (WIDTH // 2 - restart_txt.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
import sys
import random
import pygame

# 1. Configurações Iniciais
pygame.init()

WIDTH = 600
HEIGHT = 700
FPS = 60

# Cores
BLACK = (15, 15, 25)
WHITE = (255, 255, 255)
CYAN = (0, 220, 255)
RED = (255, 60, 60)
YELLOW = (255, 200, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter - Pygame")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20, bold=True)

# 2. Classes dos Objetos
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Desenha uma nave em formato de triângulo
        pygame.draw.polygon(self.image, CYAN, [(20, 0), (0, 40), (40, 40)])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 7
        self.hp = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(20, 50)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(3, 8)
        self.speed_x = random.randint(-2, 2)

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        # Reseta o asteroide se passar da tela
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 16))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# 3. Inicialização dos Grupos e Elementos
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for _ in range(8):
    ast = Asteroid()
    all_sprites.add(ast)
    asteroids.add(ast)

score = 0
game_over = False

# 4. Loop Principal
running = True
while running:
    clock.tick(FPS)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()

    if not game_over:
        # Atualização dos Objetos
        all_sprites.update()

        # Colisão: Tiro atinge Asteroide
        hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit in hits:
            score += 10
            # Cria um novo asteroide para manter a dificuldade
            new_ast = Asteroid()
            all_sprites.add(new_ast)
            asteroids.add(new_ast)

        # Colisão: Asteroide atinge Jogador
        player_hits = pygame.sprite.spritecollide(player, asteroids, True)
        for hit in player_hits:
            player.hp -= 25
            new_ast = Asteroid()
            all_sprites.add(new_ast)
            asteroids.add(new_ast)
            if player.hp <= 0:
                game_over = True

    # Renderização (Desenhar)
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Interface HUD (Pontuação e HP)
    score_text = font.render(f"Pontos: {score}", True, WHITE)
    hp_text = font.render(f"HP: {player.hp}", True, RED if player.hp <= 25 else CYAN)
    screen.blit(score_text, (10, 10))
    screen.blit(hp_text, (WIDTH - 100, 10))

    if game_over:
        over_text = font.render("GAME OVER! Pressione Fechar para sair.", True, RED)
        rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(over_text, rect)

    pygame.display.flip()

pygame.quit()
sys.exit()

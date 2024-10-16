import pygame
import random

pygame.init()


WIDTH, HEIGHT = 800, 600                      # Demensiones
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Espacial")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLAYER_IMG = pygame.image.load('assets/player.png')         # Cargar las imagenes
ENEMY_IMG = pygame.image.load('assets/enemy.png')
BULLET_IMG = pygame.image.load('assets/bullet.png')


class Player:
    def __init__(self, x, y):
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.bullets = []

    def move(self, keys):
        
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = pygame.Rect(self.rect.centerx - 5, self.rect.y - 20, 10, 20)
        self.bullets.append(bullet)

    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        for bullet in self.bullets:
            WIN.blit(BULLET_IMG, (bullet.x, bullet.y))


class Enemy:
    def __init__(self, x, y):
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 3

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

def main_menu():               # Mostrar Menu 
    run = True
    while run:
        WIN.fill(BLACK)
        font = pygame.font.SysFont('comicsans', 50)
        text = font.render("Presiona ENTER para iniciar", True, WHITE)
        WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
    game_loop()

def check_collisions(player, enemies):                 #Detecta si impacta al enemigo
    for bullet in player.bullets[:]:  
        for enemy in enemies[:]:  
            if bullet.colliderect(enemy.rect):
                player.bullets.remove(bullet) 
                enemies.remove(enemy)  
                break                                   # Para evitar o salir del bucle

def game_loop():                                         # Funcion PRINCIPAL DEL JUEGO 
    player = Player(WIDTH//2 - 40, HEIGHT - 80)
    enemies = [Enemy(random.randint(0, WIDTH-50), random.randint(-1500, -100)) for _ in range(6)]
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        
        keys = pygame.key.get_pressed()                  #Movilidad del juegodor
        player.move(keys)
        
        for enemy in enemies[:]:                          #Movilidad de los enemigos 
            enemy.move()
            
            if enemy.rect.y > HEIGHT:
                enemy.rect.y = random.randint(-1500, -100)
                enemy.rect.x = random.randint(0, WIDTH-50)
        
        for bullet in player.bullets[:]:
            bullet.y -= 10
            if bullet.y < 0:
                player.bullets.remove(bullet)
        
        check_collisions(player, enemies)
        
        player.draw()
        for enemy in enemies:
            enemy.draw()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main_menu()




import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shooting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player
player_radius = 15
player_x = screen_width // 2
player_y = screen_height - player_radius - 10
player_speed = 8
player_health = 100
player_max_health = 100
player = pygame.Rect(player_x - player_radius, player_y - player_radius, player_radius * 2, player_radius * 2)

# Health Bar
health_bar_length = 40
health_bar_height = 5
health_bar_color = GREEN
health_bar_border_color = WHITE
health_bar_border_width = 1

# Bullet
bullet_radius = 4
bullet_speed = 7
bullet_cooldown = 6  # Cooldown between shots (in frames)
bullet_cooldown_counter = 0
bullets = []

# Enemy
enemy_radius = 10
enemy_speeds = [3, 4, 5, 6, 7]  # Different speeds for enemies

class Bullet:
    def __init__(self, x, y, angle):
        self.rect = pygame.Rect(x, y, bullet_radius * 2, bullet_radius * 2)
        self.angle = angle

class Enemy:
    def __init__(self, x, y, speed, max_health):
        self.rect = pygame.Rect(x, y, enemy_radius * 2, enemy_radius * 2)
        self.speed = speed
        self.health = max_health
        self.max_health = max_health
        self.angle = 0  # Angle to the player

    def draw_health_bar(self):
        # Calculate width of health bar
        health_width = self.rect.width * (self.health / self.max_health)
        health_bar = pygame.Rect(self.rect.x, self.rect.y - 10, health_width, 5)
        pygame.draw.rect(screen, GREEN, health_bar)

    def update_angle(self):
        dx = player.x - self.rect.x
        dy = player.y - self.rect.y
        self.angle = math.atan2(dy, dx)

    def move_towards_player(self):
        dx = self.speed * math.cos(self.angle)
        dy = self.speed * math.sin(self.angle)
        self.rect.x += dx
        self.rect.y += dy

enemies = []
max_enemy_count = 10  # Maximum number of enemies
enemy_spawn_delay = 60  # Delay between spawning enemies
enemy_spawn_counter = 0
max_enemy_health = 3  # Maximum health for enemies

# Enemy Bullet
enemy_bullet_radius = 3
enemy_bullet_speed = 8
enemy_bullets = []

# Fonts
font = pygame.font.Font('assets/game.ttf', 30)
font_large = pygame.font.Font('assets/game.ttf', 100)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_circle(surface, color, center, radius):
    pygame.draw.circle(surface, color, center, radius)

def spawn_bullet(x, y, angle):
    bullet = Bullet(x, y, angle)
    bullets.append(bullet)

def spawn_enemy_bullet(enemy):
    if random.randint(0, 1000) < 3:  # Adjust the probability of enemy shooting here
        angle = math.atan2(player.y - enemy.rect.y, player.x - enemy.rect.x)
        enemy_bullet = pygame.Rect(enemy.rect.x + enemy.rect.width // 2 - enemy_bullet_radius, enemy.rect.y + enemy.rect.height // 2 - enemy_bullet_radius, enemy_bullet_radius * 2, enemy_bullet_radius * 2)
        enemy_bullets.append((enemy_bullet, angle))
        
def move_enemy_bullets():
    for enemy_bullet, angle in enemy_bullets:
        dx = enemy_bullet_speed * math.cos(angle)
        dy = enemy_bullet_speed * math.sin(angle)
        enemy_bullet.x += dx
        enemy_bullet.y += dy
        if enemy_bullet.y > screen_height:
            enemy_bullets.remove((enemy_bullet, angle))

def draw_objects():
    screen.fill(BLACK)
    draw_circle(screen, WHITE, (player.x + player_radius, player.y + player_radius), player_radius)
    for bullet in bullets:
        draw_circle(screen, WHITE, (bullet.rect.x + bullet_radius, bullet.rect.y + bullet_radius), bullet_radius)
    for enemy in enemies:
        draw_circle(screen, RED, (enemy.rect.x + enemy_radius, enemy.rect.y + enemy_radius), enemy_radius)
        enemy.draw_health_bar()
    for enemy_bullet, _ in enemy_bullets:
        draw_circle(screen, RED, (enemy_bullet.x + enemy_bullet_radius, enemy_bullet.y + enemy_bullet_radius), enemy_bullet_radius)

    # Draw health bar
    health_bar_x = player.x - (health_bar_length - 28) // 2
    health_bar_y = player.y - 10  # Place health bar 30 pixels above player's head
    pygame.draw.rect(screen, health_bar_border_color, (health_bar_x, health_bar_y, health_bar_length, health_bar_height), health_bar_border_width)
    pygame.draw.rect(screen, health_bar_color, (health_bar_x, health_bar_y, health_bar_length * (player_health / player_max_health), health_bar_height))

def draw_game_over():
    game_over_text = font_large.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
    draw_text("Click to replay", font, WHITE, screen_width // 2 - 100, screen_height // 2 + 50)

def move_enemies():
    for enemy in enemies:
        enemy.update_angle()
        enemy.move_towards_player()

def restart_game():
    global player_x, player_y, bullets, enemies, enemy_spawn_counter, bullet_cooldown_counter, game_over, score, player_health

    # Reset all variables to their initial states to restart the game
    player_x = screen_width // 2
    player_y = screen_height - player_radius - 10
    player.x = player_x
    player.y = player_y
    bullets = []
    enemies = []
    enemy_spawn_counter = 0
    bullet_cooldown_counter = 0
    game_over = False
    score = 0
    player_health = player_max_health

def main():
    global player_x, player_y, bullets, enemies, enemy_spawn_counter, bullet_cooldown_counter, game_over, score, player_health

    clock = pygame.time.Clock()
    running = True
    game_over = False  # Initialize game over state
    score = 0  # Initialize score

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:  # Check for mouse click when game is over
                restart_game()

        if not game_over:  # Check if game over

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.x -= player_speed
            if keys[pygame.K_RIGHT]:
                player.x += player_speed
            if keys[pygame.K_UP]:
                player.y -= player_speed
            if keys[pygame.K_DOWN]:
                player.y += player_speed

            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]:  # Check for left mouse button click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - (player.x + player_radius)
                dy = mouse_y - (player.y + player_radius)
                angle = math.atan2(dy, dx)
                if bullet_cooldown_counter <= 0:  # Check bullet cooldown
                    spawn_bullet(player.x, player.y, angle)
                    bullet_cooldown_counter = bullet_cooldown

            # Update bullets
            for bullet in bullets:
                dx = bullet_speed * math.cos(bullet.angle)
                dy = bullet_speed * math.sin(bullet.angle)
                bullet.rect.x += dx
                bullet.rect.y += dy
                if bullet.rect.y < -bullet_radius * 2:
                    bullets.remove(bullet)

            # Update bullet cooldown
            if bullet_cooldown_counter > 0:
                bullet_cooldown_counter -= 1

            # Enemy spawning
            if enemy_spawn_counter <= 0:
                if len(enemies) < max_enemy_count:  # Check if maximum enemy count is reached
                    enemy_x = random.randint(0, screen_width - enemy_radius * 2)
                    enemy_y = random.randint(-screen_height, -enemy_radius * 2)
                    enemy_speed = random.choice(enemy_speeds)  # Randomly choose a speed for the enemy
                    enemy = Enemy(enemy_x, enemy_y, enemy_speed, max_enemy_health)
                    enemies.append(enemy)
                enemy_spawn_counter = enemy_spawn_delay
            else:
                enemy_spawn_counter -= 1

            move_enemies()

            # Enemy shooting
            for enemy in enemies:
                spawn_enemy_bullet(enemy)

            move_enemy_bullets()

            # Collision detection
            for enemy in enemies:
                for bullet in bullets:
                    if bullet.rect.colliderect(enemy.rect):
                        bullets.remove(bullet)
                        enemy.health -= 1  # Decrease enemy health when hit
                        if enemy.health <= 0:
                            enemies.remove(enemy)  # Remove enemy when health is depleted
                            score += 1  # Increase score when enemy is defeated
                if player.colliderect(enemy.rect):  # Player-enemy collision
                    player_health -= 25  # Decrease player health when hit
                    enemies.remove(enemy)  # Remove enemy when it hits the player
                    if player_health <= 0:  # Check if player health is depleted
                        game_over = True
            for enemy_bullet, _ in enemy_bullets:
                if player.colliderect(enemy_bullet):
                    player_health -= 25  # Decrease player health when hit by enemy bullet
                    enemy_bullets.remove((enemy_bullet, _))
                    if player_health <= 0:  # Check if player health is depleted
                        game_over = True

            draw_objects()

            # Draw score
            draw_text("Score: {}".format(score), font, WHITE, 10, 10)

        else:  # Game over state
            draw_game_over()

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

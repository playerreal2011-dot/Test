from tkinter import font
from turtle import color
import pygame
import pygame.mixer as mixer
import random
from time import sleep

WIDTH = 800
HEIGHT = 600
FPS = 60
RED_DUST = (193, 68, 14)
SKY_COLOR = (45, 20, 20)
PLATFORM_COLOR = (100, 50, 30) 
WHITE = (255, 255, 255)

class UIElement(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        super().__init__()
        self.oxygen_value = 100
        self.oxygen_timer = 0
        self.oxygen = [
            pygame.image.load("D:\Documents\Тільки не воно\Pro\Oxygen_full.png").convert_alpha(),
            pygame.image.load("D:\Documents\Тільки не воно\Pro\Oxygen_half.png").convert_alpha(),
            pygame.image.load("D:\Documents\Тільки не воно\Pro\Oxygen_Low.png").convert_alpha(),
            pygame.image.load("D:\Documents\Тільки не воно\Pro\Oxygen_empty.png").convert_alpha()
        ]
        self.base_image = self.oxygen[0]
        self.base_image = pygame.transform.scale(self.base_image, (250, 250))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(topleft=(10, 0))

    def update(self):
        self.image = self.base_image.copy()
        self.text = f"Oxygen: {self.oxygen_value}%"
        font = pygame.font.SysFont(None, 28)
        text_surface = font.render(self.text, True, (0, 0, 0))
        self.image.blit(text_surface, (0, 10))
        self.oxygen_timer += 100
        if self.oxygen_timer >= FPS:
            self.oxygen_timer = 0
            self.oxygen_value -= 1
        if self.oxygen_value > 50:
            self.base_image = self.oxygen[0]
            self.base_image = pygame.transform.scale(self.base_image, (250, 250))
        elif self.oxygen_value <= 50 and self.oxygen_value > 10:
            self.base_image = self.oxygen[1]
            self.base_image = pygame.transform.scale(self.base_image, (250, 250))
        elif self.oxygen_value <= 10 and self.oxygen_value > 0:
            self.base_image = self.oxygen[2]
            self.base_image = pygame.transform.scale(self.base_image, (250, 250))
        elif self.oxygen_value <= 0:
            self.base_image = self.oxygen[3]
            self.base_image = pygame.transform.scale(self.base_image, (250, 250))
            pygame.quit()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.image.load("D:\\Documents\\Тільки не воно\\Pro\\brown platform.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.images = [
            pygame.image.load("D:\Documents\Тільки не воно\Pro\Player_R.png").convert_alpha(),
            pygame.image.load("D:\Documents\Тільки не воно\Pro\Player_Rsit.png").convert_alpha(),
            pygame.image.load("D:\Documents\Тільки не воно\Pro\Player_Rwalk.png").convert_alpha(),
            pygame.image.load("D:\Documents\Тільки не воно\Pro\Player_L.png").convert_alpha(),
            pygame.image.load("D:\Documents\Тільки не воно\Pro\Player_Lsit.png").convert_alpha(),
            pygame.image.load("D:\Documents\Тільки не воно\Pro\Player_Lwalk.png").convert_alpha()
        ]
        self.index = 0
        self.image = pygame.transform.scale(self.images[self.index], (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.animation_counter = 0
        self.animation_speed = 15
        self.idle_counter = 0
        self.idle_speed = 30
        self.speed_x = 0
        self.facing_right = True
        self.speed_y = 0
        self.gravity = 0.8
        self.jump_power = -16
        self.platforms = platforms 

    def update(self):
        # 1. Гравітація
        self.speed_y += self.gravity
        self.rect.y += self.speed_y
        
        # 2. Перевірка зіткнень по вертикалі (Y)
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits:
            # Якщо ми падаємо вниз на платформу
            if self.speed_y > 0:
                self.rect.bottom = hits[0].rect.top
                self.speed_y = 0
            # Якщо ми вдарилися головою об платформу знизу
            elif self.speed_y < 0:
                self.rect.top = hits[0].rect.bottom
                self.speed_y = 0

        # 3. Керування по осі X та анімація
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.facing_right:  # Змінили напрямок на ліво
                self.facing_right = False
                self.index = 3
                self.animation_counter = 0
                old_x, old_y = self.rect.x, self.rect.y
                self.image = pygame.transform.scale(self.images[self.index], (50, 50))
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = old_x, old_y
            self.speed_x = -7
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.index += 1
                if self.index > 5:  # Player_L, Player_Lsit, Player_Lwalk (3, 4, 5)
                    self.index = 3
                old_x, old_y = self.rect.x, self.rect.y
                self.image = pygame.transform.scale(self.images[self.index], (50, 50))
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = old_x, old_y
        elif keys[pygame.K_RIGHT]:
            if not self.facing_right:  # Змінили напрямок на право
                self.facing_right = True
                self.index = 0
                self.animation_counter = 0
                old_x, old_y = self.rect.x, self.rect.y
                self.image = pygame.transform.scale(self.images[self.index], (50, 50))
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = old_x, old_y
            self.speed_x = 7
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.index += 1
                if self.index > 2:  # Player_R, Player_Rsit, Player_Rwalk (0, 1, 2 індекс)
                    self.index = 0
                old_x, old_y = self.rect.x, self.rect.y
                self.image = pygame.transform.scale(self.images[self.index], (50, 50))
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = old_x, old_y
        self.rect.x += self.speed_x
        if self.speed_x == 0:
            self.animation_counter = 0
            self.idle_counter += 1
            if self.idle_counter >= self.idle_speed:
                self.idle_counter = 0
                if self.facing_right:
                    self.index = 1 if self.index == 0 else 0
                else:
                    self.index = 4 if self.index == 3 else 3
                old_x, old_y = self.rect.x, self.rect.y
                self.image = pygame.transform.scale(self.images[self.index], (50, 50))
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = old_x, old_y
        else:
            self.idle_counter = 0


        # 4. Перевірка зіткнень по горизонталі (x)
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits:
            if self.speed_x > 0:  # Рухаємось вправо
                self.rect.right = hits[0].rect.left
            elif self.speed_x < 0:  # Рухаємось вліво
                self.rect.left = hits[0].rect.right
        if self.rect.bottom > HEIGHT - 20:
            self.rect.bottom = HEIGHT - 20
            self.speed_y = 0
        if self.rect.left < 0:  
            self.rect.left = 0
        if self.rect.right > WIDTH: 
            self.rect.right = WIDTH

    def jump(self):
        # Перевіряємо, чи стоїть гравець на чомусь перед стрибком
        self.rect.y += 1 
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 1
        
        if hits or self.rect.bottom >= HEIGHT - 20:
            self.speed_y = self.jump_power

pygame.init()
mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Вибір одної з декількох ембіентів
music = random.randint(0, 2)
if music == 0:
    mixer.music.load("D:\Documents\Тільки не воно\Pro\Ambient_1.mp3")
elif music == 1:
    mixer.music.load("D:\Documents\Тільки не воно\Pro\Ambient_2.mp3")
elif music == 2:
    mixer.music.load("D:\Documents\Тільки не воно\Pro\Ambient_3.mp3")
mixer.music.play(-1)  # Зациклення музики

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

p1 = Platform(100, 450, 200, 30)
p2 = Platform(200, 350, 150, 30)
p3 = Platform(450, 250, 100, 30)
p4 = Platform(100, 150, 200, 30)

oxygen_ui = UIElement(600, 500, 180, 60, WHITE)
all_sprites.add(oxygen_ui)

platforms.add(p1, p2, p3, p4)
all_sprites.add(p1, p2, p3, p4)

player = Player(platforms)
all_sprites.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_UP]:
                player.jump()

    all_sprites.update()

    screen.fill(SKY_COLOR)
    pygame.draw.rect(screen, RED_DUST, (0, HEIGHT - 10, WIDTH, 20))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
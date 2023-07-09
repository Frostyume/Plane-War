import pygame
from random import *


class SmallEnemy(pygame.sprite.Sprite):
    maxHP = 1

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/enemy1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("images/enemy1_down0.png").convert_alpha(),
            pygame.image.load("images/enemy1_down1.png").convert_alpha(),
            pygame.image.load("images/enemy1_down2.png").convert_alpha(),
            pygame.image.load("images/enemy1_down3.png").convert_alpha(),
            pygame.image.load("images/enemy1_down4.png").convert_alpha()
        ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.level = 1
        self.speed = 2
        self.active = True
        self.maxHP = 1
        self.HP = self.maxHP
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-10 * self.height, 0)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.HP = SmallEnemy.maxHP
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-10 * self.height, 0)

    def update(self, level):
        SmallEnemy.maxHP = level
        self.HP = SmallEnemy.maxHP


class MidEnemy(pygame.sprite.Sprite):
    maxHP = 8

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/enemy2.png").convert_alpha()
        self.image_hit = pygame.image.load("images/enemy2_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("images/enemy2_down0.png").convert_alpha(),
            pygame.image.load("images/enemy2_down1.png").convert_alpha(),
            pygame.image.load("images/enemy2_down2.png").convert_alpha(),
            pygame.image.load("images/enemy2_down3.png").convert_alpha(),
            pygame.image.load("images/enemy2_down4.png").convert_alpha()
        ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.level = 1
        self.speed = 2
        self.active = True
        self.hit = False
        self.HP = MidEnemy.maxHP
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-20 * self.height, -self.height)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.HP = MidEnemy.maxHP
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-15 * self.height, 0)

    def update(self, level):
        MidEnemy.maxHP = 8 * level
        self.HP = MidEnemy.maxHP


class BigEnemy(pygame.sprite.Sprite):
    maxHP = 200

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("images/enemy3_n1.png").convert_alpha()
        self.image2 = pygame.image.load("images/enemy3_n2.png").convert_alpha()
        self.image_hit = pygame.image.load("images/enemy3_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("images/enemy3_down0.png").convert_alpha(),
            pygame.image.load("images/enemy3_down1.png").convert_alpha(),
            pygame.image.load("images/enemy3_down2.png").convert_alpha(),
            pygame.image.load("images/enemy3_down3.png").convert_alpha(),
            pygame.image.load("images/enemy3_down4.png").convert_alpha(),
            pygame.image.load("images/enemy3_down5.png").convert_alpha(),
            pygame.image.load("images/enemy3_down6.png").convert_alpha()
        ])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.level = 1
        self.speed = 1
        self.active = True
        self.hit = False
        self.HP = BigEnemy.maxHP
        self.mask = pygame.mask.from_surface(self.image1)
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-20 * self.height, -5 * self.height)

    def move(self, h_action, w_action):
        if self.rect.top < 30:
            self.rect.top += self.speed
        else:
            if self.rect.top < self.height // 2 and self.rect.left > 0 and self.rect.right < self.width:
                if h_action:
                    self.rect.top += self.speed
                else:
                    self.rect.top -= self.speed
                if w_action:
                    self.rect.left += self.speed
                else:
                    self.rect.left -= self.speed
            else:
                if self.rect.top > self.height // 2:
                    self.rect.top -= self.speed
                if self.rect.left < 0:
                    self.rect.left += self.speed
                if self.rect.right > self.width:
                    self.rect.left -= self.speed

    def reset(self):
        self.active = True
        self.HP = BigEnemy.maxHP
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-15 * self.height, -5 * self.height)

    def update(self, level):
        BigEnemy.maxHP = 2 * 3 ** level + 10 * level ** 2
        self.HP = BigEnemy.maxHP



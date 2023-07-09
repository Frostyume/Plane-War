import pygame
import sys
import traceback
from random import *
from pygame.locals import *
import myplane
import enemy
import bullet
import supply

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('Plane Warfare')

background = pygame.image.load("images/background.png").convert()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 载入游戏音乐
pygame.mixer.music.load("music/game_music.ogg")
pygame.mixer.music.set_volume(0.1)
bullet_sound = pygame.mixer.Sound("music/bullet.wav")
bullet_sound.set_volume(0.2)
missile_sound = pygame.mixer.Sound("music/missile.wav")
missile_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("music/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("music/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("music/get_bomb.wav")
get_bomb_sound.set_volume(0.3)
get_bullet_sound = pygame.mixer.Sound("music/get_bullet.wav")
get_bullet_sound.set_volume(0.3)
upgrade_sound = pygame.mixer.Sound("music/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("music/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("music/enemy1_down.wav")
enemy1_down_sound.set_volume(0.4)
enemy2_down_sound = pygame.mixer.Sound("music/enemy2_down.wav")
enemy2_down_sound.set_volume(0.5)
enemy3_down_sound = pygame.mixer.Sound("music/enemy3_down.wav")
enemy3_down_sound.set_volume(0.6)
me_down_sound = pygame.mixer.Sound("music/me_down.wav")
me_down_sound.set_volume(0.2)


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


# 增加敌机速度
def inc_speed(target, inc):
    for each in target:
        each.speed += inc


# 增加敌机血量
def update(target, level):
    for each in target:
        target.update(level)

    
def main():
    pygame.mixer.music.play(-1)
    # 生成我方飞机
    me = myplane.MyPlane(bg_size)

    # 生成敌人
    enemies = pygame.sprite.Group()

    # 生成小型敌机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 30)

    # 生成中型敌机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 1)

    # 生成大型敌机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 0)

    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    bullet1_num = 1
    bullet1.append(bullet.Bullet1(me.rect.midtop))

    # 生成超级子弹
    bullet2 = []
    bullet2_index = 0
    bullet2_num = 2
    for i in range(bullet2_num // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))

    # 生成导弹
    bullet3 = []
    bullet3_index = 0
    bullet3_num = 1

    # 子弹伤害
    damage = 1

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # 统计得分
    score = 0
    score_font = pygame.font.Font("font/font1.ttf", 36)

    # 标志是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image

    # 设置难度级别
    level = 1
    level_font = pygame.font.Font("font/font1.ttf", 30)

    # 全屏炸弹
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font1.ttf", 48)
    bomb_num = 3

    # 每5-15秒发放一个补给包
    supply_p = 0
    bullet_supply = supply.BulletSupply(bg_size)
    bomb_supply = supply.BombSupply(bg_size)
    ballistic_supply = supply.BallisticSupply(bg_size)
    damage_supply = supply.DamageSupply(bg_size)
    ROF_supply = supply.ROFSupply(bg_size)
    range_supply = supply.RangeSupply(bg_size)
    life_supply = supply.LifeSupply(bg_size)
    SUPPLY_TIME = USEREVENT
    # pygame.time.set_timer(SUPPLY_TIME, randint(5, 15) * 1000)
    pygame.time.set_timer(SUPPLY_TIME, 5000)

    # 弹道数量
    ballistic_num = 1

    # 超级子弹定时器
    SUPER_BULLET_TIME = USEREVENT + 1

    # 标志是否使用超级子弹
    is_super_bullet = False

    # 生命值
    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # 我方无敌时间
    INVINCIBLE_TIME = USEREVENT + 2

    # 大型敌机随机移动
    BIG_ENEMY_MOVE = USEREVENT + 3
    pygame.time.set_timer(BIG_ENEMY_MOVE, randint(5, 10) * 100)
    h_action = choice([True, False])
    w_action = choice([True, False])

    # 用于阻止重复打开记录文档
    recorded = False

    # 游戏结束画面
    gameover_font = pygame.font.Font("font/font1.ttf", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    # 判断切换图片
    switch_image = True

    # 延时计数器
    delay = 120

    # 子弹射速
    rof = 30

    # 判断升级为导弹
    update_bullet = False

    clock = pygame.time.Clock()
    running = True

    while running:
        if life_num and not paused:
            # 检测用户键盘操作
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            # 绘制背景
            screen.blit(background, (0, 0))

            # 切换图片
            delay -= 1
            if not delay:
                delay = 120
            if not (delay % 10):
                switch_image = not switch_image

            # 绘制补给并检测是否获得
            # 全屏炸弹补给
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False
            # 超级子弹补给
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_super_bullet = True
                    pygame.time.set_timer(SUPER_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False
            # 增加弹道补给
            if ballistic_supply.active:
                ballistic_supply.move()
                screen.blit(ballistic_supply.image, ballistic_supply.rect)
                if pygame.sprite.collide_mask(ballistic_supply, me):
                    get_bomb_sound.play()
                    if not update_bullet:
                        if ballistic_num < 4:
                            bullet1_index = 0
                            bullet1_num = bullet1_num * (ballistic_num + 1) // ballistic_num
                            ballistic_num += 1
                            bullet1.clear()
                            if ballistic_num == 2:
                                bullet_sound.set_volume(0.3)
                                for i in range(bullet1_num // ballistic_num):
                                    bullet1.append(bullet.Bullet1((me.rect.centerx - 10, me.rect.top)))
                                    bullet1.append(bullet.Bullet1((me.rect.centerx + 10, me.rect.top)))
                            elif ballistic_num == 3:
                                bullet_sound.set_volume(0.4)
                                for i in range(bullet1_num // ballistic_num):
                                    bullet1.append(bullet.Bullet1((me.rect.centerx - 20, me.rect.top)))
                                    bullet1.append(bullet.Bullet1(me.rect.midtop))
                                    bullet1.append(bullet.Bullet1((me.rect.centerx + 18, me.rect.top)))
                            elif ballistic_num == 4:
                                bullet_sound.set_volume(0.5)
                                for i in range(bullet1_num // ballistic_num):
                                    bullet1.append(bullet.Bullet1((me.rect.centerx - 24, me.rect.top)))
                                    bullet1.append(bullet.Bullet1((me.rect.centerx - 8, me.rect.top)))
                                    bullet1.append(bullet.Bullet1((me.rect.centerx + 8, me.rect.top)))
                                    bullet1.append(bullet.Bullet1((me.rect.centerx + 23, me.rect.top)))
                        else:
                            update_bullet = True
                            damage *= 4
                            ballistic_num = 1
                            bullet1_index = 0
                            bullet3_index = 0
                            bullet3_num = bullet1_num // 4
                            bullet1.clear()
                            for i in range(bullet3_num // ballistic_num):
                                bullet3.append(bullet.Bullet3(me.rect.midtop))
                    else:
                        if ballistic_num < 5:
                            bullet3_index = 0
                            bullet3_num = bullet3_num * (ballistic_num + 1) // ballistic_num
                            ballistic_num += 1
                            bullet3.clear()
                            if ballistic_num == 2:
                                for i in range(bullet3_num // ballistic_num):
                                    bullet3.append(bullet.Bullet3((me.rect.centerx - 18, me.rect.top)))
                                    bullet3.append(bullet.Bullet3((me.rect.centerx + 18, me.rect.top)))
                            elif ballistic_num == 3:
                                for i in range(bullet3_num // ballistic_num):
                                    bullet3.append(bullet.Bullet3((me.rect.centerx - 25, me.rect.top)))
                                    bullet3.append(bullet.Bullet3(me.rect.midtop))
                                    bullet3.append(bullet.Bullet3((me.rect.centerx + 24, me.rect.top)))
                            elif ballistic_num == 4:
                                for i in range(bullet3_num // ballistic_num):
                                    bullet3.append(bullet.Bullet3((me.rect.centerx - 29, me.rect.centery - 50)))
                                    bullet3.append(bullet.Bullet3((me.rect.centerx - 10, me.rect.top)))
                                    bullet3.append(bullet.Bullet3((me.rect.centerx + 10, me.rect.top)))
                                    bullet3.append(bullet.Bullet3((me.rect.centerx + 28, me.rect.centery - 50)))
                            elif ballistic_num == 5:
                                for i in range(bullet3_num // ballistic_num):
                                    bullet3.append(bullet.Bullet3((me.rect.centerx - 48, me.rect.centery - 50)))
                                    bullet3.append(bullet.Bullet3((me.rect.centerx - 25, me.rect.top)))
                                    bullet3.append(bullet.Bullet3(me.rect.midtop))
                                    bullet3.append(bullet.Bullet3((me.rect.centerx + 24, me.rect.top)))
                                    bullet3.append(bullet.Bullet3((me.rect.centerx + 46, me.rect.centery - 50)))
                        else:
                            ballistic_num = 5
                    ballistic_supply.active = False
            # 增加伤害补给
            if damage_supply.active:
                damage_supply.move()
                screen.blit(damage_supply.image, damage_supply.rect)
                if pygame.sprite.collide_mask(damage_supply, me):
                    get_bomb_sound.play()
                    damage += 1
                    damage_supply.active = False
            # 增加射速补给
            if ROF_supply.active:
                ROF_supply.move()
                screen.blit(ROF_supply.image, ROF_supply.rect)
                if pygame.sprite.collide_mask(ROF_supply, me):
                    get_bomb_sound.play()
                    if rof > 4:
                        rof -= 2
                    else:
                        rof = 4
                        # 射速达到上限时，增加射程
                        bullet1_num += ballistic_num
                        bullet1_index = 0
                        if not update_bullet:
                            if ballistic_num == 1:
                                bullet1.append(bullet.Bullet1(me.rect.midtop))
                            elif ballistic_num == 2:
                                bullet1.append(bullet.Bullet1((me.rect.centerx - 10, me.rect.top)))
                                bullet1.append(bullet.Bullet1((me.rect.centerx + 10, me.rect.top)))
                            elif ballistic_num == 3:
                                bullet1.append(bullet.Bullet1((me.rect.centerx - 20, me.rect.top)))
                                bullet1.append(bullet.Bullet1(me.rect.midtop))
                                bullet1.append(bullet.Bullet1((me.rect.centerx + 18, me.rect.top)))
                            elif ballistic_num == 4:
                                bullet1.append(bullet.Bullet1((me.rect.centerx - 24, me.rect.top)))
                                bullet1.append(bullet.Bullet1((me.rect.centerx - 8, me.rect.top)))
                                bullet1.append(bullet.Bullet1((me.rect.centerx + 8, me.rect.top)))
                                bullet1.append(bullet.Bullet1((me.rect.centerx + 23, me.rect.top)))
                        else:
                            if ballistic_num == 1:
                                bullet3.append(bullet.Bullet3(me.rect.midtop))
                            elif ballistic_num == 2:
                                bullet3.append(bullet.Bullet3((me.rect.centerx - 18, me.rect.top)))
                                bullet3.append(bullet.Bullet3((me.rect.centerx + 18, me.rect.top)))
                            elif ballistic_num == 3:
                                bullet3.append(bullet.Bullet3((me.rect.centerx - 25, me.rect.top)))
                                bullet3.append(bullet.Bullet3(me.rect.midtop))
                                bullet3.append(bullet.Bullet3((me.rect.centerx + 24, me.rect.top)))
                            elif ballistic_num == 4:
                                bullet3.append(bullet.Bullet3((me.rect.centerx - 29, me.rect.centery - 50)))
                                bullet3.append(bullet.Bullet3((me.rect.centerx - 10, me.rect.top)))
                                bullet3.append(bullet.Bullet3((me.rect.centerx + 10, me.rect.top)))
                                bullet3.append(bullet.Bullet3((me.rect.centerx + 28, me.rect.centery - 50)))
                            elif ballistic_num == 5:
                                bullet3.append(bullet.Bullet3((me.rect.centerx - 48, me.rect.centery - 50)))
                                bullet3.append(bullet.Bullet3((me.rect.centerx - 25, me.rect.top)))
                                bullet3.append(bullet.Bullet3(me.rect.midtop))
                                bullet3.append(bullet.Bullet3((me.rect.centerx + 24, me.rect.top)))
                                bullet3.append(bullet.Bullet3((me.rect.centerx + 46, me.rect.centery - 50)))

                        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
                        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
                        bullet2_num += 2
                    ROF_supply.active = False
            # 增加射程补给
            if range_supply.active:
                range_supply.move()
                screen.blit(range_supply.image, range_supply.rect)
                if pygame.sprite.collide_mask(range_supply, me):
                    get_bomb_sound.play()
                    if not update_bullet:
                        bullet1_num += ballistic_num
                        bullet1_index = 0
                        if ballistic_num == 1:
                            bullet1.append(bullet.Bullet1(me.rect.midtop))
                        elif ballistic_num == 2:
                            bullet1.append(bullet.Bullet1((me.rect.centerx - 10, me.rect.top)))
                            bullet1.append(bullet.Bullet1((me.rect.centerx + 10, me.rect.top)))
                        elif ballistic_num == 3:
                            bullet1.append(bullet.Bullet1((me.rect.centerx - 20, me.rect.top)))
                            bullet1.append(bullet.Bullet1(me.rect.midtop))
                            bullet1.append(bullet.Bullet1((me.rect.centerx + 18, me.rect.top)))
                        elif ballistic_num == 4:
                            bullet1.append(bullet.Bullet1((me.rect.centerx - 24, me.rect.top)))
                            bullet1.append(bullet.Bullet1((me.rect.centerx - 8, me.rect.top)))
                            bullet1.append(bullet.Bullet1((me.rect.centerx + 8, me.rect.top)))
                            bullet1.append(bullet.Bullet1((me.rect.centerx + 23, me.rect.top)))
                    else:
                        bullet3_num += ballistic_num
                        bullet3_index = 0
                        if ballistic_num == 1:
                            bullet3.append(bullet.Bullet3(me.rect.midtop))
                        elif ballistic_num == 2:
                            bullet3.append(bullet.Bullet3((me.rect.centerx - 18, me.rect.top)))
                            bullet3.append(bullet.Bullet3((me.rect.centerx + 18, me.rect.top)))
                        elif ballistic_num == 3:
                            bullet3.append(bullet.Bullet3((me.rect.centerx - 25, me.rect.top)))
                            bullet3.append(bullet.Bullet3(me.rect.midtop))
                            bullet3.append(bullet.Bullet3((me.rect.centerx + 24, me.rect.top)))
                        elif ballistic_num == 4:
                            bullet3.append(bullet.Bullet3((me.rect.centerx - 29, me.rect.centery - 50)))
                            bullet3.append(bullet.Bullet3((me.rect.centerx - 10, me.rect.top)))
                            bullet3.append(bullet.Bullet3((me.rect.centerx + 10, me.rect.top)))
                            bullet3.append(bullet.Bullet3((me.rect.centerx + 28, me.rect.centery - 50)))
                        elif ballistic_num == 5:
                            bullet3.append(bullet.Bullet3((me.rect.centerx - 48, me.rect.centery - 50)))
                            bullet3.append(bullet.Bullet3((me.rect.centerx - 25, me.rect.top)))
                            bullet3.append(bullet.Bullet3(me.rect.midtop))
                            bullet3.append(bullet.Bullet3((me.rect.centerx + 24, me.rect.top)))
                            bullet3.append(bullet.Bullet3((me.rect.centerx + 46, me.rect.centery - 50)))

                    bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
                    bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
                    bullet2_num += 2
                    range_supply.active = False
            # 增加生命值补给
            if life_supply.active:
                life_supply.move()
                screen.blit(life_supply.image, life_supply.rect)
                if pygame.sprite.collide_mask(life_supply, me):
                    get_bullet_sound.play()
                    life_num += 1
                    life_supply.active = False

            # 绘制大型敌机
            for each in big_enemies:
                if each.active:
                    each.move(h_action, w_action)
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)
                        # 绘制血槽
                        pygame.draw.line(screen, BLACK,
                                         (each.rect.left, each.rect.top - 5),
                                         (each.rect.right, each.rect.top - 5), 2)
                        # 当HP大于20%时显示绿色，否则显示红色
                        HP_remain = each.HP / enemy.BigEnemy.maxHP
                        if HP_remain > 0.2:
                            HP_color = GREEN
                        else:
                            HP_color = RED
                        pygame.draw.line(screen, HP_color,
                                         (each.rect.left, each.rect.top - 5),
                                         (each.rect.left + each.rect.width * HP_remain, each.rect.top - 5), 2)
                        # 大型敌机即将出现时，播放音效
                        if each.rect.bottom == -50:
                            enemy3_fly_sound.play(-1)
                else:
                    # 毁灭
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 7
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 2000
                            each.reset()

            # 绘制中型敌机
            for each in mid_enemies:
                if each.active:
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        each.move()
                        screen.blit(each.image, each.rect)
                        # 绘制血槽
                        pygame.draw.line(screen, BLACK,
                                         (each.rect.left, each.rect.top - 5),
                                         (each.rect.right, each.rect.top - 5), 2)
                        # 当HP大于20%时显示绿色，否则显示红色
                        HP_remain = each.HP / enemy.MidEnemy.maxHP
                        if HP_remain > 0.2:
                            HP_color = GREEN
                        else:
                            HP_color = RED
                        pygame.draw.line(screen, HP_color,
                                         (each.rect.left, each.rect.top - 5),
                                         (each.rect.left + each.rect.width * HP_remain, each.rect.top - 5), 2)
                else:
                    # 毁灭
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 5
                        if e2_destroy_index == 0:
                            score += 300
                            each.reset()

            # 绘制小型敌机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                    # 绘制血槽
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5), 2)
                    # 当HP大于20%时显示绿色，否则显示红色
                    HP_remain = each.HP / enemy.SmallEnemy.maxHP
                    if HP_remain > 0.2:
                        HP_color = GREEN
                    else:
                        HP_color = RED
                    pygame.draw.line(screen, HP_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * HP_remain, each.rect.top - 5), 2)
                else:
                    # 毁灭
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 5
                        if e1_destroy_index == 0:
                            score += 100
                            each.reset()

            # 发射子弹
            if not (delay % rof):
                if not update_bullet:
                    bullet_sound.play()
                    if ballistic_num == 1:
                        bullet1[bullet1_index].reset(me.rect.midtop)
                        bullet1_index = (bullet1_index + ballistic_num) % bullet1_num
                    elif ballistic_num == 2:
                        bullet_sound.play()
                        bullet1[bullet1_index].reset((me.rect.centerx - 10, me.rect.top))
                        bullet1[bullet1_index + 1].reset((me.rect.centerx + 10, me.rect.top))
                        bullet1_index = (bullet1_index + ballistic_num) % bullet1_num
                    elif ballistic_num == 3:
                        bullet_sound.play()
                        bullet_sound.play()
                        bullet1[bullet1_index].reset((me.rect.centerx - 20, me.rect.top))
                        bullet1[bullet1_index + 1].reset(me.rect.midtop)
                        bullet1[bullet1_index + 2].reset((me.rect.centerx + 18, me.rect.top))
                        bullet1_index = (bullet1_index + ballistic_num) % bullet1_num
                    elif ballistic_num == 4:
                        bullet_sound.play()
                        bullet_sound.play()
                        bullet_sound.play()
                        bullet1[bullet1_index].reset((me.rect.centerx - 24, me.rect.top))
                        bullet1[bullet1_index + 1].reset((me.rect.centerx - 8, me.rect.top))
                        bullet1[bullet1_index + 2].reset((me.rect.centerx + 8, me.rect.top))
                        bullet1[bullet1_index + 3].reset((me.rect.centerx + 23, me.rect.top))
                        bullet1_index = (bullet1_index + ballistic_num) % bullet1_num
                else:
                    missile_sound.play()
                    if ballistic_num == 1:
                        bullet3[bullet3_index].reset(me.rect.midtop)
                        bullet3_index = (bullet3_index + ballistic_num) % bullet3_num
                    elif ballistic_num == 2:
                        missile_sound.play()
                        bullet3[bullet3_index].reset((me.rect.centerx - 18, me.rect.top))
                        bullet3[bullet3_index + 1].reset((me.rect.centerx + 18, me.rect.top))
                        bullet3_index = (bullet3_index + ballistic_num) % bullet3_num
                    elif ballistic_num == 3:
                        missile_sound.play()
                        missile_sound.play()
                        bullet3[bullet3_index].reset((me.rect.centerx - 25, me.rect.top))
                        bullet3[bullet3_index + 1].reset(me.rect.midtop)
                        bullet3[bullet3_index + 2].reset((me.rect.centerx + 24, me.rect.top))
                        bullet3_index = (bullet3_index + ballistic_num) % bullet3_num
                    elif ballistic_num == 4:
                        missile_sound.play()
                        missile_sound.play()
                        missile_sound.play()
                        bullet3[bullet3_index].reset((me.rect.centerx - 29, me.rect.centery - 50))
                        bullet3[bullet3_index + 1].reset((me.rect.centerx - 10, me.rect.top))
                        bullet3[bullet3_index + 2].reset((me.rect.centerx + 10, me.rect.top))
                        bullet3[bullet3_index + 3].reset((me.rect.centerx + 28, me.rect.centery - 50))
                        bullet3_index = (bullet3_index + ballistic_num) % bullet3_num
                    elif ballistic_num == 5:
                        missile_sound.play()
                        missile_sound.play()
                        missile_sound.play()
                        missile_sound.play()
                        bullet3[bullet3_index].reset((me.rect.centerx - 48, me.rect.centery - 50))
                        bullet3[bullet3_index + 1].reset((me.rect.centerx - 25, me.rect.top))
                        bullet3[bullet3_index + 2].reset((me.rect.centerx, me.rect.top))
                        bullet3[bullet3_index + 3].reset((me.rect.centerx + 24, me.rect.top))
                        bullet3[bullet3_index + 4].reset((me.rect.centerx + 46, me.rect.centery - 50))
                        bullet3_index = (bullet3_index + ballistic_num) % bullet3_num

                if is_super_bullet:
                    bullet2[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullet2[bullet2_index + 1].reset((me.rect.centerx + 31, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % bullet2_num
            # 检测子弹是否击中敌机
            if not update_bullet:
                for b in bullet1:
                    if b.active:
                        b.move()
                        screen.blit(b.image, b.rect)
                        enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                        if enemy_hit:
                            b.active = False
                            for e in enemy_hit:
                                e.hit = True
                                e.HP -= damage
                                if e.HP <= 0:
                                    e.active = False
            else:
                for b in bullet3:
                    if b.active:
                        b.move()
                        screen.blit(b.image, b.rect)
                        enemy_hit = pygame.sprite.spritecollide(b, enemies, False)
                        if enemy_hit:
                            b.active = False
                            for e in enemy_hit:
                                e.hit = True
                                e.HP -= damage
                                if e.HP <= 0:
                                    e.active = False
            if is_super_bullet:
                for b in bullet2:
                    if b.active:
                        b.move()
                        screen.blit(b.image, b.rect)
                        enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                        if enemy_hit:
                            for e in enemy_hit:
                                e.hit = True
                                e.HP -= 2 * damage
                                if e.HP <= 0:
                                    e.active = False

            # 检测我方飞机是否被撞
            enemies_crash = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_crash and not me.invincible:
                me.active = False
                for e in enemies_crash:
                    e.active = False
                    score += 1000

            # 绘制我方飞机
            if me.active:
                if me.invincible:
                    if not (delay % 8):
                        screen.blit(me.image1, me.rect)
                else:
                    if switch_image:
                        screen.blit(me.image1, me.rect)
                    else:
                        screen.blit(me.image2, me.rect)
            else:
                # 毁灭
                if not (delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 5
                    if me_destroy_index == 0:
                        # life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)
            # 绘制得分
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            screen.blit(score_text, (10, -10))

            # 绘制等级
            level_text = level_font.render("level %s" % str(level), True, WHITE)
            screen.blit(level_text, (15, 30))

            # 绘制炸弹图标
            bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

            # 绘制我方生命值
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, (width - 10 - (i + 1) * life_rect.width, height - 10 - life_rect.height))

        # 生命值为0时，游戏结束
        elif life_num == 0:
            # 停止所有音乐和音效
            pygame.mixer.music.stop()
            pygame.mixer.stop()

            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)
            if not recorded:
                recorded = True
                # 读取历史最高分
                with open("record.txt", "r") as f:
                    record_score = int(f.read())

                # 如果玩家得分高于历史最高分，则存档
                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))
            # 绘制结束界面
            screen.blit(background, (0, 0))
            record_score_text = score_font.render("最高分: %d" % record_score, True, WHITE)
            screen.blit(record_score_text, (20, 20))

            gameover_text1 = gameover_font.render("你的得分", True, WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, WHITE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                (width - gameover_text2_rect.width) // 2, \
                gameover_text1_rect.bottom + 3
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                (width - again_rect.width) // 2, \
                gameover_text2_rect.bottom + 30
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                (width - gameover_rect.width) // 2, \
                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击重新开始
                if again_rect.left < pos[0] < again_rect.right and \
                        again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main()

                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                        gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()

        # 检测用户事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = pause_pressed_image
                    else:
                        paused_image = resume_pressed_image
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, randint(20, 40) * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                supply_p = choice(range(0, 100, 1))
                if 0 <= supply_p < 10:
                    bomb_supply.reset()
                elif 10 <= supply_p < 20:
                    bullet_supply.reset()
                elif 20 <= supply_p < 40:
                    ballistic_supply.reset()
                elif 40 <= supply_p < 50:
                    damage_supply.reset()
                elif 50 <= supply_p < 70:
                    ROF_supply.reset()
                elif 70 <= supply_p < 90:
                    range_supply.reset()
                elif 90 <= supply_p < 100:
                    life_supply.reset()
                pygame.time.set_timer(SUPPLY_TIME, randint(4, 5) * 1000)

            elif event.type == SUPER_BULLET_TIME:
                is_super_bullet = False
                pygame.time.set_timer(SUPER_BULLET_TIME, 0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

            elif event.type == BIG_ENEMY_MOVE:
                h_action = choice([True, False])
                w_action = choice([True, False])
                pygame.time.set_timer(BIG_ENEMY_MOVE, randint(5, 10) * 100)

        # 根据用户的得分增加难度
        if level == 1 and score >= 1000:
            level = 2
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 10)
            add_mid_enemies(mid_enemies, enemies, 2)
            update(small_enemies, level)
            update(mid_enemies, level)

        elif level == 2 and score >= 3000:
            level = 3
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 10)
            add_mid_enemies(mid_enemies, enemies, 5)
            inc_speed(small_enemies, 1)
            update(small_enemies, level)
            update(mid_enemies, level)

        elif level == 3 and score >= 10000:
            level = 4
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 20)
            add_mid_enemies(mid_enemies, enemies, 8)
            add_big_enemies(big_enemies, enemies, 1)
            inc_speed(mid_enemies, 1)
            update(small_enemies, level)
            update(mid_enemies, level)

        elif level == 4 and score >= 20000:
            level = 5
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 30)
            add_mid_enemies(mid_enemies, enemies, 15)
            add_big_enemies(big_enemies, enemies, 2)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            update(small_enemies, level)
            update(mid_enemies, level)
            update(big_enemies, level)

        elif level == 5 and score >= 50000:
            level = 6
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 30)
            add_mid_enemies(mid_enemies, enemies, 20)
            add_big_enemies(big_enemies, enemies, 3)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies, 1)
            update(small_enemies, level)
            update(mid_enemies, level)
            update(big_enemies, level)

        elif level == 6 and score >= 100000:
            level = 7
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 50)
            add_mid_enemies(mid_enemies, enemies, 25)
            add_big_enemies(big_enemies, enemies, 5)
            inc_speed(small_enemies, 1)
            inc_speed(big_enemies, 1)
            update(small_enemies, level)
            update(mid_enemies, level)
            update(big_enemies, level)

        # 绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        pygame.display.flip()
        # 60帧
        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()

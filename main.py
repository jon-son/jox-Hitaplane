#-*- coding: utf-8 -*-
import pygame
from sys import exit
import random

# 设置游戏屏幕大小
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed

# 玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 # 用来存储玩家飞机图片的列表
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.relife_pos = init_pos
        self.rect = player_rect[0]                      # 初始化图片所在的矩形
        self.rect.topleft = init_pos                    # 初始化矩形的左上角坐标
        self.speed = 8                                  # 初始化玩家飞机速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group()            # 玩家飞机所发射的子弹的集合
        self.life = 3                                   # 玩家生命
        self.wait = 0                                   #复活等待时间
        self.god_time = 0                               #无敌时间
        self.god_cd = 0                                 #无敌技能冷却时间
        self.boss = 0                                   # boss伤害

    # 发射子弹
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    # 向上移动，需要判断边界
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    # 向下移动，需要判断边界
    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    # 向左移动，需要判断边界
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    # 向右移动，需要判断边界
    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed
    def reLife(self):
        self.rect.topleft = self.relife_pos
        self.bullets.remove()


# 敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2

    # 敌机移动，边界判断及删除在游戏主循环里处理
    def move(self):
        self.rect.top += self.speed
#Boss类
class Boss(pygame.sprite.Sprite):
    def __init__(self, boss_img, boss_down_img):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_img
        self.rect = self.image.get_rect()
        self.rect.topleft =  [500, 0]
        self.down_img = boss_down_img
        self.speed = 2
        self.life = 0
        self.come = 100
        self.move_time = 300
        self.bulletleft = pygame.sprite.Group()  # 玩家飞机所发射的子弹的集合
        self.bulletright = pygame.sprite.Group()  # 玩家飞机所发射的子弹的集合
        self.bullet = pygame.sprite.Group()  # 玩家飞机所发射的子弹的集合

    # 发射子弹
    def shoot(self, bullet_img):
        bullet = Boss_bullet(bullet_img, self.rect.midbottom)
        self.bullet.add(bullet)
    def shootLeft(self,bullet_img):
        bullet = Boss_bullet_Left(bullet_img, self.rect.midbottom)
        self.bulletleft.add(bullet)
    def shootRight(self,bullet_img):
        bullet = Boss_bullet_Right(bullet_img, self.rect.midbottom)
        self.bulletright.add(bullet)
    # BOSS移动，边界判断及删除在游戏主循环里处理
    def moveLeft(self):
        if self.rect.left - self.speed*100 <=0:
            self.moveRight()
        else:
            self.rect.left -= self.speed*100
    def moveRight(self):
        if self.rect.left + self.speed*100 >=SCREEN_WIDTH-161:
            self.moveLeft()
        else:
            self.rect.left += self.speed*100
    def bloodRect(self,type):
        if type == "box":
            return (self.rect.left,self.rect.top+60)
        elif type== "blood":
            return (self.rect.left - 3, self.rect.top + 60)
    def reLife(self):
        self.rect.topleft = [490, 0]

# BOSS子弹类
class Boss_bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 8

    def move(self):
        self.rect.top += self.speed
    def moveLeft(self):
        self.rect.top += self.speed
        self.rect.left -= self.speed
    def moveRight(self):
        self.rect.left += self.speed
# BOSS子弹类
class Boss_bullet_Left(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 8

    def move(self):
        self.rect.top += self.speed
        self.rect.left -= self.speed
# BOSS子弹类
class Boss_bullet_Right(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 8

    def move(self):
        self.rect.top += self.speed
        self.rect.left += self.speed
# 道具类
class Tools(pygame.sprite.Sprite):
    def __init__(self, img, init_pos,type):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 4
        self.type = type

    # 道具移动，边界判断及删除在游戏主循环里处理
    def move(self):
        self.rect.top += self.speed


# 初始化 pygame
pygame.init()

# 设置游戏界面大小、背景图片及标题
# 游戏界面像素大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 游戏界面标题
pygame.display.set_caption('Python打飞机大战')

# 背景图
background = pygame.image.load('resources/image/background.png').convert()

# Game Over 的背景图
game_over = pygame.image.load('resources/image/gameover.png')

# 飞机及子弹图片集合
plane_img = pygame.image.load('resources/image/shoot.png')

# 飞机无敌状态
plane_god = pygame.image.load('resources/image/god.png')

#道具图片
tools_life = pygame.image.load('resources/image/tools_life.png')
tools_god = pygame.image.load('resources/image/tools_god.png')


# 设置玩家飞机不同状态的图片列表，多张图片展示为动画效果
player_rect1 = []
player_rect1.append(pygame.Rect(0, 99, 102, 126))        # 玩家飞机图片
player_rect1.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸图片

player_rect2 = []
player_rect2.append(pygame.Rect(0, 99, 102, 126))        # 玩家飞机图片
player_rect2.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸图片

#BOSS飞机
boss_img = pygame.image.load('resources/image/boss.png')
boss_img_down = pygame.image.load('resources/image/boss_down.png')

#地球血条
blood_box = pygame.image.load('resources/image/blood_box.png')
blood = pygame.image.load('resources/image/blood.png')

#BOSS血条
boss_blood_box = pygame.image.load('resources/image/boss_blood_box.png')
boss_blood = pygame.image.load('resources/image/boss_blood.png')

# 敌机不同状态的图片列表，包括正常敌机，爆炸的敌机图片
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = plane_img.subsurface(pygame.Rect(267, 347, 57, 43))

# 子弹图片
bullet_rect = pygame.Rect(1004, 987, 9, 20)
bullet_img = plane_img.subsurface(bullet_rect)

#BOSS子弹图片
boss_bullet = pygame.image.load('resources/image/boss_bullet.png')

player_pos1 = [200, 640]
player_pos2 = [720, 640]
player1 = Player(plane_img, player_rect1, player_pos1)
player2 = Player(plane_img, player_rect2, player_pos2)


boss = Boss(boss_img,boss_img_down)
#存储敌机，管理多个对象
enemies1 = pygame.sprite.Group()

#存储道具，管理多个对象
tools = pygame.sprite.Group()

# 存储被玩家1击毁的飞机
enemies_down1 = pygame.sprite.Group()

# 存储被玩家2击毁的飞机
enemies_down2 = pygame.sprite.Group()



# 初始化射击及敌机移动频率
shoot_frequency1 = 0
shoot_frequency2 = 0
enemy_frequency = 0
boss_frequency = 0


tools_num = random.randint(1000,5000)
tools_frequency = 0
# 初始化分数
score1 = 0
score2 = 0
earth_life_num = 100
boss_life = 0
# 游戏循环帧率设置
clock = pygame.time.Clock()


# 判断游戏循环退出的参数
running = True


# 游戏主循环
while running:
    clock.tick(60)
    if (player1.life<=0 and player2.life<=0 )or earth_life_num <= 0:
        running = False
    # 绘制背景
    screen.fill(0)
    screen.blit(background, (0, 0))
    print(boss.life)
    # BOSS出现
    if score1+score2 > boss.come  and boss.life == 0 :
        boss.life = random.randint(3000,5000)
        boss_life = boss.life
        boss.come = random.randint(score1+score2*10,score1+score2*12)

    # 绘制BOSS飞机
    if boss.life > 0:
        screen.blit(boss.image, boss.rect)  # 将BOSS飞机画出来
        boss_blood_rect = pygame.Rect(0, 0, boss.life * (158 / boss_life), 22)
        boss_blood_new = boss_blood.subsurface(boss_blood_rect)
        screen.blit(boss_blood_new, boss.bloodRect("box"))  # 将BOSS血条画出来
        screen.blit(boss_blood_box, boss.bloodRect("blood"))  # 将BOSS血条框画出来
        for bullet in boss.bullet:
            # 以固定速度移动子弹
            bullet.move()
            # 移动出屏幕后删除子弹
            if bullet.rect.bottom > 800:
                boss.bullet.remove(bullet)

        for bullet in boss.bulletleft:
            # 以固定速度移动子弹
            bullet.move()
            # 移动出屏幕后删除子弹
            if bullet.rect.bottom > 800:
                boss.bulletleft.remove(bullet)

        for bullet in boss.bulletright:
            # 以固定速度移动子弹
            bullet.move()
            # 移动出屏幕后删除子弹
            if bullet.rect.bottom > 800:
                boss.bulletright.remove(bullet)
        # BOSS移动
        if boss.move_time == 0:
            move_type = random.randint(1,2)
            if move_type == 1:
                boss.moveLeft()
            if move_type == 2:
                boss.moveRight()
            boss.move_time = random.randint(500,2000)
        boss.move_time -= 1

    else:
        for bullet in boss.bullet:
            boss.bullet.remove(bullet)
        for bullet in boss.bulletleft:
            boss.bulletleft.remove(bullet)
        for bullet in boss.bulletright:
            boss.bulletright.remove(bullet)



    # 绘制玩家1飞机
    if player1.life>0 and player1.wait == 0:
        screen.blit(player1.image[0], player1.rect) #将正常飞机画出来
        if not player1.god_time == 0:
            screen.blit(plane_god, player1.rect)  # 将飞机保护罩画出来
        for bullet in player1.bullets:
            # 以固定速度移动子弹
            bullet.move()
            if pygame.sprite.collide_circle(bullet, boss) and boss.life > 0 :
                boss.life-=5
                if boss.life<0:
                    boss.life = 0
                player1.boss += 1
                if boss.life == 0:
                    screen.blit(boss.down_img, boss.rect)
                    score1+=player1.boss
                    player1.boss = 0
                    boss.reLife()
                player1.bullets.remove(bullet)

            # 移动出屏幕后删除子弹
            if bullet.rect.bottom <0:
                player1.bullets.remove(bullet)

    # 绘制玩家2飞机
    if player2.life>0 and player2.wait == 0:
        screen.blit(player2.image[0], player2.rect)  # 将正常飞机画出来
        if not player2.god_time == 0:
            screen.blit(plane_god, player2.rect)  # 将飞机保护罩画出来
        for bullet in player2.bullets:
            # 以固定速度移动子弹
            bullet.move()
            if pygame.sprite.collide_circle(bullet, boss) and boss.life > 0 :
                boss.life-=5
                if boss.life<0:
                    boss.life = 0
                player2.boss += 1
                if boss.life == 0:
                    screen.blit(boss.down_img, boss.rect)
                    score2 += player2.boss
                    player2.boss = 0
                    boss.reLife()
                player2.bullets.remove(bullet)
            # 移动出屏幕后删除子弹
            if bullet.rect.bottom < 0:
                player2.bullets.remove(bullet)



    if not player1.wait == 0:
        player1.wait -= 1
    if not player2.wait == 0:
        player2.wait -= 1
    if player1.god_cd>0:
        player1.god_cd -= 1
    if player2.god_cd>0:
        player2.god_cd -= 1

    if player1.wait == 0:
        player1.god_time = 200
    if player2.wait == 0:
        player2.god_time = 200
    if not player1.god_time == 0:
        player1.god_time -= 1
    if not player2.god_time == 0:
        player2.god_time -= 1

    # 生成敌机，需要控制生成频率
    # 循环20次生成一架敌机
    if enemy_frequency % 20== 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), random.randint(0, SCREEN_HEIGHT - enemy1_rect.height-300)]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0


    for enemy in enemies1:
        #2. 移动敌机
        enemy.move()
        #3. 敌机与玩家飞机碰撞效果处理
        if pygame.sprite.collide_circle(enemy, player1) and player1.life>0 and player1.wait == 0:
            enemies_down1.add(enemy)
            enemies1.remove(enemy)
            if player1.god_time == 0:
                player1.life -= 1
                screen.blit(player1.image[1], player1.rect)
                player1.wait = 60
                player1.reLife()
                for bullet in player1.bullets:
                    # 移出子弹
                    player1.bullets.remove(bullet)

        if pygame.sprite.collide_circle(enemy, player2) and player2.life>0 and player2.wait == 0:
            enemies_down2.add(enemy)
            enemies1.remove(enemy)
            if player2.god_time == 0:
                player2.life -= 1
                screen.blit(player2.image[1], player2.rect)
                player2.wait = 60
                player2.reLife()
                for bullet in player2.bullets:
                    # 移出子弹
                    player2.bullets.remove(bullet)

        #4. 移动出屏幕后删除敌人
        if enemy.rect.top > 800:
            earth_life_num -=5
            enemies1.remove(enemy)



    #boss子弹
    for bullet in boss.bullet:
        #子弹与玩家飞机碰撞效果处理
        if pygame.sprite.collide_circle(bullet, player1) and player1.life>0 and player1.wait == 0:
            if player1.god_time == 0:
                player1.life -= 1
                screen.blit(player1.image[1], player1.rect)
                player1.wait = 60
                player1.reLife()
                for bullet in player1.bullets:
                    # 移出子弹
                    player1.bullets.remove(bullet)
        if pygame.sprite.collide_circle(bullet, player2) and player2.life>0 and player2.wait == 0:
            if player2.god_time == 0:
                player2.life -= 1
                screen.blit(player2.image[1], player2.rect)
                player2.wait = 60
                player2.reLife()
                for bullet in player2.bullets:
                    # 移出子弹
                    player2.bullets.remove(bullet)

    for bullet in boss.bulletleft:
        #子弹与玩家飞机碰撞效果处理
        if pygame.sprite.collide_circle(bullet, player1) and player1.life>0 and player1.wait == 0:
            if player1.god_time == 0:
                player1.life -= 1
                screen.blit(player1.image[1], player1.rect)
                player1.wait = 60
                player1.reLife()
                for bullet in player1.bullets:
                    # 移出子弹
                    player1.bullets.remove(bullet)
        if pygame.sprite.collide_circle(bullet, player2) and player2.life>0 and player2.wait == 0:
            if player2.god_time == 0:
                player2.life -= 1
                screen.blit(player2.image[1], player2.rect)
                player2.wait = 60
                player2.reLife()
                for bullet in player2.bullets:
                    # 移出子弹
                    player2.bullets.remove(bullet)

    for bullet in boss.bulletright:
        #子弹与玩家飞机碰撞效果处理
        if pygame.sprite.collide_circle(bullet, player1) and player1.life>0 and player1.wait == 0:
            if player1.god_time == 0:
                player1.life -= 1
                screen.blit(player1.image[1], player1.rect)
                player1.wait = 60
                player1.reLife()
                for bullet in player1.bullets:
                    # 移出子弹
                    player1.bullets.remove(bullet)
        if pygame.sprite.collide_circle(bullet, player2) and player2.life>0 and player2.wait == 0:
            if player2.god_time == 0:
                player2.life -= 1
                screen.blit(player2.image[1], player2.rect)
                player2.wait = 60
                player2.reLife()
                for bullet in player2.bullets:
                    # 移出子弹
                    player2.bullets.remove(bullet)
    boss.bullet.draw(screen)
    boss.bulletleft.draw(screen)
    boss.bulletright.draw(screen)

    #敌机被子弹击中效果处理
    #将被击中的敌机对象添加到击毁敌机 Group 中

    enemies1_down = pygame.sprite.groupcollide(enemies1, player1.bullets, 1, 1)
    for enemy_down1 in enemies1_down:
        enemies_down1.add(enemy_down1)
    enemies2_down = pygame.sprite.groupcollide(enemies1, player2.bullets, 1, 1)
    for enemy_down2 in enemies2_down:
        enemies_down2.add(enemy_down2)



    # 敌机被子弹击中效果显示
    for enemy_down in enemies_down1:
        enemies_down1.remove(enemy_down)
        score1 += 1
        screen.blit(enemy_down.down_imgs, enemy_down.rect) #将爆炸的敌机画出来

    # 敌机被子弹击中效果显示
    for enemy_down in enemies_down2:
        enemies_down2.remove(enemy_down)
        score2 += 1
        screen.blit(enemy_down.down_imgs, enemy_down.rect) #将爆炸的敌机画出来
    # 显示敌机
    enemies1.draw(screen)


    # 生成道具，需要控制生成频率
    if tools_frequency >= tools_num:
        tools_type = random.randint(0,1)
        tools1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width),0]
        if tools_type == 0 :
            tool0 = Tools(tools_life, tools1_pos,tools_type)
            tools.add(tool0)
        elif tools_type == 1:
            tool1 = Tools(tools_god, tools1_pos,tools_type)
            tools.add(tool1)
        tools_num = random.randint(1000, 5000)
        tools_frequency = 0
    tools_frequency += 1

    for tool in tools:
        # 2. 移动道具
        tool.move()
        # 3. 玩家飞机获得道具处理
        if pygame.sprite.collide_circle(tool, player1) and player1.life>0 and player1.wait == 0:
            tools.remove(tool)
            if tool.type == 0:
                player1.life += 1
            elif tool.type == 1:
                player1.god_time = 600

        if pygame.sprite.collide_circle(tool, player2) and player2.life>0 and player2.wait == 0:
            tools.remove(tool)
            if tool.type == 0:
                player2.life += 1
            elif tool.type == 1:
                player2.god_time = 600

        # 4. 移动出屏幕后删除道具
        if tool.rect.top > 800:
            tools.remove(tool)

    #显示道具
    tools.draw(screen)

    # 绘制得分
    score_font = pygame.font.Font(None, 36)
    score_text1 = score_font.render('player1: '+str(score1), True, (128, 128, 128))
    text_rect1 = score_text1.get_rect()
    text_rect1.topleft = [10, 10]
    screen.blit(score_text1, text_rect1)

    score_text2 = score_font.render('player2: '+str(score2), True, (128, 128, 128))
    text_rect2 = score_text2.get_rect()
    text_rect2.topleft = [855, 10]
    screen.blit(score_text2, text_rect2)

    # 绘制地球生命值
    blood_rect = pygame.Rect(0, 0, earth_life_num*(496/100), 18)
    blood_new = blood.subsurface(blood_rect)
    screen.blit(blood_new, (252,10)) #将地球血条画出来
    screen.blit(blood_box, (250, 10))  # 将地球血条框画出来

    # 绘制生命
    for i in range(0,player1.life):
        screen.blit(tools_life,(10+(i*30), 40))
    for i in range(player2.life-1,-1,-1):
        screen.blit(tools_life,(945-(i*30), 40))


    if player1.life<=0 and player2.life<=0:
        screen.blit(game_over, (0, 0))

    if player1.life>0 :
        player1.bullets.draw(screen)
    if player2.life>0 :
        player2.bullets.draw(screen)

    if shoot_frequency1 % 7 == 0 and player1.wait==0:
        player1.shoot(bullet_img)
    shoot_frequency1 += 1
    if shoot_frequency1 >= 7:
        shoot_frequency1 = 0

    if shoot_frequency2 % 7 == 0 and player2.wait == 0:
        player2.shoot(bullet_img)
    shoot_frequency2 += 1
    if shoot_frequency2 >= 7:
        shoot_frequency2 = 0

    if boss_frequency % 60 == 0 and boss.life > 0:
        boss.shoot(boss_bullet)
        boss.shootLeft(boss_bullet)
        boss.shootRight(boss_bullet)
    boss_frequency += 1
    if boss_frequency >= 60:
        boss_frequency = 0

    # 更新屏幕
    pygame.display.update()

    # 处理游戏退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # 获取键盘事件（上下左右按键）
    key_pressed = pygame.key.get_pressed()

    # 处理键盘事件（移动飞机的位置）
    if key_pressed[pygame.K_w]  and player1.life>0 and player1.wait == 0:
        player1.moveUp()
    if key_pressed[pygame.K_s] and player1.life>0 and player1.wait == 0:
        player1.moveDown()
    if key_pressed[pygame.K_a] and player1.life>0 and player1.wait == 0:
        player1.moveLeft()
    if key_pressed[pygame.K_d] and player1.life>0 and player1.wait == 0:
        player1.moveRight()
    if key_pressed[pygame.K_1] and player1.life>0 and player1.wait == 0 and player1.god_cd<=0:
        player1.life  -= 1
        player1.god_cd = 1200
        player1.god_time = 1200



    if key_pressed[pygame.K_UP] and player2.life>0 and player2.wait == 0:
        player2.moveUp()
    if key_pressed[pygame.K_DOWN] and player2.life>0 and player2.wait == 0:
        player2.moveDown()
    if key_pressed[pygame.K_LEFT] and player2.life>0 and player2.wait == 0:
        player2.moveLeft()
    if key_pressed[pygame.K_RIGHT] and player2.life>0 and player2.wait == 0:
        player2.moveRight()
    if key_pressed[pygame.K_KP1] and player2.life>0 and player2.wait == 0 and player2.god_cd<=0:
        player2.life -= 1
        player2.god_cd = 1200
        player2.god_time = 1200



# 游戏 Game Over 后显示最终得分
font = pygame.font.Font(None, 64)
text = font.render('Final Score: '+ str(score1+score2), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
screen.blit(game_over, (0, 0))
screen.blit(text, text_rect)

# 显示得分并处理游戏退出
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
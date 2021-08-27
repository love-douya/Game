import pygame as pg
import random
import os

FPS = 60
WIDTH = 500
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 游戏初始化and创建窗口
pg.init()
# 初始化音频
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Game')
Clock = pg.time.Clock()

# 载入图片, convert函数是为了把图片转换成pygame容易读取的格式，这样画到画面比较快
backgroud_img = pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), 'background.png')).convert()
player_img = pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), 'player.png')).convert()
player_mini_img = pg.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
rock_img = pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), 'rock.png')).convert()
bullet_img = pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), 'bullet.png')).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), f'rock{i}.png')).convert())
expl_animation = {}
expl_animation['large'] = []
expl_animation['small'] = []
expl_animation['player'] = []
for i in range(9):
    expl_img = pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), f'expl{i}.png')).convert()
    expl_img.set_colorkey(BLACK)
    expl_animation['large'].append(pg.transform.scale(expl_img, (75, 75)))
    expl_animation['small'].append(pg.transform.scale(expl_img, (30, 30)))
    player_expl_img = pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), f'player_expl{i}.png')).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_animation['player'].append(player_expl_img)
power_imgs ={}
power_imgs['shield'] = pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), 'shield.png')).convert()
power_imgs['gun'] = pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), 'gun.png')).convert()

# 载入音乐
shoot_sound = pg.mixer.Sound(os.path.join(os.path.join(os.path.abspath('.'), 'sound'), 'shoot.wav'))
gun_sound = pg.mixer.Sound(os.path.join(os.path.join(os.path.abspath('.'), 'sound'), 'pow1.wav'))
sheild_sound = pg.mixer.Sound(os.path.join(os.path.join(os.path.abspath('.'), 'sound'), 'pow0.wav'))
die_sound = pg.mixer.Sound(os.path.join(os.path.join(os.path.abspath('.'), 'sound'), 'rumble.ogg'))
expl_sounds = [
    pg.mixer.Sound(os.path.join(os.path.join(os.path.abspath('.'), 'sound'), 'expl0.wav'))
   ,pg.mixer.Sound(os.path.join(os.path.join(os.path.abspath('.'), 'sound'), 'expl1.wav'))
]
# 载入一直播放的音乐
pg.mixer.music.load(os.path.join(os.path.join(os.path.abspath('.'), 'sound'), 'background.ogg'))
# 调节音乐大小
pg.mixer.music.set_volume(0.4)

font_name = os.path.join(os.path.abspath('.'), 'font.ttf')
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    # 第二个参数True让文字平顺
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

# 删除石头后重新生成石头
def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

# 画血条
def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp / 100) * BAR_LENGTH
    # pg.Rect生成一个矩形
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    # 画里面绿色血条
    pg.draw.rect(surf, GREEN, fill_rect)
    # 画外框，第四个参数写2
    pg.draw.rect(surf, WHITE, outline_rect, 2)

# 画还剩几条命(几个小飞船)
def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 32 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    draw_text(screen, '太空生存战！', 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, '← →移动飞船 空白键发射子弹~', 22, WIDTH / 2, HEIGHT / 2)  
    draw_text(screen, '按任意键开始游戏', 18, WIDTH / 2, HEIGHT * 3/4)
    pg.display.update()
    waiting = True
    while waiting:
        Clock.tick(FPS) 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            # 这里不要写KEYDOWN，写KEYUP，等键盘按下去再松开游戏才开始
            elif event.type == pg.KEYUP:
                waiting = False

class Player (pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # self.image = pg.Surface((50, 40)) 
        # 复制飞船的图片
        self.image = pg.transform.scale(player_img, (50, 38))
        # 该方法可以把黑色变成透明
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius) # 为了测试圆形
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        # 定位中间坐标
        # self.rect.center = (WIDTH / 2, HEIGHT / 2)
        # 或者定位左上角坐标
        # self.rect.x = 200 
        # self.rect.y = 200
        # 设定速度，该字段为自定义字段，不是继承字段
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        # gun等级
        self.gun = 1
        self.gun_time = 0
    
    def update(self):
        now = pg.time.get_ticks()
        # 让吃到闪电5000毫秒后子弹等级自动下降
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now
        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        # 返回的布尔值，检测键盘上每一个按键是否被按下去，如果有返回True，否则False
        key_pressed = pg.key.get_pressed()
        # 判断右键是否有被按下去
        if key_pressed[pg.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pg.K_a]:
            self.rect.x -= self.speedx

        # 到达边界时候卡住 
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not(self.hidden):    
            if self.gun == 1:   
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1, bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()              
    
    def hide(self):
        self.hidden = True
        self.hide_time = pg.time.get_ticks()
        # 把飞船定位到视窗外，这样就会造成飞船消失的错觉
        self.rect.center = (WIDTH / 2, HEIGHT + 500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pg.time.get_ticks()

class Rock (pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # random.choice方法随机从列表中挑选一个元素
        self.image_original = random.choice(rock_imgs)
        # self.image = pg.Surface((30, 40))
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius) # 为了测试圆形
        # 初始化石头的位置，随机生成0~画布宽度减去石头宽度当中的一个数作为X坐标
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        # 画布上方的随机一个地方生成，然后掉下来
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 5)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)
    '''
    如果单纯写self.image = pg.transform.rotate(self.image, self.degree)会失真
    界面卡死，因为下一个旋转的状态依赖于上一个状态，递归很多层，直接失真卡死
    '''
    def rotate(self):
        self.total_degree += self.rot_degree
        # 超过360度没有意义，但也可超过
        self.total_degree = self.total_degree % 360
        self.image = pg.transform.rotate(self.image_original, self.total_degree)
        # 每一次旋转前都要对中心点做重新的定位，否则会始终按照初始位置的rect的中心点旋转
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        # 石头的旋转
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet (pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        # self.image = pg.Surface((10, 20))
        self.image = bullet_img    
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # 子弹位置射程传进来的值
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            # 如果子弹的底部超过了视窗，就删除，否则消耗资源，kill为Sprite的方法
            self.kill()

class Explosion (pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        # pg.time.get_ticks()回传从初始化到结束的毫秒数
        self.last_update = pg.time.get_ticks()
        # 至少过50毫秒到爆炸的下一张图片
        self.frame_rate = 50
    
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_animation[self.size]):
                # 如果更新到最后一张图片就删掉
                self.kill()
            else:
                self.image = expl_animation[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power (pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# 所有物体的组
all_sprites = pg.sprite.Group()
# 判断石头和子弹是否有碰撞，需要分别给石头和子弹创建两个Sprite群组
rocks = pg.sprite.Group()
bullets = pg.sprite.Group()  
powers = pg.sprite.Group()
# 创建一个飞机
player = Player()
all_sprites.add(player)  
# 创建若干颗石头
for i in range(8):
    new_rock()
# 分数
score = 0 

# -1表示音乐重复播放
pg.mixer.music.play(-1)

# 窗口循环
# 显示初始画面
show_init = True
running = True
while running:
    if show_init:
        draw_init()
        show_init = False
    # while循环一秒最多跑60次
    Clock.tick(FPS) 
    # 取得输入
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # 判断每次是按的什么键
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()
     
    # 更新游戏
    # 执行每个物件(sprite)中的update函数
    all_sprites.update() 
    '''
    检测两个Group是否有碰撞，如果有则第三个参数判断rock是否删掉，第四个参数判断bullet是否山删掉
    如果删除了石头则重新生成一个石头
    '''
    hits = pg.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits: 
        random.choice(expl_sounds).play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'large')
        all_sprites.add(expl)
        # random.random()返回0~1的随机数，这里设置掉宝率为9成
        if random.random() > 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()

    # 如果石头撞到飞船则结束游戏，删不删除石头都无所谓了
    # 预设是矩形碰撞，pg.sprite.collide_circle参数修改成了圆形的碰撞判断，需要再给player和rock给一个属性radius
    hits = pg.sprite.spritecollide(player, rocks, True, pg.sprite.collide_circle)     
    for hit in hits:
        new_rock()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'small')
        all_sprites.add(expl)
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            # 死亡后隐藏飞船一段时间
            player.hide()
    
    # 判断宝物和飞船相撞
    hits = pg.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 20
            if player.health > 100:
                player.health = 100
            sheild_sound.play()
        elif hit.type == 'gun':
            player.gunup()
            gun_sound.play()

    # death_expl.alive()用来判断death_expl这个爆炸实例有没有被kill掉，没有就说明动画还没放完
    if player.lives == 0 and not(death_expl.alive()):
        running = False

    # 画面显示  
    # fill((R, G, B)), ((255, 0, 0))表示255表示红色填满
    screen.fill(BLACK) 
    # blit就是画的意思
    screen.blit(backgroud_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    pg.display.update()
 
pg.quit()


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
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Game')
Clock = pg.time.Clock()

# 载入图片, convert函数是为了把图片转换成pygame容易读取的格式，这样画到画面比较快
backgroud_img = pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), 'background.png')).convert()
player_img = pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), 'player.png')).convert()
rock_img = pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), 'rock.png')).convert()
bullet_img = pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), 'bullet.png')).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pg.image.load(os.path.join(os.path.join(os.path.abspath('.'), 'img'), f'rock{i}.png')).convert())

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
    
    def update(self):
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
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Rock (pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # random.choice方法随机从列表中挑选一个元素
        self.image_original = random.choice(rock_imgs)
        # self.image = pg.Surface((30, 40))
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
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

# 所有物体的组
all_sprites = pg.sprite.Group()
# 判断石头和子弹是否有碰撞，需要分别给石头和子弹创建两个Sprite群组
rocks = pg.sprite.Group()
bullets = pg.sprite.Group()  
# 创建一个飞机
player = Player()
all_sprites.add(player)  
# 创建若干颗石头
for i in range(8):
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

# 窗口循环
running = True
while running:
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
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)

    # 如果石头撞到飞船则结束游戏，删不删除石头都无所谓了
    # 预设是矩形碰撞，pg.sprite.collide_circle参数修改成了圆形的碰撞判断，需要再给player和rock给一个属性radius
    hits = pg.sprite.spritecollide(player, rocks, False, pg.sprite.collide_circle)     
    if hits:
        running = False

    # 画面显示  
    # fill((R, G, B)), ((255, 0, 0))表示255表示红色填满
    screen.fill(BLACK) 
    # blit就是画的意思
    screen.blit(backgroud_img, (0, 0))
    all_sprites.draw(screen)
    pg.display.update()
 
pg.quit()

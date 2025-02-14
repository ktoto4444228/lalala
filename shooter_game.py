from pygame import *
from random import randint
mixer.init()
font.init()

spisok = []
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont('Arial', 40)
font3 = font.SysFont('Arial', 90)
font4 = font.SysFont('Arial', 90)
font5 = font.SysFont('Arial', 40)
font6 = font.SysFont('Arial', 40)
lost = 0
schetchik = 0
rkct_life = 3
text_render = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
text_render4 = font6.render(str(rkct_life), 1, (255, 255, 255))
text_render2 = font2.render('Убитые:' + str(schetchik), 1, (255, 0, 0))
win = font3.render('Победа', True, (255, 255, 255))
lose = font4.render('Проигрыш', True, (255, 255, 255))
text_render3 = font5.render('Жизни:' + str(rkct_life), 1, (255, 255, 255))

window = display.set_mode((700, 500))
display.set_caption('виндоу пайтен')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
window.blit(background, (0, 0))

clock = time.Clock()
FPS = 60

mixer.music.load('space.ogg')
mixer.music.play()

kick = mixer.Sound('fire.ogg')
kick.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, w = 60, h = 65):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        global schet
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 600:
            self.rect.x += self.speed
        if keys_pressed[K_SPACE] and schet > 5:
            self.fire()
            schet = 0
    def fire(self):
        bullet = Bullet('bullet.png', 7, self.rect.centerx, self.rect.top, 5, 10)
        bullit.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        global text_render
        if self.rect.y > 450:
            self.rect.y = 0
            self.rect.x = randint(20, 500)
            lost += 1
            text_render = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
            self.speed = 3 + schetchik/20
        self.rect.y += self.speed
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroids(GameSprite):
    def update(self):
        if self.rect.y > 450:
            self.rect.y = 0
            self.rect.x = randint(20, 500)
        self.rect.y += self.speed


finish = False

schet = 0

player = Player('rocket.png', 7, 250, 375, 80, 120)
enemy1 = Enemy('ufo.png', 5, 400, 0, 100, 80)
enemy2 = Enemy('ufo.png', 5, 345, 0, 100, 80)
enemy3 = Enemy('ufo.png', 5, 120, 0, 100, 80)
enemy4 = Enemy('ufo.png', 5, 56, 0, 100, 80)
enemy5 = Enemy('ufo.png', 5, 600, 0, 100, 80)

monsters = sprite.Group()
monsters.add(enemy1)
monsters.add(enemy2)
monsters.add(enemy3)
monsters.add(enemy4)
monsters.add(enemy5)

AsteroidsG = sprite.Group()
asteroid = Asteroids('asteroid.png', 4, 360, 0, 100, 80)
AsteroidsG.add(asteroid)

bullit = sprite.Group()

konec = 0

game = True
while game:
    clock.tick(FPS)

    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        AsteroidsG.draw(window)
        AsteroidsG.update()
        window.blit(text_render, (0, 100))
        window.blit(text_render2, (0, 200))
        window.blit(text_render4, (0, 300))
        bullit.draw(window)
        bullit.update()
        schet += 1
        sprites_list = sprite.groupcollide(monsters, bullit, False, True)
        for monster in sprites_list:
            monster.rect.y = 0
            monster.rect.x = randint(20, 500)
            schetchik += 1
            text_render2 = font2.render('Убитые:' + str(schetchik), 1, (255, 0, 0))
        if schetchik >= 42:
            finish = True
            window.blit(win, (250, 250))
        if lost >= 10:
            finish = True
            window.blit(lose, (250, 250))
        for m in sprite.spritecollide(player, monsters, False) + sprite.spritecollide(player, AsteroidsG, False):#создать переменную со списком, и департировать тарелки обратно в их страну
            rkct_life -= 1
            m.rect.y = 0
            text_render4 = font6.render(str(rkct_life), 1, (255, 255, 255))
            if rkct_life == 0:
                finish = True
                window.blit(lose, (250, 250))
    else:
        konec += 1
        if konec == 60:
            finish = False
            konec = 0
            lost = 0
            schetchik = 0
            rkct_life = 3
            player.rect.x = 50
            player.rect.y = 360
            player.reset()
            player.update()
            monsters.draw(window)
            monsters.update()
            AsteroidsG.draw(window)
            AsteroidsG.update()
            bullit.draw(window)
            bullit.update()
            text_render2 = font2.render('Убитые:' + str(schetchik), 1, (255, 0, 0))
            text_render = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
            text_render4 = font6.render(str(rkct_life), 1, (255, 255, 255))

    display.update()

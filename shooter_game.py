pip#Создай собственный Шутер!

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
            window.blit(self.image, (self.rect.x, self.rect.y))

    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x<700-5 - self.rect.width:
            self.rect.x+=self.speed

    def fire(self):
        y = self.rect.y
        x = self.rect.centerx
        bullet = Bullet('bullet.png',x,y,30,60,5)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y +=self.speed
        if self.rect.y >500-self.rect.height:
            self.rect.x = randint(5,700-5-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(1,2)
            lost+=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y<0:
            self.kill()


#создай окно игры
window = display.set_mode((700,500))
display.set_caption('Шутер')



#задай фон сцены
background = transform.scale(image.load('galaxy.jpg'),(700,500))
button = GameSprite('button.png', 300,225,100,50,0)



mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

font.init()
font1 = font.Font(None,36)





player = Player('rocket.png', 316, 420 ,110,70,7)


enemy_count = 5
enemyes = sprite.Group()
for i in range(enemy_count):
    enemy = Enemy('ufo.png', randint(5,700-5-50),-50,50,70,randint(1,2))
    enemyes.add(enemy)


asteroid_count = 3
asteroids = sprite.Group()
enemyes = sprite.Group()
for i in range(asteroid_count):
    enemy = Enemy('asteroid.png', randint(5,700-5-50),-50,30,70,randint(1,2))
    asteroids.add(enemy)

bullets = sprite.Group()


game = True
finish = True
menu = True
lost = 0
score = 0
text = 0
font_win = font1.render('Ты выиграл',1,(255,255,255))
font_lose = font1.render('Ты проиграл',1,(255,255,255))

clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if menu == True:
        window.blit(background, (0,0))
        button.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if button.collidepoint(pos[0], pos[1]):
                menu = False
                finish = False
        if text == 1:
            window.blit(font_win, (250,175))
        elif text == 2:
            window.blit(font_lose, (250,175))
        lost = 0
        score = 0
        enemyes.empty()
        for i in range(enemy_count):
            enemy = Enemy('ufo.png', randint(5,700-5-50),-50,50,70,randint(1,2))
            enemyes.add(enemy)
        asteroids.empty()
        for i in range(asteroid_count):
            enemy = Enemy('asteroid.png', randint(5,700-5-50),-50,30,70,randint(1,2))
            asteroids.add(enemy)
        bullets.empty()



    if finish!=True:
        window.blit(background, (0,0))
        player.update()
        player.reset()
        enemyes.update()
        enemyes.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        sprite_list1 = sprite.spritecollide(player,enemyes,False)
        sprite_list2 = sprite.spritecollide(player,asteroids,False)
        if len(sprite_list1)>0 or len(sprite_list2)>0 or lost>4:
            text = 2
            menu = True
            finish = True

        sprite_list = sprite.groupcollide(enemyes, bullets, True, True)
        for m in sprite_list:
            score+=1
            enemy = Enemy('ufo.png', randint(5,700-5-50),-50,50,70,randint(1,2))
            enemyes.add(enemy)
        if score>9:
            text =1
            menu =True
            finish = True
                
        font_lost = font1.render('Пропущено:'+str(lost),1,(255,255,255))
        font_score = font1.render('Счёт:'+str(score),1,(255,255,255))
        window.blit(font_lost, (10,50))
        window.blit(font_score, (10,20))




    display.update()
    clock.tick(FPS)

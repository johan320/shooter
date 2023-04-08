#Создай собственный Шутер!
from pygame import *
from random import *
from time import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_speed,player_x,player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(60,60))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))



class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700:
            self.rect.x += self.speed
    def fire(self):
        keys = key.get_pressed()
    
        bullets.add(Bullet('bullet.png',10,self.rect.x,self.rect.y))
            


lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y == window.get_size()[1]:
            self.rect.y = 0
            self.rect.x = randint(0,window.get_size()[0])
            lost = lost + 1

class Astro(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y == window.get_size()[1]:
            self.rect.y = 0
            self.rect.x = randint(0,window.get_size()[0])
            




class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == window.get_size()[1]:
            self.kill()
        
            
font.init()   
mixer.init()
window = display.set_mode((800,600)) #Создать главное окно
display.set_caption('летун') #Создать название окна
background = transform.scale(image.load('galaxy.jpg'),(800,600)) #загрузить фото
clock = time.Clock() #установить обновление картинки
mixer.music.load('space.ogg')
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',36)
font3 = font.SysFont('Arial',50)
font4 = font.SysFont('Arial',50)
bullets = sprite.Group()
   
score = 0
aster = sprite.Group()

num_fire = 0

rel_time = False

mixer.music.play()
ufos = sprite.Group()
for i in range(5):
    ufos.add(Enemy('ufo.png',1,randint(0,window.get_size()[0]-100),0 ))
for i in range(3):
    aster.add(Astro('asteroid.png',3,randint(0,window.get_size()[0]-100),0 ))
hero = Player('rocket.png', 10, 300,480)
game = True #переменная для игровго цикла
while game: # игровой цикл
    window.blit(background,(0,0))
    for e in event.get():# собрать все события 
        if e.type == QUIT:#проверка - если нажат крестик(заркыть прогу) 
            game = False#оконьчить игру
        elif e.type  == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    num_fire = num_fire + 1
                    
                   
                    hero.fire()
                if num_fire >= 5 and not  rel_time:
                    last_time = timer()
                    rel_time = True 

    
    # отобразить загруженную картинку в кординатах x,y
    clock.tick(60) #установить частоту кадров
    hero.reset()
    ufos.update()
    bullets.update()
    
         
    aster.update()
    aster.draw(window)
    bullets.draw(window)
    window.blit(font1.render('Пропущено:' + str(lost), 1, (255,255,255)),(0,0))
    window.blit(font2.render('Очков:' + str(score), 1, (255,255,255)),(0,50))
    ufos.draw(window)
    hero.update()

    if rel_time:
        now_time = timer()

        if now_time - last_time < 1:
            reload = font4.render('reload...',1,(150,0,0))
            window.blit(reload, (250,460))
        else:
            num_fire = 0 
            rel_time = False

    groupcol = sprite.groupcollide(bullets,ufos,True,True)
    if sprite.spritecollide(hero,ufos,False):
        break
    spritecol = sprite.spritecollide(hero,ufos,False)
    for g in groupcol:
        score = score + 1
        monster = Enemy('ufo.png',1,randint(0,window.get_size()[0]-100),0 )
        ufos.add(monster)
    if sprite.spritecollide(hero,aster,False):
       break

     

    
    
    display.update()#да
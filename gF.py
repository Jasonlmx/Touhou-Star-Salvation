import pygame
import math
from pygame.locals import *
from pygame.sprite import Group
import global_var
import background

def drawRotation(image,pos,angle,screen):
    w, h = image.get_size()
    pivot = pygame.math.Vector2(w/2, -h/2)
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
    origin = (pos[0]+ min_box[0] - pivot_move[0], pos[1] - max_box[1] + pivot_move[1])
    rotated_image = pygame.transform.rotate(image, angle)
    #rotated_image.set_colorkey((0, 0, 0))
    screen.blit(rotated_image, origin)

def returnPosition(w,h,pos,angle):
    pivot = pygame.math.Vector2(w/2, -h/2)
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
    origin = (pos[0]+ min_box[0] - pivot_move[0], pos[1] - max_box[1] + pivot_move[1])
    return origin


def drawBackground(screen):
    screen.blit(global_var.get_value('left'),(0,0))
    screen.blit(global_var.get_value('up'),(60,0))
    screen.blit(global_var.get_value('down'),(60,690))
    screen.blit(global_var.get_value('right'),(660,30))

def displayScene(frame,screen):
    sceneNum=(frame//2)%(1540)
    c=sceneNum
    dig=0
    while (c>0):
        c=c//10
        dig+=1
    i=4-dig
    address="pic2/background_2_"
    for j in range(0,i):
        address=address+"0"
    if sceneNum!=0:
        address=address+str(sceneNum)
    address=address+".png"
    sceneImage=pygame.image.load(address)
    screen.blit(sceneImage,(30,20))
    screen.blit(sceneImage,(430,20))

def displayMenu(screen,stars):
    screen.blit(global_var.get_value('levelText01'),(736,30))
    screen.blit(global_var.get_value('mainText'),(670,500))
    for star in stars:
        star.draw(screen)


def loadImage():
    gunAlpha=150
    green=pygame.image.load('resource/playerFire/mainFire_green.png').convert_alpha()
    green=pygame.transform.scale(green,(48,48))
    green.set_alpha(gunAlpha)
    global_var.set_value('playerFire_green',green)
    blue=pygame.image.load('resource/playerFire/mainFire_blue.png').convert_alpha()
    blue=pygame.transform.scale(blue,(48,48))
    blue.set_alpha(gunAlpha)
    global_var.set_value('playerFire_blue',blue)
    red=pygame.image.load('resource/playerFire/mainFire_red.png').convert_alpha()
    red=pygame.transform.scale(red,(48,48))
    red.set_alpha(gunAlpha)
    global_var.set_value('playerFire_red',red)
    yellow=pygame.image.load('resource/playerFire/mainFire_yellow.png').convert_alpha()
    yellow=pygame.transform.scale(yellow,(48,48))
    yellow.set_alpha(gunAlpha)
    global_var.set_value('playerFire_yellow',yellow)
    orange=pygame.image.load('resource/playerFire/mainFire_orange.png').convert_alpha()
    orange=pygame.transform.scale(orange,(48,48))
    orange.set_alpha(gunAlpha)
    global_var.set_value('playerFire_orange',orange)

    global_var.set_value('levelText01',pygame.image.load('resource/text/levelText01.png').convert_alpha())
    global_var.set_value('pl00',pygame.image.load('resource/player/pl00/playerImage.png').convert_alpha())
    global_var.set_value('mainText',pygame.image.load('resource/text/mainText01.png').convert_alpha())
    global_var.set_value('cloud_bg',pygame.image.load('resource/background/cloud.png').convert_alpha())
    global_var.set_value('lake_bg',pygame.image.load('resource/background/lake.png').convert_alpha())
    global_var.set_value('star_bg',pygame.image.load('resource/background/star.png').convert_alpha())

    spirit=pygame.image.load('resource/enemy/spirit.png').convert_alpha()
    spirit=pygame.transform.scale(spirit,(576,384))
    global_var.set_value('spirit',spirit)
    ghost=pygame.image.load('resource/enemy/ghost.png').convert_alpha()
    ghost=pygame.transform.scale(ghost,(384,192))
    global_var.set_value('ghost',ghost)
    nimbus=pygame.image.load('resource/enemy/nimbus1.png').convert_alpha()
    nimbus=pygame.transform.scale(nimbus,(192,48))
    global_var.set_value('nimbus',nimbus)
    item=pygame.image.load('resource/item/item.png').convert_alpha()
    item=pygame.transform.scale(item,(384,24))
    global_var.set_value('itemImage',item)

    boss_1=pygame.image.load('resource/boss/satori.png').convert_alpha()
    boss_1=pygame.transform.scale(boss_1,(288,297))
    global_var.set_value('boss_1',boss_1)
    bossTracker=pygame.image.load('resource/text/bossTracker.png').convert_alpha()
    global_var.set_value('bossTracker',bossTracker)

    global_var.set_value('lifeSign',pygame.image.load('resource/text/lifeSign.png'))
    global_var.set_value('spellSign',pygame.image.load('resource/text/spellSign1.png'))
    global_var.set_value('lifeText',pygame.image.load('resource/text/lifeText.png'))
    global_var.set_value('spellText',pygame.image.load('resource/text/spellText.png'))
    front00=pygame.image.load('resource/text/front00.png')
    front00=pygame.transform.scale(front00,(768,768))
    global_var.set_value('front00',front00)
    powerText=pygame.image.load('resource/text/powerText.png')
    powerText=pygame.transform.scale(powerText,(99,24))
    global_var.set_value('powerText',powerText)
    hogwarts_background=pygame.image.load('resource/background/hogwarts.png').convert_alpha()
    global_var.set_value('hogwarts_background',hogwarts_background)
    stars_background=pygame.image.load('resource/background/stars.jpg').convert_alpha()
    global_var.set_value('stars_background',stars_background)

    big_star_bullet_image=pygame.image.load('resource/bullet/big_star_bullet.png')
    big_star_bullet_image=pygame.transform.scale(big_star_bullet_image,(384,48))
    global_var.set_value('big_star_bullet_image',big_star_bullet_image)
    laser_bullet_image=pygame.image.load('resource/bullet/laser_bullet.png')
    global_var.set_value('laser_bullet_image',laser_bullet_image)
    circle_bullet_image=pygame.image.load('resource/bullet/circle_bullet.png')
    circle_bullet_image=pygame.transform.scale(circle_bullet_image,(384,48))
    global_var.set_value('circle_bullet_image',circle_bullet_image)

    graze_text=pygame.Surface((96,24))
    graze_text=graze_text.convert_alpha()
    graze_text.fill((0,0,0,0))
    graze_text.blit(front00, (0, 0), (525,0,96,24))
    global_var.set_value('graze_text',graze_text)








class star_effect(pygame.sprite.Sprite):
    def __init__(self):
        super(star_effect,self).__init__()
        self.surf=pygame.image.load('resource/text/stars.png')
        self.surf.set_alpha(200)
        self.rect = self.surf.get_rect()
        self.frame=0
        self.angle=0
    def initial(self,centerx,centery):
        self.rect.centerx=centerx
        self.rect.centery=centery
    
    def update(self,screen):
        self.frame+=1
    
    def draw(self,screen):
        self.angle=self.frame*3
        drawRotation(self.surf,self.rect,self.angle,screen)

def showFpsBullet(screen,myfont,frame,bulletSum,log):
    #FPS
    t = pygame.time.get_ticks()
    #print(t)
    # deltaTime in seconds.
    deltaTime = (t - global_var.get_value('getTicksLastFrame')) / 1000.0
    global_var.set_value('getTicksLastFrame',t)    
    fp=round(1/deltaTime,1)
    temp=global_var.get_value('fpSec')
    temp=temp+fp
    global_var.set_value('fpSec',temp)
    if frame%60==1:
        avgFp=round(global_var.get_value('fpSec')/60.0,1)
        fpText=myfont.render('FPS: '+str(avgFp), True, (255, 255, 255))
        global_var.set_value('fpText',fpText)
        global_var.set_value('fpSec',0)
        #log recording  
        
        #print(str(round((frame-1)/60))+','+str(avgFp)+','+str(bulletSum),file=log)
    screen.blit(global_var.get_value('fpText'),(820,692))
    bulletText=myfont.render('Bullets: '+str(bulletSum), True, (255, 255, 255))
    screen.blit(bulletText,(820,672))

def doBackground(screen,backgrounds):
    for i in range(0,3):
        for j in range(0,4):
            new_background=background.lake_bg()
            new_background.initial(128+i*256,128+j*256)
            backgrounds.add(new_background)
    
def drawBlinder(screen,surf):
    screen.blit(surf,(0,720))

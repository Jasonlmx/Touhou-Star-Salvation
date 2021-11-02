import pygame
import math
from pygame.locals import *
from pygame.sprite import Group
import global_var
import background

def shakeScreen():
    shakeFrame=global_var.get_value('shakeFrame')
    if shakeFrame>0:
        global_var.set_value('ifShaking',True)
        global_var.set_value('shakeFrame',shakeFrame-1)
    else:
        global_var.set_value('ifShaking',False)
        
    
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

def fill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

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
    reimu_fire=pygame.image.load('resource/playerFire/reimu_fire.png').convert_alpha()
    reimu_fire=pygame.transform.scale(reimu_fire,(384,168))
    global_var.set_value('reimu_fire',reimu_fire)

    global_var.set_value('levelText01',pygame.image.load('resource/text/levelText01.png').convert_alpha())
    global_var.set_value('pl00',pygame.image.load('resource/player/pl00/playerImage.png').convert_alpha())
    global_var.set_value('pl01',pygame.image.load('resource/player/pl01/playerImage.png').convert_alpha())
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
    boss_1=pygame.transform.smoothscale(boss_1,(288,297))
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
    front01=pygame.image.load('resource/text/front00.png')
    textArea=pygame.Surface((80,220)).convert_alpha()
    textArea.fill((0,0,0,0))
    #Hiscore
    textArea.blit(front01,(0,0),(256,0,80,19))
    #score
    textArea.blit(front01,(0,30),(256,19,80,19))
    #player
    textArea.blit(front01,(0,70),(256,38,80,19))
    #power
    textArea.blit(front01,(0,143),(256,57,80,19))
    #graze
    textArea.blit(front01,(0,176),(336,0,80,19))
    global_var.set_value('textArea',textArea)
    powerText=pygame.image.load('resource/text/powerText.png')
    powerText=pygame.transform.scale(powerText,(99,24))
    global_var.set_value('powerText',powerText)
    hogwarts_background=pygame.image.load('resource/background/hogwarts.png').convert_alpha()
    global_var.set_value('hogwarts_background',hogwarts_background)
    stars_background=pygame.image.load('resource/background/stars.jpg').convert_alpha()
    global_var.set_value('stars_background',stars_background)


    etama=pygame.image.load('resource/bullet/etama.png')
    etama=etama.convert_alpha()
    global_var.set_value('etama',etama)
    star_bullet_image=pygame.Surface((256,16))
    star_bullet_image=star_bullet_image.convert_alpha()
    star_bullet_image.fill((0,0,0,0))
    star_bullet_image.blit(etama, (0, 0), (0,160, 256, 16))
    #pygame.image.load('resource/bullet/big_star_bullet.png')
    star_bullet_image=pygame.transform.smoothscale(star_bullet_image,(384,24))
    global_var.set_value('star_bullet_image',star_bullet_image)
    mid_bullet_image=pygame.Surface((256,16))
    mid_bullet_image=mid_bullet_image.convert_alpha()
    mid_bullet_image.fill((0,0,0,0))
    mid_bullet_image.blit(etama, (0, 0), (0,48, 256, 16))
    #pygame.image.load('resource/bullet/big_star_bullet.png')
    mid_bullet_image=pygame.transform.smoothscale(mid_bullet_image,(384,24))
    global_var.set_value('mid_bullet_image',mid_bullet_image)
    orb_bullet_image=pygame.Surface((256,16))
    orb_bullet_image=orb_bullet_image.convert_alpha()
    orb_bullet_image.fill((0,0,0,0))
    orb_bullet_image.blit(etama, (0, 0), (0,32, 256, 16))
    #pygame.image.load('resource/bullet/big_star_bullet.png')
    orb_bullet_image=pygame.transform.scale(orb_bullet_image,(384,24))
    global_var.set_value('orb_bullet_image',orb_bullet_image)

    big_star_bullet_image=pygame.image.load('resource/bullet/big_star_bullet.png')
    big_star_bullet_image=pygame.transform.smoothscale(big_star_bullet_image,(384,48))
    global_var.set_value('big_star_bullet_image',big_star_bullet_image)
    laser_bullet_image=pygame.image.load('resource/bullet/laser_bullet.png')
    global_var.set_value('laser_bullet_image',laser_bullet_image)
    circle_bullet_image=pygame.image.load('resource/bullet/circle_bullet.png')
    circle_bullet_image=pygame.transform.smoothscale(circle_bullet_image,(384,48))
    global_var.set_value('circle_bullet_image',circle_bullet_image)
    bullet_create_image=pygame.image.load('resource/bullet/bullet_create.png')
    global_var.set_value('bullet_create_image',bullet_create_image)
    butterfly_bullet_image=pygame.image.load('resource/bullet/butterfly_bullet.png')
    butterfly_bullet_image=pygame.transform.smoothscale(butterfly_bullet_image,(384,48))
    global_var.set_value('butterfly_bullet_image',butterfly_bullet_image)
    rice_bullet_image=pygame.image.load('resource/bullet/rice_bullet.png')
    rice_bullet_image=pygame.transform.scale(rice_bullet_image,(384,24))
    global_var.set_value('rice_bullet_image',rice_bullet_image)
    satsu_bullet_image=pygame.image.load('resource/bullet/satsu_bullet.png')
    satsu_bullet_image=pygame.transform.smoothscale(satsu_bullet_image,(384,24))
    global_var.set_value('satsu_bullet_image',satsu_bullet_image)
    bact_bullet_image=pygame.image.load('resource/bullet/bact_bullet.png')
    bact_bullet_image=pygame.transform.smoothscale(bact_bullet_image,(384,24))
    global_var.set_value('bact_bullet_image',bact_bullet_image)
    effect_temp1=pygame.image.load('resource/boss/eff01.png')
    effect_temp1=pygame.transform.smoothscale(effect_temp1,(192,96))
    global_var.set_value('effect_temp1',effect_temp1)
    satoriImg=pygame.image.load('resource/boss/face04ct.png')
    satoriImg=pygame.transform.smoothscale(satoriImg,(384,768)).convert_alpha()
    global_var.set_value('satoriImg',satoriImg)
    effFlameImg=pygame.Surface((72,72)).convert_alpha()
    effFlameImg.fill((0,0,0,0))
    effFlameImg.blit(global_var.get_value('effect_temp1').convert_alpha(), (0, 0), (0,0, 72, 72))
    flameColor=(255,62,0,0)
    fill(effFlameImg,flameColor)
    effFlameImg.set_alpha(150)
    global_var.set_value('effFlameImg',effFlameImg)

    effLightImg=pygame.Surface((72,72)).convert_alpha()
    effLightImg.fill((0,0,0,0))
    effLightImg.blit(global_var.get_value('effect_temp1').convert_alpha(), (0, 0), (72,0, 72, 72))
    #flameColor=(255,255,255,0)
    fill(effLightImg,flameColor)
    effLightImg.set_alpha(150)
    global_var.set_value('effLightImg',effLightImg)


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

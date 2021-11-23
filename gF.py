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
    reimu_fire=pygame.transform.smoothscale(reimu_fire,(384,168))
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
    front00=pygame.transform.smoothscale(front00,(768,768))
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
    spell_background=pygame.image.load('resource/background/spellBack.jpg').convert()
    #spell_background=pygame.transform.smoothscale(spell_background,(850,850)).convert()
    global_var.set_value('spell_background',spell_background)
    moon=pygame.image.load('resource/background/moon.png').convert()
    global_var.set_value('moon',moon)


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
    
    laser_image=pygame.Surface((256,16))
    laser_image=laser_image.convert_alpha()
    laser_image.fill((0,0,0,0))
    laser_image.blit(etama, (0, 0), (0,0, 256, 16))
    #pygame.image.load('resource/bullet/big_star_bullet.png')
    global_var.set_value('laser_image',laser_image)



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
    pauseImg=pygame.image.load('resource/text/pause.png')
    pauseImg=pygame.transform.smoothscale(pauseImg,(384,384)).convert_alpha()
    global_var.set_value('pauseImg',pauseImg)
    pauseRound=pygame.Surface((72,312)).convert_alpha()
    pauseRound.fill((0,0,0,0))
    pauseRound.blit(pauseImg,(0,0),(0,0,72,312))
    global_var.set_value('pauseRound',pauseRound)
    titleLogo=pygame.image.load('resource/title/title_logo.png')
    kanjiLogo=pygame.Surface((610,144)).convert_alpha()
    kanjiLogo.fill((0,0,0,0))
    kanjiLogo.blit(titleLogo,(0,0),(0,0,610,144))
    global_var.set_value('kanjiLogo',kanjiLogo)
    engLogo=pygame.Surface((500,96)).convert_alpha()
    engLogo.fill((0,0,0,0))
    engLogo.blit(titleLogo,(0,0),(500,160,500,96))
    global_var.set_value('engLogo',engLogo)
    lightLogo=pygame.Surface((500,96)).convert_alpha()
    lightLogo.fill((0,0,0,0))
    lightLogo.blit(titleLogo,(0,0),(0,160,500,96))
    global_var.set_value('lightLogo',lightLogo)
    reimuLogo=pygame.image.load('resource/title/tachie.png').convert_alpha()
    reimuLogo=pygame.transform.smoothscale(reimuLogo,(360,640))
    global_var.set_value('reimuLogo',reimuLogo)
    pauseSign=[]
    pauseLim=[315,240,168,192,300,300]
    for i in range(0,6):
        new_image=pygame.Surface((312,48)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(pauseImg,(0,0),(72,i*48,pauseLim[i],48))
        pauseSign.append(new_image)
    new_image=pygame.Surface((312,48)).convert_alpha()
    new_image.fill((0,0,0,0))
    new_image.blit(pauseImg,(0,0),(192,336,192,48))
    pauseSign.append(new_image)
    pauseCate=[]
    for i in range(0,3):
        new_image=pygame.Surface((105,48)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(pauseImg,(0,0),(72+i*105,0,105,48))
        pauseCate.append(new_image)
    global_var.set_value('pauseSign',pauseSign)
    global_var.set_value('pauseCate',pauseCate)
    selectSurf=pygame.Surface((312,48)).convert_alpha()
    selectSurf.fill((200,200,200,100))
    global_var.set_value('selectSurf',selectSurf)
    global_var.set_value('pauseSelectNum',0)
    levelImg=[]
    for i in range(1,2):
        new_image=pygame.image.load('resource/title/level0'+str(i)+'.png')
        new_image=pygame.transform.smoothscale(new_image,(384,192))
        levelImg.append(new_image)
    global_var.set_value('levelImg',levelImg)
    menuImg=pygame.image.load('resource/title/title01.png')
    menuImg=pygame.transform.smoothscale(menuImg,(768,768))
    menuSign=[]
    menuShadow=[]
    for i in range(0,8):
        for j in range(0,2):
            new_image=pygame.Surface((192,48)).convert_alpha()
            new_image.fill((0,0,0,0))
            new_image.blit(menuImg,(0,0),(j*192,i*48,192,48))
            if j==0:
                menuSign.append(new_image)
            else:
                menuShadow.append(new_image)
    menuSelectImg=[]
    selectImg=pygame.image.load('resource/title/select01.png')
    for i in range(0,8):
        new_image=pygame.Surface((256,49)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(selectImg,(0,0),(0,i*49,256,49))
        new_image=pygame.transform.smoothscale(new_image,(384,74))
        menuSelectImg.append(new_image)
    global_var.set_value('menuSelectImg',menuSelectImg)
    global_var.set_value('menuSign',menuSign)
    global_var.set_value('menuShadow',menuShadow)
    playerTitle=pygame.image.load('resource/title/sl_pl00.png')
    playerTitle=pygame.transform.smoothscale(playerTitle,(768,768))
    playerTitleImg=[]
    new_image=pygame.Surface((450,768)).convert_alpha()
    new_image.fill((0,0,0,0))
    new_image.blit(playerTitle,(0,0),(0,0,450,768))
    playerTitleImg.append(new_image)
    new_image=pygame.Surface((318,768)).convert_alpha()
    new_image.fill((0,0,0,0))
    new_image.blit(playerTitle,(0,0),(450,0,318,768))
    playerTitleImg.append(new_image)
    global_var.set_value('playerTitleImg',playerTitleImg)
    effFlameImg=pygame.Surface((72,72)).convert_alpha()
    effFlameImg.fill((0,0,0,0))
    effFlameImg.blit(global_var.get_value('effect_temp1').convert_alpha(), (0, 0), (0,0, 72, 72))
    flameColor=(255,62,255,0)
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

    orb_bullet_img=[]
    c_list=['blue','darkBlue','green','grey','jade','lakeBlue','lightGreen','lightRed','lightYellow','orange','pink','purple','red','skyBlue','white','yellow']
    for i in range(0,16):
        new_image=pygame.image.load('resource/bullet/orb_bullet_'+c_list[i]+'.png').convert_alpha()
        orb_bullet_img.append(new_image)
    global_var.set_value('orb_bullet_img',orb_bullet_img)
    mid_bullet_img=[]
    c_list2=['blue','darkBlue','darkGreen','darkYellow','green','grey','lightGreen','lightRed','orange','pink','purple','red','seaBlue','skyBlue','white','yellow']
    for i in range(0,16):
        new_image=pygame.image.load('resource/bullet/mid_bullet_'+c_list2[i]+'.png').convert_alpha()
        mid_bullet_img.append(new_image)
    global_var.set_value('mid_bullet_img',mid_bullet_img)
    scale_bullet_img=[]
    c_list3=['blue','green','grey','lemonYellow','lightBlue','lightGreen','lightRed','lightYellow','orange','pink','purple','red','skyBlue','white','yellow']
    for i in range(0,15):
        new_image=pygame.image.load('resource/bullet/scale_bullet_'+c_list3[i]+'.png').convert_alpha()
        scale_bullet_img.append(new_image)
    global_var.set_value('scale_bullet_img',scale_bullet_img)
    small_bullet_img=[]
    c_list4=['blue','darkBlue','green','greenish','grey','lightBlue','lightGreen','lightYellow','orange','pink','purple','red','skyBlue','violet','white','yellow']
    for i in range(0,16):
        new_image=pygame.image.load('resource/bullet/small_bullet_'+c_list4[i]+'.png').convert_alpha()
        small_bullet_img.append(new_image)
    global_var.set_value('small_bullet_img',small_bullet_img)



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
    if not global_var.get_value('pause'):
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

def doPause(pressed_keys,screen):
    if pressed_keys[K_ESCAPE]!=global_var.get_value('escPressing') and pressed_keys[K_ESCAPE]:
        if global_var.get_value('pause') and not global_var.get_value('ifGameOver'):
            global_var.set_value('pause',False)
            pygame.mixer.music.unpause()
        elif not global_var.get_value('ifGameOver'):
            global_var.set_value('pause',True)
            pygame.mixer.music.pause()
            global_var.get_value('pause_sound').stop()
            global_var.get_value('pause_sound').play()
            global_var.get_value('nep_sound').stop()
            new_image=pygame.Surface((960,720)).convert_alpha()
            new_image.fill((0,0,0))
            new_image.blit(screen,(0,0))
            new_image=pygame.transform.smoothscale(new_image,(480,360))
            new_image=pygame.transform.smoothscale(new_image,(960,720))
            global_var.set_value('pauseScreen',new_image)
            #print(global_var.get_value('pauseScreen').get_size())

def pauseScreen(pressed_keys,pressed_keys_last,screen,frame,enemys,bullets,slaves,items,effects,backgrounds,bosses,player,booms,playerGuns):
    pause=global_var.get_value('pause')
    if pause:
        ifStopPressing=global_var.get_value('ifStopPressing')
        screen.blit(global_var.get_value('pauseScreen'),(0,0))
        #screen.blit(global_var.get_value('pauseImg'),(60,300))
        screen.blit(global_var.get_value('pauseRound'),(75,300))
        selectNum=global_var.get_value('pauseSelectNum')
        if not (pressed_keys[K_UP] and pressed_keys_last[K_UP]):
            if pressed_keys[K_UP]:
                selectNum-=1
                global_var.get_value('select_sound').stop()
                global_var.get_value('select_sound').play()
        if not (pressed_keys[K_DOWN] and pressed_keys_last[K_DOWN]):
            if pressed_keys[K_DOWN]:
                selectNum+=1
                global_var.get_value('select_sound').stop()
                global_var.get_value('select_sound').play()
        if selectNum>2:
            selectNum=0
        elif selectNum<0:
            selectNum=2
        global_var.set_value('pauseSelectNum',selectNum)
        screen.blit(global_var.get_value('selectSurf'),(72,398+48*selectNum))
        for i in range(0,4):
            if i==0:
                if not global_var.get_value('ifGameOver'):
                    screen.blit(global_var.get_value('pauseCate')[0],(60,300+48*i))
                else:
                    screen.blit(global_var.get_value('pauseCate')[1],(60,300+48*i))
            else:
                if i==1:
                    if not global_var.get_value('ifGameOver'):
                        screen.blit(global_var.get_value('pauseSign')[i],(100,398-48+48*i))
                    else:
                        screen.blit(global_var.get_value('pauseSign')[6],(100,398-48+48*i))
                else:
                    screen.blit(global_var.get_value('pauseSign')[i],(100,398-48+48*i))
        if pressed_keys[K_z]!=pressed_keys_last[K_z] and pressed_keys[K_z] and ifStopPressing and selectNum==0:
            if not global_var.get_value('ifGameOver'):
                global_var.get_value('ok_sound').play()
                global_var.set_value('pause',False)
                pygame.mixer.music.unpause()
                global_var.set_value('pauseSelectNum',0)
            else:
                global_var.get_value('ok_sound').play()
                global_var.set_value('pause',False)
                pygame.mixer.music.stop()
                if not global_var.get_value('ifBoss'):
                    pygame.mixer.music.load('resource/bgm/lightnessOnTheWay.mp3')
                    start1=global_var.get_value('bgmContinuePos')[0]
                    pygame.mixer.music.play(loops=-1,start=start1/1000)
                else:
                    pygame.mixer.music.load('resource/bgm/金卡雷 - 引燃夜空的星火.mp3')
                    start1=global_var.get_value('bgmContinuePos')[1]
                    pygame.mixer.music.play(loops=-1,start=start1/1000)
                global_var.set_value('pauseSelectNum',0)
                px=player.tx
                py=player.ty
                midPath=player.midPath
                player.__init__()
                player.midPath=midPath
                player.tx=px
                player.ty=py
                player.power=400   
                player.spellBonus=False
                global_var.set_value('ifGameOver',False)
                player.score=0
                player.unhitSetter(120)
        elif (pressed_keys[K_z]!=pressed_keys_last[K_z] and pressed_keys[K_z] and ifStopPressing and selectNum==1):
            global_var.set_value('restarting',True)
            global_var.get_value('ok_sound').play()
            global_var.set_value('pause',False)
            restart(frame,enemys,bullets,slaves,items,effects,backgrounds,bosses,player,screen,booms,playerGuns)
            pygame.mixer.music.stop()
            global_var.set_value('pauseSelectNum',0)
            global_var.set_value('menu',True)
            pygame.mixer.music.stop()
            pygame.mixer.music.load('resource/bgm/mainTitle.mp3')
            pygame.mixer.music.play(loops=-1)
        elif (pressed_keys[K_z]!=pressed_keys_last[K_z] and pressed_keys[K_z] and ifStopPressing and selectNum==2) or (pressed_keys[K_r]!=pressed_keys_last[K_r] and pressed_keys[K_r]):
            #print('do')
            global_var.set_value('restarting',True)
            global_var.get_value('ok_sound').play()
            global_var.set_value('pause',False)
            pygame.mixer.music.stop()
            restart(frame,enemys,bullets,slaves,items,effects,backgrounds,bosses,player,screen,booms,playerGuns)
            global_var.set_value('pauseSelectNum',0)
        if not pressed_keys[K_z]:
            ifStopPressing=True
            global_var.set_value('ifStopPressing',True)


def restart(frame,enemys,bullets,slaves,items,effects,backgrounds,bosses,player,screen,booms,playerGuns):
    #frame=0
    for enemy in enemys:
        enemy.kill()
    for bullet in bullets:
        bullet.kill()
    for slave in slaves:
        slave.kill()
    for item in items:
        item.kill()
    for effect in effects:
        effect.kill()
    for background in backgrounds:
        background.kill()
    for boss in bosses:
        boss.kill()
    for boom in booms:
        boom.kill()
    for playerGun in playerGuns:
        playerGun.kill()
    player.__init__()
    player.tx=357.0
    player.ty=600.0
    player.power=100    
    if global_var.get_value('ifTest'):
        player.power=400
    global_var.set_value('getTicksLastFrame',0)
    pygame.mixer.music.load('resource/bgm/lightnessOnTheWay.mp3') 
    pygame.mixer.music.play(loops=-1)
    global_var.set_value('ifBoss',False)
    global_var.set_value('pressingX',False)
    global_var.set_value('DELTA_T',17)
    global_var.set_value('ifShaking',False)
    global_var.set_value('shakeFrame',0)
    global_var.set_value('boomStatu',0)
    global_var.set_value('grazeNum',0)
    global_var.set_value('fpSec',0)
    global_var.set_value('enemyPos',(0,0,10000))
    global_var.set_value('shift_down',False)
    global_var.set_value('pause',False)
    global_var.set_value('escPressing',False)
    global_var.set_value('pauseScreen',0)
    global_var.set_value('ifStopPressing',False)
    global_var.set_value('ifGameOver',False)
    global_var.set_value('bgmContinuePos',[0,0])#[0]->for mid stage,[1]->for boss fight
    doBackground(screen,backgrounds)